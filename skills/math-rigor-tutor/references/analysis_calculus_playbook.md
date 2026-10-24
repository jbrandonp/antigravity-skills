# Guide Pratique d'Analyse Réelle & Calcul Différentiel

Ce guide présente les méthodes indispensables pour étudier les fonctions réelles d'une variable réelle ($f: \mathbb{R} \to \mathbb{R}$) avec rigueur et clarté.

---

## 1. Plan d'Étude d'une Fonction (Les 6 Étapes)

Pour toute fonction $f(x)$ :
1. **Domaine de Définition ($D_f$)** : Exclure les divisions par zéro ($x \neq 0$), les racines carrées négatives ($\sqrt{u} \implies u \ge 0$), et les logarithmes nuls ou négatifs ($\ln(u) \implies u > 0$).
2. **Parité & Périodicité** :
   - Paire si $f(-x) = f(x)$ (symétrie par rapport à l'axe des ordonnées $Oy$).
   - Impaire si $f(-x) = -f(x)$ (symétrie centrale par rapport à l'origine $O$).
   - Périodique de période $T$ si $f(x+T) = f(x)$.
3. **Limites aux Bornes & Asymptotes** :
   - Si $\lim_{x \to a} f(x) = \pm\infty$ : Asymptote verticale d'équation $x = a$.
   - Si $\lim_{x \to \pm\infty} f(x) = b$ : Asymptote horizontale d'équation $y = b$.
   - Si $\lim_{x \to \pm\infty} [f(x) - (ax + b)] = 0$ : Asymptote oblique d'équation $y = ax + b$.
4. **Dérivabilité & Dérivée Première ($f'(x)$)** :
   - Signe de $f'(x)$ $\implies$ Sens de variation (croissance/décroissance).
   - Points critiques : $f'(x) = 0$ (extrema locaux potentiels).
5. **Dérivée Seconde ($f''(x)$) & Convexité** :
   - $f''(x) \ge 0$ : Convexe (la courbe est au-dessus de ses tangentes, forme de bol $\cup$).
   - $f''(x) \le 0$ : Concave (la courbe est en-dessous de ses tangentes, forme de dôme $\cap$).
   - Changement de signe de $f''(x)$ : Point d'inflexion (la tangente traverse la courbe).
6. **Tableau de Variations & Tracé** : Synthèse complète des limites, zéros et variations.

---

## 2. Lever les Formes Indéterminées (Les 7 Cas)

Les 7 formes indéterminées classiques sont :
$$\frac{0}{0}, \quad \frac{\infty}{\infty}, \quad 0 \times \infty, \quad \infty - \infty, \quad 0^0, \quad \infty^0, \quad 1^\infty$$

### Techniques Algébriques Majeures :
1. **Factorisation par le terme dominant** (en $\pm\infty$) :
   $$\lim_{x \to +\infty} \frac{3x^2 - 5x + 2}{2x^2 + 7} = \lim_{x \to +\infty} \frac{x^2(3 - \frac{5}{x} + \frac{2}{x^2})}{x^2(2 + \frac{7}{x^2})} = \frac{3}{2}$$
2. **Expression Conjuguée** (pour les racines carrées) :
   $$\sqrt{x+1} - \sqrt{x} = \frac{(\sqrt{x+1} - \sqrt{x})(\sqrt{x+1} + \sqrt{x})}{\sqrt{x+1} + \sqrt{x}} = \frac{1}{\sqrt{x+1} + \sqrt{x}} \xrightarrow[x \to +\infty]{} 0$$
3. **Taux de Variation (Dérivée en 0)** :
   $$\lim_{x \to x_0} \frac{f(x) - f(x_0)}{x - x_0} = f'(x_0)$$
4. **Limites Fondamentales Usuelles** :
   - $\lim_{x \to 0} \frac{\sin(x)}{x} = 1$
   - $\lim_{x \to 0} \frac{e^x - 1}{x} = 1$
   - $\lim_{x \to 0} \frac{\ln(1+x)}{x} = 1$
   - Croissances comparées : $\lim_{x \to +\infty} \frac{e^x}{x^n} = +\infty$, $\lim_{x \to +\infty} \frac{\ln(x)}{x^n} = 0$, $\lim_{x \to 0^+} x^n \ln(x) = 0$ (pour $n > 0$).

---

## 3. Dérivation & Équation de la Tangente

### Définition Formelle :
$$f'(x_0) = \lim_{h \to 0} \frac{f(x_0 + h) - f(x_0)}{h}$$

### Équation de la Tangente au point d'abscisse $x_0$ :
$$y = f'(x_0)(x - x_0) + f(x_0)$$

### Formules de Dérivation :
- Produit : $(uv)' = u'v + uv'$
- Quotient : $\left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^2}$
- Composée (Chain Rule) : $(g \circ f)'(x) = f'(x) \cdot g'(f(x))$

---

## 4. Intégration

### Théorème Fondamental de l'Analyse :
Si $f$ est continue sur $[a, b]$ et $F$ une primitive de $f$ ($F' = f$) :
$$\int_a^b f(x) \, dx = [F(x)]_a^b = F(b) - F(a)$$

### Intégration par Parties (IPP) :
$$\int_a^b u(x) v'(x) \, dx = [u(x)v(x)]_a^b - \int_a^b u'(x) v(x) \, dx$$
*Règle mnémonique ALPES pour choisir $u(x)$ :*
1. **A**rcsin / Arccos / Arctan
2. **L**ogarithme ($\ln$)
3. **P**olynôme
4. **E**xponentielle ($e^x$)
5. **S**inus / Cosinus
