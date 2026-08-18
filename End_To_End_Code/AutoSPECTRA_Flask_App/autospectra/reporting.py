from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from .config import CLASS_NAMES

SEVERITY_BY_CLASS = {
    "Normal": "Informational",
    "DoS": "Critical",
    "Fuzzy": "High",
    "Gear": "Critical",
    "RPM": "High",
}

RECOMMENDATION_BY_CLASS = {
    "Normal": "Continue monitoring. No automated vehicle-control action is recommended.",
    "DoS": (
        "Alert the security operator, preserve the CAN trace, identify the flooding "
        "identifier, and isolate the suspected interface only after human review."
    ),
    "Fuzzy": (
        "Alert the security operator, preserve the trace, investigate unusual identifiers "
        "and payloads, and verify ECU integrity."
    ),
    "Gear": (
        "Issue a high-priority alert, preserve evidence, verify transmission-related "
        "signals, and require human confirmation before any intervention."
    ),
    "RPM": (
        "Issue a high-priority alert, preserve evidence, verify engine-speed signals, "
        "and require human confirmation before any intervention."
    ),
}


def generate_incident_record(
    probabilities: np.ndarray,
    metadata_row: pd.Series,
    model_name: str,
    window_size: int,
) -> tuple[dict[str, Any], str]:
    predicted_index = int(np.argmax(probabilities))
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = float(np.max(probabilities))
    severity = SEVERITY_BY_CLASS[predicted_class]
    recommendation = RECOMMENDATION_BY_CLASS[predicted_class]

    record = {
        "system": "AutoSPECTRA",
        "model": model_name,
        "window_index": int(metadata_row["window_index"]),
        "predicted_class": predicted_class,
        "confidence": round(confidence, 6),
        "severity": severity,
        "window_start_timestamp": float(metadata_row["start_timestamp"]),
        "window_end_timestamp": float(metadata_row["end_timestamp"]),
        "window_size_frames": int(window_size),
        "dominant_can_id": str(metadata_row["dominant_can_id"]),
        "message_rate_hz": round(float(metadata_row["message_rate_hz"]), 2),
        "unique_can_ids": int(metadata_row["unique_can_ids"]),
        "id_entropy_bits": round(float(metadata_row["id_entropy_bits"]), 3),
        "recommended_action": recommendation,
        "human_oversight": (
            "Decision-support alert only. Do not automatically disable braking, steering, "
            "engine, transmission, or other safety-critical functions."
        ),
    }

    if predicted_class == "Normal":
        narrative = (
            f"AutoSPECTRA analysed a {window_size}-frame CAN window ending at "
            f"{record['window_end_timestamp']:.6f}. The {model_name} classified the traffic "
            f"as normal with {confidence:.1%} confidence. The window contained approximately "
            f"{record['message_rate_hz']:.1f} messages per second and "
            f"{record['unique_can_ids']} unique CAN identifiers. Recommended action: "
            f"{recommendation}"
        )
    else:
        narrative = (
            f"{severity} AutoSPECTRA alert: {predicted_class} activity was detected in the "
            f"CAN window from {record['window_start_timestamp']:.6f} to "
            f"{record['window_end_timestamp']:.6f}. The {model_name} confidence was "
            f"{confidence:.1%}. The dominant identifier was {record['dominant_can_id']}; "
            f"the window contained approximately {record['message_rate_hz']:.1f} messages "
            f"per second and {record['unique_can_ids']} unique identifiers. Recommended "
            f"action: {recommendation} This is a decision-support alert and requires human review."
        )

    return record, narrative


def summarise_predictions(probabilities: np.ndarray) -> dict[str, Any]:
    predictions = probabilities.argmax(axis=1)
    confidences = probabilities.max(axis=1)
    counts = {name: int(np.sum(predictions == index)) for index, name in enumerate(CLASS_NAMES)}
    attack_mask = predictions != 0

    return {
        "total_windows": int(len(predictions)),
        "normal_windows": counts["Normal"],
        "attack_windows": int(attack_mask.sum()),
        "attack_rate": float(attack_mask.mean()) if len(predictions) else 0.0,
        "mean_confidence": float(confidences.mean()) if len(confidences) else 0.0,
        "highest_confidence": float(confidences.max()) if len(confidences) else 0.0,
        "class_counts": counts,
    }
