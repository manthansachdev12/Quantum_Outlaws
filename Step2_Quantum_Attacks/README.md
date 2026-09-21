# SIH26141 — Step 2: Attack Simulation Engine

Step 2 adds four controlled attack simulations to the working quantum core.

## Attacks

### 1. Forgery
Changes the presented signature payload and demonstrates an integrity mismatch.

### 2. Impersonation
Presents a different signer identity than the expected signer.

### 3. Replay
Submits the same signature identifier twice. The second submission is flagged as previously observed.

### 4. Quantum Channel Manipulation
Introduces a controlled disturbance parameter. In the next step this will be connected directly to Qiskit Aer noise and statistical measurement analysis.

## Important

These are **prototype attack simulations**, not claims that the current code implements a complete production QDS security protocol.

No AI/ML is used.

## Run

From the project folder:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m quantum_engine.attacks
```

Step 2 currently demonstrates the attack conditions.

The next step will connect these conditions to actual quantum measurement distributions and statistical detection.
