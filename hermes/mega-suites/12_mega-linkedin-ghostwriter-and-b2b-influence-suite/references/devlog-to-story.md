# Guide : Du Terminal / Git Log au Post LinkedIn (Devlog-to-Story)

> **L'Erreur Classique** : Le "changelog dump". Dire *"Cette semaine j'ai livré la v1.2, corrigé 3 bugs et refactoré l'authentification."* Personne ne lit ça. Les gens s'en fichent de la liste des fonctionnalités. Ils veulent le **moment de tension** : le bug vicieux qui a résisté 3 jours, la feature qu'on a dû sacrifier à la dernière minute, le refactoring terrifiant qui a finalement sauvé la prod.

---

## 🔍 Étape 1 : Extraction Automatique depuis le Dépôt

Si vous êtes dans un projet de code, lancez ou inspectez l'historique récent :
```bash
git log --oneline -n 30
```

### Ce que l'on recherche (Les 5 Déclencheurs de Tension) :
1. **Le bug qui résiste** : Plusieurs commits successifs de fix sur le même module (`fix: retry auth`, `fix: really fix auth`, `fix: handle edge case in auth`).
2. **La suppression radicale (Le sacrifice)** : Un commit avec des centaines de lignes supprimées (`refactor: remove legacy pipeline`, `chore: drop feature X`).
3. **Le changement de métrique mesurable** : Une amélioration concrète de performance (`perf: reduce query latency from 1.2s to 45ms`, `fix: memory leak in worker`).
4. **L'impasse architecturale** : Le moment où l'approche élégante théorique s'est écroulée face à la réalité du terrain.
5. **Le dilemme de conception** : Le choix douloureux entre deux bibliothèques, deux bases de données ou deux architectures.

---

## ✍️ Étape 2 : Transformer le Code en Leçon Universelle

Pour toucher une audience qualifiée (fondateurs, CTOs, ingénieurs, clients), **traduisez le jargon en concept d'affaires** :

| Ce qui s'est passé dans le code | La traduction humaine universelle |
| :--- | :--- |
| *Race condition sur la base SQLite* | Deux utilisateurs qui essaient de modifier la même ligne en même temps |
| *Memory leak dans la boucle de scraping* | Le serveur qui gonfle en mémoire jusqu'à exploser à 4h du matin |
| *Refactoring de 2 000 lignes en 150 lignes* | Supprimer la complexité qu'on avait ajoutée pour se faire plaisir |
| *Migration d'un ORM lourd vers du SQL brut* | Remplacer un outil magique qui ralentit tout par des requêtes directes |

---

## 🎯 Étape 3 : Structure du Post Devlog

1. **Hook (< 210 caractères)** : Plonger directement au cœur de l'échec ou du chiffre.
   - *Exemple* : *"J'ai failli corrompre la base de production à 23h30 hier soir. Pas à cause d'une cyberattaque, mais à cause d'une boucle while mal conçue."*
2. **Le Déroulé (ABT)** :
   - *And* : Ce qu'on essayait d'accomplir.
   - *But* : Le piège inattendu où la machine a refusé de coopérer.
   - *Therefore* : Les 2 ou 3 décisions concrètes qui ont réglé le problème.
3. **La Règle Transférable** : La conclusion doit servir même à quelqu'un qui ne code pas (ex: *"La simplicité est une discipline, pas un point de départ"*).
