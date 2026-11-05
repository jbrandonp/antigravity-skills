# Manuel d'Adaptation Métier & Matrice Sectorielle Universelle
## Le Squelette Administratif pour TPE & PME Tous Secteurs

> Ce guide constitue la clé de voûte du **Bureau Numérique Universel**. Il détaille comment instancier le squelette administratif, commercial, juridique et technique sur n'importe quel secteur d'activité sans jamais réinventer la roue.

---

## 🏛️ 1. LE SQUELETTE UNIVERSEL : LA LOI D'AIRAIN DES PETITES ENTREPRISES

Peu importe qu'un entrepreneur pose des pompes à chaleur, développe des applications web, répare des boîtes de vitesses ou traite des douleurs lombaires, **95 % de sa pathologie administrative est rigoureusement identique** :

1. **La fuite du chiffre d'affaires en amont :** L'entrepreneur est sur le terrain ou en production. Il envoie un prix, un devis ou une proposition, puis replonge dans son travail. Faute de relance structurée sous 7 à 14 jours, **30 % à 45 % des propositions sont oubliées** ou remportées par un concurrent plus rapide.
2. **Le piège du SaaS lourd ("L'usine à gaz") :** Les éditeurs de logiciels (Salesforce, HubSpot, Odoo, Vertuoza, Bouwsoft) tentent d'imposer des abonnements récurrents de 100 à 300 €/mois exigeant 20 champs obligatoires par fiche. Dans une structure de 1 à 10 personnes, l'outil est abandonné au bout de 90 jours au profit d'un carnet papier ou de notes éparpillées sur WhatsApp.
3. **Le chaos du vendredi et la panique trimestrielle :** En l'absence d'un rituel hebdomadaire court (15 minutes chrono), les justificatifs, factures et notes de frais s'empilent dans la boîte à gants ou les e-mails, jusqu'au coup de pression du comptable avant la clôture TVA.
4. **L'obligation Peppol 2026 :** La directive européenne et la législation belge imposent la facturation électronique structurée XML UBL (Peppol) à **toutes les entreprises assujetties en B2B**, sans distinction de métier.
5. **Le bouclier juridique absent :** Devis signés par SMS sans acompte, absence de limitation de responsabilité, acceptation de demandes hors périmètre sans facturation ("scope creep").

Le Bureau Numérique résout cette équation en fournissant un **moteur universel à 4 piliers** (Légal/Socio-fiscal, Fichier ergonomique anti-SaaS, Prospection guérilla, et Déploiement/Automatisation) personnalisable par un fichier de profilage sectoriel.

---

## 📊 2. LA MATRICE COMPARATIVE DES 6 PROFILS SECTORIELS

| Profil Sectoriel | Secteurs Cibles | Terme Document | Délai Relance Idéal | Régime TVA (Belgique) | Canal Guérilla Prioritaire |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. BTP & Artisans du Bâtiment** | Plomberie, Chauffage, Élec, Rénovation, Toiture, Menuiserie | **Devis de travaux** / Métré | **J+14** (temps de réflexion & devis comparatifs) | 6 % (logement > 10 ans) ou 21 % (neuf/tertiaire) | Comptoirs pros à 7h00 (Facq, Rexel, Cebeo) |
| **2. Services & Agences / Freelances** | Dev web, Graphisme, SEO, Conseil, Formation, Rédacteurs | **Proposition commerciale** / Lettre de mission | **J+7** (cycle B2B réactif, validation budgétaire) | 21 % standard | Réseau LinkedIn, Coworkings, Prescripteurs |
| **3. Garages & Maintenance Technique** | Réparation auto, Dépannage informatique, HVAC pro, Outillage | **Ordre de réparation (OR)** / Devis pièces & MO | **J+3** (urgence technique : machine ou véhicule bloqué) | 21 % standard | Visites directes atelier entre 11h30 et 13h00 |
| **4. Santé, Paramédical & Bien-être** | Kinés, Ostéos, Psy, Salles de sport privées, Esthétique | **Plan de soins** / Devis forfait ou cure | **J+5** (renouvellement de séance, prise de décision) | 0 % exonéré (Art. 44) ou 21 % (soins esthétiques) | Cabinets de groupe, Doctena, Réseau local |
| **5. Commerce B2B & Grossistes Locaux** | Boulangerie pro, Torréfacteurs, Fournisseurs horeca, Brasseries | **Bon de commande récurrent** / Devis volume | **J+5** (réassortiment hebdomadaire / saisonnier) | 6 % (alimentaire de base) à 21 % (boissons/matériel) | Marchés matinaux, Visite des gérants sur site |
| **6. Immobilier, Géomètres & Syndics** | Géomètres-experts, Diagnostiqueurs PEB, Petits syndics, Chasseurs | **Lettre de mission** / Devis diagnostic | **J+10** (rythme des compromis de vente & notaires) | 21 % standard | Études notariales, Agences immobilières |

---

## 🔍 3. DÉTAIL ENRICHI PAR PROFIL SECTORIEL

---

### Profil 1 : BTP & Artisans du Bâtiment
* **Psychologie du Dirigeant :** Homme/femme de chantier, debout dès 6h00, déteste l'ordinateur le soir. Sa priorité absolue est le chantier et l'approvisionnement des équipes.
* **Architecture des Colonnes du Suivi :**
  `N° Devis` | `Date Émission` | `Nom Client` | `Téléphone` | `Chantier / Adresse` | `Montant HTVA (€)` | `Statut` | `Date Relance (J+14)` | `Statut Relance (Auto)` | `Dernier Contact` | `Commentaires`
* **Formule de Relance Cible :** `=IF(B12="","",B12+14)`
* **Phrase d'Accroche WhatsApp (25 sec) :**
  > *« Bonjour Monsieur [Nom], Brandon à l'appareil. Je vois vos camionnettes tourner sur la région. Je ne vends aucun logiciel : j'aide simplement les chauffagistes et artisans du coin à récupérer les devis oubliés le soir en 15 minutes le vendredi avec leur Excel actuel. On peut en parler 5 minutes autour d'un café à votre atelier ? »*
* **Objection Reine & Riposte :**
  * *« Ma femme gère les papiers le soir. »*
  * ➔ *« Justement : au lieu d'y passer 2 heures, le système lui classe les 3 clients chauds à appeler en 10 minutes pour que vous retrouviez vos week-ends. »*

---

### Profil 2 : Services Professionnels, Agences & Conseil
* **Psychologie du Dirigeant :** Souvent indépendant ou petite équipe de 2 à 5 personnes. Très digitalisé mais souffre du syndrome du "cordonnier mal chaussé" : excellent pour ses clients, chaotique sur son propre suivi commercial par pudeur ou peur d'être insistant.
* **Architecture des Colonnes du Suivi :**
  `Réf Proposition` | `Date Envoi` | `Entreprise / Contact` | `E-mail & Téléphone` | `Objet de la Mission` | `Budget Estimé HTVA (€)` | `Statut` | `Date Relance (J+7)` | `Statut Relance (Auto)` | `Dernière Interaction` | `Prochaine Étape`
* **Formule de Relance Cible :** `=IF(B12="","",B12+7)`
* **Canal Guérilla Prioritaire :** Message LinkedIn personnalisé ou e-mail ciblé au fondateur :
  > *« Bonjour [Prénom], en tant qu'agence / consultant, on passe souvent des heures à soigner une proposition pour ensuite la laisser refroidir faute de relance méthodique. J'installe un cockpit ultra-léger sur ton Google Sheets / Excel qui automatise la relance douce de tes offres en 15 min le vendredi. Si tu veux voir la démo en 10 min sur tes chiffres, dis-moi ! »*
* **Objection Reine & Riposte :**
  * *« J'utilise déjà Notion ou Trello mais je ne le tiens pas à jour. »*
  * ➔ *« C'est le problème classique : Notion est trop malléable et demande trop d'énergie. Mon modèle Excel est verrouillé, calcule vos métriques clés instantanément et ne vous demande que 2 colonnes à remplir. »*

---

### Profil 3 : Garages Automobiles & Maintenance Technique
* **Psychologie du Dirigeant :** Chef d'atelier sous pression permanente. Les véhicules ou machines occupent de l'espace physique au sol. Chaque heure sans accord client sur un devis de réparation bloque un pont élévateur ou une baie d'atelier.
* **Architecture des Colonnes du Suivi :**
  `N° Fiche / OR` | `Date Dépôt` | `Propriétaire` | `Immatriculation / Modèle` | `Nature Travaux / Pièces` | `Devis Réparation HTVA (€)` | `Statut Accord` | `Date Relance (J+3)` | `Statut Relance (Auto)` | `Téléphone Mobile` | `Pièces Commandées (O/N)`
* **Formule de Relance Cible :** `=IF(B12="","",B12+3)` (Cycle court impératif).
* **Canal Guérilla Prioritaire :** Passage direct au comptoir du garage entre 11h45 et 12h30 avec une tablette ou fiche type.
* **Objection Reine & Riposte :**
  * *« Mon logiciel de garage gère déjà la facturation. »*
  * ➔ *« Votre logiciel fait la facture quand la voiture est terminée, mais il ne vous alerte pas sur les 5 clients qui n'ont pas encore validé le remplacement de courroie ou de turbo depuis mardi. C'est là que dorment vos ponts élévateurs ! »*

---

### Profil 4 : Professions Libérales, Paramédical & Bien-être
* **Psychologie du Dirigeant :** Praticien centré sur le patient/client. Aversion marquée pour les démarches "commerciales agressives". Besoin de courtoisie, de déontologie et de respect strict du secret professionnel (RGPD de santé).
* **Architecture des Colonnes du Suivi :**
  `ID Dossier` | `Date Premier Bilan` | `Patient / Client (Pseudonymisé)` | `Coordonnées` | `Protocole de Soins / Forfait` | `Honoraires Prévus (€)` | `Statut Accord` | `Date Rappel Suivi (J+5)` | `Statut Relance (Auto)` | `Canal Préféré (SMS/Mail)` | `Commentaires Thérapeutiques`
* **Formule de Relance Cible :** `=IF(B12="","",B12+5)`
* **Régime Fiscal :** Attention à l'exonération de TVA (Art. 44 du Code TVA belge pour les actes médicaux/paramédicaux reconnus). Les actes d'esthétique pure ou de coaching bien-être relèvent de la TVA 21 %.
* **Objection Reine & Riposte :**
  * *« Je ne veux pas harceler mes patients, ce n'est pas éthique. »*
  * ➔ *« Il ne s'agit pas de vendre, mais d'assurer la continuité de leurs soins. Un patient qui oublie de planifier sa deuxième série de séances risque une rechute. Le système prépare un SMS bienveillant de suivi médical sans aucune pression commerciale. »*

---

### Profil 5 : Commerce B2B, Artisans de Bouche & Grossistes Locaux
* **Psychologie du Dirigeant :** Rythme de production intense (tôt le matin pour les métiers de bouche, tournées de livraison l'après-midi). Marges serrées, volume récurrent.
* **Architecture des Colonnes du Suivi :**
  `Code Client B2B` | `Date Dernière Commande` | `Établissement (Resto/Hôtel)` | `Contact Gérant` | `Panier Moyen Type (€)` | `CA Mensuel Estimé (€)` | `Statut Commande` | `Date Relance Réassort (J+5)` | `Statut Alerte (Auto)` | `Fréquence Hebdo` | `Notes Préférences`
* **Formule de Relance Cible :** `=IF(B12="","",B12+5)`
* **Alerte Décroissance :** Si un client régulier ne commande pas durant son cycle habituel, la ligne s'allume en rouge pour déclencher un appel réassortiment immédiat.
* **Objection Reine & Riposte :**
  * *« Mes clients commandent par WhatsApp ou téléphone quand ils ont besoin. »*
  * ➔ *« Exactement, et quand un chef de restaurant change ou est débordé, il oublie de commander chez vous et prend chez Metro ou un grossiste industriel. L'alerte vous permet de lui envoyer un petit message avant son rush du week-end. »*

---

### Profil 6 : Immobilier, Géomètres & Services Fonciers
* **Psychologie du Dirigeant :** Expert technique ou juriste de terrain. Dépendance directe aux notaires et aux cycles de vente immobilière (délais d'attente de compromis, conditions suspensives de crédit).
* **Architecture des Colonnes du Suivi :**
  `Réf Mission` | `Date Demande` | `Donneur d'Ordre (Notaire/Particulier)` | `Adresse Bien / Parcelle` | `Nature (PEB/Bornage/Estim)` | `Montant Forfait HTVA (€)` | `Statut Accord` | `Date Relance Notaire (J+10)` | `Statut Relance (Auto)` | `Téléphone Étude` | `Date Signature Prévue`
* **Formule de Relance Cible :** `=IF(B12="","",B12+10)`
* **Objection Reine & Riposte :**
  * *« C'est le notaire qui décide du rythme, on ne peut pas forcer. »*
  * ➔ *« On ne force pas le notaire : on donne à son clerc un état clair de votre dossier pour qu'il le glisse au sommet de la pile avant la signature définitive. »*

---

## 🛠️ 4. LE BON DE COMMANDE ET CGV MODULAIRES TOUS SECTEURS

Chaque dossier de vente de Bureau Numérique s'appuie sur le même contrat d'une page (`BON_DE_COMMANDE_PROPOSITION_COMMERCIALE.md`) doté de **9 clauses de protection universelles** :

1. **Clause 1 — Obligation de Moyens :** Le prestataire fournit une organisation rigoureuse et des outils configurés. Il n'est en aucun cas responsable du taux de conversion final ou du chiffre d'affaires signé par le client.
2. **Clause 2 — Plafond de Responsabilité :** En cas de litige, la responsabilité du prestataire est expressément plafonnée aux montants nets effectivement perçus pour la prestation incriminée.
3. **Clause 3 — Protection contre l'Explosion du Périmètre (Scope Creep) :** L'installation initiale comprend l'importation ou la saisie de maximum **50 dossiers/devis/contacts historiques**. Tout volume supérieur fait l'objet d'un forfait complémentaire.
4. **Clause 4 — Garantie d'Ajustement de 14 Jours :** Toutes les modifications de formules ou d'ergonomie sont gratuites pendant les 14 premiers jours d'utilisation.
5. **Clause 5 — Créneaux de Support Dédiés (SLA Asynchrone) :** Support par message vocal/écrit WhatsApp ou e-mail traité sous 24h ouvrées durant les plages réservées (ex. 7h30–8h30 et 17h00–18h30). Pas d'assistance téléphonique temps réel interrompant la production.
6. **Clause 6 — Conformité RGPD & Zéro Rétention Locale :** Le client reste Responsable de Traitement. Le prestataire agit en sous-traitant technique sans stocker les données clients sur ses machines personnelles au-delà de la mission de configuration.
7. **Clause 7 — Conditions de Paiement 50/50 :** Acompte de 50 % à la commande pour réserver l'intervention, solde de 50 % à la remise des accès et mot de passe de protection.
8. **Clause 8 — Indépendance des Outils Tiers :** Le prestataire configure les outils existants du client (Excel, Microsoft 365, Google Workspace). Les abonnements à ces plateformes sont payés directement par le client à leurs éditeurs respectifs.
9. **Clause 9 — Non-Divulgation & Droit de Propriété :** Le client bénéficie d'un droit d'usage perpétuel sur son classeur configuré, mais les scripts et méthodologies d'automatisation propriétaires restent la propriété intellectuelle du concepteur.

---

## ⚙️ 5. SPÉCIFICATION TECHNIQUE DES OUTILS CLI UNIVERSELS

Les scripts Python du dossier `scripts/` doivent implémenter l'argument `--sector` afin d'adapter dynamiquement :
* Les libellés d'en-tête du tableur Excel généré.
* Le délai par défaut de calcul de la relance (14j pour BTP, 7j pour Services, 3j pour Garages, 5j pour Commerce/Santé, 10j pour Immo).
* Les données de démonstration injectées pour la prise en main client.
* Les scripts de relance rédigés automatiquement le vendredi.

Tous les scripts doivent être typés de façon stricte (zéro `Any`), compatibles UTF-8 sous Windows PowerShell, et exécutables directement en environnement natif Python 3.12 (uv/venv).
