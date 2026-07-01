"""HCRL Car-Hacking loader and time-ordered train/test split. Amit (Data + Eval)."""

# Why the split is time-ordered: a random shuffle would put "future" frames in
# the training set and the score would be falsely high (data leakage). We train
# on the earliest traffic and test on the latest traffic, so the test set is
# genuinely unseen. The assert below proves the split is correct.
#
# Why the split is done per file: each attack CSV is a separate capture session
# with its own time range. When the files were merged first and split after,
# three attack classes ended up completely missing from the test set. Splitting
# each file 70/30 on its own timeline keeps every class in both sets and the
# no-leakage rule still holds inside each file.

from pathlib import Path
import pandas as pd

# Class labels. 0 is normal traffic, 1 to 4 are the four attack types.
CLASSES = {"Normal": 0, "DoS": 1, "Fuzzy": 2, "Gear": 3, "RPM": 4}

# The four attack files and the attack each one contains.
ATTACK_FILES = [
    ("DoS_dataset.csv",   "DoS"),
    ("Fuzzy_dataset.csv", "Fuzzy"),
    ("gear_dataset.csv",  "Gear"),
    ("RPM_dataset.csv",   "RPM"),
]


def parse_file(path, attack_name):
    # Parse one attack CSV line by line. The rows have different lengths
    # because DLC (number of data bytes) varies, so a plain read_csv fails.
    # A row flagged 'T' is an injected attack frame, 'R' is normal traffic.
    rows = []
    with open(path) as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) < 4:
                continue
            try:
                ts = float(parts[0])
                can_id = int(parts[1], 16)
                dlc = int(parts[2])
                flag = parts[-1]
                data = [int(b, 16) for b in parts[3:3 + dlc]]
                # Pad with zeros up to 8 bytes, cut anything extra.
                while len(data) < 8:
                    data.append(0)
                data = data[:8]
                if flag == "T":
                    label = CLASSES[attack_name]
                else:
                    label = CLASSES["Normal"]
                rows.append([ts, can_id, dlc] + data + [label])
            except (ValueError, IndexError):
                # Skip lines that do not parse (header row or broken line).
                continue
    cols = ["timestamp", "can_id", "dlc"] + [f"d{i}" for i in range(8)] + ["label"]
    return pd.DataFrame(rows, columns=cols)


def load_and_split(data_dir, train_frac=0.70, return_parts=False):
    # Load every attack file and split each one 70/30 on its own timeline.
    # With return_parts=True the caller gets the per-file pieces instead of
    # one combined DataFrame. The CNN needs that, because a window of frames
    # must never span two different capture files.
    data_dir = Path(data_dir)
    parts = []

    for fname, attack in ATTACK_FILES:
        df = parse_file(data_dir / fname, attack)
        df = df.sort_values("timestamp").reset_index(drop=True)
        cut = int(len(df) * train_frac)
        tr = df.iloc[:cut].copy()
        te = df.iloc[cut:].copy()

        # The leakage check. Do NOT delete this to make the script pass.
        assert tr["timestamp"].max() <= te["timestamp"].min(), \
            f"LEAKAGE in {fname}: train contains frames later than test start."

        parts.append((attack, tr, te))
        print(f"  {attack}: {len(tr):,} train | {len(te):,} test")

    if return_parts:
        return parts

    train = pd.concat([tr for _, tr, _ in parts], ignore_index=True)
    test = pd.concat([te for _, _, te in parts], ignore_index=True)
    return train, test


if __name__ == "__main__":
    print("Loading and splitting HCRL data (per-file time-ordered split)...")
    train, test = load_and_split("data/")
    print(f"\nTotal  train {len(train):,}  |  test {len(test):,}")
    print("Train class counts:\n", train["label"].value_counts().sort_index())
    print("Test class counts:\n", test["label"].value_counts().sort_index())
