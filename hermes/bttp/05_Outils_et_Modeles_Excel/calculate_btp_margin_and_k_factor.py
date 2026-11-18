"""
Module de calcul de rentabilité, déboursé sec et coefficient K pour le BTP belge.
Permet de calculer le coût horaire réel d'un ouvrier du bâtiment (CP 124 chargé),
le déboursé sec complet d'un chantier et le coefficient de majoration K évitant toute fuite de marge.
Strictement typé, zéro 'Any'.
"""

import sys
from typing import Final, NamedTuple, TypedDict

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class WorkerCostCP124(TypedDict):
    hourly_gross_wage_eur: float
    onss_patronal_rate_pct: float
    work_accident_insurance_pct: float
    constructiv_fse_rate_pct: float
    annual_workable_hours: float
    total_hourly_cost_eur: float
    cost_multiplier_vs_gross: float


class JobMarginAnalysisResult(TypedDict):
    job_title: str
    materials_net_eur: float
    waste_allowance_eur: float  # Chutes et pertes de découpe (8-10%)
    consumables_allowance_eur: float  # Visserie, colles, consommables (3-5%)
    total_materials_eur: float
    labor_hours: float
    hourly_cost_eur: float
    total_labor_cost_eur: float
    subcontracting_eur: float
    waste_disposal_eur: float  # Évacuation gravats / déchetterie
    debourse_sec_total_eur: float  # Déboursé Sec (DS)
    general_overhead_rate_pct: float  # Frais généraux d'entreprise (camionnette, atelier, outillage)
    target_net_margin_pct: float  # Marge bénéficiaire nette cible
    k_factor: float  # Coefficient multiplicateur K
    recommended_sale_price_htva_eur: float  # Prix de vente plancher recommandé
    actual_artisan_price_htva_eur: float  # Prix vendu ou envisagé par l'artisan
    margin_leak_eur: float  # Perte ou gain de marge par rapport au plancher
    real_net_margin_achieved_pct: float  # Marge nette réelle obtenue


def compute_belgian_worker_cost_cp124(
    hourly_gross_wage_eur: float = 18.50,
    onss_patronal_pct: float = 32.5,
    accident_insurance_pct: float = 5.0,
    constructiv_fse_pct: float = 13.0,
    annual_workable_hours: float = 1580.0,
) -> WorkerCostCP124:
    """
    Calcule le coût de revient horaire réel d'un ouvrier belge du bâtiment (CP 124).

    Intègre le salaire horaire brut, les charges patronales ONSS (32,5%),
    l'assurance accidents du travail obligatoire (5%) et les cotisations
    de sécurité d'existence Constructiv / congés payés / intempéries (13%).
    """
    if hourly_gross_wage_eur <= 0:
        raise ValueError("Le salaire horaire brut doit être strictement positif.")

    total_social_multiplier = 1.0 + (onss_patronal_pct + accident_insurance_pct + constructiv_fse_pct) / 100.0
    total_hourly_cost = hourly_gross_wage_eur * total_social_multiplier

    return {
        "hourly_gross_wage_eur": round(hourly_gross_wage_eur, 2),
        "onss_patronal_rate_pct": onss_patronal_pct,
        "work_accident_insurance_pct": accident_insurance_pct,
        "constructiv_fse_rate_pct": constructiv_fse_pct,
        "annual_workable_hours": annual_workable_hours,
        "total_hourly_cost_eur": round(total_hourly_cost, 2),
        "cost_multiplier_vs_gross": round(total_social_multiplier, 3),
    }


def compute_job_k_factor_and_margin(
    job_title: str,
    materials_net_eur: float,
    labor_hours: float,
    hourly_cost_eur: float = 39.50,
    waste_rate_pct: float = 10.0,
    consumables_rate_pct: float = 3.5,
    subcontracting_eur: float = 0.0,
    waste_disposal_eur: float = 150.0,
    overhead_pct: float = 18.0,
    target_net_margin_pct: float = 15.0,
    artisan_quoted_price_htva_eur: float = 0.0,
) -> JobMarginAnalysisResult:
    """
    Calcule le Déboursé Sec (DS), le Coefficient K et la rentabilité réelle d'un devis BTP.

    Formule du Coefficient K :
        K = (1 + Frais_Généraux / 100) / (1 - Marge_Nette_Cible / 100)
    Prix de vente minimal conseillé :
        PV = Déboursé Sec × K
    """
    if materials_net_eur < 0 or labor_hours < 0 or hourly_cost_eur <= 0:
        raise ValueError("Les coûts matières et heures doivent être positifs.")
    if target_net_margin_pct >= 100.0:
        raise ValueError("La marge cible ne peut pas dépasser 100%.")

    waste_eur = materials_net_eur * (waste_rate_pct / 100.0)
    consumables_eur = materials_net_eur * (consumables_rate_pct / 100.0)
    total_materials = materials_net_eur + waste_eur + consumables_eur

    total_labor = labor_hours * hourly_cost_eur
    debourse_sec = total_materials + total_labor + subcontracting_eur + waste_disposal_eur

    # Calcul du Coefficient K
    k_factor = (1.0 + overhead_pct / 100.0) / (1.0 - target_net_margin_pct / 100.0)
    recommended_price = debourse_sec * k_factor

    actual_price = artisan_quoted_price_htva_eur if artisan_quoted_price_htva_eur > 0 else recommended_price
    margin_leak = recommended_price - actual_price

    # Calcul de la marge nette réelle obtenue si vendu au prix de l'artisan
    # actual_price = DS * (1 + overhead) / (1 - actual_margin) => actual_margin = 1 - (DS * (1+overhead)/actual_price)
    if actual_price > 0:
        actual_cost_with_overhead = debourse_sec * (1.0 + overhead_pct / 100.0)
        achieved_margin_pct = ((actual_price - actual_cost_with_overhead) / actual_price) * 100.0
    else:
        achieved_margin_pct = 0.0

    return {
        "job_title": job_title,
        "materials_net_eur": round(materials_net_eur, 2),
        "waste_allowance_eur": round(waste_eur, 2),
        "consumables_allowance_eur": round(consumables_eur, 2),
        "total_materials_eur": round(total_materials, 2),
        "labor_hours": round(labor_hours, 1),
        "hourly_cost_eur": round(hourly_cost_eur, 2),
        "total_labor_cost_eur": round(total_labor, 2),
        "subcontracting_eur": round(subcontracting_eur, 2),
        "waste_disposal_eur": round(waste_disposal_eur, 2),
        "debourse_sec_total_eur": round(debourse_sec, 2),
        "general_overhead_rate_pct": overhead_pct,
        "target_net_margin_pct": target_net_margin_pct,
        "k_factor": round(k_factor, 3),
        "recommended_sale_price_htva_eur": round(recommended_price, 2),
        "actual_artisan_price_htva_eur": round(actual_price, 2),
        "margin_leak_eur": round(margin_leak, 2),
        "real_net_margin_achieved_pct": round(achieved_margin_pct, 1),
    }


def format_margin_diagnostic_report(res: JobMarginAnalysisResult) -> str:
    """
    Rédige un rapport percutant en français démontrant la fuite de marge à l'artisan.
    """
    lines = [
        "==================================================================",
        f"   AUDIT DE RENTABILITÉ & FUITE DE MARGE BTP : {res['job_title'].upper()}",
        "==================================================================",
        "",
        "1. DÉBOURSÉ SEC (DS) — CE QUE CE CHANTIER VOUS COÛTE RÉELLEMENT :",
        f"   • Matériaux bruts grossiste : {res['materials_net_eur']:,.2f} €",
        f"   • Pertes de découpe & chutes (+10%) : {res['waste_allowance_eur']:,.2f} €",
        f"   • Consommables d'atelier (silicone, chevilles, vis) : {res['consumables_allowance_eur']:,.2f} €",
        f"   -> Sous-total Fournitures complètes : {res['total_materials_eur']:,.2f} €",
        f"   • Main d'œuvre ({res['labor_hours']}h à {res['hourly_cost_eur']} €/h chargé CP 124) : {res['total_labor_cost_eur']:,.2f} €",
        f"   • Évacuation déchets / benne / déchetterie : {res['waste_disposal_eur']:,.2f} €",
        f"   -> DÉBOURSÉ SEC TOTAL (Coût direct sorti de votre poche) : {res['debourse_sec_total_eur']:,.2f} €",
        "",
        "2. APPLICATION DU COEFFICIENT K D'ENTREPRISE :",
        f"   • Frais généraux d'atelier / véhicule / assurances : {res['general_overhead_rate_pct']:.1f} %",
        f"   • Marge bénéficiaire nette cible : {res['target_net_margin_pct']:.1f} %",
        f"   -> Coefficient multiplicateur K : x{res['k_factor']:.3f}",
        "",
        "3. LE VERDICT FINANCIER :",
        f"   • PRIX DE VENTE PLANCHER CONSEILLÉ HTVA : {res['recommended_sale_price_htva_eur']:,.2f} €",
        f"   • PRIX ACTUEL DU PATRON : {res['actual_artisan_price_htva_eur']:,.2f} €",
    ]

    if res["margin_leak_eur"] > 50.0:
        lines.extend([
            f"   🚨 ALERTE ROUGE : HÉMORRAGIE DE TRÉSORERIE DE {res['margin_leak_eur']:,.2f} € SUR CE CHANTIER !",
            f"   Votre marge réelle n'est que de {res['real_net_margin_achieved_pct']:.1f} % (au lieu des {res['target_net_margin_pct']:.1f} % prévus).",
            "   Vous financez vous-même les chutes et vos frais de camionnette sans vous en rendre compte.",
        ])
    else:
        lines.append(f"   ✅ Chantier parfaitement bordé : Marge nette de {res['real_net_margin_achieved_pct']:.1f} % sécurisée.")

    lines.append("==================================================================")
    return "\n".join(lines)


if __name__ == "__main__":
    cost = compute_belgian_worker_cost_cp124(hourly_gross_wage_eur=18.50)
    print(f"Coût horaire chargé ouvrier CP 124 : {cost['total_hourly_cost_eur']} €/h (Multiplicateur x{cost['cost_multiplier_vs_gross']})")

    # Exemple réel : Rénovation toiture 120m²
    # L'artisan pense vendre à 11 000 € alors qu'il devrait vendre à 12 850 €
    demo = compute_job_k_factor_and_margin(
        job_title="Rénovation toiture 120m² (Liège)",
        materials_net_eur=4800.0,
        labor_hours=85.0,
        hourly_cost_eur=cost["total_hourly_cost_eur"],
        waste_rate_pct=10.0,
        consumables_rate_pct=4.0,
        waste_disposal_eur=250.0,
        overhead_pct=18.0,
        target_net_margin_pct=15.0,
        artisan_quoted_price_htva_eur=10800.0,
    )
    print("\n" + format_margin_diagnostic_report(demo))
