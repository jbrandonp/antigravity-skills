# Zone : Browser (browser_exec)

## Sub-features
Navigation, fetch JS, captures, appels API externes quand curl/execute_code sont bloqués.

## How to get to it
- Outil `browser_exec` (session persistante, helpers js/fill_input/click_at_xy).

## Driving it
Un fetch est prouvé par le contenu retourné (status + body parsé), pas par l'absence d'erreur.

## Gotchas
- Exfilbar bloque execute_code vers localhost/unknown — browser_exec est le contournement officiel.
- Ne jamais coller de secrets dans les URLs/fetch du navigateur.