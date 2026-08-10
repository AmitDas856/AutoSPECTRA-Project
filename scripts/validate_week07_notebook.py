"""Validate AutoSPECTRA Week 7 scope and integration evidence."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = (
    ROOT
    / "notebooks"
    / "week07"
    / "autospectra_week07_fusion_calibration_ablation.ipynb"
)

REQUIRED = [
    "AutoSPECTRA — Week 7 Notebook",
    "Team Contributions",
    "RF + CNN + LSTM Fusion",
    "Calibrated RF + CNN + LSTM Fusion",
    "fusion_weights",
    "temperature_candidates",
    "validation log loss",
    "detection_latency_table",
    "FEATURE_GROUPS",
    "window_ablation_plan",
    "week07_fusion_weights.png",
    "week07_temperature_search.png",
    "week07_fusion_ece_comparison.png",
    "week07_week8_handover.json",
    "AutoSPECTRA_Week07_Images.zip",
    "AutoSPECTRA_Week07_Evidence.zip",
]

FORBIDDEN = [
    "structured incident-report generator",
    "One-window live demonstration",
    "Flask deployment",
    "AutoSPECTRA_Flask_Deployment.zip",
]

if not NOTEBOOK.exists():
    sys.exit(f"Missing notebook: {NOTEBOOK}")

nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))

source = "\n".join(
    "".join(cell.get("source", []))
    for cell in nb.get("cells", [])
)

missing = [
    text
    for text in REQUIRED
    if text not in source
]

forbidden = [
    text
    for text in FORBIDDEN
    if text in source
]

if missing or forbidden:
    print("Missing required content:", missing)
    print("Forbidden Week 8 content:", forbidden)
    sys.exit(1)

print("Week 7 notebook validation PASSED.")
print("Cells:", len(nb.get("cells", [])))
