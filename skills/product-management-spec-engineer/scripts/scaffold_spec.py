#!/usr/bin/env python3
"""Product & Architecture Specification Scaffolder.

Scaffolds standard, production-ready specification templates:
- PRD (Product Requirements Document with problem, outcome, metrics)
- RFC (Technical Request for Comments with architecture trade-offs)
- ADR (Architecture Decision Record using the MADR 3.0 standard)
- STORY (INVEST Agile User Story with Gherkin Given/When/Then tests)
"""

import argparse
from datetime import datetime
from pathlib import Path
import sys

TEMPLATES = {
    "prd": """# PRD: {title}

**Auteur :** {author}  
**Date :** {date}  
**Statut :** [Brouillon | En Revue | Approuvé]  
**Target Release :** QX 202X  

---

## 🎯 1. Problème & Opportunité
- **Constat :** [Quel problème utilisateur ou métier cherche-t-on à résoudre ?]
- **Preuve / Données :** [Retours utilisateurs, métriques analytics, perte de conversion observée]
- **Impact :** [Pourquoi est-ce urgent et critique de résoudre cela maintenant ?]

## 🌟 2. Proposition de Valeur & Outcome
- **Vision Produit :** [En une phrase, ce que cette fonctionnalité apporte]
- **Ce que l'utilisateur peut accomplir :** [Bénéfice direct]

## 🚫 3. Non-Goals (Périmètre Exclu)
- [Ce que cette version NE FERA PAS délibérément]
- [Fonctionnalités repoussées à la v2]

## 👤 4. Personas & User Journey
1. **Étape 1 :** L'utilisateur arrive sur...
2. **Étape 2 :** Il effectue l'action...
3. **Étape 3 :** Le système répond en...

## 📊 5. Métriques de Succès (KPIs)
- **Primary Metric :** [ex: Taux d'adoption > 40% sous 14 jours]
- **Guardrail Metric :** [ex: Aucune augmentation du taux de support client (< 1%)]

## 📋 6. Exigences Fonctionnelles (Functional Requirements)
- **FR-1 :** Le système doit permettre de...
- **FR-2 :** En cas d'erreur réseau, afficher un écran de secours avec réessai.
""",

    "rfc": """# RFC: {title}

**Auteur :** {author}  
**Date :** {date}  
**Statut :** [Draft | Under Review | Accepted | Superseded]  

---

## 📌 1. Contexte & Problématique Technique
[Décrire l'architecture actuelle, ses limites en performance, scalabilité ou maintenabilité]

## 🏗️ 2. Architecture Proposée
```text
  [ Client ] ---> [ API Gateway ] ---> [ Service Proposé ] ---> [ Base de Données ]
```
[Explication technique détaillée des composants, protocoles et formats de données]

## ⚖️ 3. Options Étudiées & Arbitrages (Trade-offs)
| Option | Avantages | Inconvénients | Verdict |
|---|---|---|---|
| **Option A (Retenue)** | Haute perf, natif | Courbe d'apprentissage | **Sélectionnée** |
| **Option B** | Plus simple au début | Ne scale pas | Rejetée |

## 🔒 4. Sécurité & Données Privées
- Authentification : [OAuth2 / JWT]
- Données sensibles : [Chiffrement au repos, hashing Argon2id]

## 🚀 5. Plan de Déploiement & Rollback
- Étape 1 : Migration de schéma avec `lock_timeout`.
- Étape 2 : Déploiement Canary (10% du trafic).
- Étape 3 : Rollback immédiat si taux d'erreur 5xx > 0.1%.
""",

    "adr": """# ADR: {title}

- **Statut :** [Proposé | Accepté | Rejeté | Remplacé]
- **Date :** {date}
- **Décideurs :** {author}

---

## Contexte et Déclencheur
[Quel changement technique ou nouveau besoin métier impose de prendre une décision ?]

## Facteurs de Décision (Decision Drivers)
- Performance & faible latence (< 5ms)
- Zéro dépendance externe lourde (Zéro-Docker)
- Typage strict et maintenabilité à long terme

## Options Considérées
1. **Option 1 :** [Description]
2. **Option 2 :** [Description]

## Décision Retenue
Nous avons choisi l'**Option 1**, car [justification clé].

## Conséquences
- **Positives :** [Gains attendus]
- **Négatives :** [Compromis acceptés ou dette technique assumée]
""",

    "story": """# Story: {title}

**En tant que :** [Rôle / Persona utilisateur]  
**Je veux :** [Accomplir cette action spécifique]  
**Afin de :** [Obtenir ce bénéfice mesurable]  

---

## Critères d'Acceptation (Gherkin Format)

### Scénario 1 : Succès nominal
- **Given (Étant donné)** : L'utilisateur est connecté avec un compte valide.
- **When (Quand)** : Il clique sur le bouton de confirmation.
- **Then (Alors)** : La transaction est validée en moins de 500 ms et un e-mail de reçu est envoyé.

### Scénario 2 : Échec et gestion d'erreur
- **Given** : Le solde est insuffisant ou la carte rejetée.
- **When** : Il tente de finaliser l'achat.
- **Then** : Un message explicite s'affiche sans recharger la page, et aucune commande n'est créée en base.

## Notes Techniques & Definition of Done (DoD)
- [ ] Tests unitaires couvrant 80%+ du code.
- [ ] Aucune violation d'accessibilité (contraste et labels ARIA validés).
- [ ] Zéro type `any`.
"""
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Product & Architecture Spec Scaffolder")
    parser.add_argument("--type", choices=["prd", "rfc", "adr", "story"], required=True, help="Type of document")
    parser.add_argument("--title", required=True, help="Title of the specification")
    parser.add_argument("--author", default="Brandon", help="Author name (default: Brandon)")
    parser.add_argument("-o", "--output", help="Output file path (default: stdout or ./[type]-[title].md)")
    args = parser.parse_args()

    date_str = datetime.now().strftime("%Y-%m-%d")
    template = TEMPLATES[args.type].format(
        title=args.title,
        author=args.author,
        date=date_str
    )

    if args.output:
        out_path = Path(args.output)
    else:
        slug = args.title.lower().replace(" ", "-").replace("/", "-")
        out_path = Path(f"{args.type}-{slug}.md")

    out_path.write_text(template, encoding="utf-8")
    print(f"✓ Scaffolded {args.type.upper()} specification at: '{out_path}'")


if __name__ == "__main__":
    main()
