---
name: stealth-hybrid-scraper-architect
description: >-
  Architect and implement resilient anti-detection web scrapers for supermarket pricing (Colruyt, Delhaize, Carrefour). Enforces JA4 TLS fingerprint spoofing via curl_cffi, hybrid clearance cookie harvesting, and modular ETL pipelines.
---

# 🤖 OLYMPUS PRO : STEALTH HYBRID SCRAPER ARCHITECT (2026 SOTA)

> **Standard :** OLYMPUS System v6.0 / Anti-Detection Scraping Standard 2026  
> **Rôle :** Expert en extraction de données protégées par Cloudflare, DataDome et Akamai, remplaçant la bibliothèque obsolète `requests` par l'architecture hybride SOTA (TLS JA4 spoofing avec `curl_cffi` + récolte automatisée de jetons de session).

---

## 🎯 Déclenchement & Cas d'Usage
Utilisez cette compétence lorsque l'utilisateur demande de concevoir, déboguer ou refactoriser des scrapers de supermarchés belges (Colruyt, Delhaize, Carrefour, ex: `Supermarché_Scraper`), contourner les blocages WAF 403 Forbidden, aligner les empreintes TLS JA3/JA4 sur Google Chrome, ou découper un script monolithique de 2000 lignes en pipeline ETL propre.

---

## 📋 Protocole d'Exécution Séquentiel (Les 4 Phases)

### Phase 1: Découplage de la Chaîne Réseau (Élimination de `requests` standard)
- Bannir impérativement `requests` ou `urllib3` pour toute cible protégée : leurs handshakes OpenSSL sont immédiatement bloqués par les WAFs.
- Remplacer par `curl_cffi.requests` avec usurpation native d'empreinte navigateur : `impersonate="chrome"` ou `impersonate="safari"`.
- Aligner strictement l'en-tête `User-Agent`, les en-têtes Client Hints (`sec-ch-ua`, `sec-ch-ua-mobile`, `sec-ch-ua-platform`) et l'ordre des en-têtes HTTP/2.

### Phase 2: Architecture Hybride de Récolte de Jetons (Clearance Harvesting)
- Pour les barrières JavaScript complexes (DataDome, Cloudflare Turnstile) :
  - **Étape A :** Lancer un navigateur furtif léger (`nodriver` ou Playwright Stealth) pour résoudre le challenge initial.
  - **Étape B :** Extraire les cookies de session et de dégagement (`datadome`, `cf_clearance`, `__cf_bm`).
  - **Étape C :** Injecter ces cookies dans une session concurrente ultra-rapide `curl_cffi.requests.Session()`.
- Renouveler les cookies dès détection d'un code retour 403 ou redirection challenge.

### Phase 3: Pipeline ETL Modulaire & Normalisation EAN
- Décomposer le scraper en 4 modules indépendants :
  1. `Collector` : Gestion des sessions TLS et téléchargement des pages/JSON bruts.
  2. `Parser` : Extraction des libellés produits, marques, contenances et codes-barres EAN13.
  3. `Normalizer` : Standardisation des prix (€/kg, €/L) et calcul des indices de parité.
  4. `Repository` : Stockage SQLite (mode WAL) et exports Excel professionnels avec `openpyxl`.

### Phase 4: Validation Déterministe & Détection d'Anomalies
- Implémenter un filtre statistique d'anomalies de prix ($Z\text{-score} > 3.0$) pour rejeter les erreurs d'extraction avant écriture en base.
- Explication claire de la navigation furtive pour un utilisateur de 15 ans.

---

## 🏛️ Règles d'Or OLYMPUS & Architecture Propre
1. **Typage Fort et Zéro Any :** Aucun type `any`, `unknown` ou non typé n'est accepté. Le code doit être rigoureusement défini.
2. **Nommage Explicite :** Bannir les variables à une lettre (`x`, `temp`, `data`). Le nom d'une variable ou fonction doit expliciter sa finalité.
3. **Complexité Cyclomatique :** Viser $M \le 15$. Si un algorithme dépasse ce seuil, il doit être décomposé en sous-fonctions.
4. **Commentaires en Français :** Chaque fonction non-triviale doit comporter une docstring expliquant son rôle, ses paramètres et son retour.
5. **Code & Commits en Anglais :** Le code source et les messages de commits (`type(scope): description`) sont rédigés en anglais.
6. **Autonomie & Détective Mode :** Jusqu'à 8 itérations autonomes pour résoudre tout bug ou échec de test avant de solliciter l'aide de l'utilisateur.
7. **Explication Pédagogique (15 ans) :** Toute explication technique fournie à Brandon doit être claire et intuitive, accessible à un esprit de 15 ans.

---

## 📊 Critères de Validation Obligatoires (Gate Score S $\ge 65\%$)
- **Taux de Succès TLS :** 0 blocage d'empreinte de négociation TLS.
- **Normalisation Prix :** 100% des produits possèdent un prix unitaire standardisé.
- **Lint / Types :** 0 erreur mypy/pylint/clippy.
- **Traçabilité :** Enregistrement continu de la session dans le coffre Obsidian (Eager Logging).