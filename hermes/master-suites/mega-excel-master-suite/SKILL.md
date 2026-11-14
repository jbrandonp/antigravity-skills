---
name: mega-excel-master-suite
description: >-
  Universal Master Enterprise Excel (.xlsx, .xlsm) & Headless Spreadsheet Engineering Suite (v3.1): Unifies the 7 state-of-the-art spreadsheet frameworks (anthropics/skills/xlsx, nousresearch/hermes-agent/xlsx, GRID-is/spreadsheet-skills, runcell/excel-data-analysis, carderne/agent-xlsx, Oria One 25-model library, and haris-musa/excel-mcp-server). Enforces zero mental arithmetic by LLMs, headless LibreOffice recalculation, reference-aware AST formula shifting, dirty ERP data unmerging with a zero-tolerance mathematical reconciliation gate (Delta = 0.00), 7 institutional financial models with automated balance sheet tie-outs, DAG error root-cause isolation, and a native Model Context Protocol (MCP) server.
version: 3.1.0
tags:
  - excel
  - xlsx
  - financial-modeling
  - openpyxl
  - mcp
  - recalc
  - libreoffice
  - data-cleaning
  - accounting
  - pivottable
  - dcf
  - lbo
  - 3-statement-model
  - super-mega-suite
consolidated_master_suites:
  - anthropics/skills/xlsx
  - nousresearch/hermes-agent/xlsx
  - GRID-is/spreadsheet-skills
  - runcell/excel-data-analysis
  - carderne/agent-xlsx
  - oria-one/excel-modeling-library
  - haris-musa/excel-mcp-server
---

# 📊 Mega Excel & Spreadsheet Engineering Suite (v3.1)

> **Suite Maîtresse d'Ingénierie Tableur & Modélisation Financière :** Fusion intégrale des 7 frameworks majeurs de l'écosystème d'agents IA (**anthropics/skills**, **hermes-agent**, **GRID.is**, **runcell**, **agent-xlsx**, **Oria One**, et **excel-mcp-server**) en une plateforme unifiée déterministe avec moteur d'exécution et serveur MCP natif.

---

## 🎯 Quand Déclencher cette Mega-Suite (Triggers)

Activez ce méga-module dès qu'une tâche implique au moins l'un des besoins suivants :
1. **Création ou Édition de Classeurs Excel (`.xlsx`, `.xlsm`) :** Génération de fichiers financiers, reporting de gestion, tableaux de bord de données ou conversion tabulaire.
2. **Modélisation Financière Institutionnelle :** 3-Statement (P&L, Bilan, Cash Flow), DCF, LBO, SaaS Runway, Debt Schedules, Cap Tables ou Working Capital.
3. **Audit de Recalcul & Zéro Erreur :** Vérification headless stricte des formules (`#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`) et des balises de cache OpenXML (`<v>`).
4. **Nettoyage d'Exports ERP Corrompus :** Ingestion de fichiers bruts sales (SAP, NetSuite, Sage), dénormalisation des fusions et réconciliation comptable stricte à somme nulle ($\Delta = 0.00$).
5. **Restructuration Structurelle :** Insertion ou suppression de lignes/colonnes avec décalage vectoriel automatique des formules via un parseur d'AST sans casser les références.
6. **Débogage de Formules & Graphe DAG :** Recherche immédiate de la cause racine d'une erreur en mémoire vive et calcul de sensibilité (Goal Seek).
7. **Serveur d'Outils MCP :** Fourniture d'outils tableur natifs à Claude Code, Cursor, OpenCode ou Antigravity via JSON-RPC stdio.

---

## 🏛️ Sommaire des 7 Piliers Consolidés

```text
                                  ┌───────────────────────────┐
                                  │      excel_master.py      │
                                  └─────────────┬─────────────┘
         ┌──────────────┬──────────────┬────────┼────────┬──────────────┬──────────────┐
         ▼              ▼              ▼        ▼        ▼              ▼              ▼
     [recalc]     [restructure]     [clean]  [model]  [debug]       [read/write]    [audit]
  (Zero-Error)      (AST Shift)    (Δ = 0.0)  (7 Mod)  (DAG)         (Atomic JSON)  (Visual UX)
                                       │
                                       ▼
                                     [mcp]
                        (Serveur MCP natif stdio)
```

1. [**Pilier 1 : Recalcul Headless & Intégrité OpenXML**](references/01_zero_error_recalculation_protocol.md)
   - Popule les valeurs en cache `<v>` via LibreOffice en mode headless.
   - Contrôle la double passe d'`openpyxl` (`data_only=False` pour les formules, `data_only=True` pour les valeurs).
   - Injecte les préfixes de namespace `_xlfn.` requis pour les fonctions post-2007 (`XLOOKUP`, `LET`, `LAMBDA`, `FILTER`, `UNIQUE`, `TEXTJOIN`, `IFS`).
2. [**Pilier 2 : Restructuration Déterministe par AST Tokenizer**](references/02_ast_reference_restructure_protocol.md)
   - Découpe chaque formule en arbre syntaxique (AST) et translate vectoriellement les coordonnées de cellules et de plages.
   - Ajuste automatiquement les plages de cellules fusionnées, les filtres automatiques et les tables.
3. [**Pilier 3 : Ingestion Dégradée & Réconciliation Mathématique $\Delta = 0.00$**](references/03_dirty_data_reconciliation_protocol.md)
   - Détection heuristique de la ligne d'en-tête (contourne les bannières et métadonnées).
   - Dénormalisation des fusions de catégories avec propagation vers le bas (*forward-fill*).
   - Coercition des devises et dates avec barrière de réconciliation stricte à somme nulle.
4. [**Pilier 4 : Modélisation Financière Institutionnelle (Pack Oria One)**](references/04_institutional_financial_modeling_matrix.md)
   - Code couleur Wall Street : Bleu (`#0000FF`) pour les inputs, Noir (`#000000`) pour les formules, Vert (`#008000`) pour les liaisons inter-feuilles.
   - 7 modèles prêts à l'emploi : `three_statement`, `dcf`, `lbo`, `saas_runway`, `debt_schedule`, `cap_table`, `working_capital`.
   - Ligne d'audit d'équilibrage de bilan obligatoire : `=Total_Actif - (Total_Passif + CP)` avec alerte conditionnelle.
5. [**Pilier 5 : Débogage par Graphe DAG & Goal Seek Numérique**](references/05_formula_dag_debugging_and_goal_seek.md)
   - Modélisation du classeur en Directed Acyclic Graph (antécédents et dépendants).
   - Remontée BFS en amont pour isoler la cellule exacte ayant introduit un `#VALUE!` ou `#DIV/0!`.
   - Résolveur de valeur cible inversée (Goal Seek) par méthode de sécante/dichotomie.
6. [**Pilier 6 : Micro-CLI Atomique JSON**](references/06_native_mcp_server_specification.md)
   - Lecture et écriture de matrices de données par notation A1 (`read`, `write`, `info`) sans overhead.
7. [**Pilier 7 : Passerelle MCP Native (Model Context Protocol)**](references/06_native_mcp_server_specification.md)
   - Démarrage stdio pour brancher les outils tableur directement dans les agents modernes sans configuration complexe.

---

## 🛠️ Matrice de Décision & Dispatcher CLI (`excel_master.py`)

Tous les outils sont regroupés dans l'exécutable unique : `scripts/excel_master.py`.

| Requête / Intention Utilisateur | Commande CLI à Exécuter |
| :--- | :--- |
| **"Vérifie que mon fichier n'a aucune erreur de formule"** | `python scripts/excel_master.py recalc <fichier.xlsx>` |
| **"Insère 3 lignes à la ligne 5 sans casser les formules"** | `python scripts/excel_master.py restructure <fichier.xlsx> --sheet "P&L" --action insert --axis row --index 5 --count 3` |
| **"Nettoie cet export comptable sale"** | `python scripts/excel_master.py clean <dirty.xlsx> --out <clean.xlsx>` |
| **"Génère un modèle 3-Statement équilibré"** | `python scripts/excel_master.py model --type three_statement --out 3statement.xlsx` |
| **"Génère une valorisation DCF complète"** | `python scripts/excel_master.py model --type dcf --out dcf.xlsx` |
| **"Génère un montage LBO avec dette"** | `python scripts/excel_master.py model --type lbo --out lbo.xlsx` |
| **"Génère une table de capitalisation de startup"** | `python scripts/excel_master.py model --type cap_table --out cap_table.xlsx` |
| **"Génère un tableau d'amortissement de dette"** | `python scripts/excel_master.py model --type debt_schedule --out debt.xlsx` |
| **"Génère un modèle de BFR et cycle du cash"** | `python scripts/excel_master.py model --type working_capital --out bfr.xlsx` |
| **"Trouve d'où vient l'erreur dans la cellule E10"** | `python scripts/excel_master.py debug <fichier.xlsx> --trace-error "'Feuil1'!E10"` |
| **"Vérifie la mise en page (volets figés, largeurs ###)"** | `python scripts/excel_master.py audit <fichier.xlsx>` |
| **"Démarre le serveur MCP pour Claude/Cursor"** | `python scripts/excel_master.py mcp` |

---

## 📁 Structure Ordonnée du Répertoire

```text
mega-excel-master-suite/
├── SKILL.md                                                ← Ce document d'orchestration
├── scripts/
│   └── excel_master.py                                     ← Moteur unifié, CLI & Serveur MCP
└── references/
    ├── 01_zero_error_recalculation_protocol.md             ← Protocole LibreOffice, cache <v> & _xlfn.
    ├── 02_ast_reference_restructure_protocol.md            ← Algorithme de translation vectorielle AST
    ├── 03_dirty_data_reconciliation_protocol.md            ← Heuristiques d'ingestion & barrière Δ=0.00
    ├── 04_institutional_financial_modeling_matrix.md      ← Spécifications des 7 modèles financiers
    ├── 05_formula_dag_debugging_and_goal_seek.md          ← Graphe DAG & solveur de valeur cible
    └── 06_native_mcp_server_specification.md              ← Spécification des outils MCP JSON-RPC
```
