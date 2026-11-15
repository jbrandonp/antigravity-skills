# French Humanizer Deep Rules & Anti-AI Linguistic Protocol

Ce document formalise les règles avancées de dé-robotisation de la langue française, issues de l'ingénierie de `samber/cc-skills@humaniseur-fr` et adaptées au standard de ghostwriting d'autorité.

---

## 🎯 Les Deux Principes Fondamentaux de la Dé-Robotisation

### 1. La Règle des 80 % : La Perfection est la Signature de l'IA
- Un texte réel écrit par un être humain contient des imperfections et des tics à faible densité. Un texte qui applique mécaniquement 100% des règles d'interdiction devient uniformément lisse d'une nouvelle manière tout aussi détectable.
- **Transgression Délibérée :** Conservez environ 20% de souplesse. Un tiret cadratin bien placé, un connecteur classique (« par ailleurs ») ou une liste ordonnée ne rendent pas un texte artificiel s'ils sont mérités par le propos.
- **Un Seul Passage :** Ne jamais ré-exécuter le linter en boucle sur le même texte. Au 2e ou 3e passage, la voix s'aplatit et perd toute aspérité. Si le texte semble encore robotique, la solution consiste à **injecter un fait, un chiffre ou une anecdote vécue**, pas à relancer un filtre.

### 2. La Règle des Trois Signaux (Three-Signal Rule)
- Un marqueur isolé est du simple bruit statistique (la plupart des mots signalés existent dans le français normal).
- **Le Seuil Critique :** C'est la co-occurrence de **3 marqueurs ou plus dans le même paragraphe** qui fait tiquer le lecteur et déclenche l'alarme anti-IA.
- *Exemple toxique :* « Dans un paysage en mutation *(signal 1)*, cet outil constitue un jalon décisif *(signal 2)*, ouvrant la voie à une résilience accrue *(signal 3)*. » → Rejet immédiat.

---

## 🏛️ Règle Impérative : Ne Jamais Abaisser le Registre de Langue

L'ennemi est l'écriture **stéréotypée et mécanique**, pas l'écriture **formelle ou soutenue**.
- Si un texte d'origine est rédigé en langage soutenu d'ingénierie ou de direction, il DOIT rester en langage soutenu.
- Réécrire de la prose technique élégante en argot ou en tutoiement familier est une autre forme d'inauthenticité tout aussi criante.
- Une proposition subordonnée bien construite, un connecteur logique rigoureux (« néanmoins », « toutefois ») et un vocabulaire riche sont des qualités de la langue française, pas des artefacts d'IA.

---

## 🚫 Les 4 Familles de Tics Français à Neutraliser

### 1. L'Inflation de Signification et d'Héritage (Significance Inflation)
Les LLMs gonflent artificiellement la portée des faits ordinaires en les rattachant à des mouvements planétaires ou historiques dont personne n'a parlé.
- **Marqueurs Détectés :** *constitue/représente un tournant, témoigne de, joue un rôle crucial/essentiel/déterminant, souligne l'importance, reflète une tendance plus large, symbolisant son caractère durable, contribuant à, ouvrant la voie à, marquant une étape, un jalon décisif, un paysage en mutation, une empreinte indélébile, profondément ancré*.
- **Correction :** Supprimer la clause de commentaire méta et laisser le fait parler de lui-même.
  - *Avant :* "Notre passage à SQLite constitue un tournant décisif, témoignant de notre volonté de résilience."
  - *Après :* "En passant à SQLite, on a divisé nos temps de réponse par trois."

### 2. Les Propositions Participiales en « -ant » (Danglers & Trailing Clauses)
Les modèles entraînés en anglais traduisent littéralement les propositions participiales finales (*"leading to", "resulting in", "highlighting"*).
- **Marqueurs Détectés :** *permettant ainsi de, facilitant le, ouvrant la voie à, marquant ainsi, renforçant l'idée que, soulignant ainsi*.
- **Correction :** Transformer en proposition indépendante avec un verbe conjugué ou un point net.

### 3. Les Anglicismes de Modèles Entraînés en Anglais
Décalques sémantiques qui sonnent faux à l'oreille d'un francophone natif :
- *Faire du sens* → **Avoir du sens**.
- *Adresser un problème* → **Traiter, résoudre, s'attaquer à un problème**.
- *Délivrer de la valeur* → **Apporter des résultats, enrichir**.
- *À la fin de la journée* → **En fin de compte, au bout du compte**.
- *Focaliser sur* → **Se concentrer sur**.

### 4. Les Rituels Didactiques et Équilibres Paresseux
- **La fausse dissertation académique :** Forcer un plan *Thèse / Antithèse / Synthèse* sur un sujet d'ingénierie direct.
- **La conclusion résumée automatique :** Phrases d'ouverture de conclusion (*"En somme", "Pour conclure", "En fin de compte"*).
- **La question de clôture feinte :** *"Et vous, qu'en pensez-vous ? Partagez vos avis en commentaire !"* → Supprimer purement et simplement.

---

## ✍️ Typographie Française Rigoureuse

1. **Espaces Insécables Obligatoires :**
   - En français, les signes de ponctuation doubles (`;`, `:`, `!`, `?`, `%`, `€`) exigent une espace insécable avant le signe (`14 €`, `Attention :`, `Pourquoi ?`).
2. **Guillemets Français (« ») :**
   - Utiliser les chevrons typographiques avec espaces insécables intérieures (`« citation »`) plutôt que les guillemets droits américains (`"citation"`).
3. **Usage Modéré du Tiret Cadratin :**
   - Pas plus d'une paire de tirets cadratins par publication de 1 000 caractères.
