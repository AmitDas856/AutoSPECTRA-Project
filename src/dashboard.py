"""AutoSPECTRA live dashboard (Streamlit).
Owner: Nagireddy (NLP + UI). This is the headline live demo for the Week 11/12 pitch.

Run:
    pip install streamlit          # or uncomment streamlit in requirements.txt
    streamlit run src/dashboard.py

What it does: pick a real HCRL capture, replay its unseen test tail through a
quick RandomForest detector, and show detections streaming past with a live
count, a per-class breakdown, and — when an attack is flagged — the
plain-language incident report from incident_report.py.

Design note (say this in the pitch): the terminal fallback demo (src/demo.py)
does the same detection with no browser and no Streamlit, so if anything breaks
on stage the demo still runs. This dashboard is the polished version of that.

The detector here is the frame-level baseline because it trains in seconds live.
Swapping in the trained CNN or LSTM is a later upgrade: load the saved model and
replace the predict call — the incident-report and UI code do not change.
"""

import sys
import time
from pathlib import Path

sys.path.append("src")

import numpy as np

try:
    import streamlit as st
except ImportError:
    sys.exit("Streamlit is not installed. Run: pip install streamlit")

from data.load_split import parse_file, ATTACK_FILES
from incident_report import build_report

CLASS_NAMES = ["Normal", "DoS", "Fuzzy", "Gear", "RPM"]
FEATURES = ["can_id", "dlc"] + [f"d{i}" for i in range(8)]
TRAIN_CAP = 150_000
CHUNK = 3_000


# Caching the parse+train keeps the UI responsive: it only reruns when the
# selected capture changes, not on every Streamlit rerender.
@st.cache_data(show_spinner=False)
def load_capture(attack_name, data_dir="data"):
    fname = next(f for f, a in ATTACK_FILES if a == attack_name)
    df = parse_file(Path(data_dir) / fname, attack_name)
    df = df.sort_values("timestamp").reset_index(drop=True)
    cut = int(len(df) * 0.70)
    return df.iloc[:cut], df.iloc[cut:]


@st.cache_resource(show_spinner=False)
def train_detector(attack_name, data_dir="data"):
    from sklearn.ensemble import RandomForestClassifier
    train, _ = load_capture(attack_name, data_dir)
    rng = np.random.default_rng(0)
    idx = rng.choice(len(train), size=min(TRAIN_CAP, len(train)), replace=False)
    sample = train.iloc[np.sort(idx)]
    clf = RandomForestClassifier(n_estimators=30, n_jobs=-1, random_state=0)
    clf.fit(sample[FEATURES].values, sample["label"].values)
    return clf


def main():
    st.set_page_config(page_title="AutoSPECTRA", page_icon="🚗", layout="wide")
    st.title("🚗 AutoSPECTRA — live CAN-bus intrusion detection")
    st.caption("Replaying a real, unseen slice of vehicle traffic and flagging "
               "injected attacks as they arrive.")

    attack = st.sidebar.selectbox("Capture to replay",
                                  [a for _, a in ATTACK_FILES], index=2)
    speed = st.sidebar.slider("Replay speed (chunks/sec)", 1, 20, 8)
    start = st.sidebar.button("Start replay")

    st.sidebar.markdown("---")
    st.sidebar.info("If the data folder is missing, see 'Get the data' in "
                    "README.md. The terminal fallback is `python src/demo.py`.")

    if not start:
        st.write("Pick a capture and press **Start replay**.")
        return

    with st.spinner(f"Parsing and training on the {attack} capture..."):
        _, test = load_capture(attack)
        clf = train_detector(attack)

    X = test[FEATURES].values
    y = test["label"].values
    ts = test["timestamp"].values
    t0 = ts[0]

    col1, col2 = st.columns(2)
    frames_metric = col1.empty()
    alert_metric = col2.empty()
    progress = st.progress(0.0)
    report_box = st.empty()
    counts = {c: 0 for c in CLASS_NAMES}

    total_flagged = 0
    for s in range(0, len(y), CHUNK):
        e = min(s + CHUNK, len(y))
        pred = clf.predict(X[s:e])
        for c in pred:
            counts[CLASS_NAMES[int(c)]] += 1
        flagged = pred != 0
        total_flagged += int(flagged.sum())

        frames_metric.metric("Frames replayed", f"{e:,} / {len(y):,}")
        alert_metric.metric("Attack frames flagged", f"{total_flagged:,}")
        progress.progress(e / len(y))

        if flagged.any():
            first = int(pred[flagged][0])
            conf = float((pred == first).mean())
            clock = ts[e - 1] - t0
            report_box.error(build_report(CLASS_NAMES[first], confidence=conf,
                                          onset_s=clock,
                                          frames_flagged=int(flagged.sum())))
        time.sleep(1.0 / speed)

    st.success("Replay complete.")
    st.subheader("Detections by class")
    st.bar_chart({k: v for k, v in counts.items() if k != "Normal"})


if __name__ == "__main__":
    main()
