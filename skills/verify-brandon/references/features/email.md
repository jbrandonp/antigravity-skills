# Zone : Email (Gmail + Outlook)

## Sub-features
Lecture, recherche, brouillons (Gmail/Outlook). AUCUN envoi sans validation du texte exact par Brandon.

## How to get to it
- Gmail : `google_gmail_search`, `google_gmail_read` (plugin Google Workspace)
- Outlook : `mcp__ms365__list_mail_folder_messages`, `mcp__ms365__get_mail_message`

## Driving it
Vérification d'un envoi : après création d'un brouillon → RELIRE le brouillon via l'API de lecture (effet de bord), jamais se fier au 200 de création.

## Gotchas
- Envoi bloqué par règle absolue (validation Brandon requise, texte exact).
- Exfilbar bloque certaines routes execute_code → passer par browser_exec ou les MCP tools.