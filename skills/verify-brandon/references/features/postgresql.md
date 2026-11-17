# Zone : PostgreSQL

## Sub-features
Bases : `brandon_ai` (données système, traces, watchtower), `litellm` (spend). MCP postgres en READ ONLY strict.

## How to get to it
- MCP : `mcp__postgres__query` (transaction READ ONLY — ne JAMAIS tenter d'INSERT par ce canal).
- Console : `sudo -u postgres psql` sur le serveur.

## Driving it
Après tout changement de schéma : relire la structure (`\d table` ou list_tables) pour vérifier l'effet réel.

## Gotchas
- Écriture via MCP = verrouillé par design ; l'écriture passe par psql/terminal UNIQUEMENT pour les migrations légitimes.
- Ne jamais exécuter de SQL destructeur sans validation explicite de Brandon.
- RAM serrée : éviter les gros scans sur la VM (7,5 Go).