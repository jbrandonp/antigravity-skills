---
name: monorepo-release-engineering
description: >-
  Manage monorepos, release automation, and software supply chains: Turborepo/Nx, pnpm workspaces, automated Semantic Versioning (SemVer), changelog generation, Software Bill of Materials (SBOM), and CI/CD secret management (Vault/SOPS).
---

# 📦 Monorepo, Release Engineering & Software Supply Chain

> **Standard :** Multi-Package Workspaces & Automated Continuous Delivery SOTA 2026  
> **Core Axiom :** *"A commit on main should automatically calculate its semantic version, update the changelog, build only affected packages with remote caching, and publish verifiable release artifacts accompanied by cryptographic signatures and an SBOM."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Gérer un gros projet avec plusieurs applications (par exemple un site web, une application mobile, et un backend qui partagent tous les mêmes types de données), c'est comme **une usine avec plusieurs lignes de montage** :
- **Le Monorepo (L'Usine Unique avec Turborepo / pnpm)** : Au lieu d'avoir 10 dépôts GitHub séparés où tu dois mettre à jour tes paquets à la main, tout ton code vit dans un seul dépôt géant. Si tu modifies un modèle de données, le site web et l'application mobile sont mis à jour ensemble en temps réel.
- **Le Cache Intelligent (Remote Caching)** : Si tu modifies juste la page d'accueil du site web, Turborepo ne recompile PAS le backend ni l'application mobile. Il réutilise le résultat de la compilation précédente en 0.2 seconde !
- **Semantic Versioning Automatique (SemVer)** : Tu n'as plus à te demander si ta version s'appelle `1.2.3` ou `1.3.0`. Tes messages de commit (`feat:`, `fix:`, `chore:`) indiquent automatiquement à l'ordinateur s'il doit incrémenter le numéro majeur, mineur ou patch.
- **Le SBOM (La Liste des Ingrédients Alimentaires)** : C'est la liste officielle de toutes les librairies externes utilisées dans ton logiciel. Les grandes entreprises l'exigent pour vérifier qu'aucune dépendance n'a de virus ou de faille de sécurité connue.

---

## 🏗️ 2. Structure Canonique d'un Monorepo (pnpm + Turborepo)

```text
my-monorepo/
├── apps/
│   ├── web/                # Application frontend Next.js / React
│   │   └── package.json
│   ├── mobile/             # Application Expo / React Native
│   │   └── package.json
│   └── api/                # Backend API FastAPI / Node
│       └── package.json
├── packages/
│   ├── ui/                 # Composants d'interface partagés
│   ├── config/             # Configs ESLint, Prettier, TypeScript
│   └── types/              # Types et schémas TypeScript / Zod partagés
├── pnpm-workspace.yaml     # Déclaration des espaces de travail
├── turbo.json              # Graphe des tâches et configuration du cache
└── package.json
```

### Configuration du Cache Turborepo (`turbo.json`)
```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": []
    },
    "lint": {
      "outputs": []
    }
  }
}
```

---

## 🏷️ 3. Versioning Sémantique Automatisé (`changesets`)

Plutôt que des versions arbitraires, utiliser `@changesets/cli` pour orchestrer les publications multi-paquets :

```bash
# 1. Déclarer une modification lors d'une PR (génère un fichier markdown temporaire)
pnpm changeset

# 2. En CI sur main : Calculer les nouvelles versions et mettre à jour les CHANGELOG.md
pnpm changeset version

# 3. Publier les paquets modifiés vers npm / registries internes
pnpm changeset publish
```

---

## 🛡️ 4. Génération de SBOM (Software Bill of Materials) avec Syft

Générer la nomenclature logicielle au format standardisé SPDX ou CycloneDX pour la conformité et la sécurité :

```bash
# Générer le SBOM complet de l'application au format CycloneDX JSON
syft dir:. -o cyclonedx-json=sbom.json

# Scanner le SBOM généré contre les vulnérabilités de sécurité avec Grype
grype sbom:sbom.json --fail-on high
```

---

## 🔒 5. Chiffrement des Secrets dans Git avec SOPS et age

Pour versionner les secrets de déploiement dans le dépôt Git sans aucun risque de fuite :

```bash
# Chiffrer un fichier de secrets pour les membres autorisés de l'équipe
sops --encrypt --age $(cat ~/.age/key.pub) secrets.prod.env > secrets.prod.enc.env

# Déchiffrer à la volée pendant le déploiement CI/CD
sops --decrypt secrets.prod.enc.env > secrets.env
```
