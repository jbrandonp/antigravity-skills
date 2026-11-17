---
name: watchtower-youtube
description: Watch Tower - veille YouTube. Surveille 20 chaines (Lex Fridman, All-In, 20VC, Acquired, Cleo Abram, Hard Fork, etc.) via `web_search` pour trouver les dernieres videos publiees.
---

# Watch Tower - YouTube

## Mission

Surveiller **20 chaines YouTube** et identifier les nouvelles videos publiees dans les 7 derniers jours. Utilise `web_search` pour trouver les videos et `web_extract` pour les metadonnees. Jamais de navigateur.

## Chaines (20)

| # | Chaine | Handle | Strategie |
|---|--------|--------|-----------|
| 1 | Lex Fridman Podcast | @lexfridman | `web_search site:youtube.com lexfridman recent` |
| 2 | All-In Podcast | @allin | `web_search site:youtube.com allin recent` |
| 3 | 20VC with Harry Stebbings | @20vc | `web_search site:youtube.com 20vc recent` |
| 4 | Acquired | @acquired | `web_search site:youtube.com acquired recent` |
| 5 | Cleo Abram | @cleoabram | `web_search site:youtube.com cleoabram recent` |
| 6 | Hard Fork (NYT) | @hardfork | `web_search site:youtube.com hardfork recent` |
| 7 | Y Combinator | @ycombinator | `web_search site:youtube.com ycombinator recent` |
| 8 | Andrej Karpathy | @andrejkarpathy | `web_search site:youtube.com andrejkarpathy recent` |
| 9 | Two Minute Papers | @TwoMinutePapers | `web_search site:youtube.com TwoMinutePapers recent` |
| 10 | 3Blue1Brown | @3blue1brown | `web_search site:youtube.com 3blue1brown recent` |
| 11 | Fireship | @fireship | `web_search site:youtube.com fireship recent` |
| 12 | Computerphile | @Computerphile | `web_search site:youtube.com Computerphile recent` |
| 13 | NetworkChuck | @NetworkChuck | `web_search site:youtube.com NetworkChuck recent` |
| 14 | ThePrimeagen | @ThePrimeagen | `web_search site:youtube.com ThePrimeagen recent` |
| 15 | AI Explained | @aiexplained | `web_search site:youtube.com aiexplained recent` |
| 16 | Matt Wolfe | @mattwolfe | `web_search site:youtube.com mattwolfe recent` |
| 17 | David Shapiro | @DavidShapiro | `web_search site:youtube.com DavidShapiro recent` |
| 18 | TheAIGRID | @theaigrid | `web_search site:youtube.com theaigrid recent` |
| 19 | Wes Roth | @wesroth | `web_search site:youtube.com wesroth recent` |
| 20 | Steve Nouri | @stevenouri | `web_search site:youtube.com stevenouri recent` |


## Workflow

1. **Pour chaque chaine**, lancer `web_search(query, limit=3)`
2. **Analyser les snippets** : titre, chaine, date, vues
3. **Extraire** les URLs prometteuses avec `web_extract`
4. **Filtrer** : garder videos < 7 jours
5. **Dedupliquer**

## Format de sortie

Rapport Markdown classe par format : Podcasts > Analyses > A surveiller.

## Regles

- Toujours inclure le lien YouTube complet
- Si chaine sans nouvelle video : marquer (rien cette semaine)
- Le snippet moteur suffit souvent - ne pas extraire chaque page video
- Signaler les invites/guests notables
- Max 25 videos par rapport
