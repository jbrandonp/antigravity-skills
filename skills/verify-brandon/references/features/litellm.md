# Zone : LiteLLM

## Sub-features
Proxy LLM (port 4000, localhost), routage multi-modèles avec fallback, budgets.

## How to get to it
- Config : `/home/arthur/.litellm/config.yaml` (config.yaml, pas Hermes)
- Env : `/home/arthur/.litellm/litellm.env` (master key + API key — JAMAIS citer)
- Test : `/v1/models` et `/v1/chat/completions` via browser_exec (execute_code bloqué sur 127.0.0.1).

## Driving it
Après tout changement de config : kill des process litellm existants, relance AVEC `set -a && . ~/.litellm/litellm.env && set +a`, attendre le boot (les migrations Prisma prennent 1-2 min, CPU élevé = normal), puis test completion réel.

## Gotchas
- Le boot sans env vars chargées = auth 401 pour les clients.
- extra_body/provider.order dans litellm_params = boot en boucle (testé 17/11) → ne pas utiliser.
- Kill d'un process litellm ne tue pas toujours son worker → vérifier `ss -tlnp` après.