import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def bell_state(shots=4096, noise_probability=0.0):
    """
    Generate |Phi+> = (|00> + |11>) / sqrt(2) and measure it.

    For noisy simulation:
    - H is a 1-qubit gate -> use a 1-qubit depolarizing error.
    - CX is a 2-qubit gate -> use a 2-qubit depolarizing error.
    """
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    backend = AerSimulator()

    if noise_probability > 0:
        from qiskit_aer.noise import NoiseModel, depolarizing_error

        noise = NoiseModel()

        # Correct error dimensions for each gate.
        h_error = depolarizing_error(noise_probability, 1)
        cx_error = depolarizing_error(noise_probability, 2)

        noise.add_all_qubit_quantum_error(h_error, ["h"])
        noise.add_all_qubit_quantum_error(cx_error, ["cx"])

        compiled = transpile(qc, backend)
        job = backend.run(
            compiled,
            shots=shots,
            noise_model=noise
        )
    else:
        compiled = transpile(qc, backend)
        job = backend.run(compiled, shots=shots)

    return job.result().get_counts()


def run_teleportation(shots=4096, input_state="+"):
    qc = QuantumCircuit(3, 3)

    if input_state == "+":
        qc.h(0)
    elif input_state == "-":
        qc.x(0)
        qc.h(0)

    qc.h(1)
    qc.cx(1, 2)

    qc.cx(0, 1)
    qc.h(0)

    qc.measure(0, 0)
    qc.measure(1, 1)

    qc.cx(1, 2)
    qc.cz(0, 2)

    qc.measure(2, 2)

    backend = AerSimulator()
    job = backend.run(transpile(qc, backend), shots=shots)
    counts = job.result().get_counts()

    receiver = {"0": 0, "1": 0}

    for bits, count in counts.items():
        receiver[bits[0]] += count

    return receiver


def pauli_measurement(pauli="X", shots=4096):
    qc = QuantumCircuit(1, 1)

    if pauli == "X":
        qc.h(0)
    elif pauli == "Y":
        qc.sdg(0)
        qc.h(0)

    qc.measure(0, 0)

    backend = AerSimulator()
    job = backend.run(transpile(qc, backend), shots=shots)

    return job.result().get_counts()
