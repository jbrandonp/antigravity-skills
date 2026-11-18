"""
CLI tool for simulating Belgian socio-fiscal transformation (2026 rules).
Calculates net take-home pay, social contributions, and tax cliff warnings
for Smart Coop (employee & student) and INASTI Student-Independent.
Strictly typed, zero 'Any'.
"""

import argparse
import os
import sys
from typing import Dict, Final, List, Optional, Tuple, TypedDict

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# --- Constantes légales Belgique 2026 ---
TAUX_SMART_GESTION: Final[float] = 0.065
TAUX_SMART_MUTUALISATION: Final[float] = 0.08
TAUX_ONSS_PATRONALE_CP200: Final[float] = 0.25
TAUX_ONSS_PERSONNELLE_CP200: Final[float] = 0.1307
ESTIMATION_PRECOMPTE_CP200: Final[float] = 0.18

TAUX_SOLIDARITE_EMPLOYEUR_ETUDIANT: Final[float] = 0.0543
TAUX_SOLIDARITE_TRAVAILLEUR_ETUDIANT: Final[float] = 0.0271
ESTIMATION_PRECOMPTE_ETUDIANT: Final[float] = 0.05

SEUIL_EXONERATION_INASTI_2026: Final[float] = 8687.04
SEUIL_PLAFOND_REDUIT_INASTI_2026: Final[float] = 17374.08
TAUX_COTISATION_INASTI: Final[float] = 0.205

PLAFOND_ENFANT_A_CHARGE_NET_ANNUEL: Final[float] = 4200.0
PLAFOND_HEURES_FAMIWAL_TRIMESTRE: Final[int] = 240
POINT_DE_BASCULE_SMART_INASTI: Final[float] = 6200.0


class SimulationResult(TypedDict):
    regime: str
    ca_htva: float
    frais_gestion_smart: float
    frais_mutualisation_smart: float
    budget_emploi: float
    cotisations_sociales: float
    brut_imposable: float
    precompte_estime: float
    net_en_poche: float
    taux_rendement_net: float
    alerte_foyer_fiscal: bool
    recommandation: str


def simuler_smart_employe(ca_htva: float) -> SimulationResult:
    """
    Simule la conversion d'une facture sous contrat d'employé ordinaire Smart (CP 200).

    Paramètres :
        ca_htva (float) : Montant de la facture client hors TVA.

    Retour :
        SimulationResult : Dictionnaire contenant la décomposition financière complète.
    """
    frais_gestion = ca_htva * TAUX_SMART_GESTION
    budget_brut = ca_htva - frais_gestion
    frais_mutuelle = budget_brut * TAUX_SMART_MUTUALISATION
    budget_emploi = budget_brut - frais_mutuelle

    salaire_brut = budget_emploi / (1.0 + TAUX_ONSS_PATRONALE_CP200)
    onss_patronale = budget_emploi - salaire_brut
    onss_personnelle = salaire_brut * TAUX_ONSS_PERSONNELLE_CP200
    brut_imposable = salaire_brut - onss_personnelle
    precompte = brut_imposable * ESTIMATION_PRECOMPTE_CP200
    net_en_poche = brut_imposable - precompte
    cotisations_totales = onss_patronale + onss_personnelle

    rendement = (net_en_poche / ca_htva) * 100.0 if ca_htva > 0 else 0.0
    alerte_foyer = net_en_poche > (PLAFOND_ENFANT_A_CHARGE_NET_ANNUEL / 12.0)

    recommandation = (
        "Régime par défaut si votre cursus en promotion sociale n'est pas qualifié pour le contrat étudiant. "
        "Le net représente environ 45% à 50% de la facture."
    )

    return {
        "regime": "Smart Coop — Contrat Employé Ordinaire (CP 200)",
        "ca_htva": round(ca_htva, 2),
        "frais_gestion_smart": round(frais_gestion, 2),
        "frais_mutualisation_smart": round(frais_mutuelle, 2),
        "budget_emploi": round(budget_emploi, 2),
        "cotisations_sociales": round(cotisations_totales, 2),
        "brut_imposable": round(brut_imposable, 2),
        "precompte_estime": round(precompte, 2),
        "net_en_poche": round(net_en_poche, 2),
        "taux_rendement_net": round(rendement, 1),
        "alerte_foyer_fiscal": alerte_foyer,
        "recommandation": recommandation,
    }


def simuler_smart_etudiant(ca_htva: float) -> SimulationResult:
    """
    Simule la conversion d'une facture sous contrat étudiant Smart (contingent 600h).

    Paramètres :
        ca_htva (float) : Montant de la facture client hors TVA.

    Retour :
        SimulationResult : Dictionnaire contenant la décomposition financière complète.
    """
    frais_gestion = ca_htva * TAUX_SMART_GESTION
    budget_brut = ca_htva - frais_gestion
    frais_mutuelle = budget_brut * TAUX_SMART_MUTUALISATION
    budget_emploi = budget_brut - frais_mutuelle

    salaire_brut = budget_emploi / (1.0 + TAUX_SOLIDARITE_EMPLOYEUR_ETUDIANT)
    onss_employeur = budget_emploi - salaire_brut
    onss_etudiant = salaire_brut * TAUX_SOLIDARITE_TRAVAILLEUR_ETUDIANT
    brut_imposable = salaire_brut - onss_etudiant
    precompte = brut_imposable * ESTIMATION_PRECOMPTE_ETUDIANT
    net_en_poche = brut_imposable - precompte
    cotisations_totales = onss_employeur + onss_etudiant

    rendement = (net_en_poche / ca_htva) * 100.0 if ca_htva > 0 else 0.0
    alerte_foyer = net_en_poche > (PLAFOND_ENFANT_A_CHARGE_NET_ANNUEL / 12.0)

    recommandation = (
        "Régime optimal sous 6 200 €/an si statut étudiant validé par Smart. "
        "Cotisations de solidarité réduites (2,71% + 5,43%), rendement net élevé (70%-75%)."
    )

    return {
        "regime": "Smart Coop — Contrat Étudiant (Contingent 600h)",
        "ca_htva": round(ca_htva, 2),
        "frais_gestion_smart": round(frais_gestion, 2),
        "frais_mutualisation_smart": round(frais_mutuelle, 2),
        "budget_emploi": round(budget_emploi, 2),
        "cotisations_sociales": round(cotisations_totales, 2),
        "brut_imposable": round(brut_imposable, 2),
        "precompte_estime": round(precompte, 2),
        "net_en_poche": round(net_en_poche, 2),
        "taux_rendement_net": round(rendement, 1),
        "alerte_foyer_fiscal": alerte_foyer,
        "recommandation": recommandation,
    }


def simuler_etudiant_independant(ca_htva: float, is_annual: bool = False, charges_pro_annuelles: float = 900.0) -> SimulationResult:
    """
    Simule les cotisations et revenus nets sous le statut Étudiant-Indépendant (INASTI 2026).

    Paramètres :
        ca_htva (float) : Chiffre d'affaires HTVA (facture ponctuelle ou CA annuel).
        is_annual (bool) : Vrai s'il s'agit d'un CA annuel global, Faux pour une facture ponctuelle.
        charges_pro_annuelles (float) : Frais professionnels (comptable, téléphone, etc.).

    Retour :
        SimulationResult : Dictionnaire contenant les cotisations sociales et le net.
    """
    # Si c'est une facture ponctuelle, les frais comptables sont lissés à ~10% au lieu d'un forfait annuel de 900€
    charges = charges_pro_annuelles if is_annual else (ca_htva * 0.10)
    revenu_net_imposable = max(0.0, ca_htva - charges)

    cotisation_annuelle = 0.0
    if revenu_net_imposable <= SEUIL_EXONERATION_INASTI_2026:
        cotisation_annuelle = 0.0
    elif revenu_net_imposable <= SEUIL_PLAFOND_REDUIT_INASTI_2026:
        tranche_depassee = revenu_net_imposable - SEUIL_EXONERATION_INASTI_2026
        cotisation_annuelle = tranche_depassee * TAUX_COTISATION_INASTI
    else:
        tranche_reduite = SEUIL_PLAFOND_REDUIT_INASTI_2026 - SEUIL_EXONERATION_INASTI_2026
        tranche_pleine = revenu_net_imposable - SEUIL_PLAFOND_REDUIT_INASTI_2026
        cotisation_annuelle = (tranche_reduite * TAUX_COTISATION_INASTI) + (tranche_pleine * TAUX_COTISATION_INASTI)

    net_en_poche = revenu_net_imposable - cotisation_annuelle
    rendement = (net_en_poche / ca_htva) * 100.0 if ca_htva > 0 else 0.0
    alerte_foyer = (net_en_poche if is_annual else net_en_poche * 12.0) > PLAFOND_ENFANT_A_CHARGE_NET_ANNUEL

    recommandation = (
        "Statut autonome conseillé au-delà de 6 200 € HTVA de CA annuel. "
        "Exonération totale de cotisations sociales si le Revenu Net Imposable reste sous 8 687,04 €."
    )

    return {
        "regime": "Statut Étudiant-Indépendant (INASTI 2026)",
        "ca_htva": round(ca_htva, 2),
        "frais_gestion_smart": 0.0,
        "frais_mutualisation_smart": 0.0,
        "budget_emploi": round(revenu_net_imposable, 2),
        "cotisations_sociales": round(cotisation_annuelle, 2),
        "brut_imposable": round(revenu_net_imposable, 2),
        "precompte_estime": 0.0,
        "net_en_poche": round(net_en_poche, 2),
        "taux_rendement_net": round(rendement, 1),
        "alerte_foyer_fiscal": alerte_foyer,
        "recommandation": recommandation,
    }


def afficher_rapport_comparatif(ca: float, is_annual: bool = False) -> None:
    """
    Affiche une synthèse comparative propre et pédagogique dans la console.
    """
    res_emp = simuler_smart_employe(ca)
    res_etu = simuler_smart_etudiant(ca)
    res_ind = simuler_etudiant_independant(ca, is_annual=is_annual)

    mode_label = "Chiffre d'Affaires Annuel" if is_annual else "Facture ponctuelle de mission"
    print("======================================================================")
    print("🇧🇪 SIMULATEUR SOCIO-FISCAL BELGIQUE 2026 — BUREAU NUMÉRIQUE BTP")
    print("======================================================================")
    print(f"Type de simulation : {mode_label}")
    print(f"Montant HTVA testé : {ca:,.2f} € HTVA\n")

    lignes: List[Tuple[str, str, str, str]] = [
        ("Métrique Financière", "Smart Employé (CP 200)", "Smart Étudiant (600h)", "Étudiant-Indépendant"),
        ("Frais Smart (6,5% + ~8%)", f"{res_emp['frais_gestion_smart'] + res_emp['frais_mutualisation_smart']:.2f} €", f"{res_etu['frais_gestion_smart'] + res_etu['frais_mutualisation_smart']:.2f} €", "0.00 € (Hors Smart)"),
        ("Cotisations Sociales", f"{res_emp['cotisations_sociales']:.2f} €", f"{res_etu['cotisations_sociales']:.2f} €", f"{res_ind['cotisations_sociales']:.2f} € (0 € si < 8 687 €)"),
        ("Précompte Professionnel", f"{res_emp['precompte_estime']:.2f} €", f"{res_etu['precompte_estime']:.2f} €", "Exonéré / Tranche 0"),
        ("NET DISPONIBLE EN POCHE", f"{res_emp['net_en_poche']:.2f} €", f"{res_etu['net_en_poche']:.2f} €", f"{res_ind['net_en_poche']:.2f} €"),
        ("Taux de Rendement Net", f"{res_emp['taux_rendement_net']:.1f} %", f"{res_etu['taux_rendement_net']:.1f} %", f"{res_ind['taux_rendement_net']:.1f} %"),
    ]

    for label, col1, col2, col3 in lignes:
        print(f"• {label:<26} | {col1:<24} | {col2:<24} | {col3}")

    print("\n----------------------------------------------------------------------")
    print("🚨 VÉRIFICATION DES EFFETS DE FALAISE FISCAUX (RISQUE PARENTS) :")
    if res_etu["alerte_foyer_fiscal"] or res_ind["alerte_foyer_fiscal"]:
        print(f"  [ATTENTION] Les revenus nets projetés dépassent le plafond d'enfant à charge (~{PLAFOND_ENFANT_A_CHARGE_NET_ANNUEL:.0f} €/an).")
        print("  Risque de perte de la majoration de quotité pour les parents (+1 500 € à 2 200 € d'impôt).")
    else:
        print(f"  [CONFORME] Les revenus nets projetés restent sous le plafond net d'enfant à charge (~{PLAFOND_ENFANT_A_CHARGE_NET_ANNUEL:.0f} €/an).")

    print("\n📌 ARBITRAGE STRATÉGIQUE RECOMMANDÉ :")
    if ca < POINT_DE_BASCULE_SMART_INASTI:
        print(f"  -> Votre CA ({ca:,.0f} €) est sous le seuil d'équilibre de 6 200 €.")
        print("  -> RECOMMANDATION : Démarrer chez Smart (zéro frais fixes, zéro risque de faillite).")
    else:
        print(f"  -> Votre CA ({ca:,.0f} €) dépasse le seuil d'équilibre de 6 200 €.")
        print("  -> RECOMMANDATION : Basculer vers le statut Étudiant-Indépendant (INASTI) avec comptable.")
    print("======================================================================\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulateur socio-fiscal belge 2026 pour le Bureau Numérique BTP")
    parser.add_argument("--revenue", type=float, default=1000.0, help="Montant HTVA de la facture ou du CA annuel à simuler (ex: 350, 1000, 7500)")
    parser.add_argument("--annual", action="store_true", help="Simule en mode CA annuel global plutôt qu'une facture unitaire")
    parser.add_argument("--regime", type=str, choices=["smart-employee", "smart-student", "inasti-student", "compare"], default="compare", help="Régime légal à simuler")

    args = parser.parse_args()

    if args.regime == "compare":
        afficher_rapport_comparatif(args.revenue, is_annual=args.annual)
    elif args.regime == "smart-employee":
        res = simuler_smart_employe(args.revenue)
        print(f"Régime : {res['regime']}\nCA HTVA : {res['ca_htva']} €\nNet en poche : {res['net_en_poche']} € ({res['taux_rendement_net']} %)")
    elif args.regime == "smart-student":
        res = simuler_smart_etudiant(args.revenue)
        print(f"Régime : {res['regime']}\nCA HTVA : {res['ca_htva']} €\nNet en poche : {res['net_en_poche']} € ({res['taux_rendement_net']} %)")
    elif args.regime == "inasti-student":
        res = simuler_etudiant_independant(args.revenue, is_annual=args.annual)
        print(f"Régime : {res['regime']}\nCA HTVA : {res['ca_htva']} €\nNet en poche : {res['net_en_poche']} € ({res['taux_rendement_net']} %)")


if __name__ == "__main__":
    main()
