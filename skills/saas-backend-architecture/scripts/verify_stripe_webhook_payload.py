#!/usr/bin/env python3
"""Stripe Webhook HMAC-SHA256 Signature Tester & Validator.

Validates and simulates Stripe webhook cryptographic signatures:
- Generates test Stripe-Signature headers (t=timestamp,v1=signature)
- Validates incoming payloads with replay attack prevention (300s drift window)
- Generates mock Stripe webhook events (checkout.session.completed, etc.)
"""

import argparse
import hashlib
import hmac
import json
import time


def generate_stripe_signature(payload_bytes: bytes, secret: str, timestamp: int | None = None) -> tuple[str, int]:
    if timestamp is None:
        timestamp = int(time.time())
    signed_payload = f"{timestamp}.".encode("utf-8") + payload_bytes
    computed = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    header_val = f"t={timestamp},v1={computed}"
    return header_val, timestamp


def verify_stripe_signature(payload_bytes: bytes, sig_header: str, secret: str, tolerance: int = 300) -> bool:
    items = dict(item.split("=", 1) for item in sig_header.split(",") if "=" in item)
    if "t" not in items or "v1" not in items:
        return False

    timestamp = int(items["t"])
    expected_v1 = items["v1"]

    # Replay attack protection
    current_time = int(time.time())
    if abs(current_time - timestamp) > tolerance:
        print(f"Error: Timestamp drift ({abs(current_time - timestamp)}s) exceeds tolerance ({tolerance}s). Replay attack rejected.")
        return False

    signed_payload = f"{timestamp}.".encode("utf-8") + payload_bytes
    computed = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, expected_v1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Stripe Webhook Signature Tester & Validator")
    parser.add_argument("--secret", default="whsec_test_secret_key_12345", help="Stripe webhook endpoint secret")
    parser.add_argument("--event", default="checkout.session.completed", help="Event name to mock")
    parser.add_argument("--customer", default="cus_test_brandon", help="Mock customer ID")
    args = parser.parse_args()

    mock_event = {
        "id": f"evt_test_{int(time.time())}",
        "object": "event",
        "api_version": "2024-06-20",
        "created": int(time.time()),
        "data": {
            "object": {
                "id": f"cs_test_{int(time.time())}",
                "object": "checkout.session",
                "customer": args.customer,
                "payment_status": "paid",
                "amount_total": 2900,
                "currency": "eur"
            }
        },
        "type": args.event
    }

    payload_json = json.dumps(mock_event, indent=2)
    payload_bytes = payload_json.encode("utf-8")

    sig_header, ts = generate_stripe_signature(payload_bytes, args.secret)

    print("=" * 65)
    print(" Stripe Webhook HMAC-SHA256 Simulation & Test")
    print("=" * 65)
    print(f"Generated Stripe-Signature Header:\n  {sig_header}\n")
    print(f"Payload Mock Event:\n{payload_json}\n")

    is_valid = verify_stripe_signature(payload_bytes, sig_header, args.secret)
    print("-" * 65)
    print(f"Verification Result with Secret '{args.secret}': {'[SUCCESS] VALID' if is_valid else '[FAILED] INVALID'}")


if __name__ == "__main__":
    main()
