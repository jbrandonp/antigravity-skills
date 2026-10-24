# Guide des Stratégies de Démonstration Mathématique OLYMPUS

Ce document récapitule les 4 méthodes fondamentales pour démontrer une proposition mathématique sans faille logique.

---

## 1. La Démonstration Directe ($P \implies Q$)

On suppose $P$ vraie, et par une chaîne d'implications logiques rigoureuses, on en déduit $Q$.
- *Exemple :* Démontrer que la somme de deux nombres pairs $a$ et $b$ est paire.
  - $a = 2k$ et $b = 2k'$ avec $k, k' \in \mathbb{Z}$.
  - $a + b = 2k + 2k' = 2(k + k')$.
  - Comme $k + k' \in \mathbb{Z}$, $a + b$ est pair. $\blacksquare$

---

## 2. La Démonstration par l'Absurde

Pour prouver que $P$ est vraie, on suppose que sa négation $\neg P$ est vraie, et on aboutit à une contradiction logique ($0 = 1$ ou $x \in A$ et $x \notin A$).
- *Exemple classique :* L'irrationalité de $\sqrt{2}$.

---

## 3. La Démonstration par Récurrence (sur $\mathbb{N}$)

Pour prouver une propriété $P(n)$ pour tout $n \ge n_0$ :
1. **Initialisation :** Vérifier que $P(n_0)$ est vraie.
2. **Hérédité :** Supposer $P(k)$ vraie pour un certain $k \ge n_0$, et prouver qu'alors $P(k+1)$ est vraie.
3. **Conclusion :** Par le principe de récurrence, $\forall n \ge n_0, P(n)$ est vraie. $\blacksquare$
