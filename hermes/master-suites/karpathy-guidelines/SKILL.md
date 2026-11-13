---
name: karpathy-guidelines
description: >-
  Enforces Andrej Karpathy's 4 foundational software development laws (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution) combined with Ponytail anti-overengineering and dead-code elimination. Banning whole-file rewrites and speculative abstractions.
version: 1.0.0
tags:
  - karpathy
  - surgical-code
  - anti-overengineering
  - ponytail
  - simplicity
---

# 🧘 Karpathy Guidelines & Ponytail Anti-Overengineering

> **Inspirations :** Andrej Karpathy (`multica-ai/andrej-karpathy-skills`) & Dietrich Gebert (`DietrichGebert/ponytail`).  
> **Axiome Central :** *"La meilleure ligne de code est celle que tu n'as pas besoin d'écrire. Ne touche jamais à 200 lignes pour corriger un bug de 2 lignes."*

---

## 🏛️ Les 4 Piliers Inviolables d'Andrej Karpathy

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. THINK BEFORE CODING: Verbaliser les hypothèses d'abord   │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. SIMPLICITY FIRST: Zéro abstraction spéculative           │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. SURGICAL CHANGES: Diffs ciblés, interdiction de réécrire │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. GOAL-DRIVEN: S'arrêter dès que l'objectif est prouvé     │
 └─────────────────────────────────────────────────────────────┘
```

### 1. Think Before Coding (Réfléchir Avant d'Écrire)
- L'agent doit obligatoirement expliciter son raisonnement en 2-3 phrases avant de modifier un fichier.
- Vérifier les préconditions et identifier les effets de bord potentiels sur les composants appelants.

### 2. Simplicity First (Simplicité Radicale)
- **Interdiction formelle de sur-architecturer** : pas de Factory, de Singleton ou de pattern générique pour un besoin à usage unique.
- **Priorité absolue à la bibliothèque standard** (`sqlite3`, `pathlib`, `re`, `subprocess`, `dataclasses`, `typing`) avant d'envisager d'ajouter une dépendance externe.
- Si une fonction de 15 lignes résout le problème, refuser d'installer un package externe de 20 Mo.

### 3. Surgical Changes (Modifications Chirurgicales)
- **Interdiction absolue d'écraser des fichiers entiers** lorsqu'un remplacement partiel suffit.
- Utiliser uniquement des modifications localisées (`edit_file` / diffs précis).
- Préserver scrupuleusement les commentaires préexistants, la mise en forme et les conventions de nommage du projet.

### 4. Goal-Driven Execution (Exécution Axée sur le But)
- Définir un critère d'achèvement formel et mesurable avant d'exécuter la tâche (un test unitaire qui passe, un code de retour 0).
- Dès que le critère de réussite est atteint, **arrêter immédiatement les modifications**. Ne pas continuer à "refactorer pour le plaisir".

---

## ✂️ Heuristiques "Ponytail" (L'Ingénieur Senior Pragmatique)

- **YAGNI (You Aren't Gonna Need It)** : Ne code jamais ce dont tu *pourrais* avoir besoin plus tard. Code ce dont tu as besoin *maintenant*.
- **Dead Code Elimination** : Tout code commenté, toute fonction devenue orpheline ou toute importation inutilisée doit être supprimée immédiatement.
- **Inlining des Indirections Simples** : Si une fonction n'est appelée qu'à un seul endroit dans tout le codebase et ne fait que 2 lignes, élimine l'intermédiaire et intègre la logique directement.
