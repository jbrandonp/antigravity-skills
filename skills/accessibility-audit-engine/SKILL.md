---
name: accessibility-audit-engine
description: >-
  Automated and manual accessibility testing engine enforcing WCAG 2.2 Level AA/AAA and European Accessibility Act (EAA) compliance. Integrates axe-core, Pa11y CLI, ARIA pattern validation, keyboard focus trap detection, and screen reader compatibility audits.
---

# ♿ Accessibility (a11y) Audit Engine & WCAG 2.2 Compliance

> **Standard :** W3C WCAG 2.2 Level AA/AAA & European Accessibility Act (EAA 2025/2026)  
> **Core Axiom :** *"Accessibility is not an afterthought or an optional toggle—it is a core software quality requirement and a legal obligation. Audit every interactive component for keyboard navigation, contrast ratios, visible focus, and screen reader announcements."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

L'accessibilité web (souvent abrégée **a11y** car il y a 11 lettres entre le 'a' et le 'y'), c'est faire en sorte que ton application soit utilisable par **100% des êtres humains**, y compris :
- Une personne aveugle qui utilise un lecteur d'écran (VoiceOver sur Mac/iPhone, NVDA sur Windows) qui lit le site à voix haute.
- Une personne qui a un bras cassé ou un handicap moteur et ne peut pas utiliser de souris (elle navigue uniquement avec la touche `Tab` et `Entrée` de son clavier).
- Une personne malvoyante ou en plein soleil sur son téléphone qui a besoin d'un fort contraste de couleur pour lire le texte.

Si ton bouton n'a pas de texte ou est un simple `<div>` sans rôle ARIA ni écouteur clavier, le lecteur d'écran dit juste *"Bouton vide"* et l'utilisateur est totalement bloqué.

---

## 📐 2. Les Règles Critiques de WCAG 2.2 AA

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Contraste de Couleur : Minimum 4.5:1 (Texte normal)      │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Navigation 100% Clavier : Zéro piège de focus (Tab/Shift)│
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Indicateur de Focus Visible (WCAG 2.2 Focus Appearance)  │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Cibles Tactiles : Min 24x24 px (WCAG 2.2), 44x44 px (HIG)│
 ├─────────────────────────────────────────────────────────────┤
 │ 5. Régions Dynamiques : aria-live="polite" pour les alertes │
 └─────────────────────────────────────────────────────────────┘
```

> **Normes des cibles tactiles (Touch Targets) :**
> - **WCAG 2.2 (Critère 2.5.8 AA)** : 24x24 px CSS minimum avec espacement suffisant.
> - **Apple Human Interface Guidelines (HIG)** : 44x44 pt minimum.
> - **Google Material Design 3** : 48x48 dp minimum.

---

## 🛠️ 3. Boîte à Outils Déterministe WAT (Scripts Python Autonomes)

La compétence embarque des outils déterministes natifs en Python standard (sans dépendance externe) pour automatiser les vérifications mathématiques et syntaxiques :

### 🎨 A. Calculateur de Contraste W3C & Suggestion Auto (`calc_color_contrast.py`)
Calcule la luminance relative W3C et les ratios exacts selon la formule :
$$L = 0.2126 \cdot R + 0.7152 \cdot G + 0.0722 \cdot B$$
$$Ratio = \frac{L_1 + 0.05}{L_2 + 0.05}$$

```bash
# Vérifier une paire de couleurs avec suggestion de correction automatique
python scripts/calc_color_contrast.py --fg "#999999" --bg "#FFFFFF" --suggest

# Sortie JSON pour intégration CI/CD
python scripts/calc_color_contrast.py --fg "#2563EB" --bg "#FFFFFF" --json

# Auditer une palette complète définie dans un fichier JSON
python scripts/calc_color_contrast.py --palette palette.json
```

### 🏷️ B. Validateur des Patterns WAI-ARIA 1.2 (`audit_aria_patterns.py`)
Scanne les composants interactifs complexes pour éliminer les violations WAI-ARIA courantes :
- **Modales (`role="dialog"`)** : Exige `aria-modal="true"` et un label accessible (`aria-labelledby` ou `aria-label`).
- **Onglets (`role="tab"`)** : Exige `aria-selected` et `aria-controls`.
- **Accordéons / Tiroirs** : Exige `aria-expanded="true|false"`.
- **Faux Boutons (`<div onclick>`)** : Détecte les divs cliquables sans `role="button"` ni `tabindex="0"`.
- **Redondance ARIA** : Alerte sur `<button role="button">` ou `<nav role="navigation">`.

```bash
python scripts/audit_aria_patterns.py path/to/template.html --json
```

### 🔍 C. Scanner d'Accessibilité HTML Hors-Ligne (`audit_html_a11y.py`)
Analyseur de structure HTML vérifiant :
- Présence et format de la balise `<html lang="...">`.
- Présence et non-redondance du texte `alt` sur les balises `<img>`.
- Association obligatoire des labels (`<label for="...">`) aux `<input>`, `<select>` et `<textarea>`.
- Détection des `tabindex` positifs destructeurs de l'ordre naturel de tabulation.
- Détection des doublons d'identifiants (`id="..."`).
- Validation de la hiérarchie des titres (interdiction de sauter de `<h1>` à `<h3>`).
- Sécurité et accessibilité des liens externes (`target="_blank"` avec `rel="noopener noreferrer"`).

```bash
python scripts/audit_html_a11y.py path/to/index.html --json
```

---

## 🛠️ 4. Automatisation des Audits E2E (Pa11y & Axe-Core)

### Exécution d'un Audit Pa11y en Ligne de Commande
```bash
# Scanner une URL locale ou distante selon WCAG 2.2 AA
npx pa11y http://localhost:3000 --standard WCAG2AA --reporter cli

# Générer un rapport JSON complet pour l'intégration CI/CD
npx pa11y http://localhost:3000 --standard WCAG2AA --reporter json > a11y-report.json
```

### Script de Validation Automatisée Playwright + axe-core
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('Vérification de conformité a11y WCAG 2.2 AA', async ({ page }) => {
  await page.goto('http://localhost:3000/dashboard');

  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

---

## 📋 5. Checklist d'Audit Manuel des Composants

1. **Test de la Touche Tab (Navigation Pure Clavier)** :
   - Débranche ta souris et parcours toute l'application avec `Tab`, `Shift+Tab` et `Espace`/`Entrée`.
   - Peux-tu ouvrir et fermer tous les menus déroulants et toutes les fenêtres modales ?
   - L'indicateur de focus bleu/noir est-il toujours visible sur chaque élément actif ?
   - Quand une boîte modale s'ouvre, le focus est-il piégé à l'intérieur (`focus trap`) et la touche `Échap` la ferme-t-elle ?
2. **Attributs ARIA Indispensables** :
   - Boutons avec seulement une icône $\rightarrow$ `aria-label="Fermer la fenêtre"` obligatoire.
   - Icônes décoratives à côté d'un texte visible $\rightarrow$ `aria-hidden="true"` obligatoire.
   - Messages d'erreur sous un champ de formulaire $\rightarrow$ reliés par `aria-describedby="error-email"`.
   - Notifications toast ou bannières $\rightarrow$ `role="status"` ou `aria-live="polite"` pour avertir les malvoyants sans couper leur lecture.

---

## 📚 6. Références et Guides Détaillés

Pour approfondir les aspects juridiques et les implémentations JavaScript critiques :
- 📖 Consulter le [Guide de Conformité WCAG 2.2 & EAA](references/wcag_eaa_compliance_playbook.md) :
  - **Directive Européenne sur l'Accessibilité (EAA / Directive UE 2019/882)** applicable depuis le 28 juin 2025.
  - Implémentation robuste d'un **Focus Trap JavaScript natif** sans framework.
  - Matrice des raccourcis essentiels pour testeurs sur **NVDA, JAWS, VoiceOver et TalkBack**.
  - Règles d'apparence de focus selon le critère WCAG 2.2 Focus Appearance (2.4.13).
