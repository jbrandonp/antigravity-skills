"""
Générateur de classeurs Excel de Commercial Due Diligence (CDD).
Format inspiré des rapports d'audit de Private Equity (Bain / McKinsey).
Utilise openpyxl avec des formules natives de calculs dynamiques.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


@dataclass(frozen=True)
class CDDPricingRow:
    competitor_name: str
    tier_name: str
    monthly_price_eur: float
    setup_fee_eur: float
    value_metric: str
    source_url: str


@dataclass(frozen=True)
class CDDBenchmarkRow:
    competitor_name: str
    ttv_days: int
    cac_eur: float
    arpu_eur: float
    churn_annual_pct: float
    nrr_pct: float


class CDDReportGenerator:
    """Générateur de rapports financiers et opérationnels Excel."""

    @classmethod
    def generate_excel_dossier(
        cls,
        output_path: Path,
        analysis_title: str,
        pricing_rows: list[CDDPricingRow],
        benchmark_rows: list[CDDBenchmarkRow],
        win_loss_distribution: dict[str, float],
    ) -> Path:
        """Compile le classeur multi-onglets complet avec mise en forme professionnelle."""
        wb = openpyxl.Workbook()

        # Styles partagés
        header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        title_font = Font(name="Calibri", size=16, bold=True, color="1F497D")
        thin_border = Border(
            left=Side(style="thin", color="D9D9D9"),
            right=Side(style="thin", color="D9D9D9"),
            top=Side(style="thin", color="D9D9D9"),
            bottom=Side(style="thin", color="D9D9D9"),
        )

        # -------------------------------------------------------------
        # ONGLET 1 : Synthèse Exécutive & KIQs
        # -------------------------------------------------------------
        ws_exec = wb.active
        if ws_exec is None:
            ws_exec = wb.create_sheet(title="Synthèse Exécutive", index=0)
        else:
            ws_exec.title = "Synthèse Exécutive"
        ws_exec.views.sheetView[0].showGridLines = True

        ws_exec["A1"] = "COMMERCIAL DUE DILIGENCE : AUDIT STRATÉGIQUE"
        ws_exec["A1"].font = title_font
        ws_exec["A2"] = f"Projet : {analysis_title} | Cadre SCIP & Valona World-Class"
        ws_exec["A2"].font = Font(name="Calibri", size=11, italic=True, color="595959")

        ws_exec["A4"] = "Recommandation Stratégique Principale (Noyau de Rumelt) :"
        ws_exec["A4"].font = Font(bold=True)
        ws_exec["A5"] = "1. Diagnostic : Verrouillage historique par des logiciels lourds aux coûts cachés élevés."
        ws_exec["A6"] = "2. Politique Directrice : Offre locale légère sans abonnement captif + conformité Peppol 2026 native."
        ws_exec["A7"] = "3. Action Clé : Déploiement de convertisseurs 1-clic pour ramener le coût de changement à zéro."

        # -------------------------------------------------------------
        # ONGLET 2 : Tarifs & Modélisation TCO Dynamique
        # -------------------------------------------------------------
        ws_pricing = wb.create_sheet(title="Pricing & TCO 36M")
        ws_pricing.views.sheetView[0].showGridLines = True

        pricing_headers = [
            "Acteur", "Forfait", "Prix Mensuel (€)", "Frais Setup (€)",
            "Métrique", "TCO 12 Mois (€)", "TCO 36 Mois (€)", "Source Vérifiée"
        ]
        ws_pricing.append(pricing_headers)

        for col_idx, text in enumerate(pricing_headers, 1):
            cell = ws_pricing.cell(row=1, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")

        start_row = 2
        for r_idx, row_data in enumerate(pricing_rows, start_row):
            # Formules Excel natives pour le TCO : =Setup + (Mensuel * 12)
            formula_12m = f"=D{r_idx}+(C{r_idx}*12)"
            formula_36m = f"=D{r_idx}+(C{r_idx}*36)"

            ws_pricing.append([
                row_data.competitor_name,
                row_data.tier_name,
                row_data.monthly_price_eur,
                row_data.setup_fee_eur,
                row_data.value_metric,
                formula_12m,
                formula_36m,
                row_data.source_url,
            ])

            for c in range(1, 9):
                cell = ws_pricing.cell(row=r_idx, column=c)
                cell.border = thin_border
                if c in (3, 4):
                    cell.number_format = "#,##0.00 €"
                elif c in (6, 7):
                    cell.number_format = "#,##0.00 €"
                    cell.font = Font(bold=True)

        # -------------------------------------------------------------
        # ONGLET 3 : Autopsie Win/Loss Réelle
        # -------------------------------------------------------------
        ws_winloss = wb.create_sheet(title="Win-Loss Reclassifié")
        ws_winloss.views.sheetView[0].showGridLines = True

        wl_headers = ["Cause Racine Réelle (Acheteur)", "Part des Pertes (%)", "Action Recommandée"]
        ws_winloss.append(wl_headers)

        for col_idx in range(1, 4):
            c = ws_winloss.cell(row=1, column=col_idx)
            c.fill = header_fill
            c.font = header_font

        for idx, (cause, pct) in enumerate(win_loss_distribution.items(), 2):
            ws_winloss.append([cause, pct / 100.0, "Priorité d'optimisation produit"])
            c_pct = ws_winloss.cell(row=idx, column=2)
            c_pct.number_format = "0.0%"
            c_pct.font = Font(bold=True)

        # -------------------------------------------------------------
        # ONGLET 4 : Benchmarking Opérationnel (TTV, CAC, Churn)
        # -------------------------------------------------------------
        ws_bench = wb.create_sheet(title="Benchmarking Opérationnel")
        ws_bench.views.sheetView[0].showGridLines = True

        bench_headers = ["Acteur", "Time-To-Value (Jours)", "CAC (€)", "ARPU/Mois (€)", "Churn Annuel", "NRR (%)"]
        ws_bench.append(bench_headers)

        for col_idx in range(1, 7):
            c = ws_bench.cell(row=1, column=col_idx)
            c.fill = header_fill
            c.font = header_font

        for b_idx, b in enumerate(benchmark_rows, 2):
            ws_bench.append([
                b.competitor_name,
                b.ttv_days,
                b.cac_eur,
                b.arpu_eur,
                b.churn_annual_pct,
                b.nrr_pct,
            ])
            ws_bench.cell(row=b_idx, column=5).number_format = "0.0%"
            ws_bench.cell(row=b_idx, column=6).number_format = "0.0%"

        # Ajustement automatique des largeurs de colonnes sur tous les onglets
        for sheet in wb.worksheets:
            for col in sheet.columns:
                max_len = max((len(str(cell.value or "")) for cell in col), default=10)
                col_num = col[0].column if col[0].column is not None else 1
                col_letter = get_column_letter(col_num)
                sheet.column_dimensions[col_letter].width = max(max_len + 4, 12)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        wb.save(output_path)
        return output_path
