# Quantum-Inspired Cyber Threat Detection for Digital Signature Security

**Smart India Hackathon 2026 --- SIH26141**\
**Team: Quantum Outlaws**

This project is a prototype security framework designed to detect suspicious
activity around **teleportation-based Quantum Digital Signature (QDS)
verification**.

The system uses **quantum-state simulation, Pauli operators, projective
measurements, calibrated measurement statistics, hypothesis-testing
concepts, and deterministic threshold rules**. It deliberately does
**not use AI or Machine Learning**.

The prototype is implemented as a web application:

``` text
React Frontend
      │
      ▼
FastAPI Backend
      │
      ├── Quantum Engine
      ├── Attack Simulation Engine
      ├── Statistical Detection Engine
      └── SQLite Result Logs
```

------------------------------------------------------------------------

# 1. Problem Statement

## Quantum-Inspired Cyber Threat Detection for Digital Signature Security

Classical public-key cryptographic systems such as RSA and ECC are
vulnerable to sufficiently capable quantum computers because algorithms
such as **Shor's algorithm** can solve the mathematical problems on
which those systems depend.

Quantum Digital Signatures provide a different approach to secure
digital signing and verification. In a teleportation-based QDS setting,
quantum states, entanglement, measurements, and Pauli corrections are
involved in the verification process.

However, a security protocol and a practical detection layer are not
exactly the same thing.

The SIH26141 problem asks for a **quantum-inspired cyber threat
detection framework** capable of identifying suspicious verification
behavior, including:

1.  **Forgery**
2.  **Impersonation**
3.  **Replay**
4.  **Unauthorized verification**
5.  **Quantum-channel manipulation**

The proposed detection approach is based on quantum principles and
statistical evidence rather than AI/ML.

------------------------------------------------------------------------

# 2. What the System Does

The system acts as a detection layer around a simulated quantum-signature
verification workflow.

The core idea is:

``` text
Expected quantum behavior
          │
          ▼
   Calibrated baseline
          │
          ▼
 New verification event
          │
          ▼
 Quantum measurement
          │
          ▼
 Statistical comparison
          │
          ▼
 Threshold / likelihood rules
          │
          ▼
 NORMAL or THREAT DETECTED
```

Instead of asking an AI model to decide whether an event is malicious,
the system uses observable measurements and explicit mathematical rules.

This makes the prototype:

-   deterministic
-   interpretable
-   reproducible
-   compatible with the SIH26141 no-AI/ML requirement
-   suitable for controlled quantum-security experimentation

------------------------------------------------------------------------

# 3. Main Security Threats

## 3.1 Forgery

A signature or signed payload is modified after signing.

The prototype demonstrates this using signature-integrity comparison:

``` text
Original Signature
        │
        ▼
Integrity value
        │
        │  modification
        ▼
Modified Signature
        │
        ▼
Integrity mismatch
        │
        ▼
THREAT DETECTED
```

The current prototype uses SHA-256-based integrity comparison to
demonstrate the attack condition.

------------------------------------------------------------------------

## 3.2 Impersonation

An attacker attempts to present a signature using another identity.

Example:

``` text
Expected signer:  Alice
Presented signer: Eve
```

The identity mismatch becomes an explicit detection signal.

``` text
Alice ≠ Eve
   ↓
THREAT DETECTED
```

------------------------------------------------------------------------

## 3.3 Replay

A previously observed signature is submitted again.

The prototype maintains a set of previously observed signature IDs.

First request:

``` text
SIG-001
   ↓
Not previously observed
   ↓
NORMAL
```

Repeated request:

``` text
SIG-001
   ↓
Previously observed
   ↓
REPLAY DETECTED
```

This makes replay detection stateful rather than simply comparing the
contents of one request.

------------------------------------------------------------------------

## 3.4 Quantum-Channel Manipulation

A quantum communication channel may experience abnormal disturbance.

The system establishes a **noise-only calibration baseline** under an
expected operating condition.

During a later verification event, the observed measurement distribution
is compared against that baseline.

Conceptually:

``` text
Calibrated behavior
      │
      ├── expected deviation
      │
      ▼
New measurement
      │
      ▼
Deviation from baseline
      │
      ▼
Statistical threshold
      │
      ├── within threshold → NORMAL
      │
      └── beyond threshold → THREAT
```

In the current controlled prototype, a stronger simulated noise level is
injected to represent channel manipulation.

------------------------------------------------------------------------

# 4. Bell State --- Quantum Foundation

One of the central quantum concepts used in the prototype is the **Bell
state**.

A Bell state is an entangled two-qubit state.

The prototype uses:

$$ |\Phi^+\rangle =
\frac{|00\rangle + |11\rangle}{\sqrt{2}} $$

This means that the two qubits are prepared in an entangled state where
measurement outcomes are correlated.

The ideal measurement probabilities are:

$$
P(00)=\frac{1}{2}
$$

$$
P(11)=\frac{1}{2}
$$

and:

$$ P(01)=P(10)=0 $$

Therefore, with a sufficiently large number of measurements, an ideal
Bell-state experiment should approximately produce:

``` text
00  ≈ 50%
11  ≈ 50%

01  ≈ 0%
10  ≈ 0%
```

For example, with 4096 shots, a normal simulated run may look
approximately like:

``` text
00 → ~50%
11 → ~50%
01 → small deviation
10 → small deviation
```

Small deviations can occur because the prototype includes a controlled
noise model.

------------------------------------------------------------------------

# 5. How the Bell State Is Created

The Bell state is created using two standard quantum gates:

``` text
q0 ── H ──●────
          │
q1 ───────X────
```

### Step 1 --- Hadamard gate

The first qubit starts in:

$$ |0\rangle $$

Applying the Hadamard gate gives:

$$ H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}
$$

### Step 2 --- CNOT gate

A CNOT is then applied with the first qubit as the control and the
second qubit as the target.

The resulting state is:

$$ |\Phi^+\rangle =
\frac{|00\rangle+|11\rangle}{\sqrt{2}} $$

This is an entangled Bell state.

The prototype uses this state as part of its quantum measurement and
anomaly-detection workflow.

------------------------------------------------------------------------

# 6. Pauli Operators and Eigenvalues

The prototype also uses the three Pauli operators:

$$
X = \begin{bmatrix}
0 & 1 \\
1 & 0
\end{bmatrix}
$$

$$
Y = \begin{bmatrix}
0 & -i \\
i & 0
\end{bmatrix}
$$

$$
Z = \begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
$$

These operators are important because they define different measurement
bases for a qubit.

## Eigenvalues

The eigenvalues of each Pauli operator are:

$$\lambda = +1, -1$$

Therefore:

``` text
Pauli X → eigenvalues +1, -1
Pauli Y → eigenvalues +1, -1
Pauli Z → eigenvalues +1, -1
```

For a projective measurement of a Pauli observable, the measurement
result corresponds to one of these eigenvalues.

------------------------------------------------------------------------

# 7. Pauli Eigenstates

## Z basis

The computational basis states are eigenstates of Z:

$$
Z|0\rangle = +|0\rangle
$$

$$
Z|1\rangle = -|1\rangle
$$

Therefore:

``` text
|0⟩ → eigenvalue +1
|1⟩ → eigenvalue -1
```

------------------------------------------------------------------------

## X basis

The X eigenstates are:

$$
|+\rangle = \frac{|0\rangle+|1\rangle}{\sqrt{2}}
$$

$$
|-\rangle = \frac{|0\rangle-|1\rangle}{\sqrt{2}}
$$

They satisfy:

$$
X|+\rangle = +|+\rangle
$$

$$
X|-\rangle = -|-\rangle
$$

------------------------------------------------------------------------

## Y basis

The Y eigenstates can be written as:

$$
|+i\rangle = \frac{|0\rangle+i|1\rangle}{\sqrt{2}}
$$

$$
|-i\rangle = \frac{|0\rangle-i|1\rangle}{\sqrt{2}}
$$

They satisfy:

$$
Y|+i\rangle = +|+i\rangle
$$

$$
Y|-i\rangle = -|-i\rangle
$$

------------------------------------------------------------------------

# 8. Why Pauli Measurements Matter

Different measurement bases reveal different properties of a quantum
state.

The prototype uses this principle to treat quantum measurements as observable
evidence.

Instead of:

``` text
Input → AI model → prediction
```

the prototype follows:

``` text
Quantum state
     ↓
Pauli / projective measurement
     ↓
Measurement outcomes
     ↓
Statistical distribution
     ↓
Deviation analysis
     ↓
Rule-based decision
```

This is one of the key design principles of the SIH26141 solution.

------------------------------------------------------------------------

# 9. Projective Measurement

A projective measurement associates a quantum observable with a set of
possible measurement outcomes.

For a Pauli operator, the possible eigenvalues are:

$$+1, -1$$

The measurement projects the quantum state onto the corresponding
eigenspace.

In the prototype, repeated measurements are more useful than a single
measurement because they create a statistical distribution.

For example:

``` text
4096 measurements

00 → 2015
11 → 2040
01 → 21
10 → 20
```

The individual result is only one observation.

The complete distribution provides evidence that can be compared against
the expected baseline.

------------------------------------------------------------------------

# 10. Statistical Detection

The prototype does not treat every small measurement variation as an attack.

Quantum simulations and physical systems can contain noise.

Therefore the prototype first performs **baseline calibration**.

Example:

``` text
50 calibration repetitions
4096 shots per repetition
noise probability = 0.01
```

The system calculates:

$$
\mu = \text{mean deviation}
$$

$$
\sigma = \text{standard deviation}
$$

and defines a prototype threshold:

$$ T = \mu + 3\sigma $$

The detection rule is:

$$
D =
\begin{cases}
\text{NORMAL}, & d \leq T \\
\text{THREAT DETECTED}, & d > T
\end{cases}
$$

where $d$ is the observed deviation.

The prototype also calculates a likelihood-ratio signal and uses a
configurable likelihood threshold.

------------------------------------------------------------------------

# 11. Example From the Prototype

During calibration, the system may produce:

``` text
Mean deviation       = 0.5186%
Standard deviation   = 0.1007%
Threshold            = 0.8204%
```

A normal verification might produce:

``` text
Observed deviation = 0.5894%

0.5894% < 0.8204%

Decision = NORMAL
```

A controlled channel-manipulation experiment may produce:

``` text
Observed deviation = 4.1748%

4.1748% > 0.8204%

Decision = THREAT DETECTED
```

The exact values vary between simulation runs because measurements are
probabilistic.

The threshold is therefore generated from the actual calibration run
rather than hard-coding a single measurement value.

------------------------------------------------------------------------

# 12. Chi-Square and Likelihood Ratio

The prototype includes statistical signals to quantify how unusual the
observed measurement distribution is.

## Chi-square statistic

The chi-square statistic compares observed and expected frequencies:

$$
\chi^2 = \sum_i \frac{(O_i-E_i)^2}{E_i}
$$

where:

-   $O_i$ = observed count
-   $E_i$ = expected count

A larger deviation from the expected distribution generally produces a
larger statistic.

------------------------------------------------------------------------

## Likelihood ratio

The prototype also compares the relative support for an attack-like
observation against a normal observation.

Conceptually:

$$ \Lambda = \frac{L(\text{observation}\mid H_1)}
{L(\text{observation}\mid H_0)} $$

where:

-   $H_0$ = normal behavior
-   $H_1$ = attack/anomalous behavior

A configurable threshold is used for the prototype decision.

These values are used as **detection signals**, not as a claim of a
formally validated real-world attack probability.

------------------------------------------------------------------------

# 13. Overall Prototype Workflow

The complete prototype follows:

``` text
                 DIGITAL SIGNATURE
                         │
                         ▼
              ┌────────────────────┐
              │ Quantum Verification│
              └──────────┬─────────┘
                         │
                         ▼
                 Bell-state / QDS
                    simulation
                         │
                         ▼
                Projective measurement
                         │
                         ▼
              Measurement distribution
                         │
                         ▼
              ┌────────────────────┐
              │ Statistical Engine │
              │                    │
              │ Deviation          │
              │ Chi-square         │
              │ Likelihood ratio   │
              │ Threshold rules    │
              └──────────┬─────────┘
                         │
                         ▼
                 Security decision
                    /          \
                   /            \
              NORMAL          THREAT
                              DETECTED
```

Attack-specific checks operate alongside the quantum measurement path:

``` text
Forgery ───────────────┐
Impersonation ─────────┤
Replay ────────────────┼──► Detection Layer
Channel manipulation ──┘
```

------------------------------------------------------------------------

# 14. System Architecture

``` text
┌───────────────────────────────────────────────────────┐
│                    REACT FRONTEND                     │
│                                                       │
│  Overview     Risk Indicator     Prototype Console    │
└───────────────────────┬───────────────────────────────┘
                        │ REST API
                        ▼
┌───────────────────────────────────────────────────────┐
│                     FASTAPI                            │
│                                                       │
│ /health                                               │
│ /baseline                                             │
│ /verify                                               │
│ /attack/forgery                                       │
│ /attack/impersonation                                 │
│ /attack/replay                                        │
│ /attack/channel                                       │
│ /results                                              │
└───────────────┬───────────────────────────────────────┘
                │
       ┌────────┼───────────┐
       ▼        ▼           ▼
 Quantum     Attack      Statistical
 Engine      Engine       Detection
       │        │           │
       └────────┼───────────┘
                ▼
             SQLite
```

------------------------------------------------------------------------

# 15. Prototype Components

## React Frontend

The frontend provides three major areas:

### Overview

Explains:

-   the SIH problem
-   quantum-security context
-   threat surface
-   Bell-state concept
-   statistical detection approach
-   prototype architecture

### Risk Indicator

Displays:

-   calibrated baseline
-   mean deviation
-   standard deviation
-   threshold
-   normal events
-   threat events
-   detection history
-   SQLite telemetry

### Prototype Console

Allows controlled execution of:

-   normal verification
-   forgery
-   impersonation
-   replay
-   channel manipulation

and displays the returned detection evidence.

------------------------------------------------------------------------

## FastAPI Backend

FastAPI connects the React interface to the quantum and security
engines.

Representative endpoints:

``` text
GET  /health
GET  /baseline
GET  /results

POST /verify
POST /attack/forgery
POST /attack/impersonation
POST /attack/replay
POST /attack/channel
```

------------------------------------------------------------------------

## Quantum Engine

The quantum engine performs:

-   Bell-state generation
-   quantum teleportation simulation
-   Pauli X/Y/Z measurement
-   controlled noise simulation
-   measurement collection

The current implementation uses **Qiskit Aer** for simulation and does
not require physical quantum hardware.

------------------------------------------------------------------------

## Attack Engine

The attack engine models the four primary prototype attack scenarios:

``` text
Forgery
Impersonation
Replay
Channel manipulation
```

These are controlled simulations intended to demonstrate the detection
logic.

------------------------------------------------------------------------

## Statistical Detection Engine

The statistical layer performs:

``` text
Baseline loading
      ↓
Measurement analysis
      ↓
Deviation calculation
      ↓
Threshold comparison
      ↓
Chi-square analysis
      ↓
Likelihood-ratio analysis
      ↓
Decision
```

The baseline is persisted to disk and reused during detection rather
than recalibrating automatically for every test.

------------------------------------------------------------------------

## SQLite

SQLite stores prototype detection events so that the frontend can
display a history of verification and attack tests.

------------------------------------------------------------------------

# 16. Risk Indicator

The prototype exposes a transparent numerical **Risk Indicator**.

Example:

``` text
0 / 100
```

may represent a normal prototype event, while:

``` text
100 / 100
```

may be assigned to a detected attack scenario.

This value is a **prototype UI/security indicator**, not a
scientifically validated probability that an attack is occurring.

The actual evidence remains the underlying:

-   measurement distribution
-   observed deviation
-   calibrated threshold
-   chi-square statistic
-   likelihood ratio
-   explicit attack-condition checks

------------------------------------------------------------------------

# 17. Current Technology Stack

``` text
Frontend
├── React
├── Vite
├── React Router
└── Recharts

Backend
├── Python
├── FastAPI
└── Uvicorn

Quantum / Numerical
├── Qiskit
├── Qiskit Aer
├── NumPy
└── SciPy

Storage
└── SQLite
```

No AI/ML framework is required by the current prototype.

------------------------------------------------------------------------

# 18. Running the Project

## Backend

Navigate to the Step 4 backend:

``` powershell
cd step4
```

Activate its virtual environment:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Start FastAPI:

``` powershell
uvicorn main:app --reload
```

Backend:

``` text
http://127.0.0.1:8000
```

Swagger API documentation:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

## Frontend

Navigate to the Step 5 React application:

``` powershell
cd step5
```

Install dependencies:

``` powershell
npm install
```

Start Vite:

``` powershell
npm run dev
```

The frontend will normally be available at:

``` text
http://localhost:5173
```

The React application connects to:

``` text
http://127.0.0.1:8000
```

------------------------------------------------------------------------

# 19. Recommended Demonstration Flow

For a Smart India Hackathon demonstration, the prototype can be
presented in this order:

### 1. Overview

Explain the security problem and why quantum-inspired detection is
needed.

### 2. Quantum foundation

Explain:

``` text
Bell state
      ↓
Entanglement
      ↓
Measurement
      ↓
Expected distribution
```

Then introduce Pauli X, Y and Z eigenstates and projective measurements.

### 3. Calibration

Show the baseline:

``` text
Mean deviation
Standard deviation
3σ threshold
```

### 4. Normal verification

Run the normal verification scenario.

Expected:

``` text
NORMAL
```

### 5. Channel manipulation

Increase the controlled channel disturbance.

Show:

``` text
Observed deviation
      >
Calibrated threshold
```

and:

``` text
THREAT DETECTED
```

### 6. Protocol-level attacks

Demonstrate:

``` text
Forgery
Impersonation
Replay
```

### 7. Risk Indicator

Open the telemetry page and show the detection history.

------------------------------------------------------------------------

# 20. What This Prototype Demonstrates

This prototype demonstrates a complete research-to-prototype pipeline:

``` text
Quantum concept
      ↓
Quantum simulation
      ↓
Attack modelling
      ↓
Measurement collection
      ↓
Statistical analysis
      ↓
Deterministic detection
      ↓
REST API
      ↓
Web security console
```

The prototype therefore connects the theoretical concepts to an
observable security workflow.

------------------------------------------------------------------------

# 21. Important Scope and Limitations

This project is a **controlled prototype and simulation**, not a
production-ready quantum digital-signature implementation.

In particular:

-   The quantum channel is simulated rather than operated on physical
    quantum hardware.
-   The attack scenarios are controlled demonstrations.
-   Thresholds are prototype calibration parameters.
-   The risk indicator is not a validated attack probability.
-   The prototype does not constitute a formal security proof for a
    complete QDS protocol.
-   The current system demonstrates detection logic rather than
    replacing a complete QDS protocol.
-   Real deployment would require protocol-specific cryptographic
    specifications, hardware/channel characterization, authentication
    infrastructure, key-management procedures, and formal security
    analysis.

These limitations are important when interpreting prototype results.

------------------------------------------------------------------------

# 22. Security Design Principle

The central design philosophy is:

> **Measure first. Quantify deviation. Apply explicit rules.**

The system intentionally avoids opaque prediction.

``` text
Quantum state
     ↓
Measurement
     ↓
Evidence
     ↓
Statistics
     ↓
Threshold
     ↓
Decision
```

This makes every detection event explainable through measurable
evidence.

------------------------------------------------------------------------

# 23. Final Summary

This project is a **quantum-inspired cyber threat detection prototype for
digital-signature security**.

It combines:

-   Bell-state entanglement
-   quantum teleportation simulation
-   Pauli operators and eigenstates
-   projective measurement
-   calibrated measurement statistics
-   chi-square analysis
-   likelihood-ratio analysis
-   deterministic thresholds
-   attack simulation
-   FastAPI
-   SQLite
-   React

to create a complete experimental detection pipeline for:

``` text
Forgery
Impersonation
Replay
Channel manipulation
```

The defining characteristic of the prototype is that its detection logic
is based on **quantum measurement evidence and statistical rules rather
than AI/ML**.

------------------------------------------------------------------------

## Team

**Quantum Outlaws**

**Smart India Hackathon 2026**

**Problem Statement:** SIH26141\
**Theme:** Quantum-Inspired Cyber Threat Detection for Digital Signature
Security
