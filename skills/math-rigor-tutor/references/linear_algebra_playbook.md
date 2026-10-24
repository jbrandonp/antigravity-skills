# Guide Pratique d'Algèbre Linéaire & Calcul Matriciel

Ce guide présente les concepts indispensables d'algèbre linéaire pour maîtriser les vecteurs, les transformations et les matrices.

---

## 1. Vecteurs & Espaces Vectoriels

### Combinaison Linéaire :
Pour des vecteurs $v_1, v_2, \dots, v_k \in \mathbb{R}^n$ et des scalaires $\lambda_1, \dots, \lambda_k \in \mathbb{R}$ :
$$v = \lambda_1 v_1 + \lambda_2 v_2 + \dots + \lambda_k v_k$$

### Liberté (Indépendance Linéaire) :
Une famille $\{v_1, \dots, v_k\}$ est dite **libre** si :
$$\lambda_1 v_1 + \dots + \lambda_k v_k = 0 \implies \lambda_1 = \dots = \lambda_k = 0$$
Si l'un des vecteurs peut s'écrire comme combinaison des autres, la famille est **liée**.

### Base & Dimension :
Une famille est une **base** d'un espace $E$ si elle est à la fois libre et génératrice de $E$.
Le nombre d'éléments d'une base est la **dimension** de $E$ ($\dim(\mathbb{R}^n) = n$).

---

## 2. Opérations sur les Matrices

### Produit Matriciel :
Pour multiplier $A \in \mathcal{M}_{m, p}(\mathbb{R})$ par $B \in \mathcal{M}_{p, n}(\mathbb{R})$ (le nombre de colonnes de $A$ doit égaler le nombre de lignes de $B$) :
$$C = A \times B \in \mathcal{M}_{m, n}(\mathbb{R}) \quad \text{où} \quad c_{ij} = \sum_{k=1}^p a_{ik} b_{kj}$$
*Attention :* Le produit matriciel n'est **généralement pas commutatif** ($AB \neq BA$).

---

## 3. Déterminant & Inversibilité

### Matrice $2 \times 2$ :
$$A = \begin{pmatrix} a & b \\ c & d \end{pmatrix} \implies \det(A) = ad - bc$$

### Matrice $3 \times 3$ (Développement par la 1ère ligne) :
$$\det \begin{pmatrix} a & b & c \\ d & e & f \\ g & h & i \end{pmatrix} = a(ei - fh) - b(di - fg) + c(dh - eg)$$

### Condition d'Inversibilité :
Une matrice carrée $A$ est inversible si et seulement si :
$$\det(A) \neq 0$$
Dans ce cas, pour une matrice $2 \times 2$ :
$$A^{-1} = \frac{1}{ad - bc} \begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$$

### Propriétés Majeures :
- $\det(AB) = \det(A) \times \det(B)$
- $\det(A^{-1}) = \frac{1}{\det(A)}$
- $\det(A^T) = \det(A)$ (la transposée conserve le déterminant)

---

## 4. Systèmes Linéaires & Résolution $AX = B$

Trois méthodes de résolution :
1. **Élimination de Gauss-Jordan** (Universelle, par opérations élémentaires sur les lignes $L_i \leftarrow L_i - \alpha L_j$).
2. **Par la Matrice Inverse** : Si $\det(A) \neq 0$, alors $X = A^{-1} B$.
3. **Formules de Cramer** (Pour petits systèmes réguliers) :
   $$x_i = \frac{\det(A_i)}{\det(A)}$$
   où $A_i$ est la matrice obtenue en remplaçant la $i$-ème colonne par le vecteur second membre $B$.

---

## 5. Valeurs Propres & Vecteurs Propres

Un scalaire $\lambda \in \mathbb{R}$ est une **valeur propre** de $A$, et $v \neq 0$ est un **vecteur propre** associé, si :
$$Av = \lambda v \iff (A - \lambda I)v = 0$$

### Équation Caractéristique :
Les valeurs propres sont les racines du **polynôme caractéristique** :
$$P(\lambda) = \det(A - \lambda I) = 0$$

Pour une matrice $2 \times 2$ :
$$P(\lambda) = \lambda^2 - \operatorname{Tr}(A)\lambda + \det(A) = 0$$
où $\operatorname{Tr}(A) = a_{11} + a_{22}$ est la **trace** de la matrice.
