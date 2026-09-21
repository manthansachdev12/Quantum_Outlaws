"""
SIH26141 - STEP 2: Attack Simulation Engine

This module adds four controlled attack simulations:
1. Forgery
2. Impersonation
3. Replay
4. Quantum-channel manipulation

The simulations are intentionally simple and transparent:
they modify a controlled input/verification condition so that
the later statistical engine can compare normal vs attacked behavior.

No AI/ML is used.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from hashlib import sha256
from typing import Dict, Optional
import random


@dataclass
class AttackResult:
    attack_type: str
    detected_signal: str
    original_value: str
    modified_value: str
    explanation: str
    severity_hint: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


# ---------------------------------------------------------------------
# 1. FORGERY
# ---------------------------------------------------------------------

def simulate_forgery(signature: str = "QDS-SIG-001") -> AttackResult:
    """
    Simulate an attacker changing a signature payload.

    This does not claim to model a complete QDS cryptographic forgery.
    It creates a controlled tampering condition for the prototype.
    """
    original_hash = sha256(signature.encode()).hexdigest()

    forged_signature = signature + "-FORGED"
    forged_hash = sha256(forged_signature.encode()).hexdigest()

    return AttackResult(
        attack_type="Forgery",
        detected_signal="Signature integrity mismatch",
        original_value=original_hash[:16],
        modified_value=forged_hash[:16],
        explanation=(
            "The presented signature payload was modified. "
            "The integrity value no longer matches the original signature."
        ),
        severity_hint="HIGH",
    )


# ---------------------------------------------------------------------
# 2. IMPERSONATION
# ---------------------------------------------------------------------

def simulate_impersonation(
    expected_signer: str = "Alice",
    presented_signer: str = "Eve",
) -> AttackResult:
    """
    Simulate a wrong identity presenting a signature.
    """
    return AttackResult(
        attack_type="Impersonation",
        detected_signal="Signer identity mismatch",
        original_value=expected_signer,
        modified_value=presented_signer,
        explanation=(
            "The identity associated with the verification request "
            "does not match the expected signer."
        ),
        severity_hint="HIGH",
    )


# ---------------------------------------------------------------------
# 3. REPLAY
# ---------------------------------------------------------------------

class ReplayGuard:
    """Very small in-memory replay detector for the prototype."""

    def __init__(self):
        self.seen_signatures = set()

    def verify(self, signature_id: str) -> AttackResult:
        if signature_id in self.seen_signatures:
            return AttackResult(
                attack_type="Replay",
                detected_signal="Previously observed signature",
                original_value=signature_id,
                modified_value=signature_id,
                explanation=(
                    "The same signature identifier was submitted again "
                    "after it had already been observed."
                ),
                severity_hint="MEDIUM",
            )

        self.seen_signatures.add(signature_id)

        return AttackResult(
            attack_type="Replay",
            detected_signal="No replay detected",
            original_value=signature_id,
            modified_value=signature_id,
            explanation="This signature identifier has not been observed before.",
            severity_hint="NONE",
        )


# ---------------------------------------------------------------------
# 4. QUANTUM CHANNEL MANIPULATION
# ---------------------------------------------------------------------

def simulate_channel_manipulation(
    baseline_noise: float = 0.01,
    injected_disturbance: float = 0.08,
) -> AttackResult:
    """
    Represent a controlled increase in channel disturbance.

    The actual quantum circuit/noise model will be connected to this
    in the next statistical-detection step.
    """
    return AttackResult(
        attack_type="Channel Manipulation",
        detected_signal="Injected channel disturbance",
        original_value=f"{baseline_noise:.3f}",
        modified_value=f"{injected_disturbance:.3f}",
        explanation=(
            "A controlled disturbance level is introduced into the "
            "quantum-channel simulation so its measurement statistics "
            "can later be compared against the calibrated baseline."
        ),
        severity_hint="HIGH",
    )


# ---------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------

def print_result(result: AttackResult):
    print(f"\nAttack: {result.attack_type}")
    print(f"Signal: {result.detected_signal}")
    print(f"Original: {result.original_value}")
    print(f"Modified: {result.modified_value}")
    print(f"Severity hint: {result.severity_hint}")
    print(f"Explanation: {result.explanation}")


def main():
    print("=" * 68)
    print("SIH26141 - STEP 2: ATTACK SIMULATION ENGINE")
    print("=" * 68)

    print_result(simulate_forgery())

    print_result(simulate_impersonation())

    replay_guard = ReplayGuard()

    print_result(replay_guard.verify("QDS-SIG-001"))
    print_result(replay_guard.verify("QDS-SIG-001"))

    print_result(simulate_channel_manipulation())

    print("\nStep 2 attack simulations initialized successfully.")


if __name__ == "__main__":
    main()
