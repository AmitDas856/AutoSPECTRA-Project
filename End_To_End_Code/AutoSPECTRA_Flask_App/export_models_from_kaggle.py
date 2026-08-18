"""
Copy trained notebook artifacts into the Flask app.

Run inside Kaggle after the AutoSPECTRA notebook has produced
/kaggle/working/autospectra_outputs/models.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

SOURCE = Path("/kaggle/working/autospectra_outputs/models")
DESTINATION = Path(__file__).resolve().parent / "models"
DESTINATION.mkdir(parents=True, exist_ok=True)

if not SOURCE.exists():
    raise FileNotFoundError(
        "Run the AutoSPECTRA training notebook first; model output directory is missing."
    )

for source_file in SOURCE.iterdir():
    if source_file.is_file():
        target = DESTINATION / source_file.name
        shutil.copy2(source_file, target)
        print("Copied:", target)

print("\nModel copy complete.")
print("For exact fusion weights, create models/fusion_config.json using the notebook cell in README.md.")
