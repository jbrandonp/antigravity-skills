# Zone : Dashboard Hermes

## Sub-features
Dashboard web (port 9119, 127.0.0.1), basic_auth user `brandon`, multi-profil (12 profils).

## How to get to it
- Local : http://127.0.0.1:9119 (auth basic, mot de passe dans ~/.dashboard-password — JAMAIS citer).
- Lancé par : `hermes dashboard --host 0.0.0.0 --port 9119 --no-open` (background).

## Driving it
Après tout changement : vérifier le process (PID, LISTEN via `ss -tlnp`) ET une requête HTTP réelle (curl local en bash, pas execute_code).

## Gotchas
- Accès public BLOQUÉ : le pare-feu Hetzner ne laisse pas passer 9119 malgré la règle inbound (non confirmé côté console — diagnostic par élimination). Tunnel SSH = alternative reportée.
- GUARDIAN peut lever une fausse alerte « plafond de redémarrages » après des kill -9 de tests — faux positif connu.