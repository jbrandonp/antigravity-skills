# 🇧🇪 GUIDE DE CONFORMITÉ & OBLIGATIONS LÉGALES DU BTP BELGE
## Référentiel Pratique pour l'Artisan Indépendant & le Chef d'Entreprise
### Complément Opérationnel au Système « Bureau Numérique BTP »

---

> [!NOTE] Positionnement & Rôle du Bureau Numérique BTP
> Le **Bureau Numérique BTP** intervient en tant que copilote d'organisation administrative, de rentabilité de chantier et de structuration pré-comptable.  
> Il ne se substitue ni à votre **expert-comptable certifié ITAA**, ni à votre **guichet d'entreprises agréé**, ni à votre **courtier d'assurances FSMA**, mais assure la passerelle technique parfaite entre vos chantiers et ces intervenants légaux.

---

## 🧭 TABLEAU DE BORD DES 7 ÉTAPES DU BTP BELGE

```text
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │  Étape Légale BTP      │ Prise en Charge Bureau Numérique BTP               │
 ├────────────────────────┼────────────────────────────────────────────────────┤
 │ 1. Statut Juridique    │ Orientation & Simulation de seuil socio-fiscal     │
 │ 2. Formalités (BCE/TVA)│ Checklist & orientation vers guichet agréé         │
 │ 3. TVA (6% vs 21%)     │ Prise en charge 100% (Attestation légale AR n° 20) │
 │ 4. Devis & Facturation │ Prise en charge 200% (Marge CP 124, Avenants, XML) │
 │ 5. Assurances BTP      │ Intégration du coût assurance au taux horaire      │
 │ 6. Spécificités BTP    │ Checklist Checkinatwork & Vérification Art. 30bis  │
 │ 7. Pré-Comptabilité    │ Prise en charge 100% (Exports CSV, Rapport Patron) │
 └────────────────────────┴────────────────────────────────────────────────────┘
```

---

### 1. ⚖️ STATUT JURIDIQUE & PROTECTION DU PATRIMOINE
- **Personne physique (Entreprise individuelle) :** Idéal au démarrage (< 45 000 € de bénéfice net). Moins de frais administratifs.
  - *Protection capitale :* Passer chez le notaire pour signer une **Déclaration d'insaisissabilité du logement familial** (évite la saisie de votre maison en cas de faillite).
- **Société (SRL) :** Recommandée dès que le chiffre d'affaires grandit ou qu'il y a des ouvriers. Responsabilité limitée aux capitaux de la société.
- **Rôle Bureau Numérique BTP :** Notre simulateur [`simulate_socio_fiscal.py`](./simulate_socio_fiscal.py) calcule votre point d'équilibre pour savoir exactement quand basculer vers la société.

---

### 2. 📝 FORMALITÉS DE LANCEMENT (BCE, TVA, INASTI)
Les démarches d'immatriculation doivent obligatoirement être effectuées auprès d'un **Guichet d'Entreprises agréé** :
- **Principaux guichets en région liégeoise :** Liantis, UCM, Securex, Xerius, Partena.
- **Accès à la profession (Wallonie) :** Justification des compétences professionnelles selon le métier (chauffage, électricité, toiture).
- **Compte bancaire professionnel :** Obligation stricte de séparer vos finances privées de la trésorerie de chantier.
- **Rôle Bureau Numérique BTP :** Fourniture de la checklist de préparation pour valider l'enregistrement de vos codes NACE-BEL exacts.

---

### 3. 💶 TVA CHANTIER : LE BOUCLIER FISCAL (6 % vs 21 %)
L'erreur de TVA est la cause n° 1 des redressements fiscaux dans le bâtiment belge :
- **Taux 21 % :** Neuf, bâtiments de moins de 10 ans, locaux à usage exclusivement professionnel.
- **Taux réduit 6 % :** Logements privés de plus de 10 ans affectés à l'habitation.
- **La règle d'or légale (AR n° 20 art. 17 § 1) :** Vous devez obligatoirement faire figurer la mention légale de décharge et faire valider au client son délai de contestation d'un mois.
- **Rôle Bureau Numérique BTP :** **Géré à 100 % !** Notre script [`generate_site_work_amendment.py`](../05_Outils_et_Modeles_Excel/generate_site_work_amendment.py) génère l'attestation conforme inattaquable en cas de contrôle fiscal.

---

### 4. 📄 DEVIS, FACTURATION & EXTENSION PEPPOL 2026
- **Les mentions obligatoires :** Numéro de TVA, BCE, coordonnées complètes, décomposition main-d'œuvre et matériaux, conditions de paiement et pénalités de retard.
- **Le vrai coût horaire :** Ne jamais facturer sur base d'un brut ouvrier de 18 € ! Un ouvrier en construction (Commission Paritaire 124) coûte au minimum **39,00 €/h chargé** (charges ONSS 32,5%, timbres intempéries Constructiv 13%, congés payés et assurances).
- **L'obligation Peppol B2B au 1er janvier 2026 :** La loi belge interdit la facture PDF traditionnelle entre entreprises assujetties. Le flux XML UBL 2.1 devient obligatoire.
- **Rôle Bureau Numérique BTP :** **Cœur de notre métier.** Le classeur [`DEVIS_SANS_OUBLI_MODELE_PRO.xlsx`](../05_Outils_et_Modeles_Excel/DEVIS_SANS_OUBLI_MODELE_PRO.xlsx) sécurise vos marges, notre générateur WhatsApp bloque les travaux supplémentaires impayés, et notre script [`generate_peppol_invoice.py`](../05_Outils_et_Modeles_Excel/generate_peppol_invoice.py) produit vos factures Peppol sans logiciel ERP coûteux.

---

### 5. 🛡️ ASSURANCES OBLIGATOIRES DU BÂTIMENT
Deux assurances sont légalement imposées par le législateur belge :
1. **Responsabilité Décennale (Loi Peeters du 31 mai 2017) :** Obligatoire pour tout entrepreneur intervenant sur le gros œuvre fermé et la stabilité du bâtiment. Durée : 10 ans après réception.
2. **Accidents du Travail (Loi du 10 avril 1971) :** Obligatoire dès l'embauche du premier ouvrier ou apprenti.
- **Assurances complémentaires indispensables :** RC Exploitation (dégâts chez le client durant les travaux), assurance camionnette et outillage.
- **Rôle Bureau Numérique BTP :** Les primes de ces assurances sont directement injectées dans la formule du Coefficient K de notre calculateur pour être refacturées au client final.

---

### 6. 🔍 OBLIGATIONS SPÉCIFIQUES BTP (CHECKINATWORK & SOUS-TRAITANTS)
- **Checkinatwork (Art. 31bis Loi 04/08/1996) :** Enregistrement obligatoire de la présence de chaque travailleur sur les chantiers immobiliers soumis à déclaration préalable. L'artisan utilise son smartphone via le portail officiel de l'ONSS (`checkinatwork.be`).
- **Enregistrement des aidants et associés (depuis juillet 2024) :** Tout aidant familial non salarié ou associé actif doit être enregistré à la BCE.
- **Vérification des dettes des sous-traitants (Articles 30bis et 30ter) :**  
  > ⚠️ **DANGER MAJEUR :** Si vous faites appel à un sous-traitant (ex. un électricien indépendant), vous devez vérifier avant chaque paiement s'il a des dettes fiscales ou sociales sur le site officiel de l'ONSS : **`www.checkobligationderetenue.be`**.  
  > S'il a des dettes, vous avez l'obligation légale de retenir **15 % (ONSS) et/ou 15 % (Fisc)** sur sa facture. Si vous ne le faites pas, vous êtes solidairement responsable et devrez payer la dette à sa place !
- **Rôle Bureau Numérique BTP :** Notre fiche de suivi intègre le champ de contrôle et le lien direct vers le portail de retenue ONSS.

---

### 7. 🧾 PRÉ-COMPTABILITÉ, TRÉSORERIE & ANTICIPATION FISCALE
- **Le problème classique de l'artisan :** Voir 15 000 € sur le compte en banque et croire que c'est du bénéfice disponible, alors que 21 % appartiennent à l'État (TVA) et que les cotisations sociales INASTI arrivent à la fin du trimestre.
- **Cotisations sociales trimestrielles :** ~20,5 % du revenu net imposable (minimum légal ~860 €/trimestre pour un indépendant principal, ~445 € pour un primostarter).
- **Rôle Bureau Numérique BTP :**  
  - Génération du **Rapport Patron Mensuel** ([`generate_rapport_patron.py`](../05_Outils_et_Modeles_Excel/generate_rapport_patron.py)) qui ventile automatiquement la TVA collectée et la trésorerie nette disponible.
  - Exportation en un clic vers un fichier CSV standardisé ([`export_devis_to_csv.py`](../05_Outils_et_Modeles_Excel/export_devis_to_csv.py)) prêt à être importé dans le logiciel de votre comptable (WinBooks, Exact Online, Bob 50).
