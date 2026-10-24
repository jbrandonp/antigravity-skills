# -*- coding: utf-8 -*-
"""
simulate_stealth_harvest_pipeline.py - Stealth Hybrid Scraper Simulator
Simulateur de pipeline de scraping furtif avec injection de cookies de clearance et normalisation EAN.
"""

from typing import Dict, List, Optional, Tuple, TypedDict

class ScrapedProduct(TypedDict):
    ean: str
    name: str
    brand: str
    supermarket: str
    raw_price: float
    unit_volume_liters: float
    price_per_liter: float

class SessionContext(TypedDict):
    impersonate: str
    cf_clearance: Optional[str]
    datadome_token: Optional[str]
    is_session_valid: bool

def parse_and_normalize_product(
    ean: str,
    name: str,
    brand: str,
    supermarket: str,
    price: float,
    volume_liters: float
) -> Optional[ScrapedProduct]:
    """Valide et normalise les donnees d'un produit alimentaire."""
    if len(ean) != 13 or not ean.isdigit():
        return None  # Rejeter EAN invalide

    if volume_liters <= 0.0 or price <= 0.0:
        return None  # Rejeter donnees corrompues

    price_per_l = round(price / volume_liters, 2)
    return {
        "ean": ean,
        "name": name,
        "brand": brand,
        "supermarket": supermarket,
        "raw_price": round(price, 2),
        "unit_volume_liters": volume_liters,
        "price_per_liter": price_per_l
    }

def simulate_stealth_request(
    url: str,
    session: SessionContext
) -> Tuple[int, Optional[str]]:
    """Simule une requete protegee par Cloudflare / DataDome."""
    # Sans jeton de clearance, le WAF bloque immediatement avec un code 403
    if not session["cf_clearance"] and "protected" in url:
        return 403, "Cloudflare Challenge Required"

    return 200, '{"status": "success", "products_count": 12}'

def run_self_test() -> int:
    """Verifie la gestion des cookies de contournement et la normalisation EAN."""
    print("Execution du self-test Stealth Hybrid Scraper...")

    # 1. Test de blocage sans cookie
    unauth_session: SessionContext = {
        "impersonate": "chrome120",
        "cf_clearance": None,
        "datadome_token": None,
        "is_session_valid": False
    }
    code, _ = simulate_stealth_request("https://delhaize.be/api/protected/catalog", unauth_session)
    assert code == 403, "WAF should have blocked request without clearance cookie!"

    # 2. Test avec jeton de clearance injecte
    auth_session: SessionContext = {
        "impersonate": "chrome120",
        "cf_clearance": "valid_clearance_token_xyz",
        "datadome_token": "valid_datadome_token_abc",
        "is_session_valid": True
    }
    code, _ = simulate_stealth_request("https://delhaize.be/api/protected/catalog", auth_session)
    assert code == 200, "Valid stealth session was unexpectedly blocked!"

    # 3. Test de normalisation EAN et prix au litre
    prod = parse_and_normalize_product(
        ean="5400141000018",
        name="Lait Demi-Ecreme 1L",
        brand="Delhaize Bio",
        supermarket="Delhaize",
        price=1.35,
        volume_liters=1.0
    )
    assert prod is not None, "Product parsing failed unexpectedly!"
    assert prod["price_per_liter"] == 1.35, "Price per liter calculation mismatch!"

    print("[PASS] Stealth Hybrid Scraper teste : Contournement WAF et normalisation EAN valides.")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run_self_test())