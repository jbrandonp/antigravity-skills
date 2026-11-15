# Moteur de Carrousel Documentaire LinkedIn (PDF 1080x1350)

> **Pourquoi le Carrousel est le Format Roi** : Un document post (carrousel PDF) génère le **Dwell Time le plus élevé de tout LinkedIn**, car chaque swipe est enregistré comme une interaction positive par l'algorithme, contrairement au simple défilement vertical.

---

## 📐 Spécifications Techniques

- **Format** : Document PDF téléversé sur LinkedIn.
- **Dimensions Recommandées** : **1080 x 1350 pixels (Ratio 4:5)** pour occuper le maximum de surface d'écran sur mobile.
- **Nombre de Slides Idéal** : **8 à 12 slides**.
  - *Moins de 8* : Ce n'est pas un carrousel, c'est un post texte découpé inutilement.
  - *Plus de 12* : Le taux de complétion s'effondre dramatiquement.

---

## 🏛️ L'Architecture Standard en 5 Rôles de Slides

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. COVER (Slide 1)       : L'accroche majeure (< 6 mots) + 1 ligne promesse │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. THE STAKE (Slide 2)   : Pourquoi ce problème vous coûte de l'argent/temps│
├─────────────────────────────────────────────────────────────────────────────┤
│ 3 à N. STEP-BY-STEP      : 1 SEULE idée par slide. Titre + < 25 mots de corps│
├─────────────────────────────────────────────────────────────────────────────┤
│ N+1. LE RÉCAPITULATIF    : La vue d'ensemble conçue pour être capturée (Écran)│
├─────────────────────────────────────────────────────────────────────────────┤
│ DERNIÈRE. L'APPEL UNIQUE : 1 seule action (Lien en bio / DM / Commentaire)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📝 Règles Typographiques & Rédactionnelles

1. **Slide 1 fait 80 % du travail** : Si la couverture ne donne pas envie de swiper, personne ne verra la slide 2. Police imposante (taille 60-72px), contraste maximal.
2. **Moins de 25 mots par slide** : Si vous avez besoin d'un paragraphe entier pour expliquer votre point, c'est que votre slide contient 2 idées. Scindez-la.
3. **Numéroter chaque slide visiblement (`3/10`)** : La complétion augmente de 25 % quand le lecteur sait exactement où il en est.
4. **La Slide de Récap est la plus partagée** : Créez une slide de synthèse épurée avec les 5 points clés. C'est celle que les lecteurs sauvegardent et capturent en photo.
5. **Votre pseudo / handle en bas de chaque slide** : Les captures d'écran voyagent sans votre nom si vous ne l'inscrivez pas discrètement dans un coin.

---

## 💻 Template HTML / CSS Prêt pour Conversion PDF

Vous pouvez générer directement le PDF via Chrome Headless (`chrome --headless --print-to-pdf=carrousel.pdf carrousel.html`) :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
  @page {
    size: 1080px 1350px;
    margin: 0;
  }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #0f172a;
    color: #f8fafc;
  }
  .slide {
    width: 1080px;
    height: 1350px;
    page-break-after: always;
    box-sizing: border-box;
    padding: 120px 100px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
  }
  .slide-header {
    font-size: 28px;
    font-weight: 600;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 2px;
  }
  .slide-content h1 {
    font-size: 64px;
    line-height: 1.15;
    margin-bottom: 30px;
    font-weight: 800;
  }
  .slide-content p {
    font-size: 34px;
    line-height: 1.4;
    color: #94a3b8;
    max-width: 850px;
  }
  .slide-footer {
    display: flex;
    justify-content: space-between;
    font-size: 24px;
    color: #64748b;
    border-top: 1px solid #1e293b;
    padding-top: 30px;
  }
</style>
</head>
<body>
  <!-- Slide 1 : Cover -->
  <section class="slide">
    <div class="slide-header">Guide Architecture</div>
    <div class="slide-content">
      <h1>Pourquoi SQLite bat PostgreSQL en local.</h1>
      <p>Et comment économiser 400 €/mois d'infrastructure sans perdre 1 transaction.</p>
    </div>
    <div class="slide-footer">
      <span>@jbrandonp</span>
      <span>1/9 →</span>
    </div>
  </section>
  <!-- Répéter les sections pour chaque slide -->
</body>
</html>
```
