"""
SIH26141 - STEP 3 REFINED: Statistical Detection Engine

Key refinement:
- The normal baseline is calibrated once and persisted to data/baseline.json.
- Future runs use that SAME baseline.
- Detection parameters are explicit and configurable.
- The risk score is clearly a prototype indicator, not an attack probability.

No AI/ML is used.
"""

from __future__ import annotations

from math import log
from pathlib import Path
from typing import Dict, Any

import numpy as np

from .engine import run_bell_state
from .attacks import (
    simulate_forgery,
    simulate_impersonation,
    ReplayGuard,
    simulate_channel_manipulation,
)
from .calibration import load_baseline, BASELINE_FILE


# ---------------------------------------------------------------------
# Prototype configuration
# ---------------------------------------------------------------------

DEFAULT_ATTACK_PROBABILITY = 0.08
DEFAULT_LR_THRESHOLD = 10.0


# ---------------------------------------------------------------------
# Measurement analysis
# ---------------------------------------------------------------------

def bell_statistics(counts: Dict[str, int]) -> Dict[str, Any]:
    total = sum(counts.values())
    if total == 0:
        raise ValueError("No measurement shots were returned.")

    observed_00 = counts.get("00", 0)
    observed_11 = counts.get("11", 0)
    observed_unexpected = counts.get("01", 0) + counts.get("10", 0)

    expected_00 = total * 0.50
    expected_11 = total * 0.50

    deviation = observed_unexpected / total

    chi_square = (
        ((observed_00 - expected_00) ** 2) / expected_00
        + ((observed_11 - expected_11) ** 2) / expected_11
    )

    return {
        "shots": total,
        "00": observed_00,
        "11": observed_11,
        "unexpected": observed_unexpected,
        "deviation": deviation,
        "chi_square": chi_square,
        "p00": observed_00 / total,
        "p11": observed_11 / total,
    }


def binomial_log_likelihood(k: int, n: int, p: float) -> float:
    eps = 1e-12
    p = min(max(p, eps), 1.0 - eps)
    return k * log(p) + (n - k) * log(1.0 - p)


def likelihood_ratio(
    unexpected_count: int,
    shots: int,
    normal_probability: float,
    attack_probability: float,
) -> float:
    log_attack = binomial_log_likelihood(
        unexpected_count, shots, attack_probability
    )
    log_normal = binomial_log_likelihood(
        unexpected_count, shots, normal_probability
    )

    log_ratio = log_attack - log_normal

    if log_ratio > 700:
        return float("inf")
    if log_ratio < -700:
        return 0.0

    return float(np.exp(log_ratio))


def analyze_measurements(
    counts: Dict[str, int],
    baseline: Dict[str, Any],
    attack_probability: float = DEFAULT_ATTACK_PROBABILITY,
    likelihood_threshold: float = DEFAULT_LR_THRESHOLD,
) -> Dict[str, Any]:
    """
    Compare measurements against the SAVED calibration baseline.
    No recalibration occurs here.
    """
    stats = bell_statistics(counts)

    threshold = float(baseline["threshold"])
    normal_probability = max(float(baseline["mean_deviation"]), 1e-6)

    threshold_breach = stats["deviation"] > threshold

    lr = likelihood_ratio(
        stats["unexpected"],
        stats["shots"],
        normal_probability,
        attack_probability,
    )

    likelihood_breach = lr > likelihood_threshold

    detected = threshold_breach or likelihood_breach

    return {
        **stats,
        "baseline_mean_deviation": normal_probability,
        "threshold": threshold,
        "likelihood_ratio_attack_vs_normal": lr,
        "likelihood_threshold": likelihood_threshold,
        "threshold_breach": threshold_breach,
        "likelihood_breach": likelihood_breach,
        "detected": detected,
        "decision": "THREAT DETECTED" if detected else "NORMAL",
    }


# ---------------------------------------------------------------------
# Direct attacks from Step 2
# ---------------------------------------------------------------------

def direct_attack_decision(attack_result) -> Dict[str, Any]:
    detected = attack_result.detected_signal not in {"No replay detected"}

    return {
        **attack_result.to_dict(),
        "detected": detected,
        "decision": "THREAT DETECTED" if detected else "NORMAL",
    }


# ---------------------------------------------------------------------
# Transparent prototype risk indicator
# ---------------------------------------------------------------------

def calculate_prototype_risk(
    channel_detected: bool,
    direct_attack_detected: bool,
    deviation: float,
    threshold: float,
) -> int:
    score = 0

    if direct_attack_detected:
        score += 60

    if channel_detected:
        score += 30

    if threshold > 0 and deviation > threshold:
        excess_ratio = min(deviation / threshold, 3.0)
        score += int(10 * (excess_ratio / 3.0))

    return min(score, 100)


# ---------------------------------------------------------------------
# Test runners
# ---------------------------------------------------------------------

def run_scenario(
    name: str,
    noise_probability: float,
    shots: int,
    baseline: Dict[str, Any],
) -> Dict[str, Any]:
    counts = run_bell_state(
        shots=shots,
        noise_probability=noise_probability,
    )

    analysis = analyze_measurements(
        counts,
        baseline,
        attack_probability=DEFAULT_ATTACK_PROBABILITY,
        likelihood_threshold=DEFAULT_LR_THRESHOLD,
    )

    return {
        "scenario": name,
        "noise_probability": noise_probability,
        "counts": counts,
        "analysis": analysis,
    }


def main():
    shots = 4096

    print("=" * 68)
    print("SIH26141 - STEP 3 REFINED")
    print("PERSISTENT BASELINE + STATISTICAL DETECTION")
    print("=" * 68)

    # --------------------------------------------------------------
    # 0. Load fixed baseline
    # --------------------------------------------------------------
    try:
        baseline = load_baseline()
    except FileNotFoundError as exc:
        print("\nERROR:", exc)
        return

    print("\n[0] SAVED CALIBRATION")
    print(f"Baseline file     : {BASELINE_FILE}")
    print(f"Calibration noise : {baseline['noise_probability']:.3f}")
    print(f"Mean deviation    : {baseline['mean_deviation']:.4%}")
    print(f"Std deviation     : {baseline['std_deviation']:.4%}")
    print(f"Threshold         : {baseline['threshold']:.4%}")

    # --------------------------------------------------------------
    # 1. Normal verification
    # --------------------------------------------------------------
    print("\n[1] NORMAL QUANTUM TEST")

    normal = run_scenario(
        "Normal",
        noise_probability=float(baseline["noise_probability"]),
        shots=shots,
        baseline=baseline,
    )

    a = normal["analysis"]

    print(f"00                  : {a['p00']:.4%}")
    print(f"11                  : {a['p11']:.4%}")
    print(f"Unexpected outcomes : {a['unexpected']}")
    print(f"Deviation           : {a['deviation']:.4%}")
    print(f"Threshold           : {a['threshold']:.4%}")
    print(f"Chi-square          : {a['chi_square']:.4f}")
    print(f"Likelihood ratio    : {a['likelihood_ratio_attack_vs_normal']:.4g}")
    print(f"Threshold breach    : {a['threshold_breach']}")
    print(f"Likelihood breach   : {a['likelihood_breach']}")
    print(f"Decision             : {a['decision']}")

    # --------------------------------------------------------------
    # 2. Channel manipulation
    # --------------------------------------------------------------
    print("\n[2] CHANNEL MANIPULATION TEST")

    attack_noise = 0.08

    attacked = run_scenario(
        "Channel Manipulation",
        noise_probability=attack_noise,
        shots=shots,
        baseline=baseline,
    )

    a2 = attacked["analysis"]

    attack = simulate_channel_manipulation(
        baseline_noise=float(baseline["noise_probability"]),
        injected_disturbance=attack_noise,
    )

    print(f"Injected disturbance: {attack.modified_value}")
    print(f"00                  : {a2['p00']:.4%}")
    print(f"11                  : {a2['p11']:.4%}")
    print(f"Unexpected outcomes : {a2['unexpected']}")
    print(f"Deviation           : {a2['deviation']:.4%}")
    print(f"Threshold           : {a2['threshold']:.4%}")
    print(f"Chi-square          : {a2['chi_square']:.4f}")
    print(f"Likelihood ratio    : {a2['likelihood_ratio_attack_vs_normal']:.4g}")
    print(f"Threshold breach    : {a2['threshold_breach']}")
    print(f"Likelihood breach   : {a2['likelihood_breach']}")
    print(f"Decision             : {a2['decision']}")

    # --------------------------------------------------------------
    # 3. Direct attacks
    # --------------------------------------------------------------
    print("\n[3] DIRECT ATTACK CONDITIONS")

    forgery = direct_attack_decision(simulate_forgery())
    impersonation = direct_attack_decision(simulate_impersonation())

    replay_guard = ReplayGuard()
    replay_guard.verify("QDS-SIG-001")
    replay = direct_attack_decision(
        replay_guard.verify("QDS-SIG-001")
    )

    print(f"Forgery       : {forgery['decision']}")
    print(f"Impersonation : {impersonation['decision']}")
    print(f"Replay        : {replay['decision']}")

    # --------------------------------------------------------------
    # 4. Prototype risk indicator
    # --------------------------------------------------------------
    normal_risk = calculate_prototype_risk(
        channel_detected=a["detected"],
        direct_attack_detected=False,
        deviation=a["deviation"],
        threshold=a["threshold"],
    )

    attack_risk = calculate_prototype_risk(
        channel_detected=a2["detected"],
        direct_attack_detected=True,
        deviation=a2["deviation"],
        threshold=a2["threshold"],
    )

    print("\n[4] PROTOTYPE RISK INDICATOR")
    print(f"Normal scenario         : {normal_risk}/100")
    print(f"Channel attack scenario : {attack_risk}/100")

    print("\nStep 3 refinement completed.")
    print("The baseline is loaded from disk; it is NOT recalibrated during detection.")
    print("No AI/ML is used.")


if __name__ == "__main__":
    main()
