"""
AutoSPECTRA — HCRL Car-Hacking loader + TIME-ORDERED train/test split.
Owner: Amit (Data + Eval).

Why time-ordered (read this, it's a viva question):
A random shuffle leaks "future" frames into training and fakes a ~99% score.
We train on the EARLIEST traffic and test on the LATEST, so the test set is
genuinely unseen. The assert at the bottom proves we did it.

Why per-file split (second key decision):
Each HCRL attack CSV is a separate capture session with its own time range.
A global merge-then-split concentrates all early attacks in train and leaves
some classes completely absent from the test set. Per-file split preserves the
no-leakage property within each session while ensuring all 5 classes appear
in both train and test.
"""

from pathlib import Path
import pandas as pd

CLASSES = {"Normal": 0, "DoS": 1, "Fuzzy": 2, "Gear": 3, "RPM": 4}

ATTACK_FILES = [
    ("DoS_dataset.csv",   "DoS"),
    ("Fuzzy_dataset.csv", "Fuzzy"),
    ("gear_dataset.csv",  "Gear"),
    ("RPM_dataset.csv",   "RPM"),
]


def _parse_file(path: Path, attack_name: str) -> pd.DataFrame:
    """Parse one HCRL attack CSV line-by-line (DLC varies so row lengths differ)."""
    rows = []
    with open(path) as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) < 4:
                continue
            try:
                ts     = float(parts[0])
                can_id = int(parts[1], 16)
                dlc    = int(parts[2])
                flag   = parts[-1]
                data   = [int(b, 16) for b in parts[3:3 + dlc]]
                data   = (data + [0] * 8)[:8]          # pad/trim to exactly 8
                label  = CLASSES[attack_name] if flag == "T" else CLASSES["Normal"]
                rows.append([ts, can_id, dlc] + data + [label])
            except (ValueError, IndexError):
                continue                                # skip malformed lines
    cols = ["timestamp", "can_id", "dlc"] + [f"d{i}" for i in range(8)] + ["label"]
    return pd.DataFrame(rows, columns=cols)


def load_and_split(data_dir: str, train_frac: float = 0.70):
    """Per-file time-ordered split — ensures all 5 attack classes in both sets.

    For each file: sort by timestamp, take first train_frac as train, rest as test.
    Then concatenate across files. The leakage assert is checked within each file.
    """
    data_dir = Path(data_dir)
    train_parts, test_parts = [], []

    for fname, attack in ATTACK_FILES:
        df = _parse_file(data_dir / fname, attack)
        df = df.sort_values("timestamp").reset_index(drop=True)
        cut = int(len(df) * train_frac)
        tr, te = df.iloc[:cut].copy(), df.iloc[cut:].copy()

        # Per-file leakage check — do NOT remove this
        assert tr["timestamp"].max() <= te["timestamp"].min(), \
            f"LEAKAGE in {fname}: train contains frames later than test start."

        train_parts.append(tr)
        test_parts.append(te)
        print(f"  {attack}: {len(tr):,} train | {len(te):,} test")

    train = pd.concat(train_parts, ignore_index=True)
    test  = pd.concat(test_parts,  ignore_index=True)
    return train, test


if __name__ == "__main__":
    print("Loading and splitting HCRL data (per-file time-ordered split)...")
    train, test = load_and_split("data/")
    print(f"\nTotal  train {len(train):,}  |  test {len(test):,}")
    print("Train class counts:\n", train["label"].value_counts().sort_index())
    print("Test class counts:\n",  test["label"].value_counts().sort_index())
