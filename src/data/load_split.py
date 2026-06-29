"""
AutoSPECTRA — HCRL Car-Hacking loader + TIME-ORDERED train/test split.
Owner: Amit (Data + Eval).

Why time-ordered (read this, it's a viva question):
A random shuffle leaks "future" frames into training and fakes a ~99% score.
We train on the EARLIEST traffic and test on the LATEST, so the test set is
genuinely unseen. The assert at the bottom proves we did it.
"""

from pathlib import Path
import pandas as pd

# Class labels we predict. 0 = normal, 1..4 = the four attack types.
CLASSES = {"Normal": 0, "DoS": 1, "Fuzzy": 2, "Gear": 3, "RPM": 4}


def load_attack_file(path: Path, attack_name: str) -> pd.DataFrame:
    """Parse one HCRL attack CSV. Rows flagged 'T' are this attack; 'R' rows are Normal.
    We parse line-by-line because rows have variable length (DLC differs)."""
    rows = []
    with open(path) as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) < 4:
                continue                       # skip blank/broken lines
            ts = float(parts[0])               # timestamp
            can_id = int(parts[1], 16)         # hex id -> integer
            dlc = int(parts[2])                # how many data bytes
            flag = parts[-1]                   # last field is R or T
            data_hex = parts[3:3 + dlc]        # the data bytes
            data = [int(b, 16) for b in data_hex]      # hex -> int
            data = (data + [0] * 8)[:8]        # pad/trim to exactly 8
            label = CLASSES[attack_name] if flag == "T" else CLASSES["Normal"]
            rows.append([ts, can_id, dlc] + data + [label])
    cols = ["timestamp", "can_id", "dlc"] + [f"d{i}" for i in range(8)] + ["label"]
    return pd.DataFrame(rows, columns=cols)


def load_normal_file(path: Path) -> pd.DataFrame:
    """The normal-run file is all Normal traffic (often no Flag column).
    Not used right now — Normal rows come from flag='R' in the attack files."""
    raise NotImplementedError("load_normal_file not needed; Normal comes from R-flagged rows.")


def load_all(data_dir: str) -> pd.DataFrame:
    """Combine every attack file into one DataFrame, sorted by timestamp."""
    data_dir = Path(data_dir)
    frames = [
        load_attack_file(data_dir / "DoS_dataset.csv",   "DoS"),
        load_attack_file(data_dir / "Fuzzy_dataset.csv", "Fuzzy"),
        load_attack_file(data_dir / "gear_dataset.csv",  "Gear"),
        load_attack_file(data_dir / "RPM_dataset.csv",   "RPM"),
        # load_normal_file(data_dir / "normal_run_data.csv"),  # add if needed
    ]
    df = pd.concat(frames, ignore_index=True)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df


def time_ordered_split(df: pd.DataFrame, train_frac: float = 0.70):
    """Earliest train_frac by time -> train; the rest -> test. NO shuffling."""
    df = df.sort_values("timestamp").reset_index(drop=True)
    cut = int(len(df) * train_frac)
    train, test = df.iloc[:cut], df.iloc[cut:]

    # Safety net — do NOT delete this assert to make it pass.
    assert train["timestamp"].max() <= test["timestamp"].min(), \
        "LEAKAGE: train contains frames later than the start of test."
    return train, test


if __name__ == "__main__":
    df = load_all("data/")
    train, test = time_ordered_split(df)
    print(f"Total {len(df):,} frames  |  train {len(train):,}  test {len(test):,}")
    print("Train class counts:\n", train["label"].value_counts().sort_index())
    print("Test class counts:\n", test["label"].value_counts().sort_index())
