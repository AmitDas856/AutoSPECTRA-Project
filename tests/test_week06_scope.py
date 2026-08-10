import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week06/autospectra_week06_lstm_autoencoder.ipynb"

def source():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    return "\n".join("".join(c.get("source", [])) for c in nb["cells"])

def test_notebook_exists():
    assert NOTEBOOK.exists()

def test_lstm_present():
    text = source()
    assert "class CANLSTMClassifier" in text
    assert "bidirectional=True" in text

def test_autoencoder_present():
    text = source()
    assert "class LSTMSequenceAutoencoder" in text
    assert 'y_train' in text and 'CLASS_TO_INDEX["Normal"]' in text

def test_threshold_uses_validation():
    text = source()
    assert "select_validation_anomaly_rule" in text
    assert "maximum_fpr=0.10" in text

def test_future_scope_absent():
    text = source()
    assert "fusion_probabilities" not in text
    assert "temperature_scale" not in text
    assert "Flask(" not in text
