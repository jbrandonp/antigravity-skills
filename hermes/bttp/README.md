# 🏗️ BUREAU NUMÉRIQUE BTP — ARCHITECTURE DU PROJET
## Organisation Administrative & Automatisation Légère pour Artisans & TPE du Bâtiment (100% Distanciel & Haute Valeur)

Bienvenue dans l'espace de travail unifié du projet **Bureau Numérique BTP**.  
Tous les fichiers sont rigoureusement ordonnés dans **6 dossiers thématiques numérotés**, chacun doté de son propre guide `README.md` explicatif.

Ce système est conçu pour délivrer une **haute valeur financière et juridique** aux artisans du bâtiment (chauffagistes, électriciens, plombiers, carreleurs, menuisiers) **exclusivement à distance (zéro déplacement physique)** :
1. **Détection des fuites de marge :** Calculateur du Déboursé Sec et Coefficient K (ouvrier CP 124 chargé à 39 €/h, charges ONSS 32,5 %, timbres intempéries Constructiv 13 %, majoration chutes 10 %).
> **Note de réconciliation ONSS :** le chiffre 32,5 % ci-dessus = cotisation patronale + charges totales (ONSS + assurances + provisions) ; les ~24-27 % de l'audit critique = cotisation patronale ONSS seule. Les deux sont corrects mais mesurent des choses différentes.
2. **Générateur d'Avenants Minute WhatsApp :** Récupération de 100 % des travaux supplémentaires imprévus demandés sur chantier en 30 secondes chrono sur smartphone.
3. **Bouclier Fiscal TVA 6 % :** Attestation obligatoire pour logements de plus de 10 ans (AR n° 20 art. 17 § 1) protégeant l'artisan contre tout redressement fiscal rétroactif à 21 %.
4. **Passerelle Peppol B2B 2026 :** Facturation électronique XML UBL 2.1 obligatoire au 1er janvier 2026 sans licence ERP ruineuse.

---

### 🗂️ SOMMAIRE COMPLET DE L'ARBORESCENCE (100% ORDONNÉ)

```
répertoire du projet → 
│
├── 01_Strategie_et_Audits/                           ← Pôle Stratégie, Études de Marché & Réglementation
│   ├── README.md                                     ← Guide du pôle stratégique & catalogue des 4 piliers
│   ├── DOSSIER_STRATEGIQUE_BUREAU_NUMERIQUE_BTP.md   ← La bible stratégique intégrale (10 chapitres, 19 concurrents)
│   ├── AUDIT_CRITIQUE_ET_STRESS_TEST_COMPLET.md      ← Analyse approfondie des risques, coin fiscal et seuil d'équilibre
│   ├── risk_management_and_red_team_protocols.md     ← Protocoles Red Team anti-blocage, gestion des no-shows et litiges
│   ├── peppol_belgium_2026_technical_guide.md        ← Guide technique Peppol B2B XML UBL 2.1 obligatoire (Belgique 2026)
│   ├── gdpr_and_data_security_btp.md                 ← Guide de cyber-hygiène, statut sous-traitant RGPD & zéro-rétention
│   ├── ACCORD_SOUS_TRAITANCE_RGPD_DPA.md             ← Convention DPA de sous-traitance RGPD (Art. 28, zéro stockage local)
│   ├── GUIDE_CONFORMITE_ET_OBLIGATIONS_BTP_BELGIQUE.md ← Guide pratique des 7 étapes légales BTP (Checkinatwork, Art. 30bis, TVA)
│   ├── diagnostic_and_audit_rubrics.md               ← Questionnaire de maturité /20 & calcul de l'hémorragie financière
│   ├── simulate_socio_fiscal.py                      ← Simulateur de conversion brut/net (Smart CP 200 vs INASTI 2026)
│   ├── universal_business_adaptation_matrix.md       ← Matrice d'adaptation sectorielle universelle (6 profils métier)
│   ├── run_bttp_competitive_analysis.py              ← Moteur automatisé d'analyse concurrentielle et de wargaming
│   └── GARTNER_MAGIC_QUADRANT_BTP_BELGIQUE.svg       ← Magic Quadrant vectoriel SVG du marché BTP belge 2026
│
├── 02_Candidature_Smart_Liege/                       ← Pôle Intégration Coopérative Smart & Cadre Légal
│   ├── README.md                                     ← Guide de dépôt Smart Liège & sécurisation du statut étudiant
│   ├── DOSSIER_CANDIDATURE_SMART_LIEGE.md            ← Lettre de cadrage officielle et fiche synthétique de projet
│   ├── CHECKLIST_PIECES_JUSTIFICATIVES.md            ← Liste à cocher des 6 pièces indispensables avant l'envoi
│   └── MODELE_EMAIL_ENVOI_SMART.md                   ← Modèle d'email prêt à l'envoi pour liege@smart.coop
│
├── 03_Vente_et_Prospection_Terrain/                  ← Pôle Vente, Télé-Prospection & Closing à Distance
│   ├── README.md                                     ← Guide commercial & machine de vente 100% à distance
│   ├── MANUEL_PROSPECTION_VENTE_ET_TERRAIN.md        ← Couteau suisse commercial (vocaux WhatsApp, 7 objections, closing)
│   ├── BATTLECARD_8SEC_VERTUOZA.md                   ← Fiche de contre-attaque scannable en 8 secondes vs ERP lourds
│   ├── LANDING_ALTERNATIVE_VERTUOZA.html             ← Page web d'assaut comparative responsive (HTML5 / Tailwind)
│   ├── SLIDES_DEMO_CLIENT_10MIN.html                 ← Présentation interactive 5 slides pour télé-démo 10 min Quick Assist
│   ├── BON_DE_COMMANDE_PROPOSITION_COMMERCIALE.md    ← Bon de commande 1 page + 9 CGV de protection juridique
│   ├── FICHIER_PROSPECTION_LIEGE_BTP.xlsx            ← Base de prospection avec prospects qualifiés région liégeoise
│   ├── generate_prospection_sheet.py                 ← Générateur automatique de la base prospects Excel
│   ├── extract_belgian_btp_leads.py                  ← Extracteur & scanner de prospects BTP certifiés par NACE-BEL et commune
│   └── WIN_WIRE_EXEMPLE_LIEGE.md                     ← Annonce flash de victoire commerciale terrain (deal Herstal 1 800 €)
│
├── 04_Operations_et_Formation_Client/                ← Pôle Déploiement à Distance & Formation Express
│   ├── README.md                                     ← Guide des opérations & protocole d'onboarding client
│   ├── PLAN_ACTION_OPERATIONNEL_JOUR_PAR_JOUR.md     ← Feuille de route chronologique pas-à-pas (Semaines 1 et 2)
│   ├── PROTOCOLE_INSTALLATION_TECHNIQUE.md           ← Guide de déploiement à distance (Quick Assist Windows, PWA mobile)
│   ├── PACK_BIENVENUE_ET_FORMATION_CLIENT.md         ← Livret d'accueil BTP & mémo du Rituel du Vendredi 16h30
│   └── PACK_BIENVENUE_ET_FORMATION_UNIVERSEL.md      ← Livret d'accueil universel multi-métiers pour toute TPE
│
├── 05_Outils_et_Modeles_Excel/                       ← Pôle Outils Techniques, Scripts Python & Modèles
│   ├── README.md                                     ← Guide complet des 16 outils (Verticale BTP vs Moteur Universel)
│   ├── DEVIS_SANS_OUBLI_MODELE_PRO.xlsx              ← Classeur maître BTP protégé (5 onglets, mot de passe : BTP2026)
│   ├── generate_devis_sans_oubli.py                  ← Générateur du classeur Excel BTP avec formules vivantes et styles
│   ├── calculate_btp_margin_and_k_factor.py          ← Calculateur Déboursé Sec & Coeff K (ouvrier CP 124 à 39 €/h, chutes 10%)
│   ├── generate_site_work_amendment.py               ← Générateur WhatsApp d'avenants minute & attestation TVA 6% (AR n° 20)
│   ├── append_new_devis.py                           ← Insertion sécurisée d'un nouveau devis sans écraser les formules
│   ├── draft_relance_messages.py                     ← Générateur de messages WhatsApp / Email pour devis BTP
│   ├── generate_rapport_patron.py                    ← Générateur du rapport mensuel exécutif BTP pour le dirigeant
│   ├── RAPPORT_PATRON_EXEMPLE.txt                    ← Exemple concret généré du rapport mensuel patron
│   ├── export_devis_to_csv.py                        ← Passerelle d'exportation standardisée UTF-8 vers tout ERP
│   ├── EXPORTS_DEVIS_ERP_COMPATIBLE.csv              ← Export CSV nettoyé des 7 devis réels (zéro disclaimer parasite)
│   ├── generate_peppol_invoice.py                    ← Générateur de factures électroniques Peppol BIS 3.0 XML UBL 2.1
│   ├── generate_digital_office_workbook.py           ← Générateur universel multi-secteurs (BTP, Services, Garages, Soins, Retail)
│   ├── append_new_deal.py                            ← Insertion sécurisée d'affaires multi-secteurs sans casser les formules
│   ├── draft_followup_messages.py                    ← Générateur universel de messages personnalisés (vocal/texte/email)
│   ├── calculate_lost_revenue_roi.py                 ← Calculateur de ROI commercial et retour sur investissement (< 15j)
│   └── generate_patron_report.py                     ← Générateur universel de rapport de gestion multi-activités
│
├── 06_Tests_et_Qualite/                              ← Pôle Validation Qualité & Audits Détective
│   ├── README.md                                     ← Guide de l'assurance qualité & pyramide de tests
│   ├── test_btp_suite.py                             ← Suite de 12 tests automatisés BTP validant 100 % des fichiers et calculs
│   ├── test_office_suite.py                          ← Suite de 8 tests automatisés universelle multi-secteurs
│   ├── audit_btp_office.py                           ← Moteur d'audit architectural détective BTP (Score 100/100)
│   └── audit_digital_office.py                       ← Moteur d'audit universel (Score 100/100, tous secteurs)
│
├── .gitignore                                        ← Règles d'exclusion Git (cache Python, pytest, ruff, fichiers temporaires)
└── README.md                                         ← Le présent guide général d'orientation
```

---

### 🚀 GUIDE DE DÉMARRAGE RAPIDE EN 3 ÉTAPES (100% DISTANCIEL)

1. **Étape 1 — Dépôt Smart Liège :**  
   Consultez le dossier [`02_Candidature_Smart_Liege`](02_Candidature_Smart_Liege), vérifiez les pièces avec [`CHECKLIST_PIECES_JUSTIFICATIVES.md`](02_Candidature_Smart_Liege/CHECKLIST_PIECES_JUSTIFICATIVES.md), adaptez vos coordonnées dans [`DOSSIER_CANDIDATURE_SMART_LIEGE.md`](02_Candidature_Smart_Liege/DOSSIER_CANDIDATURE_SMART_LIEGE.md) et envoyez l'email officiel avec [`MODELE_EMAIL_ENVOI_SMART.md`](02_Candidature_Smart_Liege/MODELE_EMAIL_ENVOI_SMART.md) à `liege@smart.coop`.

2. **Étape 2 — Préparation Numérique & Télé-Prospection :**  
   Consultez le dossier [`03_Vente_et_Prospection_Terrain`](03_Vente_et_Prospection_Terrain) et lisez [`MANUEL_PROSPECTION_VENTE_ET_TERRAIN.md`](03_Vente_et_Prospection_Terrain/MANUEL_PROSPECTION_VENTE_ET_TERRAIN.md) sur smartphone pour envoyer vos premiers vocaux WhatsApp ciblés et maîtriser les réponses aux objections.

3. **Étape 3 — Lancement & Exécution :**  
   Suivez la feuille de route pas-à-pas dans [`04_Operations_et_Formation_Client/PLAN_ACTION_OPERATIONNEL_JOUR_PAR_JOUR.md`](04_Operations_et_Formation_Client/PLAN_ACTION_OPERATIONNEL_JOUR_PAR_JOUR.md).

---

### 🧪 VALIDATION DE QUALITÉ AUTOMATISÉE

Pour vérifier en une seule commande que l'ensemble du système, des formules Excel et des calculs financiers est 100 % opérationnel :

```powershell
# Suite spécialisée BTP (12 tests)
python -B 06_Tests_et_Qualite/test_btp_suite.py

# Suite universelle multi-secteurs (8 tests)
python -B 06_Tests_et_Qualite/test_office_suite.py
```

*Résultat attendu :* `Ran 24 tests - OK (100 % de réussite)`.

Pour exécuter l'audit d'intégrité architecturale détective (score sur 100 points) :
```powershell
# Audit BTP
python -B 06_Tests_et_Qualite/audit_btp_office.py --workspace-dir .

# Audit Universel (BTP, Services, Maintenance, Soins, Retail, Immobilier)
python -B 06_Tests_et_Qualite/audit_digital_office.py --workspace-dir .
```
*Score cible :* `Score Global S : 100.0 / 100 (EXCELLENT)`.

---

### 🌐 COMPÉTENCES ANTIGRAVITY & GITHUB
Ce projet est synchronisé avec les compétences officielles de l'écosystème Antigravity :
- **[`digital-office-architect`](https://github.com/jbrandonp/antigravity-skills/tree/main/skills/digital-office-architect)** : Architecture universelle de bureau numérique pour toute TPE.
- **[`btp-digital-office-architect`](https://github.com/jbrandonp/antigravity-skills/tree/main/skills/btp-digital-office-architect)** : Spécialisation métier pour le bâtiment et les artisans.
- Dépôt public : **[https://github.com/jbrandonp/antigravity-skills](https://github.com/jbrandonp/antigravity-skills)**.
