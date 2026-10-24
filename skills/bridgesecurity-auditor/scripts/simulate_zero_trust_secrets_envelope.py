# -*- coding: utf-8 -*-
"""
simulate_zero_trust_secrets_envelope.py - Zero-Trust Secrets Simulator
Simulateur de chiffrement d'enveloppe et masquage automatique des secrets dans les logs.
"""

import base64
import hashlib
from typing import Dict, List, TypedDict

class MaskedLogResult(TypedDict):
    original_text: str
    sanitized_text: str
    secrets_redacted_count: int

def simulate_envelope_encrypt(plaintext: str, mock_master_key: str = "master_key_999") -> str:
    """Simule un chiffrement d'enveloppe type SOPS avec cle symmetrique derivee."""
    derived_key = hashlib.sha256(mock_master_key.encode()).digest()
    # Chiffrement XOR simplifie pour demonstration
    plain_bytes = plaintext.encode("utf-8")
    cipher_bytes = bytes([b ^ derived_key[i % len(derived_key)] for i, b in enumerate(plain_bytes)])
    return "ENC[AES256_GCM,data:" + base64.b64encode(cipher_bytes).decode("ascii") + "]"

def mask_secrets_in_logs(log_output: str, known_secrets: List[str]) -> MaskedLogResult:
    """Remplace toute occurrence de secrets connus par [MASKED]."""
    sanitized = log_output
    count = 0
    for s in known_secrets:
        if s and s in sanitized:
            sanitized = sanitized.replace(s, "[***MASKED_SECRET***]")
            count += 1
    return {
        "original_text": log_output,
        "sanitized_text": sanitized,
        "secrets_redacted_count": count
    }

def run_self_test() -> int:
    """Verifie le chiffrement d'enveloppe et la purge des secrets dans les logs."""
    print("Execution du self-test Zero-Trust Secrets Manager...")

    raw_secret = "sk-live-stripe-api-key-999-super-secret"
    encrypted = simulate_envelope_encrypt(raw_secret)
    assert raw_secret not in encrypted, "Plaintext secret leaked into encrypted output!"
    assert encrypted.startswith("ENC[AES256_GCM"), "Invalid envelope header format!"

    # Test masquage de logs
    log_sample = f"Connection to Stripe failed with key {raw_secret} at 12:00:00"
    res = mask_secrets_in_logs(log_sample, [raw_secret])
    assert raw_secret not in res["sanitized_text"], "Secret was not masked in log output!"
    assert res["secrets_redacted_count"] == 1, "Redaction counter mismatch!"

    print("[PASS] Zero-Trust Secrets teste : Chiffrement d'enveloppe et masquage dans les logs certifie.")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run_self_test())