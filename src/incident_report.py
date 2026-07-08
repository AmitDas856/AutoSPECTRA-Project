"""Incident-report generator for AutoSPECTRA.
Owner: Nagireddy (NLP + UI). Block-3 (NLP) component.

Turns a raw detection — an attack class plus a few numbers from the evaluation
harness — into a short, plain-language security-incident report a non-expert
(a driver, a fleet operator) could actually read and act on.

This is deliberately a template-based generator, not a large language model.
For a safety system that is the responsible choice: the output is deterministic,
auditable, and cannot hallucinate a fact that the detector did not report. The
report says exactly what the numbers say and nothing more. That argument is
itself worth marks in the ethics section (see docs/ETHICS.md §5, accountability).

    from incident_report import build_report
    print(build_report("Fuzzy", confidence=0.94, onset_s=22.1,
                        frames_flagged=312, latency_ms=88.0))
"""

# Per-class plain-language knowledge base. Each entry explains what the attack
# is, why it matters in a moving vehicle, and the recommended response. These
# are the facts a driver needs, written for a non-specialist.
ATTACK_INFO = {
    "DoS": {
        "name": "Denial-of-Service (bus flooding)",
        "what": "A flood of high-priority messages was injected onto the CAN bus, "
                "crowding out legitimate traffic from the vehicle's control units.",
        "risk": "Genuine messages (braking, steering, engine) can be delayed or "
                "lost while the bus is saturated.",
        "action": "Isolate the affected bus segment and alert the driver to reduce "
                  "speed and stop safely.",
        "severity": "High",
    },
    "Fuzzy": {
        "name": "Fuzzing (random message injection)",
        "what": "Messages with random identifiers and random contents were injected, "
                "probing the network for an exploitable response.",
        "risk": "Unpredictable actuator behaviour; often a precursor to a targeted "
                "attack once a weakness is found.",
        "action": "Log the offending identifiers, notify the driver, and flag the "
                  "vehicle for a security inspection.",
        "severity": "Medium",
    },
    "Gear": {
        "name": "Gear-status spoofing",
        "what": "Falsified transmission (gear) status messages were injected, "
                "impersonating a legitimate control unit.",
        "risk": "The dashboard or drivetrain logic may act on a false gear state — "
                "dangerous while driving.",
        "action": "Distrust the reported gear state, alert the driver, and isolate "
                  "the spoofed identifier.",
        "severity": "High",
    },
    "RPM": {
        "name": "RPM-gauge spoofing",
        "what": "Falsified engine-speed (RPM) messages were injected onto the bus.",
        "risk": "The instrument cluster shows a false RPM; automated systems relying "
                "on it may misbehave.",
        "action": "Distrust the displayed RPM, alert the driver, and isolate the "
                  "spoofed identifier.",
        "severity": "Medium",
    },
}


def _confidence_phrase(confidence):
    # Turn a probability into words a non-expert understands. Thresholds are a
    # design choice, not learned — keep them explainable.
    if confidence is None:
        return "unknown confidence"
    if confidence >= 0.90:
        return f"high confidence ({confidence:.0%})"
    if confidence >= 0.70:
        return f"moderate confidence ({confidence:.0%})"
    return f"low confidence ({confidence:.0%})"


def build_report(attack_class, confidence=None, onset_s=None,
                 frames_flagged=None, latency_ms=None):
    """Build a plain-language incident report for one detection.

    attack_class : one of DoS / Fuzzy / Gear / RPM (Normal returns an all-clear)
    The remaining arguments are optional numbers from the harness; the report
    only states the ones it is given, so it never invents detail.
    """
    if attack_class == "Normal" or attack_class is None:
        return ("AutoSPECTRA incident report\n"
                "Status: NORMAL. No intrusion detected in the monitored traffic.")

    info = ATTACK_INFO.get(attack_class)
    if info is None:
        # Fail loud but safe — an unknown class is itself worth reporting.
        return (f"AutoSPECTRA incident report\n"
                f"Status: ALERT. An unrecognised detection class '{attack_class}' "
                f"was reported. Manual review required.")

    lines = []
    lines.append("AutoSPECTRA incident report")
    lines.append(f"Status: ALERT - {info['severity']} severity")
    lines.append(f"Attack type: {info['name']} [{attack_class}]")
    lines.append(f"Detection: {_confidence_phrase(confidence)}.")
    lines.append("")
    lines.append(f"What happened: {info['what']}")
    lines.append(f"Why it matters: {info['risk']}")

    # Only add measured detail that was actually supplied.
    facts = []
    if onset_s is not None:
        facts.append(f"first seen about {onset_s:.1f}s into the capture")
    if frames_flagged is not None:
        facts.append(f"{frames_flagged:,} frames flagged")
    if latency_ms is not None:
        facts.append(f"detected within {latency_ms:.0f} ms of onset")
    if facts:
        lines.append("Evidence: " + "; ".join(facts) + ".")

    lines.append(f"Recommended action: {info['action']}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Demo the generator on one detection per class, so a fresh clone can see
    # the output with no model or data needed.
    print(build_report("Fuzzy", confidence=0.94, onset_s=22.1,
                        frames_flagged=312, latency_ms=88.0))
    print("\n" + "-" * 60 + "\n")
    print(build_report("DoS", confidence=0.99, onset_s=10.0, frames_flagged=1500))
    print("\n" + "-" * 60 + "\n")
    print(build_report("Normal"))
