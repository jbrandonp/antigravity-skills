# Guide des Stratégies de Démonstration Mathématique OLYMPUS

Ce document récapitule les 6 méthodes fondamentales pour démontrer ou réfuter une proposition mathématique avec une rigueur logique sans faille.

---

## 1. La Démonstration Directe ($P \implies Q$)

On suppose la proposition $P$ vraie, et par une succession d'implications logiques et de théorèmes établis, on en déduit $Q$.
- **Structure type :**
  - "Supposons que $P$ soit vraie..."
  - "... or d'après la définition ou le théorème $X$, nous avons..."
  - "... donc $Q$ est vraie. $\blacksquare$"
- **Exemple :** Montrer que le carré d'un nombre impair est impair.
  - Soit $n = 2k + 1$ avec $k \in \mathbb{Z}$.
  - $n^2 = (2k + 1)^2 = 4k^2 + 4k + 1 = 2(2k^2 + 2k) + 1$.
  - En posant $K = 2k^2 + 2k \in \mathbb{Z}$, $n^2 = 2K + 1$, donc $n^2$ est impair. $\blacksquare$

---

## 2. La Démonstration par Contraposée ($(\neg Q \implies \neg P) \iff (P \implies Q)$)

Pour démontrer $P \implies Q$, on démontre son équivalent logique strict : "si non-$Q$, alors non-$P$".
- **Quand l'utiliser :** Lorsque la négation de $Q$ offre une information plus facile à manipuler que $P$ directement.
- **Exemple :** Soit $n \in \mathbb{Z}$. Démontrer que si $n^2$ est pair, alors $n$ est pair.
  - La contraposée est : "Si $n$ est impair, alors $n^2$ est impair".
  - D'après l'exemple de démonstration directe ci-dessus, $n$ impair $\implies n^2$ impair est déjà prouvé.
  - Par contraposition, $n^2$ pair $\implies n$ pair. $\blacksquare$

---

## 3. La Démonstration par l'Absurde (Reductio ad Absurdum)

Pour prouver que $P$ est vraie, on suppose sa négation $\neg P$ vraie, et on dérive rigoureusement une contradiction logique intenable ($0 = 1$, ou $x > 0$ et $x \le 0$).
- **Structure type :**
  - "Supposons par l'absurde que $P$ soit fausse (c'est-à-dire $\neg P$ vraie)..."
  - "... cela entraîne que..."
  - "... ce qui contredit le fait que... (Absurdité)"
  - "Par conséquent, notre hypothèse initiale est fausse et $P$ est vraie. $\blacksquare$"
- **Exemple classique :** Irrationalité de $\sqrt{2}$.
  - Supposons $\sqrt{2} = \frac{p}{q}$ sous forme irréductible ($\operatorname{pgcd}(p, q) = 1$).
  - $2 = \frac{p^2}{q^2} \implies p^2 = 2q^2 \implies p^2$ pair $\implies p$ pair ($p = 2k$).
  - Alors $(2k)^2 = 2q^2 \implies 4k^2 = 2q^2 \implies q^2 = 2k^2 \implies q$ pair.
  - $p$ et $q$ sont tous les deux pairs, ce qui contredit l'irréductibilité de la fraction. Donc $\sqrt{2} \notin \mathbb{Q}$. $\blacksquare$

---

## 4. La Démonstration par Récurrence (sur $\mathbb{N}$)

### A. Récurrence Simple :
Pour prouver une propriété $P(n)$ pour tout $n \ge n_0$ :
1. **Initialisation :** Vérifier que $P(n_0)$ est vraie.
2. **Hérédité :** Soit $k \ge n_0$ fixé. Supposons $P(k)$ vraie (Hypothèse de récurrence). Montrons que $P(k+1)$ est vraie.
3. **Conclusion :** D'après le principe de récurrence, $P(n)$ est vraie pour tout $n \ge n_0$. $\blacksquare$

### B. Récurrence Forte :
Dans l'hérédité, on suppose que $P(i)$ est vraie pour **tous** les entiers $i$ entre $n_0$ et $k$, puis on démontre $P(k+1)$.
- Indispensable pour la décomposition en facteurs premiers.

---

## 5. La Technique de Bornage $\varepsilon - \delta$ (Continuité & Limites)

Pour prouver rigoureusement que $\lim_{x \to x_0} f(x) = L$ :
$$\forall \varepsilon > 0, \quad \exists \delta > 0, \quad 0 < |x - x_0| < \delta \implies |f(x) - L| < \varepsilon$$

### Stratégie Pratique :
1. Partir de l'expression cible $|f(x) - L|$.
2. Exprimer cette quantité en fonction de $|x - x_0|$.
3. Majorer : trouver une constante $M > 0$ telle que $|f(x) - L| \le M |x - x_0|$ dans un voisinage $|x - x_0| < 1$.
4. Poser $\delta = \min\left(1, \frac{\varepsilon}{M}\right)$.
5. Rédiger la chaîne d'implications : si $|x - x_0| < \delta$, alors $|f(x) - L| < \varepsilon$. $\blacksquare$

---

## 6. Réfutation par Contre-Exemple

Pour prouver qu'une proposition universelle $\forall x \in E, P(x)$ est **fausse**, il suffit de trouver **un seul** élément $x_0 \in E$ tel que $P(x_0)$ soit fausse.
- *Proposition fausse :* "Tous les nombres premiers sont impairs".
- *Contre-exemple :* $n = 2$ est premier et pair. Donc la proposition est fausse. $\blacksquare$
