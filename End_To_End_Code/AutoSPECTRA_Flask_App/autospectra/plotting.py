from __future__ import annotations

import base64
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .config import CLASS_NAMES


def _figure_to_base64() -> str:
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("ascii")


def prediction_distribution(probabilities: np.ndarray) -> str:
    predictions = probabilities.argmax(axis=1)
    counts = [int(np.sum(predictions == index)) for index in range(len(CLASS_NAMES))]
    plt.figure(figsize=(8, 4.5))
    plt.bar(CLASS_NAMES, counts)
    plt.title("Predicted CAN traffic classes")
    plt.xlabel("Class")
    plt.ylabel("Number of windows")
    return _figure_to_base64()


def confidence_timeline(probabilities: np.ndarray) -> str:
    predictions = probabilities.argmax(axis=1)
    confidences = probabilities.max(axis=1)
    x = np.arange(len(confidences))
    plt.figure(figsize=(10, 4.5))
    plt.plot(x, confidences, linewidth=1.2, label="Prediction confidence")
    attack_mask = predictions != 0
    if attack_mask.any():
        plt.scatter(x[attack_mask], confidences[attack_mask], s=20, label="Attack prediction")
    plt.ylim(0, 1.02)
    plt.title("Confidence across chronological windows")
    plt.xlabel("Window index")
    plt.ylabel("Confidence")
    plt.legend()
    return _figure_to_base64()


def message_rate_timeline(metadata: pd.DataFrame) -> str:
    plt.figure(figsize=(10, 4.5))
    plt.plot(metadata["window_index"], metadata["message_rate_hz"], linewidth=1.2)
    plt.title("CAN message rate by window")
    plt.xlabel("Window index")
    plt.ylabel("Messages per second")
    return _figure_to_base64()


def probability_heatmap(probabilities: np.ndarray, max_windows: int = 250) -> str:
    shown = probabilities[:max_windows].T
    plt.figure(figsize=(11, 4.5))
    image = plt.imshow(shown, aspect="auto", vmin=0, vmax=1)
    plt.colorbar(image, label="Predicted probability")
    plt.yticks(range(len(CLASS_NAMES)), CLASS_NAMES)
    plt.title(f"Class probabilities for first {shown.shape[1]} windows")
    plt.xlabel("Window index")
    plt.ylabel("Class")
    return _figure_to_base64()
