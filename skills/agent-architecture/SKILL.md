---
name: agent-architecture
description: 'Design AI agent architectures through requirements discovery, or audit and diagnose architectural flaws in existing agents. Architecture only; excludes implementation and general code review.'
license: MIT
metadata:
  version: "2.0"
  enhancements:
    - Scaffolder for production-grade agent architectures with Mermaid topologies
    - Static diagnostic auditor for the 10 Golden Architectural Invariants
    - Automated contract validator for the 7 deliverable views
    - Native pur-Python WAT toolkit with full automated unit test suite
---

# 🏛️ AI Agent Architecture Engineering & Invariants

> **Standard :** Antigravity Agent Architecture Standard & Contract v2.0  
> **Core Axiom :** *"An ideal agent architecture does not maximize the number of components or LLM loops. It minimizes stochastic exposure by enforcing strict deterministic boundaries, hard operational limits, and typed tool contracts."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Créer un agent IA, beaucoup de gens pensent que c'est juste :
*"Je prends un modèle comme Claude ou GPT, je lui donne 50 outils, je le mets dans une boucle `while(true)` et je lui dis d'être gentil et de faire attention aux erreurs dans son prompt."*

**Résultat en production :** Catastrophe garantie !
- L'agent tourne en boucle infinie et te facture \$500 en une nuit.
- L'agent hallucine qu'il a le droit de supprimer la base de données parce qu'aucune barrière déterministe en code ne l'en empêche.
- Dès que le réseau coupe pendant 2 secondes, l'agent renvoie 10 fois le même paiement par carte bancaire parce qu'il ne connaît pas la notion d'idempotence.

L'**architecture d'agent**, c'est l'art de construire une véritable forteresse d'ingénierie autour du modèle :
1. **Un garde du corps à l'entrée** qui nettoie les requêtes et bloque les attaques.
2. **Un compteur d'étapes impitoyable** en pur code qui coupe l'agent s'il dépasse 10 actions ou \$0.50 de budget.
3. **Un juge déterministe** qui vérifie les permissions AVANT que l'outil ne soit exécuté (on ne demande pas poliment à l'IA de ne pas tricher, on lui coupe l'accès si c'est interdit).
4. **Des outils typés et idempotents** avec des clés uniques pour qu'une action ne soit jamais exécutée deux fois par erreur.

---

## 🧭 2. Les 5 Topologies d'Agents en Production

| Topologie | Cas d'Usage Idéal | Latence | Coût Token | Autonomie |
| :--- | :--- | :---: | :---: | :---: |
| **Workflow Déterministe** | Tâches linéaires sans ambiguïté | ⚡ Très Faible | 🟢 Minimal | ❌ Nulle (0% risque) |
| **Router-Worker** | Triage d'intentions variées vers spécialistes | ⚡ Faible | 🟢 Bas | 🟡 Modérée |
| **Single-Agent ReAct Loop** | Exploration ciblée, recherche avec outils | ⏱️ Moyenne | 🟡 Modéré | 🟢 Élevée (Bornée) |
| **Orchestrator-Workers** | Décomposition de problèmes complexes | ⏳ Élevée | 🔴 Élevé | 🚀 Maximale |
| **Evaluator-Optimizer** | Génération de code critique ou preuves | ⏳ Élevée | 🔴 Élevé | 🟢 Auto-corrigé |

---

## 🛡️ 3. Les 10 Invariants Architecturaux d'Or

1. **Défense contre Boucle Infinie (`INV-01`)** : Limite stricte de pas (`max_steps` hard) et disjoncteur de boucle.
2. **Timeout Global de Tâche (`INV-02`)** : Watchdog indépendant coupant l'exécution après $N$ secondes.
3. **Plafond Financier & Budgétaire (`INV-03`)** : Seuil maximal en dollars (\$ USD) ou tokens par tâche.
4. **Frontière Déterministe (`INV-04`)** : Permissions et sécurités vérifiées en code/runtime, jamais dans le prompt LLM.
5. **Idempotence des Mutations (`INV-05`)** : Clés d'idempotence obligatoires et gestion de l'état `EFFECT_UNKNOWN`.
6. **Prévention de l'Engorgement (`INV-06`)** : Jamais plus de 15 outils déversés dans un même prompt; privilégier le routage.
7. **Isolation & Compaction (`INV-07`)** : Gestion du contexte long par compactage sans jamais stocker de secrets dans l'historique.
8. **Défense contre les Injections (`INV-08`)** : Cloisonnement strict des données non fiables via balises XML et passerelle d'entrée.
9. **Sandboxing d'Exécution (`INV-09`)** : Isolation étanche des environnements de code/bash/navigateur.
10. **Escalade Humaine (`INV-10`)** : File d'attente humaine pour les actions irréversibles ou critiques.

---

## 🛠️ 4. La Boîte à Outils WAT Déterministe

La compétence embarque 3 outils déterministes natifs en Python standard (sans dépendances externes) :

### 🏛️ A. Échafaudeur d'Architecture d'Agent (`scaffold_agent_architecture.py`)
Génère une spécification d'architecture d'agent complète conforme aux 7 vues contractuelles avec diagrammes Mermaid (`flowchart TD` et `sequenceDiagram`) :
```bash
python scripts/scaffold_agent_architecture.py \
  --name "SecurityTriager" \
  --role "Trier les alertes de sécurité CVE et proposer des correctifs" \
  --topology "router_worker" \
  --tools "cve_lookup,git_diff,post_slack" \
  --max-steps 10 \
  --budget-usd 0.50 \
  --output AGENT_ARCHITECTURE.md
```

### 🔍 B. Auditeur Statique des 10 Invariants (`audit_agent_design.py`)
Analyse un document d'architecture, un prompt système ou une configuration d'agent pour détecter les faiblesses structurelles (absence de timeout, boucles infinies potentielles, sécurité confiée au prompt) et calcule un Score de Préparation (0-100) :
```bash
python scripts/audit_agent_design.py AGENT_ARCHITECTURE.md
python scripts/audit_agent_design.py AGENT_ARCHITECTURE.md --json
```

### 🛡️ C. Validateur du Contrat d'Architecture (`validate_agent_architecture.py`)
Vérifie la conformité formelle d'un document aux 7 vues obligatoires du contrat :
```bash
python scripts/validate_agent_architecture.py AGENT_ARCHITECTURE.md
```

---

## 📋 5. Choix de la Route d'Ingénierie

| Demande Utilisateur | Route | Références Clés |
|---|---|---|
| Nouvel agent, exigences non stabilisées | **Design** : Cas d'usage $\to$ ébauche $\to$ contrat $\to$ livraison | [design.md](references/design.md), [architecture-contract.md](references/architecture-contract.md) |
| Architecture depuis spécification existante | **Design direct** : Compléter le connu, clarifier les écarts | [architecture-contract.md](references/architecture-contract.md) |
| Revoir un agent existant en production | **Audit** : Reconstruire les flux réels $\to$ vérifier $\to$ livrer | [audit.md](references/audit.md), [diagnostic-review.md](references/diagnostic-review.md) |
| Agent qui dérive ou déclare faussement "terminé" | **Diagnostic approfondi** : Hypothèses $\to$ tests discriminants | [diagnostic-review.md](references/diagnostic-review.md) |

---

## 📚 6. Références et Guides Embarqués

- 📖 [Playbook d'Architecture & Invariants d'Agent](references/agent_architect_reference_playbook.md)
- 📜 [Contrat des Livrables d'Architecture (7 Vues)](references/architecture-contract.md)
- 🧭 [Sélection de Topologie & Interaction Temporelle](references/architecture-selection.md)
- 🔎 [Protocole de Découverte & Questions d'Interview](references/discovery-protocol.md)
- ⚖️ [Évaluation & Qualité Opérationnelle](references/evaluation-design.md)
- ⏱️ [Continuité d'Exécution, Pauses & Reprise](references/execution-continuity.md)
- 🔬 [Revue Diagnostique & Analyse des Causes Racines](references/diagnostic-review.md)
