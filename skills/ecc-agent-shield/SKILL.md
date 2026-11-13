---
name: ecc-agent-shield
description: >-
  Agent harness security gate and continuous learning engine inspired by affaan-m/ECC (Everything Claude Code). Intercepts and blocks destructive terminal commands (AgentShield) and automatically synthesizes resolved debugging sessions into persistent agent instinct rules (.agent/instincts/*.md).
version: 1.0.0
tags:
  - agent-shield
  - safety-gate
  - continuous-learning
  - instincts
  - ecc
---

# 🛡️ ECC AgentShield: Execution Safety Gate & Continuous Learning

> **Inspiration :** Affaan Mustafa (`affaan-m/ECC` - Everything Claude Code)  
> **Axiome Central :** L'agent doit disposer d'un bouclier déterministe pré-exécution pour interdire les catastrophes système (`rm -rf`, écrasements aveugles) et d'un mécanisme de mémorisation permanente (*Instincts*) pour ne jamais répéter deux fois la même erreur.

---

## 🔒 Les Deux Modules Clés

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. AGENT SHIELD: Linter temps réel des commandes shell      │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. INSTINCT ENGINE: Compilation des bugs résolus en règles  │
 └─────────────────────────────────────────────────────────────┘
```

---

## 💻 Utilisation CLI

```bash
# Vérifier si une commande shell est sûre avant de l'exécuter
python skills/ecc-agent-shield/scripts/agent_shield.py audit-cmd --cmd "rm -rf /var/log"
# Sortie: BLOCKED: Destructive command pattern 'rm -rf /' detected!

# Compiler une leçon apprise lors d'un bug en instinct permanent
python skills/ecc-agent-shield/scripts/agent_shield.py learn-instinct \
  --title "SQLite WAL Lock Prevention" \
  --trigger "sqlite3.OperationalError: database is locked" \
  --rule "Toujours positionner busy_timeout=5000 et pragma journal_mode=WAL dès l'ouverture de la connexion."
```
