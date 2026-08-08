"""Validate the AutoSPECTRA Week 4 notebook before GitHub push."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = (
    ROOT
    / "notebooks"
    / "week04"
    / "autospectra_week04_classical_baselines.ipynb"
)

REQUIRED = [
    "AutoSPECTRA — Week 4 Notebook",
    "Team Contributions",
    "Logistic Regression",
    "Random Forest",
    "Extra Trees",
    "XGBoost",
    "calculate_multiclass_metrics",
    "metrics_confusion_",
    "metrics_roc_",
    "metrics_pr_",
    "model_random_forest_feature_importance.png",
    "AutoSPECTRA_Week04_Images.zip",
    "AutoSPECTRA_Week04_Evidence.zip",
]

FORBIDDEN = [
    "class RecurrenceCNN",
    "class LSTMClassifier",
    "class LSTMSequenceAutoencoder",
    "fusion_probabilities",
    "Flask(",
]

if not NOTEBOOK.exists():
    print(f"FAILED: notebook not found: {NOTEBOOK}")
    sys.exit(1)

notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
source = "\n".join(
    "".join(cell.get("source", []))
    for cell in notebook.get("cells", [])
)

missing = [item for item in REQUIRED if item not in source]
forbidden = [item for item in FORBIDDEN if item in source]

if missing:
    print("FAILED: missing Week 4 content:")
    for item in missing:
        print(" -", item)
    sys.exit(1)

if forbidden:
    print("FAILED: later-week implementation detected:")
    for item in forbidden:
        print(" -", item)
    sys.exit(1)

print("Week 4 notebook validation PASSED.")
print("Cells:", len(notebook.get("cells", [])))
