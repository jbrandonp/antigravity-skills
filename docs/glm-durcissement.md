---
title: "Playbook — Durcissement GLM 5.3 Flash (adapté à la stack OpenRouter)"
tags: [glm, durcissement, garde-fous, fiabilite]
date: 2026-11-17
---

# Durcissement GLM 5.3 Flash — ce qui s'applique chez nous

> Source : analyse externe (Brandon, 17/11) sur les faiblesses de GLM (revue à l'aveugle, sur-raisonnement, boucles en session longue). **Cette stack passe par OpenRouter, pas par vLLM auto-hébergé** — plusieurs réglages de l'analyse (tool_call_parser, chat_template_kwargs, en-têtes de serveur) ne nous concernent pas. Voici le mapping complet.

## ✅ Déjà en place (vérifié 17/11)

| Garde-fou recommandé | Notre équivalent | État |
|---|---|---|
| Tool Spin Guard (appels d'outils en boucle) | `tool_loop_guardrails` Hermes : warn après 2-3 échecs identiques, **hard-stop après 5-8 en session non-interactive (crons)** | ✅ actif |
| Compaction automatique du contexte | Compression Hermes intégrée (75 %→résumé) | ✅ natif |
| Validation en deux passes | quality-auditor (Bot Chat) + skill `verify-brandon` (proof bar) | ✅ en place |
| Effort de raisonnement par type de tâche | `reasoning_effort: medium` (global) ; décisions routées vers Jev (effort fixe) | ✅ équilibré |
| Boucle de rétroaction humaine | Brandon valide tout envoi/dépense ; revue hebdo quality-auditor | ✅ |

## ✅ Applicable via OpenRouter (testé en réel)

| Réglage | Test | Verdict |
|---|---|---|
| `repetition_penalty: 1.1` | Accepté par OpenRouter, réponse identique correcte | ✅ disponible — à ajouter dans les appels longs si boucles observées |
| `reasoning_effort` (low/high) | Fonctionne (testé via Jev et GLM) | ✅ disponible à la requête |
| `max_tokens` suffisant | Observé en test : <100 tokens → content vide (budget mangé par le raisonnement) | ⚠️ ne jamais demander des réponses GLM avec max_tokens < ~300 |

## ❌ Non applicable (self-hosting vLLM uniquement)

- `tool_call_parser: glm47` / `glm_xml` — paramètre de serveur vLLM/SGLang, pas d'OpenRouter
- `clear_thinking` via `chat_template_kwargs` — pareil ; l'équivalent chez nous : la compaction Hermes + le fait que OpenRouter ne rejoue pas le raisonnement entre appels
- En-têtes `x-posthog-mcp-mode` — spécifique à une pile MCP dédiée
- `tool_choice: "required"` — utile à la demande pour forcer un appel d'outil précis, pas un réglage permanent

## Métriques à surveiller (mêmes que l'analyse, adaptées)

| Métrique | Comment la mesurer ici | Seuil d'alerte |
|---|---|---|
| Réponses vides (content="") | Relecture des runs cron (status ok mais livrable vide) | > 1/run |
| Boucles d'outils | Compteur `tool_loop_guardrails` (warnings dans les logs Hermes) | hard-stop déclenché |
| **Dérive qualité (canari)** | **Cron quotidien `b85500681cad` 06:45 — 3 questions-canari à GLM via LiteLLM, jugées par Jev (noul) ; silencieux si OK, alerte Telegram si échec** | ≥ 1 canari échoué |
| Dérive qualité (humain) | Cron hebdo continual-learning + revue quality-auditor du dimanche | correction répétée de Brandon |

**Coût du drift check : ~$0.000085/jour** (3 canari : réponse GLM ~$0.00004 + jugement Jev ~$0.00004). Premier run : 18/11 06:45.

## Règle de décision modèle (encodée 17/11)

- **GLM 5.3 Flash** : tout le chat, génération, analyse, code.
- **Jev 1.14** : tout le décisionnel typé (triage, classification, gating) via `jev-decide.py` / `jev-filter.py`.
- Décisions critiques (argent, envoi, sécurité) : **jamais** de décision purement Jev ou GLM seul — validation Brandon ou règle déterministe.
