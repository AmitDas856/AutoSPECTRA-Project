"""Validate the Week 3 AutoSPECTRA notebook before GitHub push."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = (
    ROOT
    / "notebooks"
    / "week03"
    / "autospectra_week03_windowing_split_features.ipynb"
)

REQUIRED = [
    "AutoSPECTRA — Week 3 Notebook",
    "Team Contributions",
    "WINDOW_SIZE = 64",
    "STRIDE = 64",
    'SPLIT_STRATEGY = "source_class_chronological_v3"',
    "Chronological boundary audit passed",
    "Non-overlap audit passed",
    "Feature dictionary",
    "Sequence-channel dictionary",
    "sequence_to_recurrence",
    "Models trained in Week 3: No",
]

FORBIDDEN = [
    "RandomForestClassifier(",
    "ExtraTreesClassifier(",
    "LogisticRegression(",
    "XGBClassifier(",
    "class RecurrenceCNN",
    "class LSTMClassifier",
    "temperature_scale",
    "Flask(",
]

if not NOTEBOOK.exists():
    print(f"FAILED: missing notebook: {NOTEBOOK}")
    sys.exit(1)

notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
source = "\n".join(
    "".join(cell.get("source", []))
    for cell in notebook.get("cells", [])
)

missing = [text for text in REQUIRED if text not in source]
forbidden = [text for text in FORBIDDEN if text in source]

if missing:
    print("FAILED: required Week 3 content is missing:")
    for item in missing:
        print(" -", item)
    sys.exit(1)

if forbidden:
    print("FAILED: later-week implementation is present:")
    for item in forbidden:
        print(" -", item)
    sys.exit(1)

print("Week 3 notebook validation PASSED.")
print("Cells:", len(notebook.get("cells", [])))
