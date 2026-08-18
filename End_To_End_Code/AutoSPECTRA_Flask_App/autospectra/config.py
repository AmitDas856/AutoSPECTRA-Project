from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CLASS_NAMES = ["Normal", "DoS", "Fuzzy", "Gear", "RPM"]
CLASS_TO_INDEX = {name: index for index, name in enumerate(CLASS_NAMES)}
INDEX_TO_CLASS = {index: name for name, index in CLASS_TO_INDEX.items()}

WINDOW_SIZE = int(os.getenv("AUTOSPECTRA_WINDOW_SIZE", "64"))
DEFAULT_STRIDE = int(os.getenv("AUTOSPECTRA_STRIDE", str(WINDOW_SIZE)))
MAX_WINDOWS = int(os.getenv("AUTOSPECTRA_MAX_WINDOWS", "5000"))
MAX_UPLOAD_MB = int(os.getenv("AUTOSPECTRA_MAX_UPLOAD_MB", "300"))
BATCH_SIZE = int(os.getenv("AUTOSPECTRA_BATCH_SIZE", "256"))

FEATURE_NAMES = [
    "duration_s",
    "message_rate_hz",
    "iat_mean_ms",
    "iat_std_ms",
    "iat_p95_ms",
    "iat_max_ms",
    "unique_id_count",
    "id_entropy",
    "max_id_ratio",
    "id_transition_rate",
    "can_id_mean_norm",
    "can_id_std_norm",
    "dominant_id_norm",
    "zero_id_ratio",
    "dlc_mean",
    "dlc_std",
    "payload_mean",
    "payload_std",
    "payload_entropy",
    "nonzero_byte_ratio",
    "byte_change_mean",
    "byte_change_std",
    "payload_sum_mean",
    "payload_sum_std",
]

ALLOWED_EXTENSIONS = {"csv", "txt", "log"}

UPLOAD_DIR = Path(os.getenv("AUTOSPECTRA_UPLOAD_DIR", str(BASE_DIR / "uploads")))
RESULT_DIR = Path(os.getenv("AUTOSPECTRA_RESULT_DIR", str(BASE_DIR / "results")))

for directory in (UPLOAD_DIR, RESULT_DIR):
    directory.mkdir(parents=True, exist_ok=True)
