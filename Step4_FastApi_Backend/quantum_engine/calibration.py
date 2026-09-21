
import json, os
import numpy as np
from .engine import bell_state

BASELINE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "baseline.json")

def calculate_deviation(counts, shots):
    unexpected = counts.get("01", 0) + counts.get("10", 0)
    return (unexpected / shots) * 100.0

def calibrate(repetitions=50, shots=4096, noise_probability=0.01):
    deviations=[]
    for _ in range(repetitions):
        counts=bell_state(shots=shots, noise_probability=noise_probability)
        deviations.append(calculate_deviation(counts, shots))
    mean=float(np.mean(deviations))
    std=float(np.std(deviations))
    threshold=mean+3*std
    data={
        "repetitions": repetitions,
        "shots_per_run": shots,
        "noise_probability": noise_probability,
        "mean_deviation_percent": mean,
        "std_deviation_percent": std,
        "threshold_percent": threshold
    }
    os.makedirs(os.path.dirname(BASELINE_PATH), exist_ok=True)
    with open(BASELINE_PATH,"w") as f: json.dump(data,f,indent=2)
    return data

def load_baseline():
    if not os.path.exists(BASELINE_PATH):
        return None
    with open(BASELINE_PATH) as f:
        return json.load(f)

if __name__ == "__main__":
    print(json.dumps(calibrate(), indent=2))
