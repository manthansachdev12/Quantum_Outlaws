"""
SIH26141 - Persistent Baseline Calibration

The calibration is performed once (or explicitly refreshed) and stored
as JSON. Future detection runs load the same baseline instead of
recalibrating on every test.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from .engine import calibrate_noise_baseline

BASELINE_DIR = Path(__file__).resolve().parent.parent / "data"
BASELINE_FILE = BASELINE_DIR / "baseline.json"


def create_baseline(
    shots: int = 4096,
    repetitions: int = 50,
    noise_probability: float = 0.01,
) -> Dict[str, Any]:
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)

    baseline = calibrate_noise_baseline(
        shots=shots,
        repetitions=repetitions,
        noise_probability=noise_probability,
    )

    baseline["calibration_version"] = "1.0"
    baseline["purpose"] = "Noise-only Bell-state baseline"
    baseline["threshold_rule"] = "mean + 3 standard deviations"

    with BASELINE_FILE.open("w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=2)

    return baseline


def load_baseline() -> Dict[str, Any]:
    if not BASELINE_FILE.exists():
        raise FileNotFoundError(
            "No saved baseline exists. Run: "
            "python -m quantum_engine.calibration"
        )

    with BASELINE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    print("=" * 68)
    print("SIH26141 - BASELINE CALIBRATION")
    print("=" * 68)

    baseline = create_baseline(
        shots=4096,
        repetitions=50,
        noise_probability=0.01,
    )

    print(f"Saved to      : {BASELINE_FILE}")
    print(f"Shots/run     : {baseline['shots_per_run']}")
    print(f"Repetitions   : {baseline['repetitions']}")
    print(f"Noise level   : {baseline['noise_probability']:.3f}")
    print(f"Mean deviation: {baseline['mean_deviation']:.4%}")
    print(f"Std deviation : {baseline['std_deviation']:.4%}")
    print(f"Threshold     : {baseline['threshold']:.4%}")


if __name__ == "__main__":
    main()
