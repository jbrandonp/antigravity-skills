# SÉCURITÉ DES DONNÉES, CYBER-HYGIÈNE & CONFORMITÉ RGPD DANS LE BTP
## Référence Déontologique : Statut de Sous-Traitant (Art. 28), Chiffrement, Délais Légaux & Protocole Zéro-Rétention

---

## 1. QUALIFICATION JURIDIQUE RGPD (RÈGLEMENT EU 2016/679)

Dans toute intervention auprès d'un artisan ou d'une PME du bâtiment, les rôles légaux sont strictement délimités :

```
┌────────────────────────────────────────────────────────────────────────┐
│                   RÉPARTITION DES RÔLES RGPD (ART. 28)                 │
├──────────────────────────────────┬─────────────────────────────────────┤
│ L'ENTREPRISE DU BÂTIMENT (CLIENT)│ LE CONSULTANT (BUREAU NUMÉRIQUE BTP)│
│                                  │                                     │
│ • Qualité : RESPONSABLE DE       │ • Qualité : SOUS-TRAITANT TECHNIQUE │
│   TRAITEMENT (Data Controller)   │   (Data Processor)                  │
│ • Décide de la finalité :        │ • N'agit que sur instruction        │
│   gestion de ses devis et clients│   documentée du responsable.        │
│ • Collecte légale des données    │ • Zéro droit de propriété sur les   │
│   auprès des propriétaires.      │   fichiers du client.               │
└──────────────────────────────────┴─────────────────────────────────────┘
```

### 1.1 Données Traitées & Données Formellement Exclues
* **Données traitées autorisées :** Données professionnelles et d'identification courantes (Nom, Prénom, Numéro de téléphone, Adresse du chantier, Description technique des travaux, Montants chiffrés HTVA).
* **Données strictement interdites :** Aucune donnée sensible au sens de l'Article 9 du RGPD (santé, biométrie, opinions politiques, condamnations) ne doit être collectée ni enregistrée dans les outils de devis.

---

## 2. LA RÈGLE D'OR : ZÉRO RÉTENTION LOCALE (ZERO-LOCAL DATA RETENTION)

Pour neutraliser tout risque de fuite de données ou de mise en cause de votre responsabilité :

1. **Interdiction de Rapatriement en Local :**
   * Ne jamais copier ni télécharger les fichiers Excel, carnets de contacts ou bases clients de l'artisan sur votre propre ordinateur portable ou clé USB personnelle.
2. **Intervention Exclusif en Environnement Client :**
   * Toutes les opérations de configuration, de formule ou de nettoyage de base se font **directement dans l'environnement propre de l'artisan** (son PC, son OneDrive ou son espace Microsoft 365) via l'Assistance Rapide Windows.
3. **Fin de Session & Déconnexion Nette :**
   * À la fermeture de la session Quick Assist, aucun fichier temporaire, aucun journal de saisie et aucun mot de passe ne subsistent sur le poste du consultant.

---

## 3. DÉLAIS LÉGAUX DE CONSERVATION DES DONNÉES EN BELGIQUE

| Type de Document | Délai Légal de Conservation | Fondement Juridique Belge | Action au Terme du Délai |
| :--- | :--- | :--- | :--- |
| **Factures & Pièces Comptables** | **10 ans** (à compter du 1er janvier suivant la date) | Art. III.86 du Code de Droit Économique (CDE) | Archivage comptable obligatoire |
| **Devis Signés (Bons de commande)** | **10 ans** (lié à la responsabilité décennale des entrepreneurs) | Art. 1792 et 2270 de l'Ancien Code Civil | Archivage contrat |
| **Devis Refusés ou Sans Réponse** | **1 à 3 ans** (délai de prescription commerciale) | Recommandation APD (Autorité de Protection des Données) | Purge / Suppression définitive |
| **Prospects Non Convertis** | **3 ans** après le dernier contact actif | Norme simplifiée RGPD | Suppression des coordonnées |

---

## 4. PROTOCOLE TECHNIQUE DE SÉCURITÉ DU CLASSEUR CLIENT

Pour garantir la pérennité et la confidentialité du système chez l'artisan :

1. **Chiffrement du Stockage Cloud (OneDrive / SharePoint) :**
   * Activer impérativement la synchronisation OneDrive professionnelle avec chiffrement au repos (AES 256 bits) et en transit (TLS 1.3).
2. **Authentification Multi-Facteurs (MFA / 2FA) :**
   * Recommander et vérifier l'activation du MFA (via Microsoft Authenticator ou code SMS) sur le compte Microsoft du dirigeant.
3. **Protection par Mot de Passe Administrateur :**
   * Les formules du classeur sont verrouillées sous le mot de passe standard `BTP2026`.
   * Le mot de passe est transmis officiellement au patron sur la fiche de fin de mission, lui garantissant le contrôle souverain de ses outils.
4. **Portabilité et Réversibilité Totale (Zéro Lock-In) :**
   * Le client peut à tout moment exporter l'intégralité de ses devis en format ouvert CSV UTF-8 sans dépendre du prestataire.
