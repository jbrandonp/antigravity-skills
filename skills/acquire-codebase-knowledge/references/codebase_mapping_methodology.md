# 🗺️ Codebase Mapping & Software Archeology Playbook

> **Standard :** Antigravity Agentic Knowledge Acquisition Standard  
> **Axiom :** *"Never infer, never guess, never document wishful thinking. Ground every architectural claim in physical source files, verified configuration, or deterministic CLI diagnostics."*

---

## 🧭 1. Les 4 Phases de l'Archéologie Logicielle

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ Phase 1 : Scan Déterministe & Intent vs Reality             │
 │  ↳ scan.py --json + lecture PRD/README/ROADMAP              │
 ├─────────────────────────────────────────────────────────────┤
 │ Phase 2 : Investigation Systématique & Topologie            │
 │  ↳ generate_architecture_diagram.py + traçage flux vertical │
 ├─────────────────────────────────────────────────────────────┤
 │ Phase 3 : Rédaction des 7 Piliers dans docs/codebase/       │
 │  ↳ STACK, STRUCTURE, ARCHITECTURE, CONVENTIONS,             │
 │    INTEGRATIONS, TESTING, CONCERNS                          │
 ├─────────────────────────────────────────────────────────────┤
 │ Phase 4 : Validation Déterministe & Clôture                 │
 │  ↳ validate_codebase_docs.py (contrôle intégrité & preuves) │
 └─────────────────────────────────────────────────────────────┘
```

---

## 🧠 2. Modèles Mentaux pour Apprivoiser 100k+ Lignes de Code

Quand on débarque sur une base de code massive (100k à 1M de lignes), tenter de lire chaque fichier mène à la noyade cognitive. Utilisez ces trois modèles éprouvés :

### Modèle A : Le Traçage par "Vertical Slice" (La Tranche Verticale)
Au lieu de lire toute la couche contrôleur ou toute la base de données :
1. Choisissez **un seul cas d'usage critique** (ex. `POST /api/v1/orders` ou l'action de tir du joueur dans un jeu).
2. Partez de l'entrée (`router` ou `PlayerInputComponent`).
3. Suivez l'exécution pas à pas : validation $\to$ service métier $\to$ entité de domaine $\to$ persistance SQL/NoSQL $\to$ réponse.
4. Cette seule tranche révèle 80% des conventions et de l'architecture réelle de tout le projet !

### Modèle B : L'Analyse des "Hotspots" (Fragilité = Fréquence Git $\times$ Complexité)
Les bugs ne se répartissent pas uniformément. 80% des pannes proviennent de 20% des fichiers :
- Fichiers à **fort churn git** (modifiés des dizaines de fois en 90 jours).
- Fichiers de **grande taille** (>500 lignes, "God Files").
- L'intersection de ces deux critères constitue les **Hotspots critiques** à documenter en priorité dans `CONCERNS.md`.

### Modèle C : La Frontière "Hexagonale" et les Intégrations Externes
Isolez immédiatement ce qui est *interne* de ce qui est *externe* :
- **Entrées (Driving Adapters)** : Contrôleurs REST, consommateurs de files Kafka, CLI, gestionnaires d'événements UI.
- **Domaine (Core Logic)** : Règles métier pures, calculs, machines à états, zéro dépendance réseau ou SQL.
- **Sorties (Driven Adapters)** : Clients HTTP tiers (Stripe, Twilio), bases de données (PostgreSQL, SQLite), caches (Redis).

---

## 🛠️ 3. Boîte à Outils WAT de Cartographie

### 🔍 1. Découverte Initiale : `scan.py`
```bash
# Générer le rapport d'analyse textuel
python scripts/scan.py --output docs/codebase/.codebase-scan.txt

# Générer les données structurées pour outillage automatisé
python scripts/scan.py --json --output docs/codebase/.codebase-scan.json
```

### 📐 2. Graphe d'Architecture & Flux : `generate_architecture_diagram.py`
```bash
# Génère les diagrammes Mermaid (Flowchart & Sequence) prêts à insérer dans ARCHITECTURE.md
python scripts/generate_architecture_diagram.py --format markdown
```

### 📉 3. Audit de Dette & Hotspots : `audit_codebase_debt.py`
```bash
# Calcule le score de santé, détecte les God Files (>500 LOC), les cycles et les Hotspots git
python scripts/audit_codebase_debt.py --max-lines 500
```

### 🛡️ 4. Validation Déterministe Phase 4 : `validate_codebase_docs.py`
```bash
# Vérifie l'existence des 7 fichiers, la présence des sections requises et la validité des preuves
python scripts/validate_codebase_docs.py --docs-dir docs/codebase --root .
```

---

## 📋 4. Checklist des 7 Documents Contractuels

| Document | Rôle Majeur | Ce qu'il ne doit JAMAIS contenir |
| :--- | :--- | :--- |
| [`STACK.md`](../assets/templates/STACK.md) | Langages, runtime, gestionnaire de paquets, versions exactes, scripts de build. | Les outils dev confondus avec la prod (ex. TypeScript ou Jest en dépendance de prod). |
| [`STRUCTURE.md`](../assets/templates/STRUCTURE.md) | Organisation des répertoires, points d'entrée, rôles des dossiers. | Les dossiers de build (`dist/`, `build/`, `node_modules/`, `Intermediate/`). |
| [`ARCHITECTURE.md`](../assets/templates/ARCHITECTURE.md) | Style architectural, flux de données, diagrammes Mermaid, responsabilités. | Des architectures fantasmées non visibles dans le code. |
| [`CONVENTIONS.md`](../assets/templates/CONVENTIONS.md) | Normes de nommage, linters, gestion d'erreurs, règles d'import. | Des règles théoriques contredites par 50% des fichiers sources. |
| [`INTEGRATIONS.md`](../assets/templates/INTEGRATIONS.md) | APIs tierces, bases de données, auth, bus de messages, observabilité. | Des clés secrètes ou credentials en clair. |
| [`TESTING.md`](../assets/templates/TESTING.md) | Frameworks de test, répertoires de tests, stratégie de mocks, seuils. | Les TODOs des tests présentés comme de la dette de production. |
| [`CONCERNS.md`](../assets/templates/CONCERNS.md) | Risques majeurs, dette technique, God files, hotspots git, questions `[ASK USER]`. | Des critiques subjectives sans preuves de chemins de fichiers réels. |
