# -*- coding: utf-8 -*-
"""
simulate_prompt_cache_hit_rate.py - Prompt Caching Economy Simulator
Simulateur d'ordonnancement de prompts et calcul des economies financieres du Prompt Caching.
"""

from typing import Dict, List, Tuple, TypedDict

class PromptMessage(TypedDict):
    role: str
    content: str
    is_cache_breakpoint: bool

class CacheSessionResult(TypedDict):
    total_turns: int
    total_input_tokens: int
    cached_tokens_read: int
    cache_hit_rate_percent: float
    standard_cost_usd: float
    cached_cost_usd: float
    savings_percent: float

def simulate_caching_turns(
    system_tokens: int = 5000,
    tools_tokens: int = 2000,
    turn_user_tokens: int = 400,
    num_turns: int = 10
) -> CacheSessionResult:
    """Simule les couts d'une session avec et sans Prompt Caching (Tarifs Claude 3.5 Sonnet)."""
    # Tarifs par million de tokens :
    # Input standard = $3.00 / M
    # Cache Write (1er tour) = $3.75 / M
    # Cache Read (tours suivants) = $0.30 / M (90% de reduction !)
    static_prefix = system_tokens + tools_tokens

    total_tokens_sent = 0
    cached_reads = 0

    cost_standard = 0.0
    cost_cached = 0.0

    for turn in range(num_turns):
        turn_dynamic = turn_user_tokens * (turn + 1)
        turn_total = static_prefix + turn_dynamic
        total_tokens_sent += turn_total

        # Cout standard sans cache
        cost_standard += (turn_total / 1_000_000.0) * 3.00

        # Cout avec Prompt Caching
        if turn == 0:
            # 1er tour : ecriture du cache (coutlegerement superieur)
            cost_cached += (static_prefix / 1_000_000.0) * 3.75 + (turn_dynamic / 1_000_000.0) * 3.00
        else:
            # Tours 2 a N : lecture du cache a 10% du prix !
            cached_reads += static_prefix
            cost_cached += (static_prefix / 1_000_000.0) * 0.30 + (turn_dynamic / 1_000_000.0) * 3.00

    hit_rate = (cached_reads / (static_prefix * num_turns)) * 100.0
    savings = ((cost_standard - cost_cached) / cost_standard) * 100.0

    return {
        "total_turns": num_turns,
        "total_input_tokens": total_tokens_sent,
        "cached_tokens_read": cached_reads,
        "cache_hit_rate_percent": hit_rate,
        "standard_cost_usd": round(cost_standard, 4),
        "cached_cost_usd": round(cost_cached, 4),
        "savings_percent": round(savings, 2)
    }

def run_self_test() -> int:
    """Verifie le calcul deterministe des gains du Prompt Caching."""
    print("Execution du self-test Prompt Caching Optimizer...")
    res = simulate_caching_turns(system_tokens=5000, tools_tokens=2000, turn_user_tokens=500, num_turns=10)

    assert res["cache_hit_rate_percent"] >= 80.0, "Cache hit rate below threshold!"
    assert res["savings_percent"] >= 50.0, "Expected >= 50% cost savings with prompt caching!"
    assert res["cached_cost_usd"] < res["standard_cost_usd"], "Cached cost exceeded standard cost!"

    print(f"[PASS] Prompt Caching teste : {res['total_turns']} tours simules.")
    print(f"       Cout Standard = ${res['standard_cost_usd']:.4f} -> Avec Cache = ${res['cached_cost_usd']:.4f}")
    print(f"       Economie realisee = {res['savings_percent']:.1f}% (Taux de lecture cache = {res['cache_hit_rate_percent']:.1f}%)")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run_self_test())