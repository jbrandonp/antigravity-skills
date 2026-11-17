---
name: watchtower-presse-2
description: Watch Tower - veille business. Surveille 15+ sources business (WSJ, NYT, The Information, TechAltar, Bloomberg, Reuters, etc.) via `web_search` + `web_extract`. Utilisez ce skill quand l'utilisateur demande une veille economique, financiere ou business.
---

# Watch Tower - Presse 2 (Business)

## Mission

Scanner **15+ sources business / economie** et produire un rapport structure des articles recents (<= 7 jours). Utilise `web_search` + `web_extract` - jamais de navigateur.

## Sources (15)

| # | Source | URL | Strategie |
|---|--------|-----|-----------|
| 1 | Wall Street Journal | https://wsj.com | `web_search site:wsj.com` |
| 2 | The New York Times | https://nytimes.com | `web_search site:nytimes.com` |
| 3 | The Information | https://theinformation.com | `web_search site:theinformation.com` |
| 4 | TechAltar | https://youtube.com/@techaltar | `web_search site:youtube.com/@techaltar` |
| 5 | Bloomberg | https://bloomberg.com | `web_search site:bloomberg.com` |
| 6 | Reuters | https://reuters.com | `web_search site:reuters.com` |
| 7 | Financial Times | https://ft.com | `web_search site:ft.com` |
| 8 | The Economist | https://economist.com | `web_search site:economist.com` |
| 9 | CNBC | https://cnbc.com | `web_search site:cnbc.com` |
| 10 | Business Insider | https://businessinsider.com | `web_search site:businessinsider.com` |
| 11 | Forbes | https://forbes.com | `web_search site:forbes.com` |
| 12 | Harvard Business Review | https://hbr.org | `web_search site:hbr.org` |
| 13 | Stratechery | https://stratechery.com | `web_search site:stratechery.com` |
| 14 | Axios | https://axios.com | `web_search site:axios.com` |
| 15 | Semafor | https://semafor.com | `web_search site:semafor.com` |


## Workflow

1. **Pour chaque source**, lancer `web_search(query, limit=5)`
2. **Extraire** les URLs avec `web_extract(urls, char_limit=8000)`
3. **Filtrer** : garder < 7 jours
4. **Dedupliquer** : garder la source la plus fiable
5. **Signaler les paywalls** : marquer (paywall) si extraction bloquee

## Format de sortie

Rapport Markdown avec 3 niveaux : Impact majeur (rouge), Tendance (jaune), Information (gris).

## Regles

- Toujours inclure le lien complet
- Jamais de resume sans extraction - marquer (paywall - titre seulement)
- Privilegier l'angle business/impact sur le technique pur
- Signaler les articles exclusifs (scoop, analyse Stratechery, edito FT)
- Max 20 articles par rapport
