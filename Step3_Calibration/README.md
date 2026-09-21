# SIH26141 — Step 3 Refined

## What changed?

The original Step 3 recalibrated the normal baseline every time it ran.

That is useful for experimentation, but not appropriate for a stable detector.

This version separates:

### Calibration

```text
Noise-only runs
      ↓
Mean + standard deviation
      ↓
Threshold
      ↓
data/baseline.json
```

### Detection

```text
Load saved baseline
      ↓
Run new measurement
      ↓
Compare against SAME baseline
      ↓
Threshold + likelihood ratio
      ↓
NORMAL / THREAT
```

## First run

Create the baseline once:

```powershell
python -m quantum_engine.calibration
```

This creates:

```text
data/baseline.json
```

## Detection

After calibration:

```powershell
python -m quantum_engine.detection
```

Detection does NOT recalibrate the baseline.

## Refreshing calibration

If you intentionally want a new baseline because the simulation noise configuration has changed:

```powershell
python -m quantum_engine.calibration
```

This overwrites the saved calibration.

## Current prototype parameters

- Calibration noise: 1%
- Calibration runs: 50
- Shots per run: 4096
- Threshold: mean + 3 standard deviations
- Attack-channel noise: 8%
- Likelihood-ratio threshold: 10

These are prototype parameters, not validated real-world security parameters.

## Important limitation

The Bell-state anomaly model is a research prototype. A production QDS detector would require a fully specified QDS protocol, formal security analysis, statistically justified thresholds, and extensive validation across attack/noise conditions.

No AI/ML is used.
