from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

import numpy as np
import pandas as pd

from .config import FEATURE_NAMES, MAX_WINDOWS, WINDOW_SIZE


@dataclass(frozen=True)
class CANFrame:
    timestamp: float
    can_id: int
    dlc: int
    payload: np.ndarray


@dataclass
class WindowBatch:
    features: np.ndarray
    sequences: np.ndarray
    metadata: pd.DataFrame
    total_valid_frames: int
    invalid_lines: int
    truncated: bool


def shannon_entropy(values: np.ndarray) -> float:
    """Return Shannon entropy in bits for a one-dimensional integer array."""
    if values.size == 0:
        return 0.0
    _, counts = np.unique(values, return_counts=True)
    probabilities = counts / counts.sum()
    return max(0.0, float(-(probabilities * np.log2(probabilities + 1e-12)).sum()))


def _parse_hex(value: str, maximum: int) -> int:
    cleaned = value.strip()
    if cleaned.lower().startswith("0x"):
        cleaned = cleaned[2:]
    parsed = int(cleaned, 16)
    return int(np.clip(parsed, 0, maximum))


def parse_can_line(line: str) -> CANFrame | None:
    """
    Parse one HCRL-style CAN line.

    Expected layout:
      Timestamp,CAN_ID,DLC,<DLC payload bytes>[,Flag]

    The optional R/T flag is ignored during inference because it is ground truth.
    """
    stripped = line.strip()
    if not stripped:
        return None

    parts = [part.strip() for part in stripped.split(",")]
    if len(parts) < 3:
        return None

    try:
        timestamp = float(parts[0])
        can_id = _parse_hex(parts[1], 0x7FF)
        dlc = int(float(parts[2]))
        dlc = int(np.clip(dlc, 0, 8))
    except (TypeError, ValueError):
        return None

    payload = np.zeros(8, dtype=np.uint8)
    available_payload = parts[3 : 3 + dlc]

    try:
        for index, value in enumerate(available_payload[:8]):
            payload[index] = _parse_hex(value, 0xFF)
    except (TypeError, ValueError):
        return None

    return CANFrame(
        timestamp=timestamp,
        can_id=can_id,
        dlc=dlc,
        payload=payload,
    )


def iter_can_frames(path: Path) -> Iterator[CANFrame | None]:
    """Yield parsed frames; invalid non-empty lines are yielded as ``None``."""
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            yield parse_can_line(line)


def build_sequence(
    timestamps: np.ndarray,
    can_ids: np.ndarray,
    dlc: np.ndarray,
    payload: np.ndarray,
) -> np.ndarray:
    """Create the exact 11-feature frame sequence used in the notebook."""
    deltas = np.diff(timestamps, prepend=timestamps[0])
    deltas = np.clip(deltas, 0, None)

    sequence = np.zeros((len(timestamps), 11), dtype=np.float32)
    sequence[:, 0] = np.clip(can_ids.astype(np.float32) / 2047.0, 0, 1)
    sequence[:, 1] = dlc.astype(np.float32) / 8.0
    sequence[:, 2:10] = payload.astype(np.float32) / 255.0
    sequence[:, 10] = np.clip(
        np.log1p(deltas * 1_000_000.0) / 15.0,
        0,
        1,
    )
    return sequence.astype(np.float32)


def build_tabular_features(
    timestamps: np.ndarray,
    can_ids: np.ndarray,
    dlc: np.ndarray,
    payload: np.ndarray,
) -> np.ndarray:
    """Engineer the same 24 window-level features used during training."""
    duration = max(float(timestamps[-1] - timestamps[0]), 1e-9)
    deltas = np.diff(timestamps)
    positive_deltas = np.clip(deltas, 0, None)
    iat_ms = positive_deltas * 1000.0

    unique_ids, id_counts = np.unique(can_ids, return_counts=True)
    dominant_position = int(np.argmax(id_counts))
    dominant_id = int(unique_ids[dominant_position])
    max_id_ratio = float(id_counts[dominant_position] / len(can_ids))

    payload_flat = payload.reshape(-1)
    if len(payload) > 1:
        payload_differences = np.abs(
            np.diff(payload.astype(np.float32), axis=0)
        ).mean(axis=1)
    else:
        payload_differences = np.array([0.0], dtype=np.float32)

    payload_sums = payload.sum(axis=1).astype(np.float32)

    values = np.array(
        [
            duration,
            len(timestamps) / duration,
            float(iat_ms.mean()) if len(iat_ms) else 0.0,
            float(iat_ms.std()) if len(iat_ms) else 0.0,
            float(np.percentile(iat_ms, 95)) if len(iat_ms) else 0.0,
            float(iat_ms.max()) if len(iat_ms) else 0.0,
            len(unique_ids),
            shannon_entropy(can_ids),
            max_id_ratio,
            float(np.mean(can_ids[1:] != can_ids[:-1]))
            if len(can_ids) > 1
            else 0.0,
            float(can_ids.mean() / 2047.0),
            float(can_ids.std() / 2047.0),
            dominant_id / 2047.0,
            float(np.mean(can_ids == 0)),
            float(dlc.mean()),
            float(dlc.std()),
            float(payload.mean()),
            float(payload.std()),
            shannon_entropy(payload_flat),
            float(np.mean(payload_flat != 0)),
            float(payload_differences.mean()),
            float(payload_differences.std()),
            float(payload_sums.mean()),
            float(payload_sums.std()),
        ],
        dtype=np.float32,
    )

    if len(values) != len(FEATURE_NAMES):
        raise RuntimeError("Feature vector length does not match training schema.")
    return values


def _window_arrays(frames: Iterable[CANFrame]):
    frame_list = list(frames)
    timestamps = np.asarray([frame.timestamp for frame in frame_list], dtype=np.float64)
    can_ids = np.asarray([frame.can_id for frame in frame_list], dtype=np.uint16)
    dlc = np.asarray([frame.dlc for frame in frame_list], dtype=np.uint8)
    payload = np.stack([frame.payload for frame in frame_list]).astype(np.uint8)
    return timestamps, can_ids, dlc, payload


def process_can_file(
    path: Path,
    *,
    window_size: int = WINDOW_SIZE,
    stride: int | None = None,
    max_windows: int = MAX_WINDOWS,
) -> WindowBatch:
    """
    Stream a CAN capture into fixed-length windows without loading the file in RAM.

    Windows are chronological and labels/flags are not used as model inputs.
    """
    if stride is None:
        stride = window_size
    if window_size <= 1:
        raise ValueError("window_size must be greater than 1")
    if stride <= 0:
        raise ValueError("stride must be positive")
    if max_windows <= 0:
        raise ValueError("max_windows must be positive")

    buffer: deque[CANFrame] = deque()
    features: list[np.ndarray] = []
    sequences: list[np.ndarray] = []
    metadata_rows: list[dict] = []

    total_valid_frames = 0
    invalid_lines = 0
    truncated = False
    next_window_start = 0
    frame_index = 0

    for parsed in iter_can_frames(path):
        if parsed is None:
            invalid_lines += 1
            continue

        total_valid_frames += 1
        buffer.append(parsed)
        frame_index += 1

        if len(buffer) < window_size:
            continue

        # For overlapping windows, retain only the frames needed for the next start.
        current_start = frame_index - len(buffer)
        if current_start < next_window_start:
            while buffer and current_start < next_window_start:
                buffer.popleft()
                current_start += 1
            if len(buffer) < window_size:
                continue

        window_frames = list(buffer)[:window_size]
        timestamps, can_ids, dlc, payload = _window_arrays(window_frames)

        feature_vector = build_tabular_features(timestamps, can_ids, dlc, payload)
        sequence = build_sequence(timestamps, can_ids, dlc, payload)

        unique_ids, counts = np.unique(can_ids, return_counts=True)
        dominant_id = int(unique_ids[int(np.argmax(counts))])

        features.append(feature_vector)
        sequences.append(sequence)
        metadata_rows.append(
            {
                "window_index": len(features) - 1,
                "start_timestamp": float(timestamps[0]),
                "end_timestamp": float(timestamps[-1]),
                "duration_ms": float(max(timestamps[-1] - timestamps[0], 0.0) * 1000.0),
                "dominant_can_id": f"0x{dominant_id:03X}",
                "unique_can_ids": int(len(unique_ids)),
                "message_rate_hz": float(feature_vector[1]),
                "id_entropy_bits": float(feature_vector[7]),
            }
        )

        next_window_start += stride
        while buffer and (frame_index - len(buffer)) < next_window_start:
            buffer.popleft()

        if len(features) >= max_windows:
            truncated = True
            break

    if not features:
        raise ValueError(
            f"No complete {window_size}-frame windows were found. "
            "Check the file format and ensure it contains enough valid CAN frames."
        )

    return WindowBatch(
        features=np.stack(features).astype(np.float32),
        sequences=np.stack(sequences).astype(np.float32),
        metadata=pd.DataFrame(metadata_rows),
        total_valid_frames=total_valid_frames,
        invalid_lines=invalid_lines,
        truncated=truncated,
    )
