---
name: ai-redteaming-adversarial-security-suite
description: >-
  Advanced AI Red-Teaming, LLM Jailbreak Auditing & Adversarial Robustness Suite: G0DM0D3 attack simulation, Parseltongue 33-technique input obfuscation, ULTRAPLINIAN multi-model racing, encoding escalation (Base64, Hex, Leetspeak, Rot13), refusal detection heuristics, and Hermes-native prefill/system prompt integration.
version: 3.0.0
tags:
  - red-teaming
  - ai-security
  - jailbreak-testing
  - parseltongue
  - godmode
  - refusal-detection
  - adversarial-robustness
  - llm-safety
merged_member_skills:
  - godmode (01_Hermes_Skills_Core_Library\red-teaming\godmode\SKILL.md)
---

# AI Red-Teaming & Adversarial Security Suite

> **Master Suite Consolidée :** Suite d'audit de sécurité offensive et d'évaluation de la robustesse des modèles de langage (LLMs) face aux attaques par contournement de filtres, injections de prompts adverses et évasions de garde-fous.

## 🎯 Quand Déclencher cette Master Suite (Triggers)
- L'utilisateur demande d'évaluer la robustesse d'un LLM face aux attaques par jailbreak ou prompt injection.
- L'utilisateur souhaite tester les filtres de sécurité d'un modèle via des techniques d'obfuscation (Parseltongue, ULTRAPLINIAN).
- L'utilisateur effectue un audit de sécurité adverse (AI Red-Teaming / Alignment Stress-Testing).
- L'utilisateur recherche des heuristiques d'analyse de refus ou de contournement de garde-fous.

---

## 🛠️ Outils & Scripts Déterministes Embarqués

### 1. `scripts/godmode_parseltongue.py`
Obfuscateur multi-niveaux implémentant 33 techniques de mutation de prompt (encodages mixtes, homoglyphes, structures logiques imbriquées).
```bash
python scripts/godmode_parseltongue.py --technique auto --prompt "Test prompt"
```

### 2. `scripts/godmode_auto_jailbreak.py`
Boucle automatisée d'escalade adverse multi-tours pour identifier les vecteurs de contournement de filtres.

### 3. `scripts/godmode_godmode_race.py`
Moteur ULTRAPLINIAN de course multi-modèles pour comparer la résistance de différents LLMs face à un même prompt adverse.

### 4. `scripts/godmode_load_godmode.py`
Chargeur de templates et profils d'audit adverse.

---

## 📚 Références Techniques & Guides d'Audit

- **[`references/godmode_jailbreak-templates.md`](references/godmode_jailbreak-templates.md)** : Bibliothèque de templates d'attaque adverse classifiés par vecteur.
- **[`references/godmode_refusal-detection.md`](references/godmode_refusal-detection.md)** : Heuristiques et expressions régulières de détection des réponses de refus standardisé.

---

## 📋 Directives Éthiques & Pratiques de Sécurité
Cette suite est conçue pour l'audit de robustesse défensif et la recherche en sécurité IA (Blue Teaming & Red Teaming légal). Toute utilisation doit respecter les politiques de sécurité applicables et les normes de divulgation responsable.
