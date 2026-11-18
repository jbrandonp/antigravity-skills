# 🧪 06 — TESTS AUTOMATISÉS, QUALITÉ & AUDITS DÉTECTIVE
## Le Bouclier de Fiabilité & d'Assurance Qualité

Ce dossier contient l'infrastructure de validation automatisée garantissant qu'aucun fichier, formule Excel, calcul socio-fiscal ou clause juridique ne présente la moindre anomalie ou régression.

---

### 🗂️ SOMMAIRE DES 4 MOTEURS DE QUALITÉ

```
06_Tests_et_Qualite/
│
├── README.md                  ← Ce guide de référence qualité
├── test_btp_suite.py          ← Suite de 12 tests automatisés spécialisés BTP
├── test_office_suite.py       ← Suite de 8 tests automatisés universels multi-secteurs
├── audit_btp_office.py        ← Moteur d'audit détective BTP (Score global sur 100 points)
└── audit_digital_office.py    ← Moteur d'audit détective universel (Score global sur 100 points)
```

---

### 🔬 LES 2 SUITES DE TESTS UNITAIRES (20 TESTS AU TOTAL)

#### 1. Suite BTP Spécialisée (`test_btp_suite.py` — 12 tests)
Vérifie en profondeur l'écosystème BTP belge :
- Génération du classeur `DEVIS_SANS_OUBLI_MODELE_PRO.xlsx` et présence des 5 onglets.
- Zonage des protections : déverrouillage de la saisie client, verrouillage strict de la colonne 9.
- Présence de formules vivantes dans les lignes vides (lignes 12 à 50).
- Insertion incrémentale d'un devis via `append_new_devis.py`.
- Algorithme de relance dynamique ($J+14, J+7, J+3$).
- Calcul mathématique du coût horaire ouvrier CP 124 (39 €/h chargé) et du Coefficient K.
- Détection des fuites de marge sur chantier.
- Génération d'avenant minute WhatsApp et conformité de l'attestation TVA 6% (AR n° 20).
- Facturation électronique Peppol BIS 3.0 XML UBL 2.1.
- Filtrage propre du disclaimer lors de l'export CSV.
- Génération du fichier de prospection commerciale liégeois.
- Compilation du rapport mensuel dirigeant.

#### 2. Suite Universelle Multi-Secteurs (`test_office_suite.py` — 8 tests)
Vérifie la robustesse multi-métiers :
- Complétude des 6 profils sectoriels (BTP, Services, Garages, Soins, Retail, Immobilier).
- Génération et invariants de protection des classeurs sectoriels.
- Insertion sécurisée d'affaires avec identifiant incrémental universel.
- Adaptation dynamique du vocabulaire des relances selon le secteur.
- Conformité de la structure XML Peppol universelle.
- Équilibre de l'équation socio-fiscale (point de bascule ~6 200 €).
- Calcul du retour sur investissement et délai d'amortissement (< 15 jours).
- Compilation des métriques du rapport patron universel.

---

### 🛡️ LES 2 MOTEURS D'AUDIT DÉTECTIVE (SCORE SUR 100 POINTS)

Les deux scripts d'audit analysent l'espace de travail selon une grille stricte de 5 contrôles pondérés :

| Contrôle Audité | Poids | Critère de Réussite |
| :--- | :--- | :--- |
| **1. Arborescence Standardisée** | 20 pts | Présence des 6 dossiers numérotés |
| **2. Intégrité Excel & Ergonomie** | 30 pts | 5 feuilles, protection active, zonage validé, formules vivantes |
| **3. Exportation ERP & Disclaimer** | 20 pts | CSV d'exportation sans ligne parasite de disclaimer |
| **4. Couverture Juridique & 9 CGV** | 15 pts | 7 clauses obligatoires dans le bon de commande |
| **5. Suite de Tests Automatisée** | 15 pts | 100 % de réussite de la suite unitaire |
| **TOTAL** | **100 pts** | **Seuil minimum de production : ≥ 65 pts** |

---

### 🚀 COMMANDES D'EXÉCUTION RAPIDE

```powershell
# 1. Exécuter tous les tests unitaires (20 tests)
python -B 06_Tests_et_Qualite/test_btp_suite.py
python -B 06_Tests_et_Qualite/test_office_suite.py

# 2. Exécuter l'audit BTP complet (Score 100/100)
python -B 06_Tests_et_Qualite/audit_btp_office.py --workspace-dir .

# 3. Exécuter l'audit Universel (Score 100/100)
python -B 06_Tests_et_Qualite/audit_digital_office.py --workspace-dir .
```
