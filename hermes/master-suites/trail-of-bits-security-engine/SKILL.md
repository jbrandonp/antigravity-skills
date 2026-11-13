---
name: trail-of-bits-security-engine
description: >-
  Trail of Bits software security methodology and static analysis orchestrator. Enforces automated AST taint tracking, constant-time arithmetic verification (side-channel mitigation), Semgrep/CodeQL pattern orchestration, and software supply chain dependency audits.
version: 1.0.0
tags:
  - trail-of-bits
  - security-audit
  - static-analysis
  - codeql
  - semgrep
  - side-channel
---

# 🛡️ Trail of Bits Security Engine: Formal Static Analysis & AST Auditing

> **Inspiration :** Trail of Bits security consulting methodology, Semgrep Rulesets, CodeQL query models, and Constant-Time Cryptographic Auditing.  
> **Axiome Central :** Ne confie pas l'analyse de sécurité critique aux seules hallucinations stochastiques d'un LLM. Utilise des analyseurs statiques déterministes, inspecte le flux de données (*taint analysis*) et vérifie l'absence de fuites temporelles.

---

## 🔍 Mécanismes Internes & Capacités

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. CONSTANT-TIME VERIFICATION: Détection des failles timing │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. AST TAINT TRACKING: Traque des entrées non assainies     │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. DANGEROUS SINKS: Éradication de eval(), shell=True, SQL  │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. SUPPLY CHAIN AUDIT: Détection de paquets typosquattés    │
 └─────────────────────────────────────────────────────────────┘
```

---

## 💻 Utilisation du Moteur Déterministe

Le skill inclut un moteur d'analyse statique autonome en Python standard :

```bash
# Scanner un répertoire ou un fichier source
python skills/trail-of-bits-security-engine/scripts/static_analyzer.py --target src/

# Scanner avec sortie au format JSON machine-readable
python skills/trail-of-bits-security-engine/scripts/static_analyzer.py --target src/ --format json --output audit-report.json

# Mode paranoïaque (arrête le build si score de sécurité < 90)
python skills/trail-of-bits-security-engine/scripts/static_analyzer.py --target src/ --strict
```

---

## 📋 Règles Vérifiées par Défaut

1. **Vérification Constant-Time :**
   - Interdiction de comparer des tokens d'authentification ou des signatures HMAC avec l'opérateur d'égalité direct `==` (vulnérable aux attaques temporelles).
   - Obligation d'utiliser `hmac.compare_digest()` ou équivalent à temps constant.

2. **Éradication des Puits Dangereux (Dangerous Sinks) :**
   - Détection d'appels à `eval()`, `exec()`, `pickle.loads()`, `yaml.unsafe_load()`.
   - Détection de `subprocess.run(..., shell=True)` recevant des variables externes non filtrées.

3. **Injection SQL & Échappement :**
   - Détection des requêtes SQL concaténées avec f-strings ou `%s` au lieu de requêtes paramétrées avec tuples `?`.
