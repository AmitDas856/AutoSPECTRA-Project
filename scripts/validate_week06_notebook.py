from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week06/autospectra_week06_lstm_autoencoder.ipynb"

required = [
    "AutoSPECTRA — Week 6 Notebook",
    "class CANLSTMClassifier",
    "bidirectional=True",
    "class LSTMSequenceAutoencoder",
    "select_validation_anomaly_rule",
    "week06_lstm_predictions.csv",
    "week06_autoencoder_predictions.csv",
    "AutoSPECTRA_Week06_Images.zip",
    "AutoSPECTRA_Week06_Evidence.zip",
]
forbidden = ["fusion_probabilities", "temperature_scale", "Flask("]

if not NOTEBOOK.exists():
    sys.exit(f"Missing notebook: {NOTEBOOK}")

nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
source = "\n".join("".join(c.get("source", [])) for c in nb["cells"])

missing = [x for x in required if x not in source]
bad = [x for x in forbidden if x in source]

if missing or bad:
    print("Missing:", missing)
    print("Forbidden:", bad)
    sys.exit(1)

print("Week 6 notebook validation PASSED.")
