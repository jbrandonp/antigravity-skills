# Zone : Calendar (Google + Outlook)

## Sub-features
Lecture agenda, création/édition d'events (avec validation), RSVP.

## How to get to it
- Google : `google_calendar_search`, `google_calendar_agenda`
- Outlook : `mcp__ms365__get_calendar_view`, `list_calendar_events`

## Driving it
Création d'event → RELIRE l'event créé (`get_calendar_event`) et vérifier heures/fuseau (Europe/Brussels).

## Gotchas
- OAuth Google configuré pour Gmail ; Calendar peut nécessiter un scope supplémentaire (voir 10-CEO/Connecteurs-n8n-CEO.md).
- Fuseau : CET/CEST — toujours vérifier l'heure réellement enregistrée.