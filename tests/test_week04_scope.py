import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = (
    ROOT
    / "notebooks"
    / "week04"
    / "autospectra_week04_classical_baselines.ipynb"
)


def source():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in nb["cells"]
    )


def test_notebook_exists():
    assert NOTEBOOK.exists()


def test_classical_models_are_present():
    text = source()
    assert "LogisticRegression(" in text
    assert "RandomForestClassifier(" in text
    assert "ExtraTreesClassifier(" in text
    assert "XGBClassifier(" in text


def test_week4_saves_images():
    text = source()
    assert "AutoSPECTRA_Week04_Images.zip" in text
    assert 'PLOT_DIR / "week04_macro_f1_comparison.png"' in text or \
           'save_current_figure("week04_macro_f1_comparison.png")' in text


def test_later_models_are_not_present():
    text = source()
    assert "class RecurrenceCNN" not in text
    assert "class LSTMClassifier" not in text
    assert "class LSTMSequenceAutoencoder" not in text
