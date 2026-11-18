# OPTIONS POINT D'ACCÈS PEPPOL — recherche 18/11/2026 (pour décision Brandon)

Contexte : facturation électronique belge **obligatoire depuis le 01/01/2026** entre entreprises.
Notre générateur produit du XML UBL 2.1 / BIS 3.0 conforme — il manque l'envoi par un
point d'accès certifié. 2 options crédibles trouvées (tarifs vérifiés sur les sites officiels) :

## Option A — Billit : plan gratuit
| Élément | Détail |
|---|---|
| Plan « Envoi uniquement » | **0,00 €/mois** — envoi de factures de vente via Peppol, 1 utilisateur |
| Plans payants | 6,90-7,50 €/mois (25 docs/mois) → 22,92 €/mois (500 docs/mois) |
| Accès Peppol | **inclus sans frais supplémentaires** |
| Essai | 15 jours gratuit, sans carte |
| Limite pour nous | envoi via LEUR interface (pas d'API clairement documentée en gratuit) |

## Option B — Peppol Box by Flexina : envoi XML/API
| Élément | Détail |
|---|---|
| Plan Micro | **5 €/mois** (60 €/an) — 100 documents/an, sans engagement |
| Plan Standard | 15 €/mois (600 docs/an) |
| Envoi | **API + envoi XML direct** — compatible avec notre `generate_peppol_invoice.py` |
| Avantage technique | le seul des deux qui accepte explicitement du XML généré en externe |

## Recommandation (préparée, décision à Brandon)
1. **Test gratuit Billit 15 jours** pour valider le flux Peppol avec un vrai destinataire (0 €).
2. Si l'envoi XML automatisé est requis (pipeline 100 % IA) → **Peppol Box Micro à 5 €/mois** : notre XML passe par leur API, zéro ressaisie.
3. Ne rien souscrire avant le premier client réel.

## Coût vs modèle
- 5 €/mois = 1,7 % d'un Pack 1 (290 €) — négligeable au premier client.
- Trigger d'achat : le jour où le premier client signé doit recevoir une facture Peppol.

Sources : billit.eu/fr-be/tarifs, billit.eu/fr-be/envoyer-des-factures-electroniques-via-peppol, peppol-box.be/tarifs-peppol (consultés 18/11/2026).
