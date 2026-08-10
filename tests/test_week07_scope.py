import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = (
    ROOT
    / "notebooks/week07/"
    / "autospectra_week07_fusion_calibration_ablation.ipynb"
)

def source():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in nb["cells"]
    )

def test_week7_notebook_exists():
    assert NOTEBOOK.exists()

def test_fusion_present():
    text = source()
    assert "fusion_weights" in text
    assert "RF + CNN + LSTM Fusion" in text

def test_temperature_calibration_present():
    text = source()
    assert "temperature_candidates" in text
    assert "best_temperature" in text

def test_ablation_present():
    text = source()
    assert "FEATURE_GROUPS" in text
    assert "window_ablation_plan" in text

def test_latency_present():
    assert "detection_latency_table" in source()

def test_week8_scope_absent():
    text = source()
    assert "Structured incident-report generator" not in text
    assert "One-window live demonstration" not in text
    assert "Flask deployment" not in text
