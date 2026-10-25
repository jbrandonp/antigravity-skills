---
name: senior-code-reviewer
description: >-
  Conduct structured senior-level code reviews, anti-bloat architectural audits (Google, Anthropic, Smol Architect), and exhaustive 9-dimension technical debt audits producing TECH_DEBT_AUDIT.md. Classifies findings by strict severity tiers (Critical, Major, Minor, Nit), eliminates speculative generality, and audits codebase health.
---

# 🧐 Senior Code Reviewer & Smol Architecture Auditor (SOTA 2026)

> **Inspirations & Provenance :** Google & Anthropic Engineering Review Standards, Swyx (*Smol Architect* & *Minimal Viable Surface Area*), Martin Fowler (*Refactoring*).  
> **Core Axiom :** *"The best code is the code you never had to write. Review with rigorous severity, demand deterministic fixes, and relentlessly prune speculative complexity."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Imagine que tu construis une cabane en bois avec tes amis :
1. **Le Réviseur Senior (L'Inspecteur des Travaux Finis)** :
   Avant de monter sur le toit, un charpentier d'expérience vérifie la solidité. Si une poutre menace de s'effondrer (**[CRITICAL]**), personne ne monte tant que ce n'est pas consolidé. S'il manque un coup de pinceau cosmétique (**[NIT]**), il le note gentiment mais te laisse jouer.
2. **La Règle "Smol Architect" (Moins de Code = Moins de Bugs)** :
   Beaucoup de développeurs aiment fabriquer des usines à gaz compliquées : ils créent 5 classes abstraites, 3 interfaces et 4 couches de conversion au cas où le projet deviendrait un jour une multinationale. La doctrine Smol dit : **Stop !** N'écris que le code strictement nécessaire pour aujourd'hui. Si une fonction n'est appelée qu'une seule fois dans tout le projet, écris-la directement là où tu en as besoin au lieu de créer un fichier séparé.
3. **La Traque du Code Mort** :
   Les vieilles fonctions abandonnées et les variables oubliées sont comme des toiles d'araignées : elles alourdissent le projet et perturbent l'intelligence artificielle. Le réviseur les supprime sans pitié.

---

## 🚦 2. Les 4 Niveaux de Sévérité (Google / Anthropic)

Chaque remarque de revue doit obligatoirement être étiquetée avec son niveau :

| Niveau | Définition & Impact | Règle de Fusion (Merge) |
|---|---|---|
| **`[CRITICAL]`** | Faille de sécurité (injection, fuite de clé), perte de données, corruption mémoire, blocage du système. | **INTERDICTION STRICTE DE MERGE.** |
| **`[MAJOR]`** | Régression de performance ($> 15\%$), fuite de ressource (socket/connexion non fermée), absence de test sur logique critique, complexité $O(N^2)$ inutile. | Blocage jusqu'à correction ou dérogation documentée. |
| **`[MINOR]`** | Nommage imprécis, duplication mineure de code, documentation manquante sur fonction non-triviale. | Correction vivement conseillée. |
| **`[NIT]`** | Préférence stylistique cosmétique, ponctuation, détail d'alignement. | Optionnel à la discrétion de l'auteur. |

---

## 🔬 3. La Doctrine "Smol Architect" (Anti-Bloat Swyx Standard)

Pour maximiser la vitesse de convergence de l'agent et la clarté du code :

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Minimal Surface Area (Reject Speculative Generality)     │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Inline Single-Use Indirections                           │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Flat Hierarchy (Prefer composition over deep OOP trees)  │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Dead Code Pruning (Zero orphaned functions or imports)   │
 └─────────────────────────────────────────────────────────────┘
```

1. **Rejeter la Généralité Spéculative (YAGNI)** :
   - Refuser les fabriques de fabriques, les adaptateurs pour des bases de données que le projet n'utilisera jamais, et les paramètres optionnels inutilisés.
2. **Inliner les Indirections à Usage Unique** :
   - Si une fonction utilitaire de 3 lignes n'est appelée qu'à un seul endroit, intégrez-la directement dans son appelant pour supprimer un niveau de saut mental.
3. **Hiérarchie Plate (Composition > Héritage)** :
   - Bannir les arbres d'héritage profonds ($> 2$ niveaux). Préférer des structures simples et des fonctions pures.
4. **Élimination Systématique du Code Mort** :
   - Détecter et supprimer immédiatement tout module orphelin, import inutilisé ou fonction non référencée.

---

## 📋 4. Protocole d'Exécution de Revue

1. **Audit des Invariants & Cas Limites** :
   - Vérifier la résistance aux entrées `None`/nulles, listes vides, caractères Unicode exotiques et dépassements d'entiers.
   - S'assurer que chaque ressource ouverte est garantie d'être fermée via `with` ou `try...finally`.
2. **Proposition Systématique de Solution** :
   - Ne jamais formuler une critique sans fournir le bloc de code corrigé prêt à l'emploi.
3. **Verdict Clair** :
   - Rendre une décision sans ambiguïté : `APPROVE`, `REQUEST_CHANGES` ou `COMMENT`.

---

## 🛠️ 5. Outils Déterministes

```bash
# 1. Auditer la conformité et la qualité d'une Pull Request ou d'un diff
python scripts/audit_pull_request_quality.py --demo

# 2. Auditer l'espace de travail pour traquer le code mort et le bloat architectural
python scripts/audit_code_bloat.py --scan-dir .
```


---

## 🏛️ 6. Protocole d'Audit de Dette Technique Globale (`TECH_DEBT_AUDIT.md`)

Quand l'utilisateur demande un audit de santé de base de code (*codebase health check*, *tech debt audit*, *architecture review*), exécuter l'audit selon les **9 dimensions fondamentales** et consigner les résultats dans `TECH_DEBT_AUDIT.md` à la racine :

### Les 9 Dimensions d'Audit
1. **Code Churn & Hotspots** : Fichiers modifiés le plus fréquemment (`git log --oneline -200`).
2. **God Objects & Taille Fichiers** : Détection des fichiers monolithiques (>300 lignes).
3. **Complexité Cyclomatique** : Calcul $M = E - N + 2P$, fonctions avec imbrications profondes (>4 niveaux).
4. **Santé des Dépendances** : Bibliothèques obsolètes, vulnérables ou redondantes.
5. **Couverture de Tests (Test Gap)** : Modules critiques dépourvus de tests unitaires/intégration.
6. **Rigueur du Typage** : Chasse absolue au type `any` ou équivalents, fonctions non typées.
7. **Bloat Spéculatif (Smol Architect)** : Abstractions prématurées, indirections à usage unique.
8. **Secrets & Sécurité** : Détection de clés API ou tokens codés en dur.
9. **Dérive Documentaire** : Docstrings ou README en décalage avec le code réel.

### Structure Obligatoire de l'Artéfact `TECH_DEBT_AUDIT.md`
```markdown
# Rapport d'Audit de Dette Technique

## 1. Executive Summary
- Santé globale de la base de code (3-5 phrases).
- Dimension la plus critique et nombre de victoires rapides (*quick wins*).

## 2. Modèle Mental de l'Architecture
- Architecture du dépôt en 1 paragraphe (stack, frontières modulaires).

## 3. Tableau des Constats (Findings Table)
| ID | Catégorie | Fichier:Ligne | Sévérité ([CRITICAL]/[MAJOR]/[MINOR]/[NIT]) | Effort (h) | Description | Recommandation |

## 4. Top 5 des Priorités
- Classées par ratio d'impact/effort.

## 5. Quick Wins (<30 minutes chacune)
- [ ] Tâche rapide 1

## 6. "Semble Suspect mais Intentionnel" (False Positives)
- Justification des motifs inhabituels mais légitimes.
```
