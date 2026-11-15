# Référence Complète : Les 6 Frameworks de Hooks LinkedIn & Ingénierie Mobile

## 📱 L'Impératif Géométrique des 210 Caractères

Sur l'application mobile LinkedIn (environ 60 % de l'audience), le composant d'affichage applique la règle de troncature `-webkit-line-clamp`.
- Le texte est coupé entre **140 et 210 caractères** (ou au 3e/4e saut de ligne).
- **Règle absolue** : La tension dramatique, le chiffre pivot ou la contradiction intellectuelle **doit se situer AVANT ce seuil**. Si vous donnez la réponse avant le clic, personne ne déplie le post. Si vous attendez après le seuil pour poser le problème, personne ne clique.

---

## 🎯 Les 6 Frameworks de Hooks Validés

### 1. Le Curiosity Gap Quantifié (Règle 80/20)
- **Mécanique** : Révèle 80 % du résultat chiffré, mais garde 20 % de mystère sur la méthode ou l'outil pour obliger au clic.
- **Formule** : `[Résultat chiffré spectaculaire] + [Négation de la cause évidente] + [Amorce de la cause réelle]`
- **Exemple sous 210 caractères** :
  ```text
  On a fait passer notre scraper de supermarchés de 40 % de blocages à 0 %.
  Sans acheter de proxies résidentiels rotatifs à 500 €/mois.
  
  Voici l'erreur d'ingénierie que font 9 devs sur 10 :
  ```
  *(197 caractères — Déclenchement automatique du « ...voir plus »)*

---

### 2. Le Signal Coûteux (Costly Signal / Skin in the Game)
- **Mécanique** : Afficher un investissement disproportionné en temps, en sueur ou en argent pour prouver que vous n'êtes pas un théoricien.
- **Formule** : `[Investissement lourd en temps ou argent] + [Ce qu'on cherchait] + [La seule chose qui a marché]`
- **Exemple sous 210 caractères** :
  ```text
  J'ai passé 45 heures cette semaine à inspecter des trames Wireshark et des ciphers TLS.
  
  Pour résoudre un seul problème : pourquoi notre bot se faisait flagger en 3 requêtes.
  
  La réponse tenait en 2 lignes de config :
  ```
  *(209 caractères)*

---

### 3. L'Erreur de Diagnostic / Le Faux Consensus
- **Mécanique** : Prendre une croyance unanime de votre industrie et prouver factuellement qu'elle est fausse.
- **Formule** : `[Ce que 90% des gens croient] + [Le constat brutal d'échec] + [Le vrai coupable]`
- **Exemple sous 210 caractères** :
  ```text
  9 développeurs sur 10 pensent qu'il leur faut PostgreSQL et Docker dès le premier jour.
  
  Puis ils passent 3 semaines à debugger des migrations.
  
  Une base SQLite locale en WAL mode encaisse 10 000 req/sec sans broncher.
  ```
  *(208 caractères)*

---

### 4. Le Post-Mortem d'Échec (Brutal Honesty)
- **Mécanique** : Démarrer sans fard par une perte financière ou technique cuisante. Les réussites parfaites inspirent la méfiance ; les échecs instruits forcent le respect.
- **Formule** : `[Somme ou temps perdu] + [L'hypothèse stupide] + [Ce qu'on a réécrit]`
- **Exemple sous 210 caractères** :
  ```text
  J'ai brûlé 3 semaines de dev et 2 400 € d'infra sur un système de queue Redis complexe.
  
  Pour découvrir qu'un simple fichier de verrou SQLite faisait le même travail en 15 lignes.
  
  Voici mon autopsie du bug :
  ```
  *(208 caractères)*

---

### 5. L'Asymétrie Contrastée (Niveau 1 vs Niveau 10)
- **Mécanique** : Opposer deux manières de résoudre un même problème technique sans fioritures.
- **Formule** : `[Approche complexe de débutant] vs [Approche sobre d'expert]`
- **Exemple sous 210 caractères** :
  ```text
  Un dev junior ajoute une dépendance npm de 40 Mo pour formater une date.
  Un dev confirmé écrit 4 lignes de regex.
  Un dev senior demande pourquoi on a besoin d'afficher cette date et supprime la colonne.
  ```
  *(197 caractères)*

---

### 6. Le Constat d'Inconfort (Cold Reality)
- **Mécanique** : Dire tout haut ce que tout le monde pense tout bas dans les équipes techniques ou business.
- **Formule** : `[Ce que le client/marché fait semblant d'aimer] + [Ce qui l'intéresse réellement]`
- **Exemple sous 210 caractères** :
  ```text
  Vos clients ne lisent pas votre documentation de 80 pages.
  Ils ne regardent pas vos vidéos Loom de 15 minutes.
  
  Ce qu'ils veulent, c'est appuyer sur un bouton et que leur problème disparaisse en 10 secondes.
  ```
  *(199 caractères)*

---

## 🚫 La Règle d'Or de l'Accroche
Ne jamais poser de question ouverte ou timide en première ligne (*"Avez-vous déjà pensé à... ?"*, *"Saviez-vous que... ?"*). Une accroche de haut niveau est une **affirmation non-négociable** qui crée une rupture cognitive dans le fil de lecture.
