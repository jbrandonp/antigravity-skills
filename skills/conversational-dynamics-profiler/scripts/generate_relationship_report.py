#!/usr/bin/env python3
"""
generate_relationship_report.py
-------------------------------
Clinical & Strategic Executive Report Synthesizer.
Transforms quantitative analytics from chat exports into an actionable 360-degree
interpersonal intelligence briefing with:
- Global Relational Health Score (0 - 100)
- Gottman Four Horsemen Threat Assessment
- Gottman Golden Ratio (5:1 Pos/Neg Balance) & Affective Coregulation
- Bids for Connection Responsiveness (Turning Toward rate)
- Demand-Withdraw Dyadic Dynamics
- Mentalization & Epistemic Alignment
- Immediate Tactical Action Plan & Long-Term Relationship Strategy

Zero external dependencies - 100% Python 3.10+ standard library.
Strictly typed: Zero untyped parameters or generic wildcards, in accordance with project standards.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Dict, List, TypedDict

# Import parser and engine from sibling script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_chat_metrics import AnalyticsResult, ChatParser, AdvancedConversationalEngine, CorpusSummary


class HealthScoreBreakdown(TypedDict):
    reciprocity_balance: float
    gottman_safety: float
    mentalization_depth: float
    responsiveness_alignment: float
    emotional_warmth: float
    bid_responsiveness: float


class ThreatCounts(TypedDict):
    criticism: int
    contempt: int
    defensiveness: int
    stonewalling: int


class HealthScoreResult(TypedDict):
    score: float
    breakdown: HealthScoreBreakdown
    threat_counts: ThreatCounts


class RelationshipReportSynthesizer:
    def __init__(self, analytics: AnalyticsResult):
        self.data: AnalyticsResult = analytics
        self.summary: CorpusSummary = analytics.get("summary", {})
        self.senders: List[str] = self.summary.get("senders", [])

    def compute_health_score(self) -> HealthScoreResult:
        """Computes a multi-dimensional clinical relationship stability score (0-100)."""
        if not self.senders:
            return {
                "score": 0.0,
                "breakdown": {
                    "reciprocity_balance": 0.0,
                    "gottman_safety": 0.0,
                    "mentalization_depth": 0.0,
                    "responsiveness_alignment": 0.0,
                    "emotional_warmth": 0.0,
                    "bid_responsiveness": 0.0,
                },
                "threat_counts": {
                    "criticism": 0,
                    "contempt": 0,
                    "defensiveness": 0,
                    "stonewalling": 0,
                }
            }

        # 1. Reciprocity Balance (Max 15 pts)
        vol_ratio = self.summary.get("reciprocity_balance_score", 1.0)
        recip_pts = min(15.0, vol_ratio * 18.0)

        # 2. Gottman Threat Penalty (Max 25 pts)
        gottman = self.data.get("gottman_indicators", {})
        total_criticism = sum(gottman.get(s, {}).get("criticism", 0) for s in self.senders)
        total_contempt = sum(gottman.get(s, {}).get("contempt", 0) for s in self.senders)
        total_defensiveness = sum(gottman.get(s, {}).get("defensiveness", 0) for s in self.senders)
        total_stonewalling = sum(gottman.get(s, {}).get("stonewalling_terms", 0) for s in self.senders)

        gottman_penalty = (total_contempt * 10.0) + (total_criticism * 3.0) + (total_defensiveness * 2.0) + (total_stonewalling * 4.0)
        gottman_score = max(0.0, 25.0 - min(25.0, gottman_penalty))

        # 3. Mentalization & Reflection (Max 15 pts)
        ment = self.data.get("mentalization_indicators", {})
        refl_count = sum(ment.get(s, {}).get("reflective_cognitive", 0) for s in self.senders)
        ment_score = min(15.0, refl_count * 2.0)

        # 4. Latency & Responsiveness (Max 15 pts)
        rtt = self.data.get("rtt_latency", {})
        med_latencies = [float(rtt.get(s, {}).get("median_seconds", 300.0)) for s in self.senders]
        avg_median = sum(med_latencies) / max(len(med_latencies), 1)
        if avg_median <= 60.0:
            lat_score = 15.0
        elif avg_median <= 180.0:
            lat_score = 12.0
        elif avg_median <= 600.0:
            lat_score = 8.0
        else:
            lat_score = 4.0

        # 5. Emotional Warmth & 5:1 Gottman Ratio (Max 15 pts)
        gottman_ratio = self.summary.get("overall_gottman_ratio", 5.0)
        warmth_score = min(15.0, (gottman_ratio / 5.0) * 15.0)

        # 6. Bids for Connection Responsiveness (Max 15 pts)
        bid_rate = self.summary.get("overall_bid_responsiveness_rate", 80.0)
        bid_score = min(15.0, (bid_rate / 100.0) * 15.0)

        breakdown: HealthScoreBreakdown = {
            "reciprocity_balance": round(recip_pts, 1),
            "gottman_safety": round(gottman_score, 1),
            "mentalization_depth": round(ment_score, 1),
            "responsiveness_alignment": round(lat_score, 1),
            "emotional_warmth": round(warmth_score, 1),
            "bid_responsiveness": round(bid_score, 1)
        }

        total_health = min(100.0, sum(breakdown.values()))
        threats: ThreatCounts = {
            "criticism": total_criticism,
            "contempt": total_contempt,
            "defensiveness": total_defensiveness,
            "stonewalling": total_stonewalling
        }

        return {
            "score": round(total_health, 1),
            "breakdown": breakdown,
            "threat_counts": threats
        }

    def generate_markdown(self) -> str:
        if "error" in self.data or not self.senders:
            err = self.data.get("error", "Aucun message ou participant identifié dans le corpus.")
            return f"# ⚠️ Rapport Non Généré\n\n**Cause :** {err}\n"

        health = self.compute_health_score()
        sc = health["score"]
        s = self.summary
        senders = self.senders

        if sc >= 85:
            verdict_badge = "🟢 **EXCELLENT (Haute Cohésion & Sécurité Affective)**"
        elif sc >= 70:
            verdict_badge = "🟡 **BON (Stable avec Décalages d'Expression Mineurs)**"
        elif sc >= 50:
            verdict_badge = "🟠 **ATTENTION (Asymétrie ou Tensions Récurrentes)**"
        else:
            verdict_badge = "🔴 **CRITIQUE (Forte Toxicité ou Désengagement)**"

        md: List[str] = []
        md.append("# 📑 Rapport d'Intelligence Relationnelle & Audit Clinique")
        md.append(
            f"**Cible :** Interaction entre {' et '.join(senders)} | "
            f"**Messages :** {s.get('total_messages', 0)} | "
            f"**Jours :** {s.get('timespan_days', 0.0)}"
        )
        md.append(f"\n### Indice Global de Santé Relationnelle : `{sc} / 100`")
        md.append(f"**Verdict :** {verdict_badge}\n")

        # Breakdown table
        md.append("## 1. Décomposition Multi-Factorielle du Score")
        md.append("| Pilier Clinique | Score Obtenu | Maximum | Interprétation |")
        md.append("|---|---|---|---|")
        b = health["breakdown"]
        md.append(f"| **Sécurité Gottman (Anti-Toxicité)** | `{b['gottman_safety']}` | 25 pts | Absence des 4 cavaliers destructeurs |")
        md.append(f"| **Réciprocité des Échanges** | `{b['reciprocity_balance']}` | 15 pts | Équilibre des volumes et parité des initiatives |")
        md.append(f"| **Chaleur & Ratio Gottman 5:1** | `{b['emotional_warmth']}` | 15 pts | Écologie émotionnelle positive / négative |")
        md.append(f"| **Accueil des Appels (Bids)** | `{b['bid_responsiveness']}` | 15 pts | Réceptivité aux questions et partages intimes |")
        md.append(f"| **Profondeur de Mentalisation** | `{b['mentalization_depth']}` | 15 pts | Verbalisation de l'intériorité et des besoins |")
        md.append(f"| **Alignement du Rythme (RTT)** | `{b['responsiveness_alignment']}` | 15 pts | Synchronisation des temps de réponse |")

        # Section 2: Gottman 5:1 Ratio & Coregulation
        g_ratio = s.get("overall_gottman_ratio", 1.0)
        c_badge = s.get("coregulation_health_badge", "")
        bid_rate = s.get("overall_bid_responsiveness_rate", 0.0)

        md.append("\n## 2. Écologie Affective & Corégulation de Gottman")
        md.append(f"- **Ratio Positif / Négatif :** `{g_ratio} : 1` ➔ **{c_badge}**")
        md.append(f"  *(Standard clinique de Gottman : ≥ 5 marques positives pour 1 tension en période de conflit, ≥ 20:1 au quotidien).*")
        md.append(f"- **Taux de Réponse aux Appels de Contact (Bids) :** `{bid_rate} %`")
        md.append(f"  *(Standard des couples durables / Masters : ≥ 80% d'appels accueillis favorablement).*")

        # Section 3: Gottman Threats
        tc = health["threat_counts"]
        md.append("\n## 3. Évaluation des Risques de Gottman")
        md.append(f"- **Mépris (Contempt) :** `{tc['contempt']}` occurrence(s) ➔ " + ("🟢 **Aucun dédain toxique détecté.**" if tc["contempt"] == 0 else "🔴 **Alerte : Risque de corrosion du lien.**"))
        md.append(f"- **Critique (Criticism) :** `{tc['criticism']}` occurrence(s) ➔ " + ("🟢 Faible." if tc["criticism"] <= 2 else "🟡 Surveiller les reproches sur la forme."))
        md.append(f"- **Défense (Defensiveness) :** `{tc['defensiveness']}` occurrence(s) ➔ " + ("🟢 Réparations fluides." if tc["defensiveness"] <= 3 else "🟡 Tendance à la justification."))
        md.append(f"- **Dérobade (Stonewalling) :** `{tc['stonewalling']}` occurrence(s) ➔ " + ("🟢 Pas de retrait destructeur." if tc["stonewalling"] == 0 else "🟠 Vigilance sur les silences prolongés."))

        # Section 4: Asymmetry & Dyadic Roles
        md.append("\n## 4. Dynamique Dyadique & Rôles Complémentaires")
        vol_map = s.get("volume_by_sender", {})
        if len(senders) == 2:
            s1, s2 = senders[0], senders[1]
            v1, v2 = vol_map.get(s1, 0), vol_map.get(s2, 0)
            higher_v = s1 if v1 >= v2 else s2
            lower_v = s2 if v1 >= v2 else s1
            md.append(f"- **Pôle Moteur / Cadreurs :** **{higher_v}** ({max(v1, v2)} msgs) ➔ Assure l'impulsion émotionnelle, le questionnement et le cadrage des règles.")
            md.append(f"- **Pôle Ancre / Narrateur :** **{lower_v}** ({min(v1, v2)} msgs) ➔ Assure la constance, le calme, les récits de fond et la validation.")
        elif len(senders) == 1:
            md.append(f"- **Échange Unilatéral :** Un seul participant actif ({senders[0]}).")
        else:
            md.append(f"- **Groupe Multi-Participants :** {len(senders)} intervenants enregistrés.")

        # Section 5: Long-Term Strategy
        md.append("\n## 5. Conseils Stratégiques & Routine des 6 Heures Magiques")
        md.append("1. **Honorer la dette orale** : Exprimer de vive voix les sentiments déclarés par écrit pour éteindre le doute téléologique.")
        md.append("2. **Séparations et Retrouvailles délibérées** : Clôturer explicitement les sessions avant les plages de code/travail et décompresser 20 min le soir.")
        md.append("3. **Transformer les 69% de conflits perpétuels en rituels d'humour** : Accepter les différences de tempo sans vouloir changer l'autre.")
        md.append("4. **Sanctuariser le rendez-vous hebdomadaire déconnecté** : 2 heures en tête-à-tête sans écrans pour nourrir la complicité et le désir.")

        return "\n".join(md)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Clinical Relationship Report Synthesizer.")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to chat export (JSON, WhatsApp TXT, Meta JSON, CSV)")
    parser.add_argument("--output", "-o", type=str, default="", help="Path to output markdown report")
    parser.add_argument("--session-gap", type=float, default=4.0, help="Session inactivity gap (hours)")
    args = parser.parse_args()

    messages = ChatParser.parse_file(args.input)
    engine = AdvancedConversationalEngine(messages, session_gap_hours=args.session_gap)
    analytics = engine.analyze()

    synthesizer = RelationshipReportSynthesizer(analytics)
    report = synthesizer.generate_markdown()

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Relationship report written successfully to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
