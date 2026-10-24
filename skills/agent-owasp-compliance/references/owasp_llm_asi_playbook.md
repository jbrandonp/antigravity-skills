# 🛡️ OWASP Agentic Security Initiative (ASI 2026) Playbook

> **Standard :** OWASP ASI Top 10 Standards for Autonomous AI Agents  
> **Core Axiom :** *"Agentic security is not about filtering text output; it is about governing action execution, enforcing cryptographic trust boundaries, and guaranteeing deterministic policy gates."*

---

## 🧭 1. Les 10 Risques Critiques de l'OWASP ASI

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ ASI-01 : Protection contre les Injections de Prompt        │
 ├─────────────────────────────────────────────────────────────┤
 │ ASI-02 : Gouvernance Sécurisée des Outils (Allowlists)      │
 ├─────────────────────────────────────────────────────────────┤
 │ ASI-03 : Limitation de l'Agence & Anneaux d'Exécution       │
 ├─────────────────────────────────────────────────────────────┤
 │ ASI-04 : Contrôle des Élévations de Privilèges              │
 ├─────────────────────────────────────────────────────────────┤
 │ ASI-05 : Cloisonnement & Vérification Cryptographique       │
 ├─────────────────────────────────────────────────────────────┤
 │ ASI-06 : Journalisation Immuable & Chaînage de Hashs        │
 ├─────────────────────────────────────────────────────────────┤
 │ ASI-07 : Identité Cryptographique (DIDs / Clés Ed25519)     │
 ├─────────────────────────────────────────────────────────────┤
 │ ASI-08 : Évaluation Déterministe des Politiques (Zero-LLM)  │
 ├─────────────────────────────────────────────────────────────┤
 │ ASI-09 : Intégrité de la Chaîne d'Approvisionnement (SBOM)  │
 ├─────────────────────────────────────────────────────────────┤
 │ ASI-10 : Disjoncteurs Comportementaux & Bouton d'Arrêt      │
 └─────────────────────────────────────────────────────────────┘
```

---

## 💻 2. Modèles d'Implémentation Recommandés

### 🔒 ASI-01 : Séparation Stricte des Enveloppes de Prompt
Ne mélangez jamais les données externes non fiables avec les instructions système.
```python
def format_safe_user_prompt(system_rules: str, untrusted_data: str) -> str:
    # Utilisation d'un délimiteur XML strict et typage
    escaped = untrusted_data.replace("<untrusted_input>", "").replace("</untrusted_input>", "")
    return f"""{system_rules}

<untrusted_input context="external_user_query">
{escaped}
</untrusted_input>"""
```

### ⚙️ ASI-02 : Allowlists et Validation Pydantic V2
```python
from pydantic import BaseModel, Field
from typing import Dict, Callable

class SafeSearchArgs(BaseModel):
    query: str = Field(..., max_length=120)
    limit: int = Field(default=5, ge=1, le=20)

ALLOWED_TOOLS: Dict[str, Callable] = {
    "search": lambda **args: execute_search(SafeSearchArgs(**args))
}
```

### 💍 ASI-03 : Anneaux d'Exécution (Execution Rings)
- **Ring 0 (Noyau Critique)** : Déploiement en production, suppression de base de données. *Exige une attestation SRE / clé physique.*
- **Ring 1 (Mutation Standard)** : Écriture en base, envoi d'emails. *Exige un jeton de confirmation.*
- **Ring 2 (Lecture Seule)** : Requêtes SQL `SELECT`, recherche web, lecture de fichiers. *Automatisé.*
- **Ring 3 (Brouillon & Synthèse)** : Génération de texte, calculs locaux. *Automatisé sans outil externe.*

### ⛓️ ASI-06 : Chaîne de Hash d'Audit (AuditChain)
```python
import hashlib, json, time

class AuditChain:
    def __init__(self):
        self.last_hash = "0" * 64

    def log_action(self, agent_id: str, tool: str, args: dict, result: str) -> dict:
        entry = {
            "timestamp": time.time(),
            "agent_id": agent_id,
            "tool": tool,
            "args": args,
            "result_digest": hashlib.sha256(result.encode()).hexdigest(),
            "prev_hash": self.last_hash
        }
        serialized = json.dumps(entry, sort_keys=True)
        self.last_hash = hashlib.sha256(serialized.encode()).hexdigest()
        entry["entry_hash"] = self.last_hash
        return entry
```

### 🛑 ASI-10 : Disjoncteur Automatique (Circuit Breaker)
```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, reset_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.failures = 0
        self.state = "CLOSED"  # CLOSED (Normal), OPEN (Bloqué)

    def record_failure(self):
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
            print("🚨 CIRCUIT BREAKER TRIPPED: Agent halted.")

    def record_success(self):
        self.failures = 0
        self.state = "CLOSED"
```

---

## 🛠️ 3. Commandes CLI Déterministes

```bash
# Scanner une base de code agentique
python scripts/scan_owasp_compliance.py --root .

# Sortie structurée JSON pour intégration CI/CD
python scripts/scan_owasp_compliance.py --root . --json

# Générer l'attestation officielle de conformité
python scripts/generate_security_attestation.py --agent "SupportBot" --version "1.0.0"
```
