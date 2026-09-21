# SIH26141 Quantum Security Prototype — Step 1

This is the first prototype layer for:

**Quantum-Inspired Cyber Threat Detection for Digital Signature Security**

## What this step implements

- Bell-state generation
- Quantum teleportation circuit
- Pauli X/Y/Z eigenstate preparation
- Projective measurements
- Controlled depolarizing noise
- Noise-only baseline calibration
- Statistical deviation threshold

There is **no AI/ML** in this implementation.

## Recommended environment

Python 3.11 or newer.

## Installation

Create and activate a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install packages:

```powershell
pip install -r requirements.txt
```

Run:

```powershell
python -m quantum_engine.engine
```

## Expected behavior

### Bell state

The Bell state |Phi+> should produce mostly:

```text
00
11
```

with roughly equal probability in an ideal simulation.

### Teleportation

The example teleports the |+> state. The receiver's final measurement should be consistent with |+>.

### Pauli measurements

For a +1 eigenstate measured in its own Pauli basis, the ideal result should be deterministic.

### Baseline

The baseline experiment repeats a Bell-state measurement under controlled noise and calculates:

```text
mean deviation
standard deviation
threshold = mean + 3 * standard deviation
```

This threshold is a prototype calibration rule. It should be experimentally validated and tuned before being presented as a final security parameter.

## Next step

After this runs correctly, add:

1. forgery simulation
2. impersonation simulation
3. replay simulation
4. channel-manipulation/noise attack
5. chi-square and likelihood-ratio tests
6. risk scoring
7. FastAPI backend
8. React dashboard
