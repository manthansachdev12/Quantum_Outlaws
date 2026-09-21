
import math
from .engine import bell_state
from .calibration import load_baseline, calculate_deviation

DEFAULT_ATTACK_PROBABILITY=0.08
DEFAULT_LR_THRESHOLD=10.0

def chi_square_for_bell(counts, shots):
    expected=shots/2
    a=counts.get("00",0)
    b=counts.get("11",0)
    return ((a-expected)**2/expected)+((b-expected)**2/expected)

def detect_channel(shots=4096, noise_probability=0.08, likelihood_threshold=DEFAULT_LR_THRESHOLD):
    baseline=load_baseline()
    if baseline is None:
        raise RuntimeError("Baseline not calibrated. Run /calibrate first.")
    counts=bell_state(shots=shots, noise_probability=noise_probability)
    deviation=calculate_deviation(counts, shots)
    threshold=baseline["threshold_percent"]
    chi=chi_square_for_bell(counts, shots)
    normal_mean=max(baseline["mean_deviation_percent"], 1e-9)
    likelihood_ratio=math.exp(min(700, (deviation-normal_mean)*12))
    threshold_breach=deviation > threshold
    likelihood_breach=likelihood_ratio > likelihood_threshold
    detected=threshold_breach or likelihood_breach
    risk=100 if detected else 0
    return {
        "attack":"channel_manipulation",
        "counts":counts,
        "shots":shots,
        "observed_deviation_percent":deviation,
        "baseline_mean_percent":baseline["mean_deviation_percent"],
        "baseline_std_percent":baseline["std_deviation_percent"],
        "threshold_percent":threshold,
        "chi_square":chi,
        "likelihood_ratio":likelihood_ratio,
        "likelihood_threshold":likelihood_threshold,
        "threshold_breach":threshold_breach,
        "likelihood_breach":likelihood_breach,
        "decision":"THREAT DETECTED" if detected else "NORMAL",
        "risk_score":risk
    }
