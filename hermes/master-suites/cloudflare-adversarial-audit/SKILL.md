---
name: cloudflare-adversarial-audit
description: >-
  Cloudflare 6-phase security auditing protocol with mandatory adversarial falsification. Prohibits the discovering agent from validating its own findings; requires an independent skeptic verifier agent to actively attempt to disprove/break candidate vulnerabilities before writing to findings.json.
version: 1.0.0
tags:
  - cloudflare
  - security-audit
  - adversarial-testing
  - vulnerability-triage
  - zero-false-positives
---

# 🛡️ Cloudflare Adversarial Security Audit Gate

> **Inspiration :** Cloudflare AI Security Research (`cloudflare/security-audit-skill`).  
> **Axiome Central :** Les LLMs hallucinent des failles imaginaires. **L'agent qui découvre une vulnérabilité potentielle n'a PAS le droit de la valider.** Seul un second agent vérificateur distinct, jouant le rôle d'avocat du diable, doit tenter activement de démolir la preuve avant toute confirmation.

---

## 🔬 Le Cycle d'Audit en 6 Phases

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ Phase 1: Reconnaissance (Frontières de confiance & surfaces)│
 ├─────────────────────────────────────────────────────────────┤
 │ Phase 2: Hunting (Sous-agents traqueurs en parallèle)       │
 ├─────────────────────────────────────────────────────────────┤
 │ Phase 3: Validation Adversariale (L'avocat du diable teste) │
 ├─────────────────────────────────────────────────────────────┤
 │ Phase 4: Enregistrement Structuré (findings.json strict)    │
 ├─────────────────────────────────────────────────────────────┤
 │ Phase 5: Re-vérification des Lignes & Schémas               │
 ├─────────────────────────────────────────────────────────────┤
 │ Phase 6: Rapport Définitif (REPORT.md & FINDINGS-DETAIL.md) │
 └─────────────────────────────────────────────────────────────┘
```

---

## 📋 La Règle Inviolable d'Indépendance

Pour chaque vulnérabilité candidate :
1. **L'Agent A (Hunter)** isole le fichier, la ligne suspecte, la classe CWE et formule une hypothèse d'exploit.
2. **L'Agent B (Adversarial Verifier)** reçoit le cas sans avoir accès aux conclusions subjectives de l'Agent A. Sa mission est d'essayer de **prouver que la faille est impossible à exploiter** (ex: assainissement amont, validation de type, barrière réseau).
3. **Verdict Déterministe** :
   - Si l'Agent B parvient à exécuter l'exploit ou à contourner la défense ➔ La faille est **VALIDÉE** et signée par les deux agents.
   - Si l'Agent B démontre que l'exploit échoue ou est bloqué ➔ La faille est **REJETÉE** comme faux positif.

---

## 🛠️ Outil de Validation du Schéma & Compilation de Rapport

```bash
# Vérifier et filtrer les vulnérabilités validées contradictoirement
python skills/cloudflare-adversarial-audit/scripts/adversarial_gate.py --findings findings.json --report REPORT.md
```
