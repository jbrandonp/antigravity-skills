# Zone : n8n

## Sub-features
Automatisations (localhost:5678/5679, v2.35.7, ~308 connecteurs, PID ~1277).

## How to get to it
- UI : http://127.0.0.1:5678 (webhook/test via browser_exec si besoin).
- Docker : containers n8n sous /srv (vérifier `docker ps`).

## Driving it
Après toute modification de workflow : exécuter le workflow en mode test et vérifier l'OUTPUT réel (données produites), pas juste « workflow executed ».

## Gotchas
- Gmail digest remplacé par crons Hermes (14/11) — ne pas recréer de doublon.
- Scopes OAuth Google : Gmail OK, Calendar peut nécessiter scope supplémentaire.
- Ne jamais déclencher un workflow qui envoie un e-mail sans validation du texte exact.