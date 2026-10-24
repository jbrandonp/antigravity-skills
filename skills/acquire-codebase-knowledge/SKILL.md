---
name: acquire-codebase-knowledge
description: 'Use this skill when the user explicitly asks to map, document, or onboard into an existing codebase. Trigger for prompts like "map this codebase", "document this architecture", "onboard me to this repo", or "create codebase docs". Do not trigger for routine feature implementation, bug fixes, or narrow code edits unless the user asks for repository-level discovery.'
license: MIT
compatibility: 'Cross-platform. Requires Python 3.8+ and git. Run scripts from the target project root.'
metadata:
  version: "2.0"
  enhancements:
    - Multi-language manifest detection (25+ languages supported)
    - Automated Mermaid architecture & data flow diagram generation
    - Quantitative technical debt auditor (god files, git churn hotspots, circular imports)
    - Automated contract validator for all 7 documentation files (Phase 4 validation loop)
    - Full automated unit test suite
    - Multi-platform CI/CD, container, security, and performance markers
argument-hint: 'Optional: specific area to focus on, e.g. "architecture only", "testing and concerns"'
---

# 🗺️ Acquire Codebase Knowledge & Software Archeology

> **Standard :** Antigravity Agentic Knowledge Acquisition Standard  
> **Core Axiom :** *"Never infer, never guess, never document wishful thinking. Ground every architectural claim in physical source files, verified configuration, or deterministic CLI diagnostics."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Arriver sur un projet de 100 000 lignes de code qu'on ne connaît pas, c'est comme atterrir en parachute au milieu d'une immense ville inconnue sans GPS :
- Si tu te mets à visiter chaque maison une par une (lire chaque fichier ligne par ligne), tu vas mettre des mois et avoir le cerveau complètement saturé.
- Si tu te fies uniquement aux vieux panneaux de signalisation ou au plan touristique dessiné il y a trois ans (le fichier `README.md`), tu vas te perdre parce que la ville a changé depuis !
- La bonne méthode, c'est **l'archéologie logicielle méthodique** :
  1. Tu montes en hélicoptère pour voir la carte globale : quels langages, quelles autoroutes principales, quels conteneurs (`scan.py`).
  2. Tu traces une voiture de livraison du début à la fin : comment une requête utilisateur traverse les couches pour aller chercher des données dans la base (`generate_architecture_diagram.py`).
  3. Tu repères les quartiers dangereux et délabrés : les fichiers géants de plus de 500 lignes et ceux que les développeurs modifient constamment (`audit_codebase_debt.py`).
  4. Tu rédiges 7 dossiers ultra-précis dans `docs/codebase/` et tu fais vérifier par un robot qu'aucune affirmation n'est inventée (`validate_codebase_docs.py`).

---

## 📋 2. Le Contrat des 7 Documents Obligatoires

Avant de considérer la mission comme terminée, **exactement ces 7 fichiers** doivent exister et être validés dans `docs/codebase/` :

1. [STACK.md](assets/templates/STACK.md) — Langages, runtimes, dépendances de prod vs outillage dev, scripts de build.
2. [STRUCTURE.md](assets/templates/STRUCTURE.md) — Arborescence, points d'entrée (`main`), rôles stricts des dossiers.
3. [ARCHITECTURE.md](assets/templates/ARCHITECTURE.md) — Style architectural, diagrammes Mermaid, flux de données, responsabilités des couches.
4. [CONVENTIONS.md](assets/templates/CONVENTIONS.md) — Normes de nommage, linters, gestion des erreurs, imports et frontières de modules.
5. [INTEGRATIONS.md](assets/templates/INTEGRATIONS.md) — APIs tierces, bases de données, authentification, bus de messages, observabilité.
6. [TESTING.md](assets/templates/TESTING.md) — Frameworks de test, organisation des suites, stratégie de mocks, couverture.
7. [CONCERNS.md](assets/templates/CONCERNS.md) — Risques prioritaires, dette technique (God files, cycles), hotspots git, questions `[ASK USER]`.

---

## 🛠️ 3. La Boîte à Outils WAT Déterministe

La compétence intègre 4 outils CLI natifs en pur Python (sans dépendances tierces) pour automatiser chaque phase :

### 🔍 A. Scanner de Découverte Globale (`scan.py`)
Scanne l'arborescence, les manifests, les points d'entrée, les variables d'environnement, les commits récents et les pipelines CI/CD.
```bash
# Générer le scan texte standard
python scripts/scan.py --output docs/codebase/.codebase-scan.txt

# Générer les données structurées en JSON pour exploitation automatisée
python scripts/scan.py --json --output docs/codebase/.codebase-scan.json
```

### 📐 B. Générateur de Diagrammes d'Architecture Mermaid (`generate_architecture_diagram.py`)
Analyse les imports et relations entre modules pour générer un `flowchart TD` des sous-systèmes et un `sequenceDiagram` du flux de commande, prêts à coller dans `ARCHITECTURE.md` :
```bash
# Générer le Markdown complet avec blocs Mermaid
python scripts/generate_architecture_diagram.py --format markdown --output docs/codebase/DIAGRAMS.md

# Sortie JSON structurée des dépendances inter-modules
python scripts/generate_architecture_diagram.py --format json
```

### 📉 C. Auditeur de Dette Technique & Hotspots (`audit_codebase_debt.py`)
Identifie mathématiquement les zones à haut risque de régression :
- **God Files** : Fichiers dépassant le seuil de 500 lignes de code (SRP violé).
- **Hotspots Git** : Fichiers à fort churn combiné à une haute complexité ($\text{Risk} = \text{churn} \times \frac{\text{LOC}}{100}$).
- **Dépendances Cycliques** : Détection des cycles d'imports internes (A $\leftrightarrow$ B).
- **Densité de TODOs** : Nombre d'annotations par millier de lignes.
- **Score de Santé Global** : Calculé sur 100 points avec verdict (`HEALTHY`, `MODERATE_DEBT`, `HIGH_TECH_DEBT`).

```bash
python scripts/audit_codebase_debt.py --max-lines 500
python scripts/audit_codebase_debt.py --json
```

### 🛡️ D. Moteur de Validation du Contrat (`validate_codebase_docs.py`)
Valide automatiquement la Phase 4 avant livraison :
- Présence des 7 documents obligatoires dans `docs/codebase/`.
- Présence de toutes les sections requises par chaque template.
- Zéro placeholder de template non rempli (`[item]`, `[path]`, `[risk]`, etc.).
- Extraction automatique des `[TODO]` et des questions numérotées `[ASK USER]`.
- **Vérification physique des preuves** : Contrôle que chaque chemin de fichier cité dans les sections *Evidence* existe réellement sur le disque !

```bash
python scripts/validate_codebase_docs.py --docs-dir docs/codebase --root .
```

---

## 🔄 4. Le Workflow en 4 Phases

```text
- [ ] Phase 1 : Exécuter scan.py, lire les fichiers d'intention (README, SPEC, PRD)
- [ ] Phase 2 : Investiguer les 7 axes avec inquiry-checkpoints.md et les diagrammes
- [ ] Phase 3 : Remplir les 7 documents dans docs/codebase/ depuis les templates
- [ ] Phase 4 : Valider avec validate_codebase_docs.py, résoudre les [ASK USER]
```

### Phase 1 : Scan Déterministe & Alignement Intention
1. Lancez `python scripts/scan.py --json --output docs/codebase/.codebase-scan.json`.
2. Lisez `README.md`, `SPEC.md` ou `DESIGN.md` pour capturer l'intention initiale annoncée.

### Phase 2 : Investigation & Modélisation
1. Chargez [`references/inquiry-checkpoints.md`](references/inquiry-checkpoints.md) pour la grille de questions par template.
2. Si la pile technique est ambiguë, consultez [`references/stack-detection.md`](references/stack-detection.md).
3. Générez les flux avec `generate_architecture_diagram.py`.
4. Évaluez la dette avec `audit_codebase_debt.py`.

### Phase 3 : Rédaction des 7 Documents
Copiez les modèles depuis `assets/templates/` vers `docs/codebase/` et complétez chaque section avec des preuves vérifiables.

### Phase 4 : Validation Automatisée
Exécutez `python scripts/validate_codebase_docs.py`. Répétez les corrections jusqu'à obtenir un score de 100% et le statut `PASS`.

---

## 🚫 5. Anti-Patterns & Pièges Fréquents

| ❌ À Ne Jamais Faire | ✅ Bonne Pratique |
| :--- | :--- |
| Inventer une architecture "Clean/DDD" alors qu'aucun répertoire ne la reflète | Documenter uniquement la structure physique réelle des dossiers |
| Confondre `devDependencies` avec la pile de production | Séparer strictement ce qui tourne en production du tooling local |
| Documenter les dossiers générés (`dist/`, `build/`, `.next/`, `Intermediate/`) | Exclure les artefacts de compilation et documenter le code source |
| Traiter les `README.md` anciens comme une vérité absolue | Vérifier systématiquement que le code source concorde avec le README |
| Laisser des placeholders bruts `[item]` ou `[path]` dans les documents finaux | Remplacer par des faits ou marquer explicitement `[TODO]` / `[ASK USER]` |

---

## 📚 6. Ressources et Guides Embarqués

- 📖 [Méthodologie d'Archéologie Logicielle](references/codebase_mapping_methodology.md)
- ❓ [Points de Contrôle et Questions d'Enquête](references/inquiry-checkpoints.md)
- 🔎 [Guide de Détection de Piles Exotiques](references/stack-detection.md)
- 📁 Modèles de référence : [`STACK.md`](assets/templates/STACK.md), [`STRUCTURE.md`](assets/templates/STRUCTURE.md), [`ARCHITECTURE.md`](assets/templates/ARCHITECTURE.md), [`CONVENTIONS.md`](assets/templates/CONVENTIONS.md), [`INTEGRATIONS.md`](assets/templates/INTEGRATIONS.md), [`TESTING.md`](assets/templates/TESTING.md), [`CONCERNS.md`](assets/templates/CONCERNS.md).
