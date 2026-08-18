from pathlib import Path
import sys

required = [
    "app.py", "requirements.txt", "autospectra/config.py",
    "autospectra/modeling.py", "autospectra/preprocessing.py",
    "templates/index.html", "static/css/style.css"
]
missing = [name for name in required if not (Path(__file__).parent / name).exists()]
if missing:
    print("Missing required files:", missing)
    sys.exit(1)
print("Flask package structure is complete.")
