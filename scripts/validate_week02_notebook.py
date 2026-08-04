"""Validate the AutoSPECTRA Week 2 notebook before pushing."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "week02" / "autospectra_week02_dataset_audit_eda.ipynb"

REQUIRED_TEXT = [
    "AutoSPECTRA — Week 2 Notebook",
    "Team Contributions",
    "DLC-aware parser",
    "Audit all four captures",
    "Models trained in Week 2: No",
    "Week 3 boundary",
]

FORBIDDEN_WEEK2_TEXT = [
    "RandomForestClassifier(",
    "XGBClassifier(",
    "class RecurrenceCNN",
    "class LSTMClassifier",
    "temperature_scale",
    "Flask deployment ZIP",
]

if not NOTEBOOK.exists():
    print(f"FAILED: notebook not found: {NOTEBOOK}")
    sys.exit(1)

notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
combined = "\n".join(
    "".join(cell.get("source", []))
    for cell in notebook.get("cells", [])
)

missing = [item for item in REQUIRED_TEXT if item not in combined]
if missing:
    print("FAILED: missing Week 2 content:")
    for item in missing:
        print(" -", item)
    sys.exit(1)

forbidden = [item for item in FORBIDDEN_WEEK2_TEXT if item in combined]
if forbidden:
    print("FAILED: later-week implementation found:")
    for item in forbidden:
        print(" -", item)
    sys.exit(1)

print("Week 2 notebook validation PASSED.")
print("Notebook:", NOTEBOOK)
print("Cells:", len(notebook.get("cells", [])))
