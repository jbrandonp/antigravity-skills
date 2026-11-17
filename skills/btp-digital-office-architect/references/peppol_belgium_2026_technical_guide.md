# GUIDE TECHNIQUE PEPPOL BELGIQUE 2026 : FACTURATION ÉLECTRONIQUE B2B OBLIGATOIRE
## Cadre Légal, Modèle en 4 Coins, Schéma UBL 2.1 & Stratégie Commerciale "Cheval de Troie"

---

## 1. LE CADRE LÉGAL BELGE DU 1ER JANVIER 2026

### 1.1 La Loi et le Calendrier d'Application
* **Base Légale :** Loi du 28 décembre 2023 et Arrêté Royal du 9 mars 2024 transposant la directive européenne sur la facturation électronique.
* **Date d'effet :** **1er janvier 2026**.
* **Périmètre strict :** Toutes les transactions **B2B (Business-to-Business)** entre entreprises assujetties à la TVA établies en Belgique.
* **Ce qui est INTERDIT :** Les factures au format papier, les simples PDF envoyés par email ou les fichiers Excel ne sont **plus considérés comme des factures légales valides**.
* **Ce qui est OBLIGATOIRE :** Une facture électronique structurée au format **XML UBL 2.1**, acheminée via le réseau décentralisé sécurisé **PEPPOL** (*Pan-European Public Procurement On-Line*).

---

## 2. L'ARCHITECTURE DU RÉSEAU PEPPOL (LE MODÈLE EN 4 COINS)

Contrairement à un simple envoi de courriel (qui transite en clair et peut être intercepté ou falsifié), Peppol fonctionne selon un modèle d'échange à 4 acteurs certifiés :

```
┌─────────────────┐                                  ┌─────────────────┐
│     COIN 1      │                                  │     COIN 4      │
│  Fournisseur /  │                                  │   Client B2B /  │
│  L'Artisan BTP  │                                  │   Entreprise    │
└────────┬────────┘                                  └────────▲────────┘
         │ (1. Émission XML)                                  │ (4. Réception XML)
         ▼                                                    │
┌─────────────────┐         (3. Acheminement)        ┌────────┴────────┐
│     COIN 2      │ ───────────────────────────────> │     COIN 3      │
│   Point d'Accès │      Protocole Sécurisé          │   Point d'Accès │
│  Certifié Peppol│            AS4                   │  Certifié Peppol│
└─────────────────┘                                  └─────────────────┘
```

1. **Coin 1 (Émetteur) :** Votre entreprise ou l'artisan produit le fichier XML UBL 2.1.
2. **Coin 2 (Point d'accès émetteur) :** La passerelle certifiée (Smart Coop, Billit, WinBooks, Odoo, Sage) qui signe et valide le message.
3. **Coin 3 (Point d'accès récepteur) :** Le point d'accès du client qui réceptionne et contrôle la conformité.
4. **Coin 4 (Destinataire) :** Le logiciel comptable du client qui intègre automatiquement la facture sans aucune saisie manuelle.

---

## 3. SPÉCIFICATIONS TECHNIQUES DU SCHÉMA UBL 2.1 BELGE

Toute facture transmise sur le réseau Peppol en Belgique doit impérativement respecter la norme européenne **EN 16931** et le profil **PEPPOL BIS Billing 3.0** :

### 3.1 Identifiants et Métadonnées Obligatoires
* **CustomizationID :** `urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0`
* **ProfileID :** `urn:fdc:peppol.eu:2017:poacc:billing:01:1.0`
* **InvoiceTypeCode :** `380` (Facture commerciale de vente) ou `381` (Note de crédit).
* **DocumentCurrencyCode :** `EUR`

### 3.2 L'Identifiant Belge Unique (Schéma 0208)
En Belgique, l'identifiant légal des entreprises sur le réseau Peppol est leur **numéro de Banque-Carrefour des Entreprises (BCE / KBO)** au format standardisé à 10 chiffres préfixé par le schéma `0208` :
* `EndpointID schemeID="0208"` : `0459180573` (Exemple : Smart Coop)
* `CompanyID` (TVA) : `BE0459180573`

---

## 4. LA STRATÉGIE COMMERCIALE DU "CHEVAL DE TROIE" PEPPOL

Le patron du BTP est souvent apeuré ou désinformé par rapport à l'obligation Peppol.  
Le Bureau Numérique BTP utilise cette anxiété comme un **levier d'acquisition majeur** :

```
┌────────────────────────────────────────────────────────────────────────┐
│                   L'ARGUMENT COMMERCIAL "CHEVAL DE TROIE"              │
├────────────────────────────────────────────────────────────────────────┤
│ "Monsieur [Nom], tout le monde vous parle de Peppol pour la facture    │
│  finale. C'est vrai, c'est obligatoire dès 2026.                       │
│                                                                        │
│  Mais posez-vous la vraie question :                                   │
│  À quoi bon avoir un système Peppol ultra-moderne pour facturer si 40 %│
│  de vos devis ne deviennent jamais des factures parce qu'ils sont      │
│  oubliés au fond d'une camionnette ?                                   │
│                                                                        │
│  Mon rôle, c'est de sécuriser l'AMONT : avec « Devis sans oubli »,     │
│  vos offres sont relancées et signées. Une fois le chantier signé et   │
│  terminé, la facture sort automatiquement vers Peppol sans stress."    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 5. LES PASSERELLES D'INTÉGRATION PEPPOL POUR L'ARTISAN

1. **Option A (Via Smart Coop) :**  
   Pour vos propres prestations de consultant, Smart gère nativement le point d'accès Peppol (BE 0459.180.573). Vos factures sont envoyées en XML UBL sans configuration technique.
2. **Option B (Pour l'artisan équipé de Billit / WinBooks / Odoo) :**  
   Export des données validées de `DEVIS_SANS_OUBLI_MODELE_PRO.xlsx` via [`export_devis_to_csv.py`](file:///c:/Users/brand/.agents/skills/btp-digital-office-architect/templates/tools/export_devis_to_csv.py) pour injection directe dans sa passerelle Peppol.
3. **Option C (Pour l'artisan sans logiciel — Portail Public Hermes) :**  
   Pour les micro-entreprises sans logiciel de facturation payant, le SPF Économie met à disposition le portail public gratuit **Hermes**, permettant de déposer ou saisir manuellement des factures converties en UBL Peppol.
