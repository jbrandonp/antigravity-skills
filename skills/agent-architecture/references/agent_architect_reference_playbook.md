# 🏛️ AI Agent Architecture Engineering & Invariants Playbook

> **Standard :** Antigravity Agent Architecture Standard v2.0  
> **Core Axiom :** *"An ideal agent architecture does not maximize the number of components or LLM loops. It minimizes stochastic exposure by enforcing strict deterministic boundaries, hard operational limits, and typed tool contracts."*

---

## 🧭 1. Matrice des 5 Topologies d'Agents en Production

| Topologie | Cas d'Usage Idéal | Latence | Coût Token | Autonomie | Risque de Dérive |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Workflow Déterministe** | Tâches linéaires sans ambiguïté | ⚡ Très Faible | 🟢 Minimal | ❌ Nulle | 🟢 0% (Déterministe) |
| **Router-Worker** | Triage d'intentions variées vers spécialistes | ⚡ Faible | 🟢 Bas | 🟡 Modérée | 🟢 Faible |
| **Single-Agent ReAct Loop** | Exploration ciblée, recherche avec outils | ⏱️ Moyenne | 🟡 Modéré | 🟢 Élevée | 🟡 Bounded Loop |
| **Orchestrator-Workers** | Décomposition de problèmes complexes | ⏳ Élevée | 🔴 Élevé | 🚀 Maximale | 🟠 Risque de désynchronisation |
| **Evaluator-Optimizer** | Génération de code critique ou preuves | ⏳ Élevée | 🔴 Élevé | 🟢 Haute | 🟢 Auto-corrigé |

---

## 🛡️ 2. Les 10 Invariants Architecturaux d'Or

Tout système d'agent autonome prêt pour la production **doit** satisfaire ces 10 invariants :

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Défense contre Boucle Infinie (Max N itérations hard)   │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Timeout Global de Tâche (Watchdog indépendant)          │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Plafond Financier & Budgétaire Strict ($ USD / Tokens)   │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Frontière Déterministe (Politique en Code, jamais Prompt)│
 ├─────────────────────────────────────────────────────────────┤
 │ 5. Idempotence des Mutations & Gestion de l'Incertitude     │
 ├─────────────────────────────────────────────────────────────┤
 │ 6. Prévention de l'Engorgement d'Outils (Max 15 outils/LLM) │
 ├─────────────────────────────────────────────────────────────┤
 │ 7. Isolation de Mémoire & Compaction Contextuelle           │
 ├─────────────────────────────────────────────────────────────┤
 │ 8. Défense contre les Injections de Prompt (Zero-Trust)     │
 ├─────────────────────────────────────────────────────────────┤
 │ 9. Isolation d'Exécution & Sandboxing (Docker / gVisor)     │
 ├─────────────────────────────────────────────────────────────┤
 │ 10. Escalade Humaine (Human-in-the-Loop sur effets majeurs) │
 └─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ 3. Les 4 Fonctions de l'Environnement Runtime

Un agent ne doit jamais interagir directement avec des API externes sans passer par les 4 fonctions d'environnement :

1. **Translation (Traduction)** :
   - Transforme l'instruction utilisateur en contexte typé.
   - Injecte les autorisations vérifiées du tenant/utilisateur.
2. **Execution (Exécution)** :
   - Exécute l'action dans un sandbox isolé.
   - Enforce les quotas, la liste blanche des domaines réseau et les permissions.
3. **Observation (Observation)** :
   - Capture la réponse brute de l'outil.
   - Tronque les réponses gigantesques (évite l'explosion du contexte) et masque les PII.
4. **Correction (Correction)** :
   - En cas d'erreur ou d'état `EFFECT_UNKNOWN`, détermine si un retry borné est licite ou s'il faut escalader à l'opérateur humain.

---

## 🛠️ 4. Boîte à Outils WAT de la Compétence

### A. Échafauder une Architecture Conforme
```bash
python scripts/scaffold_agent_architecture.py \
  --name "SecurityTriager" \
  --role "Trier les alertes de sécurité CVE et proposer des correctifs" \
  --topology "router_worker" \
  --tools "cve_lookup,git_diff,post_slack" \
  --output AGENT_ARCHITECTURE.md
```

### B. Auditer un Design contre les 10 Invariants
```bash
python scripts/audit_agent_design.py AGENT_ARCHITECTURE.md
```

### C. Valider le Contrat Documentaire (7 Vues)
```bash
python scripts/validate_agent_architecture.py AGENT_ARCHITECTURE.md
```
