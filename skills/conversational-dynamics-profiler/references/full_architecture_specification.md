# Spécification Complète de l'Architecture : Conversational Dynamics Profiler (v7.0 Ultimate Suite)

Ce document formalise l'**architecture logicielle, clinique et mathématique complète** du moteur d'intelligence conversationnelle et de profilage relationnel.

---

## 🏗️ Vue d'Ensemble de l'Architecture en 7 Couches

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │ COUCHE 7 : PRÉSENTATION MULTI-SURFACES & COCKPIT INTERACTIF CLI        │
 │ ↳ Rapport Markdown 360°, Dashboard HTML/SVG offline, Cockpit terminal │
 ├────────────────────────────────────────────────────────────────────────┤
 │ COUCHE 6 : SIMULATION NON LINÉAIRE & STRESS-TESTING CHAOTIQUE          │
 │ ↳ Attracteurs étranges, Simulations What-If, Vulnérabilité aux chocs   │
 ├────────────────────────────────────────────────────────────────────────┤
 │ COUCHE 5 : SOCIOGRAMME, TRIANGULATION & ÉCOLOGIE SYSTÉMIQUE            │
 │ ↳ Tiers pivots (Bowen), Triangle de Karpman/TED, Sanctuarisation       │
 ├────────────────────────────────────────────────────────────────────────┤
 │ COUCHE 4 : FORMULATION CLINIQUE 4P & ATTACHEMENT DYNAMIQUE             │
 │ ↳ 4P Model, Échelle Fonagy, Danse Demande-Retrait, Porges Polyvagal    │
 ├────────────────────────────────────────────────────────────────────────┤
 │ COUCHE 3 : THÉORIE DE L'INFORMATION & DYNAMIQUE STOCHASTIQUE           │
 │ ↳ Entropie de Shannon H, IAT Burstiness B, RTT Latency, Cycles 24h     │
 ├────────────────────────────────────────────────────────────────────────┤
 │ COUCHE 2 : PSYCHOLINGUISTIQUE, ACTES DE LANGAGE & SÉMIOTIQUE           │
 │ ↳ 4 Cavaliers Gottman, Actes performatifs (Searle), Morphologie        │
 ├────────────────────────────────────────────────────────────────────────┤
 │ COUCHE 1 : INGESTION UNIVERSELLE, NORMALISATION & HYGIÈNE PII          │
 │ ↳ Meta (Insta/Mess), WhatsApp, Telegram, Discord, iMessage, CSV/JSONL  │
 └────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Détail des 7 Couches Techniques

### Couche 1 : Ingestion Universelle & Normalisation (`universal_chat_converter.py`)
- **Connecteurs supportés** :
  - *Meta GDPR Exports* (Instagram DMs, Facebook Messenger) : Gestion du double décodage latin1 ➔ UTF-8.
  - *WhatsApp Text Exports* : Multi-lignes, horodatages européens (`DD/MM/YYYY`) et US (`MM/DD/YY`), pièces jointes omises.
  - *Telegram Desktop Exports* (`result.json`) : Extraction des messages texte, vocaux et réactions.
  - *Discord Exports* (via DiscordChatExporter JSON/CSV).
  - *Apple iMessage / SMS* : Dumps standardisés CSV/JSON.
  - *JSON Lines (JSONL)* et JSON génériques.
- **Hygiène & Anonymisation PII** : Filtrage automatique des numéros de carte bancaire, numéros de téléphone (BE, FR, intl), adresses emails, IBAN et coordonnées privées tout en préservant intacts les surnoms, émojis et tonalités affectives.
- **Format Canonique Pivot** : `templates/normalized_chat_schema.json`.

---

### Couche 2 : Psycholinguistique & Actes de Langage (`analyze_chat_metrics.py`)
- **Détecteur des 4 Cavaliers de Gottman** :
  - *Critique* (attaques globales d'identité vs faits précis).
  - *Mépris* (sarcasmes, condescendance, dédain - toxique n°1).
  - *Défense* (victimisation, rejet de responsabilité).
  - *Dérobade* (retrait brutal, monosyllabes hostiles).
- **Pragmatique des Actes Performatifs (Searle/Austin)** :
  - Identification des énoncés déclaratifs qui changent la réalité du couple (*« On est en couple alors ? »*).
  - Évaluation de la clause de validité vocale (*« Quand tu le verbaliseras... »*).
- **Morphologie Affective** :
  - Suffixations hypocoristiques (*-ou*, animalisations tendres, fusions de prénoms).
  - Température émotionnelle : Allongements (*« ouiiiii »*), majuscules d'emphase, syntaxe exclamative.

---

### Couche 3 : Théorie de l'Information & Stochastique (`analyze_chat_metrics.py`)
- **Entropie de Shannon de Prise de Parole ($H$)** :
  $$H = -\sum_{i=1}^{n} p_i \log_2(p_i) \quad \text{normalisé sur } [0, 1]$$
  Mesure l'équité informationnelle des tours de parole.
- **Inter-Arrival Time (IAT) & Paramètre de Burstiness ($B$)** :
  $$B = \frac{\sigma_{IAT} - \mu_{IAT}}{\sigma_{IAT} + \mu_{IAT}} \in [-1, 1]$$
  Distingue les flux réguliers périodiques ($B < 0$) des clusters humains passionnels ($B > 0$).
- **Response Turnaround Time (RTT)** :
  Distribution de la latence médiane en secondes, filtrée des cycles de sommeil (> 4 h).
- **Régularité Circadienne & Hebdomadaire** :
  Histogramme horaire 24h et matrice d'activité Lundi-Dimanche.

---

### Couche 4 : Formulation Clinique & Neurobiologie (`references/`, `generate_relationship_report.py`)
- **Modèle des 4P** : Prédéterminants, Précipitants, Perpétuants, Protecteurs.
- **Échelle de Mentalisation (Fonagy)** :
  - *Niveau Réflexif* : Compréhension de l'intériorité et des émotions de l'autre.
  - *Mode Téléologique* : Preuve obligatoire par l'acte ou le son réel.
  - *Mode Équivalence Psychique* : Le ressenti intérieur est confondu avec la réalité du partenaire.
  - *Mode Semblant* : Vannes systématiques pour esquiver l'intimité brute.
- **Théorie Polyvagale (Porges)** :
  - Suivi de la bascule entre tonus ventral vagal (sécurité), mobilisation sympathique (rafales anxieuses) et shutdown dorsal vagal (retrait total).

---

### Couche 5 : Sociogramme & Systémique Bowen (`references/sociogram_and_triangulation.md`)
- **Cartographie des Tiers Pivots** :
  - Tiers Tampons (amis communs, régulateurs d'anxiété).
  - Tiers Ancrages (mère, grand-père, lignée sacrée).
  - Tiers Fétiches (terrain, maison en construction, animal).
- **Triangle Dramatique de Karpman ➔ TED (The Empowerment Dynamic)** :
  - Sortir de la dynamique Sauveur/Victime pour adopter la posture Coach/Créateur.
- **Sanctuarisation des Frontières** :
  - Confidentialité externe stricte et autonomie interne (50/50 sans emprise).

---

### Couche 6 : Simulation Non Linéaire & Chaos (`simulate_conversational_scenarios.py`)
- **Attracteur Étrange du Couple** : Modélisation des orbites stables et des cycles de réinitialisation.
- **Simulateur de Stress « What-If »** :
  - Évaluation dynamique de crises probables (Silence prolongé, laconisme '👍', indiscrétion d'amis, choc matériel/financier).
  - Génération prédictive de la trajectoire et prescription de l'antidote.

---

### Couche 7 : Présentation Multi-Surfaces & Cockpit Interactif CLI
- **Cockpit Terminal Interactif & Mode Batch (`scripts/interactive_profiler_cli.py`)** :
  - Menu textuel complet de navigation [0-6] pour piloter l'ensemble du framework.
  - Pipeline automatisé `--run-all` produisant les 4 artefacts de restitution (JSON normalisé, métriques quantitatives, rapport clinique 360°, tableau de bord HTML).
- **Rapport Exécutif Markdown 360° (`scripts/generate_relationship_report.py`)** : Score de santé relationnelle sur 100 points.
- **Tableau de Bord Visuel Interactif HTML/SVG (`scripts/export_html_dashboard.py`)** : Visualisation graphique autonome (100% offline, zéro CDN).
- **Playbook de Désescalade Immédiate (`references/crisis_deescalation_playbook.md`)** : Arbres décisionnels (Protocoles Alpha, Beta, Gamma, Delta).
