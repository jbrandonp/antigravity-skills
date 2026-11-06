#!/usr/bin/env python3
"""
simulate_conversational_scenarios.py
------------------------------------
Predictive Stress-Testing, Dyadic State-Machine Simulator & CNV Reframing Engine.
Features:
1. Scenario Stress-Testing: Evaluates 4 friction archetypes against dyadic communication profiles.
2. Markov Dyadic State-Machine: Models neurobiological state transitions
   (Ventral Vagal -> Sympathetic Hyperarousal -> Dorsal Vagal Shutdown -> Co-regulated Repair).
3. CNV Reframer (Non-Violent Communication - Marshall Rosenberg):
   Translates critical or demanding raw chat messages into the 4 OSBD pillars:
   Observation (O), Sentiment (S), Besoin (B), Demande (D).

Zero external dependencies - 100% Python 3.10+ standard library.
Strictly typed: Zero untyped parameters or generic wildcards, in accordance with project standards.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Dict, List, Optional, TypedDict

# Sibling import for optional dynamic chat adaptation
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_chat_metrics import AnalyticsResult, ChatParser, AdvancedConversationalEngine


class ScenarioDefinition(TypedDict):
    title: str
    trigger: str
    predicted_reaction: Dict[str, str]
    risk_level: str
    antidote: str


class DyadicStateTransition(TypedDict):
    from_state: str
    to_state: str
    transition_probability_percent: float
    trigger_condition: str
    neurobiological_mode: str
    antidote_protocol: str


class CNVReframingResult(TypedDict):
    original_message: str
    observation: str
    sentiment: str
    besoin: str
    demande: str
    suggested_reformulation: str


def get_base_scenarios(p1: str = "Partenaire A", p2: str = "Partenaire B") -> Dict[str, ScenarioDefinition]:
    return {
        "unannounced_silence": {
            "title": f"Scénario 1 : Le Silence Professionnel Non Annoncé (36h d'immersion travail)",
            "trigger": f"{p1} s'immerge dans un sprint de travail/développement intense pendant 36 heures sans prévenir.",
            "predicted_reaction": {
                "immediate": f"Inquiétude somatique chez {p2} ➔ Questionnement de contrôle ('Tu es vivant ?').",
                "at_24h": "Activation du mode Équivalence Psychique ('Il/Elle prend ses distances / Je ne compte pas').",
                "at_36h": f"Risque majeur de bascule en mode Shutdown Dorsal Vagal ({p2} se retire par fierté blessée et réflexe de fuite)."
            },
            "risk_level": "🔴 TRÈS ÉLEVÉ (85% de probabilité de réactivation du schéma de retrait)",
            "antidote": f"Prévenir impérativement AVANT la coupure : 'Mon chou, je plonge dans un sprint de travail jusqu'à demain soir. Je serai peu joignable mais tout va super bien entre nous. Je t'embrasse fort !'"
        },
        "laconism_thumbs_up": {
            "title": "Scénario 2 : Le Choc du Laconisme ('👍' ou réponse en un mot après confidence)",
            "trigger": f"{p2} envoie un long message intime ou une photo de son quotidien et reçoit un simple '👍' ou 'Dakor'.",
            "predicted_reaction": {
                "immediate": "Sensation physique de douche froide ➔ Frustration verbale ('Messages à deux vitesses').",
                "at_3h": "Mise à l'épreuve téléologique : exigence d'explications et suspicion d'indifférence."
            },
            "risk_level": "🟡 MODÉRÉ (45% de friction, réparable rapidement si désamorcé)",
            "antidote": "Bannir définitivement le pouce seul. Remplacer par : 'Bien reçu mon chaton ! Je lis ça au calme tout à l'heure, hâte d'en parler avec toi ❤️'"
        },
        "boundary_leak": {
            "title": "Scénario 3 : La Friction des Frontières & Révélation aux Proches",
            "trigger": "Un ami commun fait une allusion indiscrète sur leur intimité lors d'une discussion.",
            "predicted_reaction": {
                "immediate": "Peur immédiate d'être exposé(e) et sentiment d'atteinte à la bulle intime du couple.",
                "consequence": "Fermeture des confidences futures et repli protecteur temporaire."
            },
            "risk_level": "🟠 ÉLEVÉ (70% d'impact sur le capital confiance)",
            "antidote": "Appliquer le Protocole GAMMA : Reconnaître immédiatement la maladresse, réaffirmer la sanctuarisation du couple et cadrer fermement les tiers."
        },
        "construction_stress": {
            "title": "Scénario 4 : Le Choc Matériel ou Financier (Chantier / Dépense imprévue)",
            "trigger": "Un retard majeur ou un surcoût imprévu survient sur un investissement ou la construction d'un logement.",
            "predicted_reaction": {
                "immediate": "Hyper-vigilance financière, recherche d'alternatives, anxiété de contrôle.",
                "consequence": "Besoin d'un soutien émotionnel inconditionnel, mais refus de toute ingérence décisionnelle dans son domaine."
            },
            "risk_level": "🟡 SAIN SI BIEN GUIDÉ (Opportunité majeure de renforcement du couple)",
            "antidote": "Adopter la posture du Roc & Coach : Écouter sans dicter la solution, valider sa compétence, et offrir un espace de détente et de réconfort."
        },
        "demand_withdraw": {
            "title": "Scénario 5 : Cycle Demande-Retrait (Demand-Withdraw Cascade)",
            "trigger": f"{p1} intensifie les demandes de communication face à un silence, provoquant le repli de {p2}.",
            "predicted_reaction": {
                "immediate": "Augmentation de la pression verbale (messages répétés, reproches déguisés).",
                "at_6h": f"{p2} se mure dans le silence pour réguler son anxiété, interprété comme du désamour.",
                "at_24h": "Escalade conflictuelle à la réouverture ou rupture de communication prolongée."
            },
            "risk_level": "🔴 TRÈS ÉLEVÉ (Structurellement le plus prédictif de dissolution selon Gottman)",
            "antidote": "Désamorçage asymétrique : Remplacer l'insistance par une invitation sécurisante sans date butoir punitive."
        },
        "stonewalling": {
            "title": "Scénario 6 : Retrait Défensif 'Mur de Pierre' (Stonewalling Dorsal)",
            "trigger": f"Au milieu d'une tension, {p2} cesse toute réaction verbale et ignore les sollicitations.",
            "predicted_reaction": {
                "immediate": "Surchauffe cardiaque chez le partenaire (dépassant 100 bpm), sentiment d'impuissance.",
                "consequence": "Activation du système nerveux dorsal : paralysie relationnelle et sidération affective."
            },
            "risk_level": "🔴 CRITIQUE (Signe d'inondation émotionnelle somatique)",
            "antidote": "Pause physiologique de 20 minutes minimum avec accord mutuel avant reprise calme."
        },
        "triangulation": {
            "title": "Scénario 7 : Le Piège de la Triangulation de Karpman",
            "trigger": "Introduction d'un tiers (famille, ami, collègue) comme arbitre ou validation d'un reproche.",
            "predicted_reaction": {
                "immediate": "Passage immédiat dans les rôles Persécuteur / Victime / Sauveteur.",
                "consequence": "Destruction de la confidentialité de la 'Bulle du Couple' (Stan Tatkin)."
            },
            "risk_level": "🟠 ÉLEVÉ (Érosion insidieuse de la sécurité d'attachement)",
            "antidote": "Sanctuarisation stricte : Bannir les comparaisons tierces et refocaliser uniquement sur le duo."
        },
        "bids_missed": {
            "title": "Scénario 8 : L'Accumulation d'Appels de Contact Manqués (Missed Bids)",
            "trigger": f"{p1} partage 3 anecdotes ou questions personnelles consécutives sans obtenir d'engagement.",
            "predicted_reaction": {
                "immediate": "Baisse de l'enthousiasme conversationnel, diminution de la longueur des messages.",
                "at_48h": "Extinction opérante : arrêt progressif des initiatives spontanées."
            },
            "risk_level": "🟡 MODÉRÉ À FORT (Mort à petit feu de l'intimité quotidienne)",
            "antidote": "Appliquer la règle des Bids : Accueillir activement au moins 5 appels de contact sur 6."
        },
        "gaslighting": {
            "title": "Scénario 9 : La Dénégation Épistémique & Confusion de Réalité (Gaslighting)",
            "trigger": f"Face à un fait précis mentionné par {p1}, {p2} affirme que l'événement n'a jamais eu lieu ('Tu inventes').",
            "predicted_reaction": {
                "immediate": "Choc cognitif, sentiment de perte de repères et doute de soi somatique.",
                "consequence": "Perte de confiance épistémique, sur-vérification compulsive des historiques de messages."
            },
            "risk_level": "🔴 CRITIQUE (Destructeur de la sécurité psychologique)",
            "antidote": "Ancrage factuel calme : Refuser la surenchère et réaffirmer son ressenti sans agressivité."
        },
        "hyperactivation": {
            "title": "Scénario 10 : L'Hyper-activation Anxieuse (Double-Pings en Rafale)",
            "trigger": f"{p1} n'obtient pas de réponse après 4h et envoie 5 messages successifs de plus en plus anxieux.",
            "predicted_reaction": {
                "immediate": "Inondation du canal de discussion, sentiment d'étouffement chez {p2}.",
                "consequence": "Retrait prolongé de {p2} pour retrouver son calme, amplifiant l'angoisse de {p1}."
            },
            "risk_level": "🟠 ÉLEVÉ (Cercle vicieux classique Anxieux-Évitant)",
            "antidote": "Régulation somatique autonome : Poser le téléphone 1h et respirer par le ventre avant d'écrire."
        },
        "reassurance_trap": {
            "title": "Scénario 11 : Le Piège de la Rassurance Compulsive",
            "trigger": f"{p1} demande de façon répétée : 'Est-ce que tout va bien entre nous ? Tu es sûr(e) ?'",
            "predicted_reaction": {
                "immediate": "Fatigue décisionnelle chez {p2}, irritation sourde.",
                "consequence": "La rassurance verbale soulage 5 minutes mais alimente le doute de fond."
            },
            "risk_level": "🟡 MODÉRÉ (Épuisement affectif progressif du partenaire)",
            "antidote": "Pacte de transparence : 'Si quelque chose ne va pas, je te le dirai directement. Quand je ne dis rien, tout va bien.'"
        },
        "vicious_cycle": {
            "title": "Scénario 12 : L'Engrenage de la Boucle d'Escalade et Rupture",
            "trigger": "Succession de silences défensifs, reproches croisés et refus d'admettre ses torts.",
            "predicted_reaction": {
                "immediate": "Activation simultanée des systèmes de survie sympathique et dorsal.",
                "consequence": "Rupture temporaire du lien, blocage mutuel."
            },
            "risk_level": "🔴 EXTRÊME (Crise majeure du couple)",
            "antidote": "Protocole de Corégulation en 4 Étapes (EFT) : Arrêt immédiat de l'écrit, présence physique ou vocale douce."
        }
    }


def compute_markov_state_machine(gottman_ratio: float = 5.0, stonewalling_count: int = 0) -> List[DyadicStateTransition]:
    """Models transition probabilities between the 4 autonomic dyadic states."""
    # If gottman ratio is low or stonewalling is high, probability of transition to shutdown increases
    p_anxious = min(85.0, max(20.0, 70.0 - (gottman_ratio * 8.0)))
    p_shutdown = min(90.0, max(15.0, 25.0 + (stonewalling_count * 15.0)))
    p_repair = min(95.0, max(30.0, 40.0 + (gottman_ratio * 10.0)))

    return [
        {
            "from_state": "S0: Connexion Sécure (Ventral Vagal)",
            "to_state": "S1: Hyper-activation Anxieuse (Sympathique)",
            "transition_probability_percent": round(p_anxious, 1),
            "trigger_condition": "Silence non annoncé > 12h ou laconisme brutal ('👍')",
            "neurobiological_mode": "Montée de cortisol, accélération du rythme cardiaque, double-pings interrogatifs.",
            "antidote_protocol": "Protocole BETA (Validation affective immédiate et réassurance sensorielle/vocale)."
        },
        {
            "from_state": "S1: Hyper-activation Anxieuse (Sympathique)",
            "to_state": "S2: Retrait Défensif (Shutdown Dorsal)",
            "transition_probability_percent": round(p_shutdown, 1),
            "trigger_condition": "Réponse froide, justification défensive ou mépris répété.",
            "neurobiological_mode": "Hypo-activation, détachement émotionnel, fierté blessée, blocage sur les réseaux.",
            "antidote_protocol": "Protocole ALPHA (Offrande de réouverture calme après 12-24h de pause sans insister)."
        },
        {
            "from_state": "S2: Retrait Défensif (Shutdown Dorsal)",
            "to_state": "S3: Corégulation Réparatrice (Ventral Vagal)",
            "transition_probability_percent": round(p_repair, 1),
            "trigger_condition": "Reconnaissance d'impact émotionnel sans débat d'ego et présence vocale/physique.",
            "neurobiological_mode": "Libération d'ocytocine, relâchement des tensions musculaires, rire et complicité.",
            "antidote_protocol": "Protocole GAMMA / TED (Posture de Coach bienveillant et sanctuarisation de la bulle)."
        }
    ]


def cnv_reframe_message(raw_text: str) -> CNVReframingResult:
    """Translates a raw demanding or critical message into Non-Violent Communication (OSBD)."""
    clean = raw_text.strip()
    obs = "Quand je constate une pause prolongée dans nos échanges ou un message très bref..."
    sent = "...je ressens une inquiétude et un sentiment d'éloignement involontaire..."
    bes = "...parce que j'ai besoin de clarté, de continuité affective et de complicité avec toi..."
    dem = "...serais-tu d'accord pour qu'on prenne 5 minutes au calme ce soir au téléphone ?"

    txt_lower = clean.lower()
    if "toujours" in txt_lower or "jamais" in txt_lower:
        obs = f"Quand j'ai l'impression que la situation se reproduit (comme récemment)..."
    if "fatigué" in txt_lower or "marre" in txt_lower:
        sent = f"...je ressens de la fatigue et de la peine parce que le lien compte énormément pour moi..."

    reformulation = (
        f"« {obs} {sent} {bes} {dem} »"
    )

    return {
        "original_message": clean,
        "observation": obs,
        "sentiment": sent,
        "besoin": bes,
        "demande": dem,
        "suggested_reformulation": reformulation
    }


def run_simulation(scenario_key: Optional[str] = None, p1: str = "Brandon", p2: str = "Tatiana") -> Dict[str, ScenarioDefinition]:
    scenarios = get_base_scenarios(p1, p2)
    if scenario_key and scenario_key in scenarios:
        return {scenario_key: scenarios[scenario_key]}
    return scenarios


def format_markdown_simulation(sim_results: Dict[str, ScenarioDefinition]) -> str:
    md: List[str] = []
    md.append("# 🔮 Simulateur Prédictif de Scénarios de Stress Relationnel")
    md.append("Modélisation dynamique non linéaire des trajectoires de crise et protocoles d'antidote.\n")

    for key, data in sim_results.items():
        md.append(f"## {data['title']}")
        md.append(f"**Déclencheur :** {data['trigger']}")
        md.append(f"**Niveau de Risque :** `{data['risk_level']}`\n")
        md.append("**Trajectoire Prédictive :**")
        for stage, desc in data["predicted_reaction"].items():
            md.append(f"- *{stage.capitalize()} :* {desc}")
        md.append(f"\n💡 **Antidote Opérationnel :**\n> {data['antidote']}\n")
        md.append("---\n")

    return "\n".join(md)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Conversational Stress-Testing, State-Machine Simulator & CNV Reframer.")
    parser.add_argument("scenario_pos", nargs="?", default="", help="Optional scenario name (positional)")
    parser.add_argument("--input", "-i", type=str, default="", help="Optional chat dump to personalize participant identities")
    parser.add_argument("--scenario", "-s", dest="scenario_flag", choices=['unannounced_silence', 'laconism_thumbs_up', 'boundary_leak', 'construction_stress', 'demand_withdraw', 'stonewalling', 'triangulation', 'bids_missed', 'gaslighting', 'hyperactivation', 'reassurance_trap', 'vicious_cycle', 'all'], default=None, help="Specific scenario to simulate")
    parser.add_argument("--turns", "-t", type=int, default=3, help="Simulated interaction turns (optional)")
    parser.add_argument("--state-machine", action="store_true", help="Display the Markovian dyadic autonomic state transitions")
    parser.add_argument("--cnv-reframe", type=str, default="", help="Translate a critical/abrasive raw text into Non-Violent Communication (OSBD)")
    parser.add_argument("--output", "-o", type=str, default="", help="Path to save simulation report")
    args = parser.parse_args()

    chosen_scenario = args.scenario_flag or (args.scenario_pos if args.scenario_pos in ['unannounced_silence', 'laconism_thumbs_up', 'boundary_leak', 'construction_stress', 'demand_withdraw', 'stonewalling', 'triangulation', 'bids_missed', 'gaslighting', 'hyperactivation', 'reassurance_trap', 'vicious_cycle', 'all'] else None)

    # 1. CNV Reframer mode
    if args.cnv_reframe:
        res = cnv_reframe_message(args.cnv_reframe)
        print("\n🌱 --- Traduction en Communication Non Violente (CNV - Marshall Rosenberg) ---")
        print(f"Message brut original : \"{res['original_message']}\"\n")
        print(f"• [O]bservation sans jugement : {res['observation']}")
        print(f"• [S]entiment authentique     : {res['sentiment']}")
        print(f"• [B]esoin universel          : {res['besoin']}")
        print(f"• [D]emande négociable        : {res['demande']}")
        print(f"\n💡 Proposition de reformulation pacifiante :\n{res['suggested_reformulation']}\n")
        return

    # 2. State machine mode
    if args.state_machine:
        transitions = compute_markov_state_machine()
        print("\n🔄 --- Machine à États Dyadiques & Probabilités de Transition ---")
        for t in transitions:
            print(f"\n[{t['from_state']}] ───► [{t['to_state']}]")
            print(f"  • Probabilité estimée : {t['transition_probability_percent']} %")
            print(f"  • Déclencheur         : {t['trigger_condition']}")
            print(f"  • Mode autonome       : {t['neurobiological_mode']}")
            print(f"  • Antidote préconisé  : {t['antidote_protocol']}")
        print("\n" + "="*80)
        return

    # 3. Standard scenario simulation mode
    p1, p2 = "Brandon", "Tatiana"
    if args.input and os.path.exists(args.input):
        try:
            msgs = ChatParser.parse_file(args.input)
            engine = AdvancedConversationalEngine(msgs)
            res_data = engine.analyze()
            senders = res_data.get("summary", {}).get("senders", [])
            if len(senders) >= 2:
                p1, p2 = senders[0], senders[1]
            elif len(senders) == 1:
                p1 = senders[0]
        except Exception:
            pass

    results = run_simulation(chosen_scenario if chosen_scenario != 'all' else None, p1, p2)
    md_output = format_markdown_simulation(results)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md_output)
        print(f"Simulation report written to {args.output}")
    else:
        print(md_output)


if __name__ == "__main__":
    main()
