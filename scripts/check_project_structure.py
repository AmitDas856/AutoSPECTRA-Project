from pathlib import Path
import sys

REQUIRED_PATHS = [
    "README.md",
    "requirements.txt",
    "configs/week1_baseline.yaml",
    "data/README.md",
    "docs/architecture/system_architecture.md",
    "docs/project-management/project_charter.md",
    "docs/project-management/roles_and_responsibilities.md",
    "docs/project-management/week1_issues.md",
    "docs/ethics/initial_risk_register.md",
    "docs/meeting-notes/week01-kickoff.md",
    "docs/AI-USE-LOG.md",
    "src/autospectra",
    "tests",
]

root = Path(__file__).resolve().parents[1]
missing = [path for path in REQUIRED_PATHS if not (root / path).exists()]

if missing:
    print("Project structure check FAILED.")
    print("Missing:")
    for item in missing:
        print(f"  - {item}")
    sys.exit(1)

print("Project structure check PASSED.")
print(f"Checked {len(REQUIRED_PATHS)} required paths.")
