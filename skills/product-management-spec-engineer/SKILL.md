---
name: product-management-spec-engineer
description: >-
  Author professional Product Requirements Documents (PRD), Technical Architecture RFCs, Architecture Decision Records (ADRs), and Agile sprint planning user stories with INVEST criteria and explicit acceptance tests.
---

# 📋 Product Management, Technical RFCs & Agile Specifications

> **Standard :** Big Tech Product Management & Engineering Alignment  
> **Core Axiom :** *"Writing code without a rigorous specification is the fastest way to build the wrong product. A great engineer clarifies user problems, quantifies success metrics, documents non-goals, and explores rejected architectural alternatives before touching a single line of code."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Dans une équipe de développement, **coder sans plan précis, c'est comme commencer à couler du béton sans plan d'architecte** :
- **Le PRD (Product Requirements Document - La Vision du Produit)** : C'est le document écrit pour expliquer *POURQUOI* on fabrique cette fonctionnalité, *POUR QUI*, et *COMMENT* on saura si c'est un succès (ex: *"Augmenter le taux de conversion de 5%"*).
- **La RFC (Request for Comments - Le Débat Technique)** : C'est l'architecte technique qui propose : *"Voilà comment je compte structurer le backend. J'ai envisagé l'option A et l'option B, et j'ai rejeté l'option B pour telle raison. Qu'en pensez-vous ?"*
- **L'ADR (Architecture Decision Record - Le Journal des Choix)** : Un document court qui fige une décision majeure pour que dans 2 ans, personne ne se demande *"Mais pourquoi ils ont choisi PostgreSQL plutôt que MongoDB en 2026 ?"*.
- **Les User Stories INVEST** : Une façon propre de découper le travail en petites tâches claires, indépendantes et testables.

---

## 📄 2. Template de PRD de Production (Product Requirements Document)

```markdown
# 🚀 PRD : [Nom de la Fonctionnalité]

- **Auteur :** [Nom]
- **Statut :** [Brouillon | En Revue | Approuvé | Déployé]
- **Date :** YYYY-MM-DD
- **Target Release :** Q2 2026

---

## 🎯 1. Problème Utilisateur & Opportunité
[Décrire en 2-3 paragraphes clairs quel problème réel rencontre l'utilisateur et pourquoi c'est douloureux aujourd'hui.]

## 👥 2. Personas Cibles
- **Persona Principal :** [Ex: Brandon, développeur indépendant créant des microservices]
- **Cas d'usage :** [Ex: Déployer son API en 1 commande sans gérer de serveurs complexes]

## 🚫 3. Non-Goals (Ce que nous NE ferons PAS dans cette version)
- Nous ne supporterons pas le multi-région dans la v1.
- Nous ne construirons pas de tableau de bord graphique dédié (CLI uniquement).

## 📊 4. Métriques de Succès (KPIs)
- **Objectif Principal :** Réduire le temps de déploiement moyen sous les 60 secondes.
- **Taux d'adoption :** 40% des utilisateurs actifs créent au moins un projet la première semaine.
- **Fiabilité :** Taux de succès des déploiements $\ge 99.5\%$.

## 📝 5. User Stories & Critères d'Acceptation (Gherkin)

### Story 1: Création d'une clé API sécurisée
En tant que développeur,  
Je veux générer une clé API secrète depuis mon terminal,  
Afin d'authentifier mes requêtes CI/CD sans stocker mon mot de passe.

**Critères d'acceptation :**
- [ ] La clé est affichée une seule fois à la création (`sk_live_...`).
- [ ] Le hash SHA-256 de la clé est stocké en base, jamais la clé brute.
- [ ] La clé peut être révoquée instantanément depuis le CLI.
```

---

## 🏛️ 3. Template de RFC Technique (Request for Comments)

```markdown
# 🛠️ RFC : [Titre Architectural]

- **Date :** YYYY-MM-DD
- **Décideurs :** [Équipe Technique]

## 1. Contexte & Motivation
[Pourquoi l'architecture actuelle atteint ses limites.]

## 2. Solution Proposée
[Diagrammes de séquence, schéma de données, contrats d'API.]

## 3. Alternatives Rejetées (Trade-offs)
| Option | Avantages | Inconvénients | Raison du Rejet |
|---|---|---|---|
| **Option A (Redis Pub/Sub)** | Ultra-rapide | Pas de persistance des messages | Risque de perte de données en cas de crash |
| **Option B (Kafka)** | Très haute capacité | Trop lourd à opérer pour notre échelle | Surcoût opérationnel inutile |
| **Option Retenue (RabbitMQ)** | Fiable, persistant, léger | Moins scalable que Kafka | Parfait compromis pour notre volume actuel |

## 4. Stratégie de Déploiement & Rollback
- Déploiement progressif (Canary 10% -> 50% -> 100%).
- Procédure de retour arrière immédiat si latence $p99 > 300\text{ ms}$.
```

---

## 📐 4. Les Critères INVEST pour une User Story Parfaite

Toute tâche découpée pour un sprint agile doit respecter les 6 critères :
1. **I - Independent** : La tâche ne bloque pas et n'est pas bloquée par une autre tâche du sprint.
2. **N - Negotiable** : La solution technique peut être adaptée avec l'équipe.
3. **V - Valuable** : La tâche apporte une valeur concrète visible pour l'utilisateur.
4. **E - Estimable** : La complexité est claire et peut être chiffrée en story points.
5. **S - Small** : La tâche se termine en 1 à 2 jours maximum.
6. **T - Testable** : On peut prouver mathématiquement par un test automatisé si elle est réussie ou ratée.
