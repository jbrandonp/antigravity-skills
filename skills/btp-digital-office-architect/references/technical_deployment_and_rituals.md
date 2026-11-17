# PROTOCOLE DE DÉPLOIEMENT TECHNIQUE, RITUELS OPÉRATIONNELS & ROADMAP
## Référence Technique : Prise en Main Quick Assist, Épinglage Mobile, Rituel Vendredi 16h30 & Roadmap 14 Jours

---

## 1. PROTOCOLE D'INSTALLATION TECHNIQUE À DISTANCE (QUICK ASSIST)

Pour éviter les déplacements chronophages et coûteux sur les chantiers, 95 % des installations s'effectuent à distance via l'outil natif de Windows : **Assistance Rapide (Quick Assist)**.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   DÉPLOIEMENT À DISTANCE EN 4 ÉTAPES                   │
│                                                                        │
│  [ Étape 1 : Connexion ] ➔ [ Étape 2 : Configuration & Formules ]       │
│                                     │                                  │
│  [ Étape 4 : Raccourci Mobile ]  [ Étape 3 : Verrouillage BTP2026 ]   │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.1 Pré-requis Techniques
* Un PC sous Windows 10 ou 11 connecté à Internet (côté artisan).
* Microsoft Excel 2016, 2019, 2021 ou Microsoft 365 installé.
* Le dossier `05_Outils_et_Modeles_Excel/` prêt sur votre poste.

### 1.2 Étape 1 : Établissement de la Prise en Main (5 Minutes)
1. Téléphoner à l'artisan ou à son assistante au bureau à l'heure convenue (7h15 le matin ou 17h00).
2. Lui faire presser simultanément : `Touche Windows + Ctrl + Q`.
3. Sur votre PC, ouvrir Assistance Rapide et cliquer sur **« Aider une personne »** pour générer un **code de sécurité à 6 chiffres** (valable 10 minutes).
4. Dicter le code à l'artisan qui le tape dans son champ et clique sur **« Partager l'écran »**.
5. L'artisan confirme le partage. Vous prenez le contrôle complet de la souris et du clavier.

### 1.3 Étape 2 : Installation & Personnalisation du Modèle (15 Minutes)
1. Créer sur le bureau de l'artisan un dossier intitulé : `01_BUREAU_NUMERIQUE_BTP`.
2. Si l'artisan possède OneDrive ou Google Drive, créer ce dossier **à l'intérieur du cloud synchronisé** pour garantir des sauvegardes automatiques.
3. Copier le fichier `DEVIS_SANS_OUBLI_MODELE_PRO.xlsx` dans ce dossier.
4. Ouvrir le fichier sous Excel.
5. Personnaliser la ligne 2 de la feuille `Suivi des Devis` : indiquer la raison sociale exacte de l'entreprise, son numéro de téléphone et son email.
6. Vérifier la date du jour affichée dans la cellule d'en-tête (formule `=TODAY()`).

### 1.4 Étape 3 : Audit de Sécurité & Protection des Formules (5 Minutes)
1. Vérifier que la feuille est bien protégée par le mot de passe standard `BTP2026`.
2. **Tester les cellules déverrouillées :**
   - Cliquer sur la cellule A12 (`N° Devis`) et taper `DEV-2026-001` : la saisie doit fonctionner.
   - Cliquer sur la cellule B12 (`Date Émission`) et taper une date : la saisie doit fonctionner.
   - Cliquer sur la cellule H12 (`Date Relance Prévue`) : la date cible se calcule automatiquement à J+14.
   - Cliquer sur la cellule I12 (`Statut Relance`) et tenter de modifier : **Excel doit afficher un message de verrouillage**.
   *(Règle d'or : Les colonnes 1 à 8, 10 et 11 sont libres de saisie ; seule la colonne 9 est blindée).*
3. Créer un raccourci direct sur le bureau Windows : Clic droit sur le fichier ➔ `Envoyer vers` ➔ `Bureau (créer un raccourci)`. Renommer l'icône : **« 📊 SUIVI DEVIS & RELANCES »**.

### 1.5 Étape 4 : Épinglage du Raccourci Smartphone (10 Minutes)
Sur le téléphone du patron et/ou de la secrétaire :
* **Sur iPhone (Safari) :**
  1. Ouvrir dans Safari le lien de saisie rapide (fichier OneDrive web ou formulaire PWA).
  2. Toucher l'icône de partage carrée avec la flèche vers le haut.
  3. Sélectionner **« Sur l'écran d'accueil »**.
  4. Nommer le raccourci **« 📲 NOUVEAU DEVIS »** et valider.
* **Sur Android (Google Chrome) :**
  1. Ouvrir le lien dans Chrome.
  2. Toucher les 3 points verticaux en haut à droite.
  3. Sélectionner **« Ajouter à l'écran d'accueil »** ou **« Installer l'application »**.
  4. Valider l'icône.

---

## 2. LE RITUEL D'ADOPTION DU VENDREDI 16H30 (15 MINUTES CHRONO)

Sans rituel ancré, un tableau Excel est abandonné en moins de 3 semaines.  
Le Bureau Numérique BTP instaure une habitude hebdomadaire non négociable le vendredi en fin d'après-midi :

```
┌────────────────────────────────────────────────────────────────────────┐
│                   LE RITUEL DU VENDREDI 16H30 (15 MIN)                 │
├───────────────┬────────────────────────────────────────────────────────┤
│ Minute 0 – 2  │ 1. OUVRIR LE FICHIER                                   │
│               │ Double-clic sur l'icône de bureau. Constater le        │
│               │ Chiffre d'Affaires en attente sur le Tableau de Bord.  │
├───────────────┼────────────────────────────────────────────────────────┤
│ Minute 2 – 5  │ 2. CLÉBRER LES VICTOIRES (VERT)                        │
│               │ Passer en statut « Accepté » les devis validés de la   │
│               │ semaine. Constater la hausse du CA Gagné.              │
├───────────────┼────────────────────────────────────────────────────────┤
│ Minute 5 – 10 │ 3. ISOLER LES URGENCES (ROUGE)                         │
│               │ Repérer les lignes clignotant en rouge :               │
│               │ « À RELANCER D'URGENCE » (devis sans nouvelle > 14j).  │
├───────────────┼────────────────────────────────────────────────────────┤
│ Minute 10 – 15│ 4. PASSER LES 3 COUPS DE FIL GAGNANTS                  │
│               │ Appeler directement les 3 clients chauds avec le script│
│               │ direct : « Bonjour M. [Nom], je prépare mon planning de│
│               │ la semaine prochaine, je voulais savoir si vous        │
│               │ validiez pour qu'on vous réserve la date. »            │
└───────────────┴────────────────────────────────────────────────────────┘
```

> **Bénéfice Psychologique Immédiat :** L'artisan part en week-end l'esprit libéré, sans culpabilité ni peur d'avoir oublié un client. Le dimanche à table ne tourne plus autour de la gestion des devis.

---

## 3. FEUILLE DE ROUTE OPÉRATIONNELLE : LES 14 PREMIERS JOURS

### Semaine 1 : Sécurisation & Amorçage Commercial
* **Jour 1 (Lundi) :** Dépôt de la candidature officielle Smart Liège (lettre, attestation student@work 600h, certificat promotion sociale, carte d'identité).
* **Jour 2 (Mardi) :** Tests techniques unitaires (`python 06_Tests_et_Qualite/test_btp_suite.py`) et simulation Quick Assist.
* **Jour 3 (Mercredi) :** Qualification fine des 5 prospects locaux dans `FICHIER_PROSPECTION_LIEGE_BTP.xlsx`.
* **Jour 4 (Jeudi 6h45) :** Infiltration des comptoirs pros (Facq, Rexel) pour nouer contact avec les patrons au café.
* **Jour 5 (Vendredi 16h30) :** Envoi des 5 vocaux WhatsApp personnalisés de 25 secondes.

### Semaine 2 : Diagnostic, Closing & Déploiement
* **Jour 6-7 (Lundi-Mardi) :** Réalisation de 2 diagnostics gratuits de 15 minutes en direct sur les vrais chiffres du patron.
* **Jour 8 (Mercredi) :** Signature du premier bon de commande officiel (Pack Découverte à 250 € HTVA) et encaissement de l'acompte de 50 % (151,25 € TTC).
* **Jour 9 (Jeudi avant minuit) :** Encodage de la déclaration Dimona préalable sur le portail Smart Liège.
* **Jour 10 (Vendredi) :** Installation à distance via Quick Assist (45 min), encodage des devis récents et première session du Rituel 16h30. Encaissement du solde.

---

## 4. GUIDE DE SOUMISSION DE DOSSIER CHEZ SMART LIÈGE

Pour lancer l'activité en parfaite conformité légale au sein de la coopérative Smart :

### 4.1 Composition Obligatoire du Dossier de Candidature
1. **Dossier de candidature rempli :** issu de `02_Candidature_Smart_Liege/DOSSIER_CANDIDATURE_SMART_LIEGE.md`.
2. **Attestation Student@work (ONSS) :** téléchargée sur [studentatwork.be](https://www.studentatwork.be) via Itsme, attestant du solde disponible sur le contingent des 600 heures annuelles.
3. **Attestation d'inscription scolaire :** délivrée par l'établissement de promotion sociale, mentionnant explicitement le nombre d'heures de cours ou crédits hebdomadaires.
4. **Copie recto-verso de la carte d'identité électronique belge (eID).**
5. **Relevé d'identité bancaire personnel (RIB).**

### 4.2 Les 4 Règles Inviolables de Smart
1. **Plancher de facturation :** Minimum **250,00 € HTVA** par commande (pour couvrir le RMMMG journalier de la CP 200).
2. **Déclaration Dimona préalable :** Toujours déclarer la prestation sur le portail Smart **la veille du jour de travail avant minuit**. Tout travail rétroactif expose à de lourdes sanctions de l'ONSS.
3. **Interdiction d'achat pour revente :** Smart interdit d'acheter des licences ou du matériel pour les refacturer avec marge.
4. **Taux de TVA normal (21 %) :** Appliquer obligatoirement 21 % sur toutes les prestations informatiques et organisationnelles (le taux 6 % est réservé aux travaux immobiliers).
