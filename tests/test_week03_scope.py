import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = (
    ROOT
    / "notebooks"
    / "week03"
    / "autospectra_week03_windowing_split_features.ipynb"
)


def notebook_source():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
    )


def test_week3_notebook_exists():
    assert NOTEBOOK.exists()


def test_non_overlapping_window_configuration():
    source = notebook_source()
    assert "WINDOW_SIZE = 64" in source
    assert "STRIDE = 64" in source


def test_source_class_chronological_split():
    source = notebook_source()
    assert 'SPLIT_STRATEGY = "source_class_chronological_v3"' in source


def test_required_representations():
    source = notebook_source()
    assert "features.shape[1] == 24" in source
    assert "sequences.shape[1:] == (WINDOW_SIZE, 11)" in source
    assert "sequence_to_recurrence" in source


def test_week3_does_not_train_models():
    source = notebook_source()
    assert "RandomForestClassifier(" not in source
    assert "class RecurrenceCNN" not in source
    assert "class LSTMClassifier" not in source
