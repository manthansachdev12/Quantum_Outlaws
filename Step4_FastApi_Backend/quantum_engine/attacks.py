
import hashlib
from dataclasses import dataclass

def forgery_attack(original_signature, modified_signature):
    original_hash = hashlib.sha256(original_signature.encode()).hexdigest()
    modified_hash = hashlib.sha256(modified_signature.encode()).hexdigest()
    detected = original_hash != modified_hash
    return {
        "attack": "forgery",
        "detected": detected,
        "reason": "Signature integrity mismatch" if detected else "No integrity mismatch",
        "severity": "HIGH" if detected else "LOW"
    }

def impersonation_attack(expected_signer, presented_signer):
    detected = expected_signer != presented_signer
    return {
        "attack": "impersonation",
        "detected": detected,
        "reason": f"Signer mismatch: expected {expected_signer}, received {presented_signer}" if detected else "Signer identity matches",
        "severity": "HIGH" if detected else "LOW"
    }

@dataclass
class ReplayGuard:
    seen_ids: set

    def __init__(self):
        self.seen_ids = set()

    def check(self, signature_id):
        detected = signature_id in self.seen_ids
        self.seen_ids.add(signature_id)
        return {
            "attack": "replay",
            "detected": detected,
            "reason": "Signature ID was previously observed" if detected else "Signature ID is new",
            "severity": "HIGH" if detected else "LOW"
        }

def channel_manipulation_signal(baseline_probability=0.01, injected_probability=0.08):
    detected = injected_probability > baseline_probability
    return {
        "attack": "channel_manipulation",
        "baseline_noise": baseline_probability,
        "injected_noise": injected_probability,
        "detected": detected,
        "severity": "HIGH" if detected else "LOW"
    }
