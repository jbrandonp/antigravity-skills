---
name: watchtower-presse-1
description: Watch Tower - veille technologique. Surveille 15+ sources tech (Ars Technica, The Verge, Mashable, TechCrunch, Vox, VentureBeat, WIRED, etc.) via `web_search` + `web_extract`. Utilisez ce skill quand l'utilisateur demande un scan des actualites tech, une veille concurrentielle, ou un rapport des dernieres news tech.
---

# Watch Tower - Presse 1 (Tech)

## Mission

Scanner **15+ sources technologiques** et produire un rapport structure des articles recents (<= 7 jours). Utilise `web_search` + `web_extract` - jamais de navigateur.

## Sources (15)

| # | Source | URL | Strategie |
|---|--------|-----|-----------|
| 1 | Ars Technica | https://arstechnica.com | `web_search site:arstechnica.com` |
| 2 | The Verge | https://theverge.com | `web_search site:theverge.com` |
| 3 | Mashable | https://mashable.com | `web_search site:mashable.com` |
| 4 | TechCrunch | https://techcrunch.com | `web_search site:techcrunch.com` |
| 5 | Vox | https://vox.com | `web_search site:vox.com` |
| 6 | VentureBeat | https://venturebeat.com | `web_search site:venturebeat.com` |
| 7 | WIRED | https://wired.com | `web_search site:wired.com` |
| 8 | MIT Technology Review | https://technologyreview.com | `web_search site:technologyreview.com` |
| 9 | ZDNet | https://zdnet.com | `web_search site:zdnet.com` |
| 10 | CNET | https://cnet.com | `web_search site:cnet.com` |
| 11 | Engadget | https://engadget.com | `web_search site:engadget.com` |
| 12 | Gizmodo | https://gizmodo.com | `web_search site:gizmodo.com` |
| 13 | The Next Web | https://thenextweb.com | `web_search site:thenextweb.com` |

| 14 | The Verge - AI | https://www.theverge.com/ai-artificial-intelligence | `web_search site:theverge.com ai` |
| 15 | TechCrunch - AI | https://techcrunch.com/category/artificial-intelligence | `web_search site:techcrunch.com artificial-intelligence` |

## Workflow

1. **Pour chaque source**, lancer `web_search(query, limit=5)` avec le site + mot-cle si pertinent
2. **Extraire** les URLs prometteuses avec `web_extract(urls, char_limit=8000)`
3. **Filtrer** : garder uniquement les articles de moins de 7 jours
4. **Dedupliquer** : ne pas reporter le meme sujet deux fois - garder la meilleure source

## Format de sortie

Rapport Markdown avec 3 niveaux de priorite : Haute (rouge), Notable (jaune), A suivre (gris).

## Regles

- Toujours inclure le lien complet
- Ne jamais resumer sans extraction - marquer (extraction partielle) sinon
- Si source inaccessible (blocage, paywall), noter mais continuer
- Prioriser l'impact produit/produit/strategie sur le simple communique
- Max 25 articles par rapport
