# Zone : Crons Hermes

## Sub-features
Jobs planifiés Hermes (briefing 07:30, résumé 21:00, bilan hebdo dim 19:00, sécurité dim 18:00, continual learning dim 19:30, watchtower 7h/12h/18h). Paused : veille BTP/concurrentielle/prospection.

## How to get to it
- CLI : `hermes cron list` / `hermes cron runs <id>`.
- MCP : `cronjob_manage` (list/create/update/pause/resume/remove/run).

## Driving it
Après création/modification : `cronjob_manage action=list` pour VÉRIFIER la schedule réellement enregistrée (next_run_at cohérent). Test d'un job : action=run puis vérifier la sortie.

## Gotchas
- `action=disable` n'existe pas → utiliser `pause`.
- Les jobs tournent sur le modèle principal du moment (sauf pinned) — un changement de modèle les affecte.
- Coût : chaque job consomme des tokens OpenRouter — annoncer le coût d'une nouvelle récurrence avant de la créer (règle autonomie-avec-garde-fous).
- Install lock Hermes bloquant (11/11) peut faire échouer les crons — vérifier si échecs en masse.