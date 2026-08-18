# AutoSPECTRA Flask Application

This application turns the completed AutoSPECTRA Kaggle notebook into a live web demonstration. It accepts an HCRL-style CAN capture, creates chronological windows using the same preprocessing used during training, runs an available model, displays charts, and generates downloadable incident reports.

## Features

- Upload `.csv`, `.txt`, or `.log` CAN captures.
- Exact 24-feature Random Forest preprocessing from the training notebook.
- Exact 11-variable sequence representation for the LSTM and recurrence CNN.
- Optional Random Forest + CNN + LSTM fusion.
- Five classes: Normal, DoS, Fuzzy, Gear, and RPM.
- Class-distribution, confidence, message-rate, and probability visualisations.
- Plain-language and structured JSON incident reports.
- CSV and JSON downloads.
- `/api/predict` endpoint for programmatic use.
- Human-oversight and safety warnings built into every attack report.

## 1. Copy trained models

After the Kaggle training notebook finishes, its models are normally located at:

```text
/kaggle/working/autospectra_outputs/models/
```

Copy these files into this application's `models/` folder. The minimum file is:

```text
random_forest.joblib
```

The app automatically enables deeper options when these are also present:

```text
recurrence_cnn.pt
lstm_classifier.pt
extra_trees.joblib
logistic_regression.joblib
fusion_calibration.json
fusion_config.json
```

You can instead set:

```bash
AUTOSPECTRA_MODEL_DIR=/absolute/path/to/autospectra_outputs/models
```

## 2. Run locally on Windows

Open Command Prompt in this folder and run:

```bat
run_local.bat
```

Or run manually:

```bat
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 3. Run locally on macOS or Linux

```bash
chmod +x run_local.sh
./run_local.sh
```

## 4. Run in Kaggle

### A. Add the Flask app

Upload `AutoSPECTRA_Flask_App.zip` as a Kaggle dataset or notebook file, then unzip it:

```python
import zipfile
from pathlib import Path

zip_path = Path("/kaggle/input/YOUR-UPLOAD/AutoSPECTRA_Flask_App.zip")
app_dir = Path("/kaggle/working/AutoSPECTRA_Flask_App")

with zipfile.ZipFile(zip_path) as archive:
    archive.extractall("/kaggle/working")

print(app_dir)
```

### B. Copy the trained model artifacts

```python
import shutil
from pathlib import Path

source = Path("/kaggle/working/autospectra_outputs/models")
target = Path("/kaggle/working/AutoSPECTRA_Flask_App/models")
target.mkdir(parents=True, exist_ok=True)

for model_file in source.iterdir():
    if model_file.is_file():
        shutil.copy2(model_file, target / model_file.name)
```

### C. Export the exact validation-derived fusion settings

Run this in the same notebook session after the training/fusion cells:

```python
import json
from pathlib import Path

flask_model_dir = Path("/kaggle/working/AutoSPECTRA_Flask_App/models")
flask_model_dir.mkdir(parents=True, exist_ok=True)

if "fusion_weights" in globals():
    payload = {
        "weights": {name: float(value) for name, value in fusion_weights.items()},
        "temperature": float(globals().get("best_temperature", 1.0)),
    }
    (flask_model_dir / "fusion_config.json").write_text(
        json.dumps(payload, indent=2)
    )
    print(payload)
else:
    print("Fusion variables are not in memory. The app can still use Random Forest.")
```

### D. Install and launch through ngrok

Create an ngrok account, place the token in a Kaggle secret named `NGROK_AUTHTOKEN`, and run:

```python
!pip install -q -r /kaggle/working/AutoSPECTRA_Flask_App/requirements.txt

from kaggle_secrets import UserSecretsClient
import os

os.environ["NGROK_AUTHTOKEN"] = UserSecretsClient().get_secret("NGROK_AUTHTOKEN")
%cd /kaggle/working/AutoSPECTRA_Flask_App
!python kaggle_launch.py
```

The cell prints a public HTTPS URL. Keep the cell running during the demonstration.

## 5. Recommended live-demonstration settings

- Model: `RF + CNN + LSTM Fusion` when exact weights were exported; otherwise `Random Forest`.
- Window size: fixed automatically from the trained checkpoint, normally 64.
- Stride: 64 for non-overlapping windows.
- Maximum windows: 100–500 for a fast pitch demonstration.
- Input: a small unseen excerpt rather than an entire multi-million-row dataset.

## 6. API example

```bash
curl -X POST \
  -F "can_file=@sample.csv" \
  -F "model_key=random_forest" \
  -F "max_windows=100" \
  http://127.0.0.1:5000/api/predict
```

## 7. Production note

`python app.py` uses Flask's development server and is suitable for local assessment demonstrations. For a more stable Windows run:

```bat
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

For Linux/macOS, a production WSGI server can be used instead. Never enable Flask debug mode on a public tunnel.

## Safety and limitations

AutoSPECTRA is an academic decision-support prototype. It was trained on public data from a limited vehicle context. It must not automatically disable ECUs or control braking, steering, engine, or transmission systems. Predictions require human review.
