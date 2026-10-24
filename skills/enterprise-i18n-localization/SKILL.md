---
name: enterprise-i18n-localization
description: >-
  Architect and implement software internationalization (i18n) and localization (l10n). Covers ICU MessageFormat, plural and gender rules, Right-to-Left (RTL) layout mirroring (Arabic, Hebrew), locale-aware date/currency formatters, pseudo-localization testing, and multilingual SEO (hreflang).
---

# 🌍 Enterprise Internationalization (i18n) & Localization (l10n)

> **Standard :** Unicode CLDR (Common Locale Data Repository) & ICU MessageFormat  
> **Core Axiom :** *"Internationalization is not just translating words with Google Translate. It requires handling complex pluralization rules, grammatical genders, currency/date formatting by locale, bidirectional text (RTL layout mirroring), and automated pseudo-localization to eliminate UI clipping before deployment."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Traduire un logiciel dans le monde entier, c'est **bien plus complexe que de remplacer un mot par un autre** :
- **Le Piège des Pluriels** : En français et en anglais, il n'y a que 2 formes de pluriel (0 ou 1 pomme = singulier, 2+ pommes = pluriel). Mais en **russe** ou en **arabe**, il y a **6 formes de pluriels différentes** selon les chiffres ! Si tu écris `"Vous avez " + count + " messages"`, ton code sera grammaticalement faux dans la moitié du monde.
- **La Norme ICU MessageFormat** : C'est le standard mondial qui permet d'écrire des phrases dynamiques intelligentes avec gestion des pluriels et des genres.
- **Le Mode RTL (Right-to-Left - De droite à gauche)** : En arabe ou en hébreu, on lit de droite à gauche. Toute ton interface doit être inversée comme dans un miroir (le bouton retour passe à droite, les menus s'ouvrent vers la gauche, les barres de progression avancent vers la gauche).
- **La Pseudo-Localisation (Le Détecteur de Bugs Visuels)** : Pour tester si ton interface est prête avant même d'avoir payé des traducteurs, on transforme automatiquement le texte en faux allemand avec des accents étranges et du texte 30% plus long (`[!!! Ṫḗşṫḗḓ Ḿḗşşȧɠḗş !!!]`). Si un bouton déborde ou coupe le texte, tu le vois immédiatement !

---

## 📜 2. La Norme ICU MessageFormat

Ne JAMAIS concaténer des bouts de chaînes (`"Hello " + name`). Utiliser les syntaxes ICU standard :

```json
{
  "cart.item_count": "{count, plural, =0 {Votre panier est vide} one {Vous avez # article dans votre panier} other {Vous avez # articles dans votre panier}}",
  "user.greeting": "{gender, select, female {Bienvenue sur votre profil, Madame {name} !} male {Bienvenue sur votre profil, Monsieur {name} !} other {Bienvenue sur votre profil, {name} !}}"
}
```

---

## 📐 3. Support Bidirectionnel (RTL Layout Mirroring)

En CSS et Tailwind CSS, bannir les propriétés directionnelles rigides (`left`, `right`) et utiliser les **Propriétés Logiques CSS** :

| Ancienne Propriété Rigide | Propriété Logique Universelle (LTR & RTL) | Classe Tailwind Équivalente |
|---|---|---|
| `margin-left: 16px;` | `margin-inline-start: 1rem;` | `ms-4` |
| `padding-right: 24px;`| `padding-inline-end: 1.5rem;` | `pe-6` |
| `text-align: left;` | `text-align: start;` | `text-start` |
| `left: 0;` | `inset-inline-start: 0;` | `start-0` |
| `border-right: 1px;` | `border-inline-end: 1px;` | `border-e` |

```html
<!-- La balise html définit la direction pour tout le navigateur -->
<html lang="ar" dir="rtl">
  <body class="text-start">
    <div class="ms-4 pe-6">Ce bloc s'inverse automatiquement en miroir en arabe !</div>
  </body>
</html>
```

---

## 💶 4. Formatage International avec l'API Native `Intl`

Ne jamais formater les devises et dates avec des regex. Toujours utiliser l'API standard JavaScript / Python :

```javascript
// Formatage monétaire adapté à la locale du client
const amount = 1450.50;

// En France : "1 450,50 €"
new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(amount);

// Aux États-Unis : "$1,450.50"
new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);

// Formatage de date relative (ex: "il y a 3 jours")
const rtf = new Intl.RelativeTimeFormat('fr', { numeric: 'auto' });
rtf.format(-3, 'day'); // "il y a 3 jours"
```

---

## 🔍 5. SEO Multilingue & Balises `hreflang`

Pour éviter que Google pénalise ton site pour contenu dupliqué et pour diriger chaque internaute vers sa langue maternelle :

```html
<link rel="alternate" hreflang="fr" href="https://yourdomain.com/fr/pricing" />
<link rel="alternate" hreflang="en" href="https://yourdomain.com/en/pricing" />
<link rel="alternate" hreflang="de" href="https://yourdomain.com/de/pricing" />
<link rel="alternate" hreflang="x-default" href="https://yourdomain.com/en/pricing" />
```

---

## 🛠️ 6. Générateur Déterministe de Pseudo-Localisation

Un outil CLI Python est inclus pour tester la résistance de vos interfaces aux textes longs (+30%) et repérer instantanément les chaînes restées en anglais :
```bash
python scripts/pseudo_localize.py locales/en.json -o locales/en.pseudo.json
```
Préserve les variables d'interpolation (`{name}`, `%s`), ajoute des caractères accentués (`Ħééllôô Wôôrld`) et encadre le texte de marqueurs `[!!! ... !!!]`.
