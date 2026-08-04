#!/usr/bin/env python3
"""
AutoSPECTRA - CAN-bus Intrusion Detection prototype (AAI group project).

Pipeline:  CAN frames -> window -> features (+ optional image encoding) -> classifier -> attack class -> incident report

This runs with NO download and NO GPU: it generates synthetic CAN traffic with
injected attacks (DoS, Fuzzy, Spoof, Gear) so the whole pipeline is demoable today.
Swap `generate_can_traffic()` for a loader of the real HCRL Car-Hacking dataset
(same (timestamp, can_id, payload, label) shape) when you download it.

    pip install -r requirements.txt
    python src/can_ids.py --demo        # generate -> train -> evaluate -> sample report
"""
from __future__ import annotations

import argparse
import math
import random
from collections import Counter
from typing import Optional

try:
    import numpy as np
except ImportError:
    np = None  # type: ignore

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, confusion_matrix
    SKLEARN = True
except ImportError:
    SKLEARN = False

# Typical periodic CAN arbitration IDs (stand-ins for real ECU IDs).
NORMAL_IDS = [0x130, 0x131, 0x140, 0x153, 0x164, 0x18F, 0x220, 0x316, 0x329, 0x370]
ATTACK_WINDOWS = {  # (start_s, end_s) -> attack injected during that interval
    "DoS": (10, 13), "Fuzzy": (22, 25), "Spoof": (34, 37), "Gear": (46, 49),
}


# --------------------------------------------------------------------------- #
# 1. Data: synthetic CAN traffic with injected attacks (swap for Car-Hacking)
# --------------------------------------------------------------------------- #
def generate_can_traffic(seconds: int = 60, hz: int = 500, seed: int = 0) -> list[tuple]:
    """Return frames as (timestamp, can_id, payload[8], label)."""
    random.seed(seed)
    frames = []
    dt = 1.0 / hz
    for i in range(seconds * hz):
        t = i * dt
        cid = random.choice(NORMAL_IDS)
        payload = [random.randint(0, 255) for _ in range(8)]
        label = "Normal"
        for atk, (a, b) in ATTACK_WINDOWS.items():
            if a <= t < b:
                if atk == "DoS":            # flood a high-priority ID
                    cid, payload, label = 0x000, [0] * 8, "DoS"
                elif atk == "Fuzzy":        # random IDs + payloads
                    cid, payload, label = random.randint(0, 0x7FF), [random.randint(0, 255) for _ in range(8)], "Fuzzy"
                elif atk == "Spoof":        # legit ID, falsified payload
                    cid, payload, label = 0x316, [0xFF] * 8, "Spoof"
                elif atk == "Gear":         # injected gear-status ID
                    cid, payload, label = 0x43F, [random.randint(0, 255) for _ in range(8)], "Gear"
                break
        frames.append((t, cid, payload, label))
    return frames


# --------------------------------------------------------------------------- #
# 2. Feature engineering over sliding windows
# --------------------------------------------------------------------------- #
def _entropy(counts) -> float:
    total = sum(counts)
    return -sum((c / total) * math.log2(c / total) for c in counts if c) if total else 0.0


def window_features(frames: list[tuple], win: int = 50, step: int = 25):
    """Return (X feature rows, y labels) over sliding windows of frames."""
    X, y = [], []
    for s in range(0, len(frames) - win, step):
        w = frames[s:s + win]
        ids = [f[1] for f in w]
        idc = Counter(ids)
        n = len(w)
        bytes_ = [b for f in w for b in f[2]]
        interarr = [w[k][0] - w[k - 1][0] for k in range(1, n)]
        X.append([
            len(idc),                                   # unique IDs
            _entropy(list(idc.values())),               # ID entropy (drops in DoS)
            max(idc.values()) / n,                      # max single-ID rate (spikes in DoS)
            _entropy(list(Counter(bytes_).values())),   # payload byte entropy (spikes in Fuzzy)
            sum(bytes_) / len(bytes_),                  # mean byte value
            (sum(interarr) / len(interarr)) if interarr else 0.0,  # mean inter-arrival
        ])
        attack = [f[3] for f in w if f[3] != "Normal"]
        y.append(Counter(attack).most_common(1)[0][0] if attack else "Normal")
    return X, y


def to_image(frames: list[tuple], win: int = 50):
    """CV layer (Block 2): encode a window's ID sequence as a recurrence-style image
    for a CNN (Rec-CNN style). Returned for the CNN model; the baseline below uses features."""
    if np is None:
        return None
    ids = np.array([f[1] for f in frames[:win]], dtype=float)
    ids = ids / (ids.max() + 1e-9)
    return (np.abs(ids[:, None] - ids[None, :]) < 0.02).astype(float)  # recurrence matrix


# --------------------------------------------------------------------------- #
# 3. Train + evaluate (baseline) and report
# --------------------------------------------------------------------------- #
def run_demo(seconds: int = 60) -> None:
    frames = generate_can_traffic(seconds=seconds)
    X, y = window_features(frames)
    n_attack = sum(1 for v in y if v != "Normal")
    print(f"[data] {len(frames)} CAN frames -> {len(X)} windows ({n_attack} contain attacks)")

    if not SKLEARN:
        print("[note] scikit-learn not installed - showing rule-based fallback.")
        # simple rule: high max-ID-rate or high payload entropy => attack
        preds = ["DoS" if row[2] > 0.5 else ("Fuzzy" if row[3] > 7.5 else "Normal") for row in X]
        acc = sum(p == t for p, t in zip(preds, y)) / len(y)
        print(f"[rule-based] accuracy = {acc:.0%}  (install scikit-learn for the ML model)")
        return

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
    clf = RandomForestClassifier(n_estimators=120, random_state=0)
    clf.fit(Xtr, ytr)
    pred = clf.predict(Xte)
    print("\n=== Evaluation (per-class precision / recall / F1) ===")
    print(classification_report(yte, pred, zero_division=0))
    print("=== Confusion matrix ===")
    labels = sorted(set(y))
    print("labels:", labels)
    print(confusion_matrix(yte, pred, labels=labels))
    print("\n" + incident_report(yte, pred, frames))


def incident_report(y_true, y_pred, frames) -> str:
    """NLP layer (Block 3): plain-language security-incident summary from detections."""
    detected = Counter(p for p in y_pred if p != "Normal")
    if not detected:
        return "[report] No intrusions detected in the evaluated window."
    lines = ["=== AutoSPECTRA incident report ==="]
    for atk, count in detected.most_common():
        first = next((f[0] for f in frames if f[3] == atk), 0.0)
        lines.append(f"- {atk} attack detected: {count} flagged windows; earliest onset ~{first:.1f}s. "
                     f"Recommended action: isolate affected ECU / alert driver.")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="AutoSPECTRA CAN-bus intrusion detection prototype")
    ap.add_argument("--demo", action="store_true", help="generate synthetic traffic, train, evaluate")
    ap.add_argument("--seconds", type=int, default=60, help="seconds of synthetic CAN traffic")
    args = ap.parse_args()
    if args.demo:
        run_demo(args.seconds)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
