# Index feature map — zones BRANDON AI

Une zone = un fichier. L'agent ouvre UN fichier par changement (token-efficace). Ordre de sweep de haut en bas après toute modification structurelle.

Prérequis baseline : `/srv/brandon-ai/workspaces/health-check.sh` passe sans erreur avant tout test.

| # | Zone | Fichier |
|---|---|---|
| 1 | Email | email.md |
| 2 | Calendar | calendar.md |
| 3 | Browser | browser.md |
| 4 | Vault Obsidian | vault.md |
| 5 | Git | git.md |
| 6 | LiteLLM | litellm.md |
| 7 | PostgreSQL | postgresql.md |
| 8 | n8n | n8n.md |
| 9 | Dashboard Hermes | dashboard.md |
| 10 | Crons Hermes | crons.md |

Rapport de sweep : OK / ÉCHEC / INATTEIGNABLE (raison) par zone.