"""
SIH26141 - Quantum Security Prototype
STEP 1: Quantum Core

This module provides:
1. Bell-state generation and measurement
2. Teleportation circuit construction and verification
3. Pauli X/Y/Z eigenstate preparation and projective measurements
4. Controlled noise simulation
5. Noise-only baseline calibration

No AI/ML is used.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


# ---------------------------------------------------------------------
# Common simulator
# ---------------------------------------------------------------------

def simulator(shots: int = 4096, noise_probability: float = 0.0):
    """Return an Aer simulator. If noise_probability > 0, add depolarizing noise."""
    if noise_probability <= 0:
        return AerSimulator()

    noise_model = NoiseModel()

    one_qubit_error = depolarizing_error(noise_probability, 1)
    two_qubit_error = depolarizing_error(noise_probability, 2)

    noise_model.add_all_qubit_quantum_error(
        one_qubit_error,
        ["h", "x", "y", "z", "s", "sdg"],
    )
    noise_model.add_all_qubit_quantum_error(
        two_qubit_error,
        ["cx"],
    )

    return AerSimulator(noise_model=noise_model)


def run_counts(circuit: QuantumCircuit, shots: int = 4096,
               noise_probability: float = 0.0) -> Dict[str, int]:
    """Execute a measured circuit and return counts."""
    backend = simulator(shots, noise_probability)
    compiled = transpile(circuit, backend)
    result = backend.run(compiled, shots=shots).result()
    return result.get_counts()


# ---------------------------------------------------------------------
# 1. Bell state
# ---------------------------------------------------------------------

def bell_state_circuit() -> QuantumCircuit:
    """Create |Phi+> = (|00> + |11>) / sqrt(2)."""
    qc = QuantumCircuit(2, 2, name="Bell State")
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def run_bell_state(shots: int = 4096,
                   noise_probability: float = 0.0) -> Dict[str, int]:
    return run_counts(bell_state_circuit(), shots, noise_probability)


# ---------------------------------------------------------------------
# 2. Quantum teleportation
# ---------------------------------------------------------------------

def teleportation_circuit(input_state: str = "plus") -> QuantumCircuit:
    """
    Build a 3-qubit teleportation circuit.

    q0 = state to teleport
    q1,q2 = Bell pair
    c0,c1 = Bell-measurement results

    Supported input states:
        "zero"  -> |0>
        "one"   -> |1>
        "plus"  -> |+>
        "minus" -> |->
    """
    qc = QuantumCircuit(3, 3, name="Quantum Teleportation")

    # Prepare the input state on q0.
    if input_state == "one":
        qc.x(0)
    elif input_state == "plus":
        qc.h(0)
    elif input_state == "minus":
        qc.x(0)
        qc.h(0)
    elif input_state != "zero":
        raise ValueError("input_state must be zero, one, plus, or minus")

    # Create Bell pair q1-q2.
    qc.h(1)
    qc.cx(1, 2)

    qc.barrier()

    # Bell measurement between q0 and q1.
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, 0)
    qc.measure(1, 1)

    # Pauli corrections on receiver q2.
    # c1 controls X, c0 controls Z.
    with qc.if_test((qc.clbits[1], True)):
        qc.x(2)

    with qc.if_test((qc.clbits[0], True)):
        qc.z(2)

    qc.measure(2, 2)
    return qc


# def run_teleportation(input_state: str = "plus",
#                       shots: int = 4096,
#                       noise_probability: float = 0.0) -> Dict[str, int]:
#     return run_counts(
#         teleportation_circuit(input_state),
#         shots,
#         noise_probability,
#     )
def run_teleportation(
    input_state: str = "plus",
    shots: int = 4096,
    noise_probability: float = 0.0,
) -> Dict[str, int]:

    circuit = teleportation_circuit(input_state)

    backend = simulator(shots, noise_probability)
    compiled = transpile(circuit, backend)

    result = backend.run(
        compiled,
        shots=shots
    ).result()

    raw_counts = result.get_counts()

    receiver_counts = {
        "0": 0,
        "1": 0
    }

    for bitstring, count in raw_counts.items():

        # Qiskit displays:
        # c2 c1 c0
        #
        # c2 = receiver measurement

        receiver_bit = bitstring[0]

        receiver_counts[receiver_bit] += count

    return receiver_counts


# ---------------------------------------------------------------------
# 3. Pauli eigenstates + projective measurements
# ---------------------------------------------------------------------

def pauli_eigenstate_circuit(basis: str = "Z", eigenvalue: int = +1) -> QuantumCircuit:
    """
    Prepare a single-qubit Pauli eigenstate and measure it in that same basis.

    Z,+1 = |0>
    Z,-1 = |1>
    X,+1 = |+>
    X,-1 = |->
    Y,+1 = |+i>
    Y,-1 = |-i>
    """
    basis = basis.upper()
    if basis not in {"X", "Y", "Z"}:
        raise ValueError("basis must be X, Y, or Z")
    if eigenvalue not in {+1, -1}:
        raise ValueError("eigenvalue must be +1 or -1")

    qc = QuantumCircuit(1, 1, name=f"{basis}{eigenvalue:+d} measurement")

    # Prepare eigenstate.
    if basis == "Z":
        if eigenvalue == -1:
            qc.x(0)

    elif basis == "X":
        if eigenvalue == -1:
            qc.x(0)
        qc.h(0)

    elif basis == "Y":
        # |+i> = S H |0>; |-i> = X S H |0>
        if eigenvalue == -1:
            qc.x(0)
        qc.h(0)
        qc.s(0)

    qc.barrier()

    # Projective measurement in requested Pauli basis.
    if basis == "X":
        qc.h(0)
    elif basis == "Y":
        qc.sdg(0)
        qc.h(0)

    qc.measure(0, 0)
    return qc


def run_pauli_measurement(
    basis: str = "Z",
    eigenvalue: int = +1,
    shots: int = 4096,
    noise_probability: float = 0.0,
) -> Dict[str, int]:
    return run_counts(
        pauli_eigenstate_circuit(basis, eigenvalue),
        shots,
        noise_probability,
    )


# ---------------------------------------------------------------------
# 4. Convert counts to probabilities
# ---------------------------------------------------------------------

def counts_to_probabilities(counts: Dict[str, int]) -> Dict[str, float]:
    total = sum(counts.values())
    if total == 0:
        return {}
    return {key: value / total for key, value in counts.items()}


# ---------------------------------------------------------------------
# 5. Noise-only baseline calibration
# ---------------------------------------------------------------------

def calibrate_noise_baseline(
    shots: int = 4096,
    repetitions: int = 20,
    noise_probability: float = 0.01,
) -> Dict[str, object]:
    """
    Run the Bell-state experiment repeatedly under controlled noise.

    We track the fraction of unexpected Bell outcomes.
    For |Phi+>, expected outcomes are 00 and 11.
    """
    deviations = []

    for _ in range(repetitions):
        counts = run_bell_state(shots, noise_probability)

        unexpected = sum(
            count for bitstring, count in counts.items()
            if bitstring not in {"00", "11"}
        )

        deviation = unexpected / shots
        deviations.append(deviation)

    mean_deviation = float(np.mean(deviations))
    std_deviation = float(np.std(deviations, ddof=1)) if repetitions > 1 else 0.0

    # Prototype baseline threshold:
    # mean + 3 standard deviations.
    threshold = mean_deviation + (3.0 * std_deviation)

    return {
        "shots_per_run": shots,
        "repetitions": repetitions,
        "noise_probability": noise_probability,
        "mean_deviation": mean_deviation,
        "std_deviation": std_deviation,
        "threshold": threshold,
        "deviations": deviations,
    }


# ---------------------------------------------------------------------
# 6. Human-readable demo
# ---------------------------------------------------------------------

def print_section(title: str):
    print("\n" + "=" * 68)
    print(title)
    print("=" * 68)


def main():
    shots = 4096

    print_section("1. BELL STATE")

    bell = run_bell_state(shots)

    print("Counts:", bell)
    print("Probabilities:", counts_to_probabilities(bell))


    print_section("2. TELEPORTATION")

    teleport = run_teleportation("plus", shots)

    total = sum(teleport.values())

    p0 = teleport["0"] / total
    p1 = teleport["1"] / total

    print("Input state: |+>")
    print()
    print("Receiver measurement:")
    print(f"0 → {p0:.4%}")
    print(f"1 → {p1:.4%}")

    if abs(p0 - 0.5) < 0.05 and abs(p1 - 0.5) < 0.05:
        print()
        print("Teleportation verification: ✓ PASSED")
    else:
        print()
        print("Teleportation verification: ⚠ CHECK")


    print_section("3. PAULI PROJECTIVE MEASUREMENTS")

    for basis in ("X", "Y", "Z"):
        counts = run_pauli_measurement(
            basis,
            +1,
            shots
        )

        print(f"{basis}, eigenvalue +1 -> {counts}")


    print_section("4. NOISE-ONLY BASELINE")

    baseline = calibrate_noise_baseline(
        shots=shots,
        repetitions=20,
        noise_probability=0.01,
    )

    print(f"Mean deviation : {baseline['mean_deviation']:.6f}")
    print(f"Std deviation  : {baseline['std_deviation']:.6f}")
    print(f"Threshold      : {baseline['threshold']:.6f}")


if __name__ == "__main__":
    main()


