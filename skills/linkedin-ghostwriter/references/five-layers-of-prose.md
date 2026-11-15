# The Five Layers of Prose Architecture

> *"Le style est le fond qui remonte à la surface."* — Victor Hugo.
> Le style n'est pas une décoration ou un vernis esthétique : c'est un acte sémantique. Chaque choix syntaxique, chaque rupture de rythme et chaque profondeur de subordonnée façonne directement la compréhension et l'autorité perçue du message.

Pour codifier ou analyser l'empreinte vocale d'un dirigeant ou d'un ingénieur, décomposez la prose selon ces **5 couches orthogonales**.

---

## 층 COUCHE 1 : Le Lexique (Vocabulary & Dictionary Rules)

C'est la couche la plus déterministe et facilement testable par des linters.

### 1.1 Règle du Bilan Binaire (Use vs Avoid)
Ne jamais interdire un mot sans fournir immédiatement son alternative directe, sinon l'auteur comble le vide par un pire tic.

| Terme à Éviter | Pourquoi l'Éviter | Terme de Remplacement | Pourquoi le Remplacement |
| :--- | :--- | :--- | :--- |
| *Faciliter* | Verbe abstrait, latin creux | **Aider, simplifier, accélérer** | Concret, direct, actif |
| *Tirer parti de / Leverager* | Jargon corporatif vide | **Exploiter, utiliser, rentabiliser** | Action vérifiable |
| *En raison du fait que* | Remplissage verbeux | **Parce que, car** | Économie de souffle |
| *Délivrer (au sens abstrait)* | Décalque de l'anglais "deliver" | **Fournir, livrer, produire** | Seules les pizzas et le courrier se "délivrent" |
| *Écosystème* | Métaphore biologique galvaudée | **Marché, ensemble d'outils, stack** | Réalité concrète |
| *Holistique* | Mot valise de consultant | **Global, complet, transversal** | Précision conceptuelle |

### 1.2 L'Échelle de Jargon par Canal (The Jargon Ladder)
- **Articles & Guides Techniques :** Jusqu'à 5 termes pointus par pièce (avec glose d'une ligne si nécessaire).
- **Posts LinkedIn :** Maximum 2 termes spécialisés par publication (ancrés dans le code ou l'architecture).
- **Notes d'invitation & DMs :** Zéro jargon non standard ; clarté conversationnelle absolue.

---

## 층 COUCHE 2 : La Syntaxe (Sentence Architecture)

La syntaxe dicte l'effort cognitif requis pour lire.

1. **L'Ordre Fondamental SVO (Sujet - Verbe - Objet) :**
   - En B2B et en écriture technique, la voix active SVO préserve l'énergie mentale du lecteur.
   - *Passif :* "Une baisse de 40% de la latence a été mesurée par l'équipe."
   - *Actif SVO :* "Notre équipe a réduit la latence de 40%."
2. **Profondeur de Clause (Clause Depth $\le 2$) :**
   - Interdiction formelle d'empiler plus de 2 niveaux de propositions relatives ("Le système *qui* utilise la base *qui* a été configurée par...").
   - Solution : Découper en deux propositions indépendantes coordonnées ou séparées par un point.
3. **Le Test du Zombie :**
   - Ajoutez mentalement "par les zombies" après le verbe. Si la phrase a du sens, c'est du passif : réécrivez à l'actif.

---

## 층 COUCHE 3 : Le Rythme & La Cadence (Burstiness)

La monotonie est la signature la plus évidente des modèles de langage (LLMs). Une IA écrit des phrases de 12 à 15 mots en boucle continue.

1. **L'Alternance Tri-Modal :**
   - **Phrase Courte (Impact) :** 3 à 6 mots (*"Zéro corruption. Facture divisée par trois."*).
   - **Phrase Moyenne (Explication) :** 10 à 15 mots (*"En activant le mode WAL, les requêtes de lecture ne bloquent plus les écritures concurrentes."*).
   - **Phrase Longue (Nuance) :** 18 à 25 mots (*"Même sous une charge de 10 000 écritures par seconde, la latence médiane reste stable parce que les données sont écrites séquentiellement dans un journal séparé."*).
2. **L'Indice de Burstiness ($\sigma \ge 3.5$) :**
   - L'écart-type de la longueur des phrases doit dépasser 3,5 mots pour garantir une voix vivante et humaine.

---

## 층 COUCHE 4 : La Structure & Les Points de Pivot

Chaque texte est un parcours qui guide le lecteur d'un point A à un point B.

1. **Le Contrat d'Ouverture :** L'accroche promet un enseignement, un avertissement ou une solution concrète.
2. **Le Point de Pivot (Le "Mais") :** Le moment de tension où l'hypothèse de départ s'effondre face à la réalité du terrain.
3. **La Preuve Centrale :** Le chiffre, l'extrait de code, le tableau comparatif ou l'anecdote vécue qui prouve l'affirmation.
4. **La Résolution / Chute :** La leçon d'ingénierie durable et l'invitation sobre au dialogue.

---

## 층 COUCHE 5 : Les Signatures & Empreintes Singulières (Signature Moves)

Ce sont les idiosyncrasies stylistiques qui font reconnaître un auteur entre mille.

- **Le Tiret Cadratin Inattendu :** Pour insérer un aparté incisif sans alourdir.
- **La Litote Technique :** Exprimer beaucoup en disant peu (*"Une facture de 14 € par mois n'a jamais tué personne"*).
- **L'Analogisme Matériel :** Comparer un concept logiciel abstrait à un objet physique familier (un disque vinyle, une vanne hydraulique, un interrupteur).
- **Le Refus Délibéré :** Assumer publiquement de ne pas suivre une mode (*"On n'utilise pas de microservices, et on dort très bien la nuit"*).
