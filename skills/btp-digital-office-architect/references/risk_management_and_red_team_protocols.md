# Manuel de Gestion des Risques & Protocoles Red Team
## Les 14 Points de Défaillance Critiques du Bureau Numérique & Parades Opérationnelles

> Ce manuel de référence synthétise l'analyse Red Team issue de l'audit critique et des stress-tests de terrain. Il fournit la réponse immédiate et déterministe à chacun des 14 risques opérationnels, juridiques, fiscaux et commerciaux du projet.

---

## 🧭 TABLEAU DE BORD DES 14 RISQUES RED TEAM

| Réf. | Domaine | Risque Identifié | Impact Potentiel | Protocole de Défense Immédiat |
| :---: | :--- | :--- | :---: | :--- |
| **R01** | Commercial | Échec du Cold Email (taux de réponse < 2 %) | Épuisement | Bascule 100 % sur comptoirs pros à 7h et vocaux WhatsApp 25s. |
| **R02** | Opérations | Dérive du périmètre gratuit (Scope Creep) | Taux horaire < 14 € | Barrière stricte des 50 fiches incluses ; 75 €/h au-delà. |
| **R03** | Technique | Conflits de versions OneDrive / Excel | Perte de données | Zonage de cellules verrouillées (`OFFICE2026`), sauvegardes locales. |
| **R04** | Rétention | Churn élevé sur l'abonnement mensuel (15 %) | LTV plafonnée à 400 € | Envoi mensuel systématique du "Rapport Patron" le 1er du mois. |
| **R05** | Juridique | Conflit sur les licences logicielles (M365) | Rejet par Smart | Règle d'or : le client paie directement son abonnement Microsoft/Google. |
| **R06** | Légal | Accusation de perte financière sur devis oublié | Litige judiciaire | Obligation de moyens stricte + plafond de responsabilité au net facturé. |
| **R07** | Socio-fiscal | Refus du contrat étudiant Smart (Promotion sociale) | Net divisé par deux | Bascule sous statut Étudiant-Indépendant (INASTI 2026, 0 € sous 8 687 €). |
| **R08** | Foyer fiscal | Perte du statut "Enfant à charge" des parents | Surcoût fiscal 2 000 € | Plafond strict des ressources nettes annuelles sous 3 980 € - 4 200 €. |
| **R09** | Allocations | Suspension des allocations familiales (FAMIWAL) | Perte de 200 €/mois | Plafonnement strict à 240 heures par trimestre sous contrat salarié. |
| **R10** | Déontologie | Demande récurrente de travail au noir / cash | Risque pénal & fiscal | Argumentation fiscale positive : déductibilité 100 % et récup TVA 21 %. |
| **R11** | Agenda | Conflit entre études (30h) et urgences clients | Burnout étudiant | Créneaux SLA fermés : 7h00-8h00 et 17h00-18h30. Zéro appel en journée. |
| **R12** | Réglementaire | Confusion sur le mandat Peppol 2026 | Perte de crédibilité | Clarification : Peppol s'applique aux factures B2B, pas aux devis. |
| **R13** | Concurrentiel | Pression des éditeurs de logiciels BTP | Perte de prospects | Contre-attaque sur les coûts cachés (865 € de démarrage Bouwsoft). |
| **R14** | Adoption | Abandon du tableur Excel après 3 semaines | Échec mission | Ancrage du Rituel du Vendredi 16h30 + affiche mémo sur le bureau. |

---

## 🔍 PROTOCOLES DÉTAILLÉS PAR SCÉNARIO DE CRISE

---

### R01 — Le Piège du Cold Email : L'Inondation de Spams
* **Cause Racine :** Les artisans et patrons de petites entreprises passent leur journée sur les chantiers, dans leur atelier ou chez leurs clients. Ils ne consultent pas leurs boîtes e-mails génériques (`info@...`), qui sont de toute façon submergées de sollicitations commerciales.
* **Contre-Mesure Opérationnelle :**
  1. Interdire le cold emailing de masse.
  2. Concentrer 80 % des efforts de prospection sur le **créneau 6h45–8h00** aux comptoirs des fournisseurs professionnels locaux (Facq, Rexel, Cebeo, Gedimat). 5 minutes de dialogue direct autour d'un café valent 200 emails.
  3. Pour la prospection à distance, utiliser exclusivement le **vocal WhatsApp de 25 secondes** sur le numéro mobile direct du gérant.

---

### R02 — La Dérive du Périmètre Gratuit (Scope Creep)
* **Cause Racine :** Le patron, soulagé de voir un prestataire informatique compétent, commence à demander de "nettoyer 400 vieux contacts éparpillés", de "réparer l'imprimante wifi" ou de "regarder pourquoi Outlook rame".
* **Contre-Mesure Opérationnelle :**
  1. La proposition commerciale et les CGV fixent une **barrière infranchissable : 50 fiches historiques incluses** au démarrage.
  2. Toute demande hors périmètre déclenche immédiatement la formule diplomatique :
     > *« C'est tout à fait faisable ! Cela sort du pack d'installation initiale. Je peux vous l'intégrer dans le cadre de notre forfait d'accompagnement trimestriel, ou sur un ticket d'intervention complémentaire à 75 € HTVA de l'heure. Quel format préférez-vous ? »*

---

### R03 — Conflits de Version OneDrive et Écran Mobile Brisé
* **Cause Racine :** Une mauvaise connexion 4G sur un chantier ou l'ouverture simultanée du classeur sans verrouillage engendre des conflits de fichiers.
* **Contre-Mesure Opérationnelle :**
  1. Toutes les cellules de formules (colonne 9) sont verrouillées par mot de passe (`OFFICE2026`).
  2. Les colonnes de saisie (1 à 8, 10, 11) restent en saisie libre déverrouillée.
  3. L'artisan sur le terrain utilise un raccourci mobile ultra-léger (PWA) qui n'exige que 3 champs (Nom, Contact, Montant estimé).

---

### R04 — L'Érosion des Abonnements Mensuels (Churn à 15 %)
* **Cause Racine :** Dès que le tableur tourne bien et que les devis sont organisés, le dirigeant a l'impression que "tout fonctionne tout seul" et envisage d'économiser son abonnement de support (60 €/mois ou 180 €/trimestre).
* **Contre-Mesure Opérationnelle :**
  1. Rendre la valeur tangible chaque mois via le **Rapport Patron du 1er du mois** généré par [`generate_patron_report.py`](file:///c:/Users/brand/.agents/skills/digital-office-architect/scripts/generate_patron_report.py).
  2. Le rapport met en évidence le montant exact du CA signé grâce aux relances (ex. : 8 500 € gagnés) face au coût modique de l'accompagnement (60 €).
  3. L'effet de réassurance psychologique ancre la rétention client dans la durée.

---

### R05 — Revente Illégale de Licences & Interdiction Smart
* **Cause Racine :** Vouloir "revendre" un abonnement Microsoft 365 ou Google Workspace au client pour augmenter sa marge.
* **Règle Légale Smart :** Smart Coop interdit formellement l'achat de licences logicielles pour revente. L'activité doit être strictement intellectuelle et organisationnelle.
* **Contre-Mesure Opérationnelle :**
  1. Le client souscrit et règle son abonnement directement auprès de Microsoft ou de Google.
  2. Le prestataire facture exclusivement son temps d'installation, de paramétrage, de formation et de maintenance.

---

### R06 — Réclamation Client en Cas de Devis Perdu
* **Cause Racine :** Un client oublie de répondre à un appel d'offres public et tente d'imputer la responsabilité de sa perte financière à son outil de relance.
* **Contre-Mesure Juridique :**
  1. Clause contractuelle 1 : **Obligation stricte de moyens**. Le prestataire fournit un cadre organisationnel, jamais une garantie de signature ou de réponse.
  2. Clause contractuelle 2 : **Plafond d'indemnisation** limité au montant net perçu pour la prestation.
  3. Mention de bas de page inscrite dans le classeur Excel : *"Outil d'aide interne. La décision et la vérification des offres relèvent de la responsabilité exclusive du donneur d'ordre."*

---

### R07 — Rejet du Contrat Étudiant par Smart (Promotion Sociale)
* **Cause Racine :** L'Office National de Sécurité Sociale (ONSS) exige que les études soient l'occupation principale pour bénéficier du taux de solidarité réduit (2,71 %). En promotion sociale, si le cursus compte moins de 17h/semaine ou 27 crédits, Smart applique le contrat employé ordinaire (rendement net divisé par deux).
* **Contre-Mesure Fiscale :**
  1. Si le statut étudiant salarié est rejeté, **basculer immédiatement sous le statut d'Étudiant-Indépendant (INASTI 2026)**.
  2. Sous ce statut, les cotisations sociales sont de **0 €** tant que le Revenu Net Imposable reste sous le seuil d'exonération de **8 687,04 € par an**.

---

### R08 & R09 — Protection du Foyer Fiscal Parental & Allocations Familiales
* **Les Deux Falaise Fiscales Belges :**
  - **Plafond Personne à Charge (IPP SPF Finances) :** Si les ressources nettes de l'étudiant dépassent **~3 980 € à 4 200 € nets par an**, ses parents perdent la quotité exemptée d'impôt (perte sèche de **1 500 € à 2 200 € d'impôts supplémentaires** pour les parents).
  - **Plafond Heures FAMIWAL (Wallonie) :** Dépasser **240 heures par trimestre** sous contrat d'employé ordinaire suspend le versement des allocations familiales (~200 €/mois perdus).
* **Protocole de Régulation :**
  1. Tenir une comptabilité rigoureuse au centime près des montants nets perçus.
  2. Dès que le total net approche 3 500 €, freiner la facturation personnelle ou déduire des frais professionnels réels (ordinateur, matériel de formation, déplacements) pour compresser le net imposable.

---

### R10 — Refus Ferme du Travail au Noir par l'Optimisation Fiscale
* **Cas de Figure :** Le prospect demande : *« Fais-moi ça à 200 € en liquide sans facture. »*
* **Riposte Financière Positive (Verbatim) :**
  > *« En réalité, me payer en liquide vous coûterait plus cher ! Sur facture officielle, mes 350 € sont une charge professionnelle déductible à 100 %, ce qui fait baisser votre bénéfice imposable et vous fait économiser entre 25 % et 50 % d'impôt (soit 90 à 175 € d'impôt en moins). Vous récupérez aussi l'intégralité de la TVA. Au final, l'opération officielle ne vous coûte réellement qu'environ 180 € nets, tout en vous offrant une garantie écrite de 14 jours, un contrat en règle et zéro risque fiscal pour votre entreprise. »*

---

### R11 — Gestion du Temps d'Études (30h/semaine) vs Disponibilité Client
* **Problème :** Un artisan appelle en panique à 10h15 alors que Brandon est en plein cours ou en examen.
* **Protocole SLA Contractuel :**
  1. Définir des **créneaux de support asynchrones** gravés dans le bon de commande :
     - Matin : **7h00 – 8h00** (avant le démarrage des chantiers/ateliers).
     - Soir : **17h00 – 18h30** (au retour au bureau/dépôt).
  2. Tous les échanges urgents s'effectuent par message vocal WhatsApp ou e-mail, traités sous 24h ouvrées.

---

### R12 — Clarification Peppol 2026 : Le Cheval de Troie Commercial
* **Le Piège :** Laisser croire au client qu'un tableur Excel de devis remplace le logiciel de facturation Peppol obligatoire.
* **Le Positionnement Stratégique :**
  > *« Peppol concerne uniquement la facture électronique finale. Mais 40 % des devis n'arrivent jamais au stade de la facture Peppol parce qu'ils sont oubliés avant d'avoir été signés ! Mon rôle est de sécuriser votre pipeline en amont pour que vous ayez des devis signés à convertir en factures Peppol. »*

---

### R13 — L'Argument d'Élimination face aux Logiciels Lourds (Bouwsoft, Vertuoza)
* **Chiffres d'Ancrage :**
  - **Bouwsoft :** Frais de démarrage de **865 € HTVA obligatoires** + abonnement mensuel lourd.
  - **Vertuoza :** 100 à 300 € / mois + engagement annuel + dizaines de champs complexes.
* **Pitch Différenciateur :**
  > *« Vertuoza et Bouwsoft sont d'excellents outils pour des structures de 20 personnes avec une équipe administrative dédiée. Pour votre entreprise, c'est comme utiliser un semi-remorque de 40 tonnes pour aller acheter du pain. Mon système utilise votre Excel existant : 0 € d'abonnement logiciel supplémentaire, prise en main en 15 minutes, et vous en êtes propriétaire à vie. »*

---

### R14 — L'Ancrage Anti-Abandon : Le Rituel du Vendredi 16h30
* **Statistique Réelle :** 80 % des tableurs non ritualisés sont abandonnés en moins de 3 semaines.
* **Protocole d'Ancrage Comportemental :**
  1. Intégrer l'onglet `Rituel Hebdomadaire` directement dans le classeur.
  2. Laisser une **fiche cartonnée plastifiée mémo** sur le bureau du patron ou de l'assistante.
  3. Programmer une notification récurrente sur le smartphone du gérant chaque vendredi à 16h30 : *« 📲 15 minutes chrono : 3 devis en vert, 3 relances passées, week-end libéré. »*
