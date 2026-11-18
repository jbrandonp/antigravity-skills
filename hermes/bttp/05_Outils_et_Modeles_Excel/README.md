# 📊 05 — OUTILS TECHNIQUES, MODÈLES EXCEL & CALCULATEURS
## Le Moteur Numérique & Financier du Bureau Digital

Ce dossier rassemble l'ensemble des scripts Python, classeurs Excel protégés, générateurs de documents légaux et passerelles d'exportation.

Le dossier est structuré en **deux branches complémentaires** :
1. **La Verticale Construction & BTP Belgique (Spécialisée Métier) :** Outillage de haute précision calibré sur la convention collective CP 124, la TVA 6 % rénovation et la gestion de chantier.
2. **Le Moteur Universel Multi-Secteurs (Générique) :** Plateforme modulaire permettant de déployer la même architecture bureautique pour d'autres secteurs d'activité (services, garages, cabinets de soins, commerces).

---

### 🗂️ SOMMAIRE DES FICHIERS PAR BRANCHE

```
05_Outils_et_Modeles_Excel/
│
├── 🏗️ BRANCHE A : VERTICALE SPÉCIALISÉE BTP BELGIQUE
│   ├── DEVIS_SANS_OUBLI_MODELE_PRO.xlsx        ← Le classeur maître BTP protégé (5 onglets, mot de passe : BTP2026)
│   ├── generate_devis_sans_oubli.py            ← Générateur du classeur Excel BTP avec formules vivantes et styles
│   ├── calculate_btp_margin_and_k_factor.py    ← Calculateur Déboursé Sec & Coeff K (ouvrier CP 124 à 39 €/h, chutes 10%)
│   ├── generate_site_work_amendment.py         ← Générateur WhatsApp d'avenants chantier minute & attestation TVA 6% (AR n° 20)
│   ├── append_new_devis.py                     ← Insertion sécurisée d'un nouveau devis sans écraser les formules
│   ├── draft_relance_messages.py               ← Générateur automatique des vocaux/textes de relance (J+14, J+7, J+3)
│   ├── generate_rapport_patron.py              ← Générateur du rapport mensuel exécutif pour le dirigeant
│   ├── RAPPORT_PATRON_EXEMPLE.txt              ← Exemple concret du rapport patron BTP généré
│   ├── export_devis_to_csv.py                  ← Passerelle d'exportation des devis vers les logiciels comptables
│   ├── EXPORTS_DEVIS_ERP_COMPATIBLE.csv        ← Données exportées et filtrées (zéro ligne de disclaimer parasite)
│   └── generate_peppol_invoice.py              ← Générateur de facture électronique Peppol BIS 3.0 XML UBL 2.1
│
└── 🌐 BRANCHE B : MOTEUR UNIVERSEL MULTI-SECTEURS
    ├── generate_digital_office_workbook.py     ← Générateur de classeur adaptable (BTP, Services, Garages, Soins, Retail)
    ├── append_new_deal.py                      ← Insertion universelle d'une affaire commerciale
    ├── draft_followup_messages.py              ← Générateur de relances multi-vocabulaires selon le secteur
    ├── calculate_lost_revenue_roi.py           ← Calculateur d'hémorragie financière et retour sur investissement (< 15j)
    └── generate_patron_report.py               ← Générateur universel de rapport de gestion multi-activités
```

---

### 💻 GUIDE DE RÉFÉRENCE DES COMMANDES CLI

#### 1. Commandes Spécialisées BTP

| Action | Commande PowerShell / Bash | Sortie Générée |
| :--- | :--- | :--- |
| **Générer le classeur BTP complet** | `python generate_devis_sans_oubli.py` | `DEVIS_SANS_OUBLI_MODELE_PRO.xlsx` |
| **Calculer Déboursé Sec & Coeff K** | `python calculate_btp_margin_and_k_factor.py` | Analyse de rentabilité & alerte marge |
| **Générer un Avenant Chantier Minute** | `python generate_site_work_amendment.py` | Texte WhatsApp & attestation TVA 6% |
| **Ajouter un devis BTP** | `python append_new_devis.py --client "Dupont" --montant 4500` | Ligne insérée avec formule dynamique |
| **Générer les relances BTP** | `python draft_relance_messages.py` | Messages WhatsApp / SMS prêts à l'envoi |
| **Extraire le Rapport Patron BTP** | `python generate_rapport_patron.py` | `RAPPORT_PATRON_EXEMPLE.txt` |
| **Exporter vers ERP / Comptabilité** | `python export_devis_to_csv.py` | `EXPORTS_DEVIS_ERP_COMPATIBLE.csv` |
| **Générer une facture Peppol XML** | `python generate_peppol_invoice.py` | Facture XML UBL 2.1 conforme 2026 |

#### 2. Commandes Universelles Multi-Secteurs

| Action | Commande PowerShell / Bash | Sortie Générée |
| :--- | :--- | :--- |
| **Générer un classeur multi-secteur** | `python generate_digital_office_workbook.py --sector SERVICES` | `SUIVI_AFFAIRES_MODELE_PRO.xlsx` |
| **Ajouter une affaire universelle** | `python append_new_deal.py --client "Cabinet Martin" --montant 1200` | Affaire enregistrée avec identifiant |
| **Générer relances adaptées** | `python draft_followup_messages.py --sector SERVICES` | Messages adaptés au secteur |
| **Calculer le ROI client** | `python calculate_lost_revenue_roi.py --devis-moyen 5000 --nb-devis 8` | Délai d'amortissement en jours |
| **Rapport de gestion universel** | `python generate_patron_report.py` | Synthèse de performance multi-secteur |

---

### 🔒 SÉCURITÉ ET INTÉGRITÉ DES FORMULES EXCEL

- **Mot de passe de protection :** `BTP2026`
- **Zonage ergonomique :**
  - Colonnes 1 à 8, 10 et 11 : Déverrouillées pour la saisie quotidienne (Nom, Date, Montant, Statut, etc.).
  - Colonne 9 (« Date Relance Conseillée ») : **Strictement verrouillée** pour empêcher tout écrasement accidentel de la formule de calcul automatique par l'artisan ou sa secrétaire.
  - Lignes futures (12 à 50) : Pré-chargées avec des formules dormantes qui s'activent dès qu'un montant est saisi.
