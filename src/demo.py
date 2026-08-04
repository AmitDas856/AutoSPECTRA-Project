# demo.py - fallback live demo: replay real CAN traffic and flag attacks as
# they stream past. Ad (CV + Lead).
#
# this is the insurance policy for the week 11/12 pitch: no streamlit, no
# browser, nothing to break - a terminal, one capture file, live detections.
# the streamlit dashboard (Nagireddy's slice) is the headline demo; if it
# isn't ready or dies on the day, this runs instead and the pitch survives.
#
#   python src/demo.py                 # replay the Gear capture's test tail
#   python src/demo.py --file RPM      # or DoS / Fuzzy / RPM
#   python src/demo.py --max-frames 100000
#
# what it does: parse ONE capture -> same 70/30 time split as everywhere else
# -> train a quick RandomForest on the train head -> stream the test tail in
# chunks, printing an alert the moment an attack class is flagged. detector is
# the frame-level baseline (not the CNN) because it trains in seconds live on
# stage - "the model you watched train just caught a real attack" is a better
# story than a pickle file.

import argparse
import sys
import time
from pathlib import Path

sys.path.append("src")

import numpy as np

from data.load_split import parse_file, ATTACK_FILES, CLASSES

CLASS_NAMES = ["Normal", "DoS", "Fuzzy", "Gear", "RPM"]
FEATURES = ["can_id", "dlc"] + [f"d{i}" for i in range(8)]   # frame-level features
TRAIN_CAP = 200_000    # frames used to fit the demo model - keeps startup quick
CHUNK = 2_000          # frames per replay tick
PAUSE_S = 0.05         # small pause per tick so the stream is watchable


def pick_file(name):
    # accept "gear", "Gear", "RPM"... fail with a friendly list, not a traceback
    for fname, attack in ATTACK_FILES:
        if attack.lower() == name.lower():
            return fname, attack
    options = ", ".join(a for _, a in ATTACK_FILES)
    sys.exit(f"unknown capture '{name}' - pick one of: {options}")


def main():
    ap = argparse.ArgumentParser(description="AutoSPECTRA fallback demo - replay real CAN traffic")
    ap.add_argument("--file", default="Gear", help="which capture to replay (DoS/Fuzzy/Gear/RPM)")
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--max-frames", type=int, default=300_000, help="cap the replay length")
    args = ap.parse_args()

    fname, attack = pick_file(args.file)
    path = Path(args.data_dir) / fname
    if not path.exists():
        sys.exit(f"cant find {path} - see 'Get the data' in README.md")

    print(f"[load] parsing {fname} (a couple of minutes - real capture, ~4M frames)")
    df = parse_file(path, attack).sort_values("timestamp").reset_index(drop=True)

    # same time-ordered 70/30 cut as the rest of the project - train on the
    # past, replay the future. no leakage in the demo either.
    cut = int(len(df) * 0.70)
    train, test = df.iloc[:cut], df.iloc[cut:]
    if args.max_frames:
        test = test.iloc[:args.max_frames]

    from sklearn.ensemble import RandomForestClassifier
    rng = np.random.default_rng(0)
    idx = rng.choice(len(train), size=min(TRAIN_CAP, len(train)), replace=False)
    sample = train.iloc[np.sort(idx)]
    print(f"[train] RandomForest on {len(sample):,} train frames...")
    t0 = time.time()
    clf = RandomForestClassifier(n_estimators=30, n_jobs=-1, random_state=0)
    clf.fit(sample[FEATURES].values, sample["label"].values)
    print(f"[train] done in {time.time() - t0:.1f}s - replaying the unseen test tail\n")

    X = test[FEATURES].values
    y = test["label"].values
    ts = test["timestamp"].values
    t_start = ts[0]

    in_alert = False
    alerts = 0
    preds = np.empty(len(y), dtype=np.int64)
    for s in range(0, len(y), CHUNK):
        e = min(s + CHUNK, len(y))
        preds[s:e] = clf.predict(X[s:e])
        flagged = preds[s:e] != 0
        clock = ts[e - 1] - t_start
        if flagged.any():
            if not in_alert:
                first = s + int(np.argmax(flagged))
                name = CLASS_NAMES[int(preds[first])]
                print(f"  t+{clock:7.2f}s  *** ALERT: {name} attack flagged "
                      f"(frame {first:,}, capture time {ts[first]:.2f}) ***")
                alerts += 1
                in_alert = True
        else:
            if in_alert:
                print(f"  t+{clock:7.2f}s  traffic back to normal")
            in_alert = False
        print(f"  t+{clock:7.2f}s  {e:,}/{len(y):,} frames   "
              f"attack frames flagged so far: {int((preds[:e] != 0).sum()):,}",
              end="\r")
        time.sleep(PAUSE_S)
    print()

    # honest wrap-up: how well did the live model actually do on what you saw
    sys.path.append("eval")
    from run_eval import detection_latency, false_positive_rate
    n_attack = int((y != 0).sum())
    caught = int(((y != 0) & (preds == y)).sum())
    print(f"\n[summary] replayed {len(y):,} unseen frames from {fname}")
    print(f"[summary] {n_attack:,} injected attack frames; {caught:,} correctly flagged")
    print(f"[summary] false-positive rate: {false_positive_rate(y, preds)}")
    print(f"[summary] latency: {detection_latency(ts, y, preds)}")
    print("[summary] alert episodes shown:", alerts)


if __name__ == "__main__":
    main()
