# 🏗️ Playbooks Sectoriels Spécifiques : BTP Belge & B2B SaaS

Ce manuel regroupe les règles de terrain pour les deux secteurs majeurs de déploiement.

---

## 1. Playbook Artisans & PME du BTP (Belgique / France)

### Les 4 Spécificités Réglementaires & Fiscales Incontournables :
1. **L'Attestation TVA 6% Rénovation (Belgique) :**
   - Pour les logements privés de plus de 10 ans, le taux réduit s'applique sous réserve d'une mention légale obligatoire sur la facture.
   - *Faille des concurrents :* 80% des logiciels concurrents obligent l'artisan à faire signer un papier séparé. Une génération automatique de la mention libellée avec case à cocher électronique est un avantage massif.
2. **Le Séisme Peppol & Facturation B2B Obligatoire (1er janvier 2026 en Belgique) :**
   - Fin des simples factures PDF par e-mail entre professionnels. Tout doit transiter au format structuré XML UBL via un point d'accès certifié Peppol.
   - *Point faible des logiciels historiques :* Batappli et vieux logiciels monolithiques vont facturer des modules d'export exorbitants.
3. **Les Situations de Travaux & Décomptes d'Acomptes :**
   - Les chantiers durent des mois : la facturation se fait par pourcentage d'avancement (ex: 30% commande, 40% gros œuvre, 30% réception).
   - Les logiciels généralistes (Stripe, QuickBooks) ne savent pas gérer les situations de travaux sans bricolage.
4. **L'Alternative du Portage Salarial (Smart Coop à Liège) :**
   - De nombreux artisans et indépendants démarrent via une coopérative d'emploi comme Smart pour s'épargner la gestion administrative et sociale.
   - Une solution qui s'interface avec les bordereaux de Smart Coop offre un boulevard d'acquisition exclusif.

---

## 2. Playbook SaaS B2B & Outils Collaboratifs

### Les 3 Métriques Fondamentales à Évaluer :
1. **Time-to-Value (TTV) :** Nombre de minutes avant que l'utilisateur atteigne le moment "Aha!" (première valeur perçue).
2. **Métrique de Valeur :** Facturation par utilisateur actif vs forfait illimité. Les artisans fuient la facturation au poste car ils partagent souvent un même compte familial.
3. **Souveraineté des Données :** Architecture locale (fichiers SQLite locaux sur PC) vs Cloud US exclusif. Le local-first rassure les professionnels qui craignent les pannes de réseau sur les chantiers.
