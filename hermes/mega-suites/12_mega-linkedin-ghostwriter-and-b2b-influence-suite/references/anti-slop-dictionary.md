# Dictionnaire Unifié Anti-Slop & Dé-Robotisation (Bilingue FR / EN)
## La Synthèse Exhaustive des 38 Patterns Français + 26 Patterns Anglais + 17 Classes Invisibles

Ce dictionnaire unifie le standard d'investigation de Wikipédia (*Signs of AI writing*), les règles stylistiques de `blader/humanizer`, l'inventaire complet des 38 tics francophones de `samber/humaniseur-fr`, le lexique de `Jakeschincariol/slop.json` et les portes de validation de `coreyhaines31/marketingskills`.

---

## 🛑 PARTIE 1 : Nettoyage Automatique des Filigranes & Typographie

### 1. Les 17 Classes de Caractères Invisibles (Watermarks LLM)
Les modèles de langage et les interfaces de chat injectent régulièrement des caractères de formatage ou des filigranes invisibles. Ces caractères ne sont jamais générés par un clavier humain et sont détectés par les algorithmes :
- `\u200B` (Zero-Width Space)
- `\u200C` (Zero-Width Non-Joiner)
- `\u200D` (Zero-Width Joiner)
- `\u2060` (Word Joiner)
- `\uFEFF` (Zero-Width No-Break Space / BOM)
- `\u00AD` (Soft Hyphen)
- `\u200E` / `\u200F` (Left-to-Right / Right-to-Left Marks)
- `\u202A` à `\u202E` (Directional Formatting)
- *Règle* : Tous ces caractères sont supprimés silencieusement lors du nettoyage.

### 2. Typographie & Gras Mécanique
- **Tirets cadratins (`—`)** : Limiter à 1 maximum par post. Les remplacer par une virgule, deux-points ou des parenthèses.
- **Gras mécanique** : Bannir les puces verticales où chaque ligne commence par un mot en gras suivi de deux-points (`- **Sécurité :** Renforcée...`). Remplacer par de la prose fluide ou des phrases directes.
- **Gras Unicode** : N'utiliser le gras mathématique Unicode (`𝗯𝗼𝗹𝗱`) que pour 1 à 2 termes clés ou métriques pivots par post.

---

## 🇫🇷 PARTIE 2 : Les 38 Patterns d'Écriture IA en Français

### A. Vocabulaire Surutilisé & Mots-Fouines (High-Frequency AI Lexicon)

| Mot ou expression interdite | Pourquoi c'est du slop | Remplacement humain direct |
| :--- | :--- | :--- |
| **crucial / essentiel** | Le mot n°1 trahissant l'IA en français | "majeur", "vital", "le plus gros problème", ou suppression |
| **notamment** | Utilisé 4x plus souvent par les IA que les humains | "en particulier", "surtout", ou restructurer la phrase |
| **également** | Marqueur n°1 mesuré dans les corpus d'IA | Utiliser "aussi" ou supprimer (1 max par paragraphe) |
| **décryptage** | Tic journalistique pompeux | "analyse", "ce qui s'est passé", ou suppression |
| **incontournable** | Paresseux, superlatif sans preuve | "utile", "requis", ou expliquer concrètement pourquoi |
| **catalyseur / levier puissant** | Métaphores de consultant fatiguées | "accélérateur", "déclencheur", décrire le mécanisme réel |
| **révolutionner / transformateur** | Emphase artificielle | "changer", "simplifier", donner le chiffre du gain |
| **holistique** | Calque de l'anglais "holistic" | "global", "complet", ou supprimer |
| **synergie / écosystème** | Jargon corporate creux | "coopération", "notre équipe", "notre stack" |
| **pierre angulaire** | Cliché d'écriture automatique | "base", "fondation", "le cœur du projet" |
| **s'avérer** | Tic d'évitement du verbe être | Utiliser simplement "c'est" ou "est" |
| **enjeu / défi** | Mots-valises institutionnels | "difficulté", "obstacle", "risque de casse" |
| **résilience** | Moralisme d'entreprise | "endurance", "capacité à tenir la charge" |

### B. Formules d'Ouverture et de Fermeture à Bannir Définitivement

- ❌ *« Dans le paysage [actuel/numérique/technologique]... »*
- ❌ *« À l'ère de l'intelligence artificielle / du tout-numérique... »*
- ❌ *« Dans un monde où tout va plus vite... »*
- ❌ *« Il est essentiel/crucial de noter que... »*
- ❌ *« Plongeons dans les détails... »* / *« Décryptons ensemble... »*
- ❌ *« En conclusion »* / *« En résumé »* / *« Au final »* en tête de dernier paragraphe.
- ❌ *« Et vous, qu'en pensez-vous en commentaires ? »* (Appel à commentaire paresseux).

### C. Structures Rhétoriques Robotiques

1. **La Fausse Opposition Binaire** :
   - ❌ *"Ce n'est pas seulement X, c'est Y"* ou *"Il ne s'agit pas de X, mais de Y"*.
   - ✅ Remplacer par une affirmation directe : *"Coder vite ne sert à rien si le serveur plante."*
2. **Le Rythme Ternaire Forcé (Règle de Trois)** :
   - ❌ *"Une solution rapide, efficace et robuste."* / *"Analyser, concevoir et déployer."*
   - ✅ Casser la symétrie : grouper par deux ou découpler en phrases asymétriques.
3. **Analyses Superficielles en Participe Présent (`-ant`)** :
   - ❌ *"L'outil optimise la mémoire, permettant une meilleure scalabilité, renforçant la sécurité et favorisant l'adoption."*
   - ✅ Transformer en verbes conjugués précis : *"L'outil consomme 4 fois moins de RAM. Le serveur ne plante plus sous 10 000 requêtes/sec."*
4. **Anglicismes d'Architecture des LLMs** :
   - ❌ *"faire du sens"* → ✅ *"avoir du sens"*
   - ❌ *"adresser un problème"* → ✅ *"traiter / régler un problème"*
   - ❌ *"supporter"* (= soutenir) → ✅ *"prendre en charge / tolérer"*
   - ❌ *"définitivement"* (= assurément) → ✅ *"sans aucun doute / clairement"*
   - ❌ *"basiquement"* → ✅ *"en gros / concrètement"*
5. **Connecteurs Authentiques Humains (que les LLMs n'utilisent presque jamais)** :
   - Utiliser : *« Or »*, *« Reste que »*, *« N'empêche que »*, *« Soit dit en passant »*, *« Quoi qu'il en soit »*.

### D. Marqueurs Régionaux & Humanisateurs Concrets

Pour un auteur francophone basé en Belgique ou en Europe :
- **Belgicismes légitimes** : *septante, nonante, GSM, kot, tantôt, drache, savoir (= pouvoir : "je ne saurais pas le livrer ce soir")*.
- **Abréviations et apocopes humaines** : *pb, tjs, 14h30, 25€, réu, config, admin, doc, algo, prod, dev*. (Un LLM n'écrit jamais spontanément *"On a mis la nouvelle config en prod à 14h30"*).

---

## 🇬🇧 PARTIE 3 : Les 26 Patterns Anglais (Wikipedia Anti-AI)

| Pattern | Signes d'alerte | Correction |
| :--- | :--- | :--- |
| **1. Not X but Y** | *not just X, it's Y*, *X rather than Y*, *..., no guessing* | State the positive claim directly |
| **2. One-line closers** | *That is the real win.*, *Let that sink in.*, *Read that again.* | Delete or merge with a concrete fact |
| **3. Fake profundity** | *at its core*, *what really matters*, *X is the currency of Y* | State the plain mechanical truth |
| **4. Staged run-up** | *Let's dive in*, *Here's the thing*, *Honestly?*, *Real talk* | Delete the run-up; start in medias res |
| **5. Arguing with no one** | *This isn't to say*, *I'm not saying*, *Don't get me wrong* | Drop the defensive pre-empting |
| **6. Forced triads** | Grouping adjectives or examples strictly by 3 | Use 1 strong example or 2 asymmetrical ones |
| **7. Universal Em Dash** | Heavy reliance on `—` to avoid choosing connectors | Replace with comma, period, or rewrite |
| **8. Stacked qualifiers** | *could potentially arguably in some cases* | State the calibrated estimate directly |
| **9. Overused AI words** | *delve, tapestry, leverage, foster, harness, crucial, realm, robust, vibrant* | Use plain Saxon verbs: *use, test, check, build* |
| **10. Sales language** | *groundbreaking, game-changer, breathtaking, bespoke* | Replace with the exact number or metric |
| **11. Chat residue** | *I hope this helps!*, *Great question!*, *Here is a breakdown...* | Delete wrapper completely |
| **12. Knowledge disclaimers**| *As of my last update...*, *While specific details are limited...* | State the source or omit |

---

## 🧠 PARTIE 4 : Les Portes de Contrôle (The Gates)

### 1. The Zombie Test (Voix Active Obligatoire)
- **Le Test** : Si vous pouvez ajouter **« par des zombies »** après le verbe, la phrase est passive.
  - ❌ *"La migration a été effectuée sans incident [par des zombies]."*
  - ✅ *"On a migré la base en 12 minutes sans couper le service."*

### 2. The Three-Question Gate (Règle de Corey Haines)
Passez chaque phrase clé par ces 3 filtres :
1. **Le lecteur peut-il visualiser l'image ?** (Une ligne de code, un terminal noir, un ticket Jira, un serveur en surchauffe > un concept abstrait).
2. **L'affirmation est-elle falsifiable ?** (Un chiffre, une date, un outil précis peut être vérifié ; *"nous visons l'excellence"* ne veut rien dire).
3. **Un concurrent pourrait-il écrire exactement cette phrase ?** (Si oui, la phrase est éliminée car elle manque de signature unique).
