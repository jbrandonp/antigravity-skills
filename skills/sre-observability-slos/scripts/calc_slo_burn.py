#!/usr/bin/env python3
"""SRE SLO & Error Budget Calculator.

Calculates Site Reliability Engineering (SRE) metrics and Prometheus alert thresholds:
- Total allowed monthly downtime
- Allowed failed requests per million
- Multi-window burn rates (14.4x, 6x, 1x)
- Generates copy-pasteable Prometheus YAML alert rules
"""

import argparse
import sys


def calculate_slo(target_slo: float, window_days: int = 30) -> None:
    slo_fraction = target_slo / 100.0
    error_budget_fraction = 1.0 - slo_fraction

    total_seconds = window_days * 24 * 3600
    allowed_downtime_seconds = total_seconds * error_budget_fraction
    allowed_downtime_minutes = allowed_downtime_seconds / 60.0
    allowed_downtime_hours = allowed_downtime_minutes / 60.0

    allowed_errors_per_million = error_budget_fraction * 1_000_000

    print("=" * 65)
    print(f" SRE Error Budget Summary (SLO: {target_slo}% over {window_days} days)")
    print("=" * 65)
    print(f"Target Availability (SLO) : {target_slo:.4f}%")
    print(f"Error Budget Fraction     : {error_budget_fraction:.6f} ({error_budget_fraction*100:.4f}%)")
    print(f"Allowed Downtime          : {allowed_downtime_minutes:.2f} minutes ({allowed_downtime_hours:.2f} hours)")
    print(f"Allowed Failed Requests   : {allowed_errors_per_million:.0f} per 1,000,000 requests")
    print("-" * 65)
    print(" Multi-Window Multi-Burn-Rate Matrix (Google SRE Standard):")
    print("-" * 65)
    print(f" 1. Fast Burn (14.4x) : Consumes 2% budget in 1h.  Severity: CRITICAL (Page)")
    print(f" 2. Slow Burn (6.0x)  : Consumes 5% budget in 6h.  Severity: WARNING (Slack)")
    print(f" 3. Steady Burn (1.0x): Consumes 100% budget in {window_days}d. Severity: NOTICE (Ticket)")
    print("=" * 65)
    print("\nGenerated Prometheus Rules YAML:\n")

    yaml_template = f"""groups:
  - name: slo_alerts_{target_slo}
    rules:
      # Recording rule: availability error rate over 5m
      - record: job:api:error_rate_5m
        expr: |
          sum(rate(http_requests_total{{status=~"5.."}}[5m]))
          /
          sum(rate(http_requests_total[5m]))

      # Fast Burn Alert: 14.4x over 1h (consommation critique)
      - alert: FastErrorBudgetBurn
        expr: job:api:error_rate_5m > {error_budget_fraction:.6f} * 14.4
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Error budget burning at 14.4x (2% per hour)"
          description: "At current error rate, monthly budget will be exhausted in ~50 hours."

      # Slow Burn Alert: 6x over 6h (consommation progressive)
      - alert: SlowErrorBudgetBurn
        expr: job:api:error_rate_5m > {error_budget_fraction:.6f} * 6.0
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Error budget burning at 6x (5% in 6 hours)"
          description: "Service reliability is degrading steadily."
"""
    print(yaml_template)


def main() -> None:
    parser = argparse.ArgumentParser(description="SRE SLO & Error Budget Calculator")
    parser.add_argument("slo", type=float, help="Target SLO percentage (e.g. 99.9, 99.95, 99.99)")
    parser.add_argument("--window", type=int, default=30, help="Rolling window in days (default: 30)")
    args = parser.parse_args()

    if args.slo <= 0 or args.slo >= 100:
        print("Error: SLO must be between 0 and 100 (exclusive).", file=sys.stderr)
        sys.exit(1)

    calculate_slo(args.slo, args.window)


if __name__ == "__main__":
    main()
