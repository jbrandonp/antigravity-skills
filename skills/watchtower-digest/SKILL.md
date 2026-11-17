---
name: watchtower-digest
description: Watch Tower - digest quotidien. Agrege les rapports des 3 agents Watch Tower (presse-1, presse-2, youtube), score chaque article sur 5 dimensions, et produit un rapport consolide. Point d entree principal du systeme Watch Tower.
---

# Watch Tower - Digest

## Mission

Agreger les rapports des 3 agents Watch Tower, scorer chaque article sur **5 dimensions**, produire un **rapport consolide priorise**.

## Dependances

- `watchtower-presse-1` - doit avoir produit son rapport
- `watchtower-presse-2` - idem
- `watchtower-youtube` - idem

## Dimensions de score (5)

Chaque article recoit un score de 0 a 10 sur chaque dimension :

| Dimension | Signification | 0-3 | 4-7 | 8-10 |
|-----------|--------------|-----|-----|------|
| **Pertinence** | Alignment interets utilisateur | Hors-sujet | Lie indirectement | Core du sujet |
| **Impact** | Consequences potentielles | Anodin | Changement modere | Disruptif |
| **Fraicheur** | Nouveaute information | > 7 jours | 3-7 jours | < 24h / scoop |
| **Profondeur** | Qualite de l analyse | Clickbait | Correct | Original, donnees |
| **Urgence** | Necessite d agir/reagir | Peut attendre | Cette semaine | Aujourd hui |

**Score global** = moyenne ponderee:
- Pertinence: x2
- Impact: x2
- Fraicheur: x1.5
- Profondeur: x1
- Urgence: x1.5

## Workflow

1. **Recuperer les 3 rapports**
2. **Agreger et deduplicater** - si meme sujet couvert par plusieurs sources, garder la meilleure, marquer (aussi chez X, Y)
3. **PRE-FILTRE JEV (obligatoire, economie)** — avant tout scoring GLM :
   ```bash
   python3 /home/arthur/.hermes/scripts/jev-filter.py
   ```
   en passant sur stdin un JSON array `[{"titre":..., "source":..., "resume":...}, ...]` (resume = premier paragraphe, max 600 chars). Le script renvoie `{total, garder, ecarter, cost, items}`. **Ne scorer GLM (5 dimensions) QUE les articles `garder=true`** (score Jev >= 1.5). Les ecartes vont au tableau final sans scoring, marques `[Jev: ecarte]`. Mentionner le coût Jev du pre-filtre dans les statistiques.
4. **Scorer chaque article retenu** sur 5 dimensions
5. **Classer par score global** decroissant
6. **Generer le rapport structure**

## Format de sortie

Rapport Markdown avec:
- Top 5 du jour (avec score global et scores dimension par dimension)
- Tableau de tous les articles (classes par score) — les articles ecartes par Jev en fin de tableau, une ligne chacun
- Statistiques (N articles, N gardes par pre-filtre Jev, N ecartes, cout Jev du run, provenance, scores moyens, sujet dominant)
- Synthese IA (narratif du jour, signaux faibles)

## Regles

- Toujours inclure les scores dimension par dimension
- Toujours marquer les doublons avec sources alternatives
- Top 5 doit contenir exactement 5 articles
- Synthese IA ne resumee pas les articles - elle degage la tendance
- Si rapport de collecte absent: signaler avec (Agent manquant)
- Max 200 lignes pour le digest complet
