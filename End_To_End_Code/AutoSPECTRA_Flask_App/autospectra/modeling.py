from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from .config import BATCH_SIZE, BASE_DIR, CLASS_NAMES, WINDOW_SIZE

try:
    import torch
    import torch.nn as nn
except ImportError:  # Classical models can still run without PyTorch.
    torch = None
    nn = None


if nn is not None:
    class RecurrenceCNN(nn.Module):
        def __init__(self, number_of_classes: int = len(CLASS_NAMES)):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(1, 16, kernel_size=3, padding=1),
                nn.BatchNorm2d(16),
                nn.ReLU(),
                nn.MaxPool2d(2),
                nn.Conv2d(16, 32, kernel_size=3, padding=1),
                nn.BatchNorm2d(32),
                nn.ReLU(),
                nn.MaxPool2d(2),
                nn.Conv2d(32, 64, kernel_size=3, padding=1),
                nn.BatchNorm2d(64),
                nn.ReLU(),
                nn.AdaptiveAvgPool2d((1, 1)),
            )
            self.classifier = nn.Sequential(
                nn.Flatten(),
                nn.Dropout(0.25),
                nn.Linear(64, number_of_classes),
            )

        def forward(self, inputs):
            return self.classifier(self.features(inputs))


    class CANLSTMClassifier(nn.Module):
        def __init__(
            self,
            input_size: int = 11,
            hidden_size: int = 64,
            number_of_classes: int = len(CLASS_NAMES),
        ):
            super().__init__()
            self.lstm = nn.LSTM(
                input_size=input_size,
                hidden_size=hidden_size,
                num_layers=1,
                batch_first=True,
                bidirectional=True,
            )
            self.classifier = nn.Sequential(
                nn.LayerNorm(hidden_size * 2),
                nn.Dropout(0.25),
                nn.Linear(hidden_size * 2, number_of_classes),
            )

        def forward(self, inputs):
            outputs, _ = self.lstm(inputs)
            representation = outputs.mean(dim=1)
            return self.classifier(representation)


def sequence_to_recurrence_batch(sequences: np.ndarray, gamma: float = 8.0) -> np.ndarray:
    """Convert [N,T,11] sequences to [N,1,T,T] recurrence images."""
    signal = (
        0.35 * sequences[:, :, 0]
        + 0.10 * sequences[:, :, 1]
        + 0.45 * sequences[:, :, 2:10].mean(axis=2)
        + 0.10 * sequences[:, :, 10]
    )
    distance = np.abs(signal[:, :, None] - signal[:, None, :])
    return np.exp(-gamma * distance)[:, None, :, :].astype(np.float32)


def apply_temperature(probabilities: np.ndarray, temperature: float) -> np.ndarray:
    clipped = np.clip(probabilities, 1e-12, 1.0)
    adjusted = clipped ** (1.0 / max(float(temperature), 1e-6))
    return adjusted / adjusted.sum(axis=1, keepdims=True)


def _safe_torch_load(path: Path, device):
    try:
        return torch.load(path, map_location=device, weights_only=False)
    except TypeError:
        return torch.load(path, map_location=device)


class ModelRegistry:
    """Discover, load, and run AutoSPECTRA model artifacts."""

    CLASSICAL_FILES = {
        "random_forest": "random_forest.joblib",
        "extra_trees": "extra_trees.joblib",
        "logistic_regression": "logistic_regression.joblib",
    }

    DISPLAY_NAMES = {
        "random_forest": "Random Forest",
        "extra_trees": "Extra Trees",
        "logistic_regression": "Logistic Regression",
        "recurrence_cnn": "Recurrence CNN",
        "lstm_classifier": "LSTM Classifier",
        "fusion": "RF + CNN + LSTM Fusion",
    }

    def __init__(self, model_dir: str | Path | None = None):
        self.model_dir = self._resolve_model_dir(model_dir)
        self.device = (
            torch.device("cuda" if torch and torch.cuda.is_available() else "cpu")
            if torch
            else None
        )
        self.models: dict[str, Any] = {}
        self.warnings: list[str] = []
        self.fusion_weights: dict[str, float] = {}
        self.temperature = 1.0
        self.expected_window_size = WINDOW_SIZE
        self._load_models()

    @staticmethod
    def _candidate_dirs() -> list[Path]:
        candidates = []
        env_dir = os.getenv("AUTOSPECTRA_MODEL_DIR")
        if env_dir:
            candidates.append(Path(env_dir))
        candidates.extend(
            [
                BASE_DIR / "models",
                BASE_DIR / "autospectra_outputs" / "models",
                Path("/kaggle/working/autospectra_outputs/models"),
            ]
        )
        return candidates

    def _resolve_model_dir(self, model_dir: str | Path | None) -> Path:
        if model_dir:
            return Path(model_dir).expanduser().resolve()
        for candidate in self._candidate_dirs():
            if candidate.exists() and any(candidate.iterdir()):
                return candidate.resolve()
        return (BASE_DIR / "models").resolve()

    def _load_models(self) -> None:
        self.model_dir.mkdir(parents=True, exist_ok=True)

        for key, filename in self.CLASSICAL_FILES.items():
            path = self.model_dir / filename
            if path.exists():
                try:
                    self.models[key] = joblib.load(path)
                except Exception as exc:  # Keep app usable with other artifacts.
                    self.warnings.append(f"Could not load {filename}: {exc}")

        if torch is not None:
            cnn_path = self.model_dir / "recurrence_cnn.pt"
            if cnn_path.exists():
                try:
                    checkpoint = _safe_torch_load(cnn_path, self.device)
                    self.expected_window_size = int(
                        checkpoint.get("window_size", self.expected_window_size)
                    )
                    cnn = RecurrenceCNN(len(CLASS_NAMES)).to(self.device)
                    cnn.load_state_dict(checkpoint["state_dict"])
                    cnn.eval()
                    self.models["recurrence_cnn"] = cnn
                except Exception as exc:
                    self.warnings.append(f"Could not load recurrence_cnn.pt: {exc}")

            lstm_path = self.model_dir / "lstm_classifier.pt"
            if lstm_path.exists():
                try:
                    checkpoint = _safe_torch_load(lstm_path, self.device)
                    self.expected_window_size = int(
                        checkpoint.get("window_size", self.expected_window_size)
                    )
                    lstm = CANLSTMClassifier(
                        input_size=int(checkpoint.get("input_size", 11)),
                        number_of_classes=len(CLASS_NAMES),
                    ).to(self.device)
                    lstm.load_state_dict(checkpoint["state_dict"])
                    lstm.eval()
                    self.models["lstm_classifier"] = lstm
                except Exception as exc:
                    self.warnings.append(f"Could not load lstm_classifier.pt: {exc}")
        else:
            if (self.model_dir / "recurrence_cnn.pt").exists() or (
                self.model_dir / "lstm_classifier.pt"
            ).exists():
                self.warnings.append("PyTorch is not installed, so deep models were skipped.")

        self._load_fusion_config()

    def _load_fusion_config(self) -> None:
        config_path = self.model_dir / "fusion_config.json"
        calibration_path = self.model_dir / "fusion_calibration.json"

        if config_path.exists():
            try:
                config = json.loads(config_path.read_text(encoding="utf-8"))
                raw_weights = config.get("weights", {})
                aliases = {
                    "Random Forest": "random_forest",
                    "Recurrence CNN": "recurrence_cnn",
                    "LSTM Classifier": "lstm_classifier",
                    "random_forest": "random_forest",
                    "recurrence_cnn": "recurrence_cnn",
                    "lstm_classifier": "lstm_classifier",
                }
                self.fusion_weights = {
                    aliases.get(name, name): float(weight)
                    for name, weight in raw_weights.items()
                }
                self.temperature = float(config.get("temperature", 1.0))
            except Exception as exc:
                self.warnings.append(f"Could not read fusion_config.json: {exc}")

        if calibration_path.exists() and self.temperature == 1.0:
            try:
                calibration = json.loads(calibration_path.read_text(encoding="utf-8"))
                self.temperature = float(calibration.get("temperature", 1.0))
            except Exception as exc:
                self.warnings.append(f"Could not read fusion_calibration.json: {exc}")

        fusion_members = [
            key
            for key in ("random_forest", "recurrence_cnn", "lstm_classifier")
            if key in self.models
        ]
        if len(fusion_members) == 3:
            if not self.fusion_weights:
                self.fusion_weights = {key: 1.0 / 3.0 for key in fusion_members}
                self.warnings.append(
                    "fusion_config.json was not found; fusion uses equal weights. "
                    "Export validation-derived weights from the notebook for exact replication."
                )
            else:
                valid = {
                    key: max(float(self.fusion_weights.get(key, 0.0)), 0.0)
                    for key in fusion_members
                }
                total = sum(valid.values())
                self.fusion_weights = (
                    {key: value / total for key, value in valid.items()}
                    if total > 0
                    else {key: 1.0 / 3.0 for key in fusion_members}
                )

    @property
    def available_models(self) -> list[dict[str, str]]:
        keys = list(self.models)
        if all(key in self.models for key in ("random_forest", "recurrence_cnn", "lstm_classifier")):
            keys.append("fusion")
        preferred_order = [
            "fusion",
            "random_forest",
            "extra_trees",
            "recurrence_cnn",
            "lstm_classifier",
            "logistic_regression",
        ]
        return [
            {"key": key, "name": self.DISPLAY_NAMES[key]}
            for key in preferred_order
            if key in keys
        ]

    @property
    def default_model_key(self) -> str | None:
        available = [item["key"] for item in self.available_models]
        for candidate in ("fusion", "random_forest", "extra_trees", "lstm_classifier", "recurrence_cnn", "logistic_regression"):
            if candidate in available:
                return candidate
        return None

    @staticmethod
    def _align_classical_probabilities(model, probabilities: np.ndarray) -> np.ndarray:
        output = np.zeros((len(probabilities), len(CLASS_NAMES)), dtype=np.float64)
        classes = getattr(model, "classes_", np.arange(probabilities.shape[1]))
        for source_column, class_index in enumerate(classes):
            index = int(class_index)
            if 0 <= index < len(CLASS_NAMES):
                output[:, index] = probabilities[:, source_column]
        row_sums = output.sum(axis=1, keepdims=True)
        return output / np.clip(row_sums, 1e-12, None)

    def _predict_classical(self, key: str, features: np.ndarray) -> np.ndarray:
        model = self.models[key]
        probabilities = model.predict_proba(features)
        return self._align_classical_probabilities(model, probabilities)

    def _predict_lstm(self, sequences: np.ndarray) -> np.ndarray:
        if torch is None:
            raise RuntimeError("PyTorch is required for the LSTM model.")
        batches = []
        model = self.models["lstm_classifier"]
        with torch.no_grad():
            for start in range(0, len(sequences), BATCH_SIZE):
                inputs = torch.from_numpy(sequences[start : start + BATCH_SIZE]).to(self.device)
                probabilities = torch.softmax(model(inputs), dim=1)
                batches.append(probabilities.cpu().numpy())
        return np.concatenate(batches)

    def _predict_cnn(self, sequences: np.ndarray) -> np.ndarray:
        if torch is None:
            raise RuntimeError("PyTorch is required for the CNN model.")
        batches = []
        model = self.models["recurrence_cnn"]
        with torch.no_grad():
            for start in range(0, len(sequences), BATCH_SIZE):
                recurrence = sequence_to_recurrence_batch(
                    sequences[start : start + BATCH_SIZE]
                )
                inputs = torch.from_numpy(recurrence).to(self.device)
                probabilities = torch.softmax(model(inputs), dim=1)
                batches.append(probabilities.cpu().numpy())
        return np.concatenate(batches)

    def predict(
        self,
        model_key: str,
        features: np.ndarray,
        sequences: np.ndarray,
    ) -> np.ndarray:
        if model_key in self.CLASSICAL_FILES:
            return self._predict_classical(model_key, features)
        if model_key == "recurrence_cnn":
            return self._predict_cnn(sequences)
        if model_key == "lstm_classifier":
            return self._predict_lstm(sequences)
        if model_key == "fusion":
            sources = {
                "random_forest": self._predict_classical("random_forest", features),
                "recurrence_cnn": self._predict_cnn(sequences),
                "lstm_classifier": self._predict_lstm(sequences),
            }
            probabilities = sum(
                self.fusion_weights[name] * source
                for name, source in sources.items()
            )
            return apply_temperature(probabilities, self.temperature)
        raise KeyError(f"Unknown or unavailable model: {model_key}")

    def status(self) -> dict[str, Any]:
        return {
            "model_directory": str(self.model_dir),
            "available_models": self.available_models,
            "default_model": self.default_model_key,
            "window_size": self.expected_window_size,
            "device": str(self.device) if self.device else "not available",
            "fusion_weights": self.fusion_weights,
            "temperature": self.temperature,
            "warnings": self.warnings,
        }
