from pathlib import Path

def test_readme_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "README.md").exists()

def test_architecture_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "docs/architecture/system_architecture.md").exists()

def test_responsible_use_statement_exists():
    root = Path(__file__).resolve().parents[1]
    text = (root / "README.md").read_text(encoding="utf-8").lower()
    assert "decision-support" in text
    assert "must not automatically control" in text
