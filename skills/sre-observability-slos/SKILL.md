---
name: sre-observability-slos
description: >-
  Design and manage Site Reliability Engineering (SRE) systems: SLI/SLO definition, error budget calculation and burn rates, Prometheus metric collectors & alerting rules, Grafana dashboard architecture, blameless incident post-mortems, and load testing with k6.
---

# 📈 SRE, Observability, SLOs & Production Reliability

> **Standard :** Google Site Reliability Engineering (SRE) Framework  
> **Core Axiom :** *"100% availability is the wrong target for almost everything. Define Service Level Objectives (SLOs), measure Service Level Indicators (SLIs), track Error Budget Burn Rates, and embrace blameless incident post-mortems."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

L'ingénierie SRE (Site Reliability Engineering, inventée par Google), c'est la différence entre **un pompier épuisé qui éteint des incendies toute la nuit** et **un architecte qui construit un bâtiment ignifugé** :
- **SLI (Service Level Indicator - Le Thermomètre)** : C'est ce que tu mesures concrètement. Par exemple : *"99.2% de nos requêtes répondent en moins de 200 ms."*
- **SLO (Service Level Objective - L'Objectif Officiel)** : C'est l'engagement de l'équipe. Par exemple : *"On vise 99.0% de requêtes rapides sur 30 jours."*
- **L'Error Budget (Le Droit à l'Erreur)** : Si ton objectif est de 99.0%, tu as le droit à 1% d'erreurs ! Tant qu'il te reste du budget, tu peux déployer de nouvelles fonctionnalités rapidement. Si tu grilles ton budget d'erreur, on gèle les déploiements et toute l'équipe se concentre sur la stabilité.
- **Le Post-Mortem Blameless (Sans Blâme)** : Quand un serveur tombe en panne, on ne cherche JAMAIS de coupable individuel. On cherche **pourquoi le système a permis l'erreur humaine** et on met en place des barrières pour que ça n'arrive plus jamais.
- **L'Observabilité selon Charity Majors (Le Télescope)** : En production, le code doit expliquer son état interne via des événements JSON structurés larges (wide events). Quand une requête échoue ou ralentit, on ne doit pas deviner : la trace (`trace_id`, `span_id`, durée en ms) doit donner la cause exacte immédiatement.

---

## 🔭 2. Les 4 Invariants de l'Observabilité Applicative (Charity Majors ODD)

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Événements JSON Structurés (Bannir les prints bruts)     │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Haute Cardinalité (trace_id, customer_id, store_id)      │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Mesure de Durée Monotone Haute Résolution (perf_counter) │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Zéro Panne Silencieuse (Capture explicite des causes)    │
 └─────────────────────────────────────────────────────────────┘
```

Exemple d'événement canonique émis en production :
```json
{
  "timestamp": "2026-10-24T14:30:00Z",
  "level": "INFO",
  "event": "order_processed",
  "trace_id": "tr-7f9a8b1c",
  "customer_id": "cus_9942",
  "duration_ms": 142.5,
  "http_status": 200
}
```

---

## 📐 3. Mathématiques des SLOs & Burn Rate

### Formule de Disponibilité (SLI)
$$\text{SLI} = \frac{\text{Requêtes Valides et Réussies}}{\text{Total des Requêtes Reçues}} \times 100$$

### Budget d'Erreur (Error Budget)
Pour un SLO de $99.9\%$ ($3\text{ nines}$) sur une fenêtre de 30 jours ($43\,200\text{ minutes}$) :
$$\text{Budget d'Erreur} = 100\% - 99.9\% = 0.1\% \implies 43.2\text{ minutes d'indisponibilité autorisée par mois.}$$

### Taux de Consommation (Burn Rate Alerting)
Plutôt que d'attendre la fin du mois pour voir si le budget est dépassé, on déclenche une alerte PagerDuty si le taux de consommation s'envole :
- **Burn Rate de $14.4\times$** : Consomme 10% du budget d'erreur mensuel en 5 heures. Déclenche une alerte immédiate (Page d'urgence).
- **Burn Rate de $6\times$** : Consomme 5% du budget en 6 heures. Notification par ticket ou Slack.

---

## 📊 3. Règles Prometheus & Alertmanager (`prometheus.rules.yml`)

```yaml
groups:
  - name: api_slo_alerts
    rules:
      # Calcul du SLI de disponibilité sur 5 minutes
      - record: job:api_requests:sli_availability
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))

      # Alerte si le Burn Rate dépasse 14.4 sur 1 heure
      - alert: FastErrorBudgetBurn
        expr: |
          (1 - job:api_requests:sli_availability) > (1 - 0.999) * 14.4
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Consommation rapide du budget d'erreur (Burn Rate 14.4x)"
          description: "Le service api-service consomme son budget mensuel à un rythme critique."
```

---

## 🧪 4. Tests de Charge de Production avec k6

Pour valider qu'un service respecte ses SLOs sous forte charge (ex: 500 utilisateurs virtuels concurrents) :

```javascript
// load_test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },   // Montée en charge progressive
    { duration: '1m', target: 500 },    // Pic de trafic
    { duration: '30s', target: 0 },     // Redescente
  ],
  thresholds: {
    // SLO de latence : 95% des requêtes sous 250ms
    http_req_duration: ['p(95)<250'],
    // SLO de disponibilité : moins de 0.1% d'erreurs HTTP 5xx
    http_req_failed: ['rate<0.001'],
  },
};

export default function () {
  const res = http.get('https://api.yourdomain.com/v1/health');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  sleep(1);
}
```

---

## 📋 5. Template de Post-Mortem Blameless (Markdown)

```markdown
# 📝 Post-Mortem d'Incident : [Titre Clair de l'Incident]

- **Date :** YYYY-MM-DD
- **Durée totale :** 47 minutes (14:15 UTC -> 15:02 UTC)
- **Impact utilisateur :** 12 400 utilisateurs ont rencontré une erreur 502 lors du checkout.
- **Budget d'erreur consommé :** 18% du budget mensuel.

## 🕒 Chronologie des Événements
- **14:15 UTC** : Déploiement de la version v2.4.1.
- **14:18 UTC** : Déclenchement de l'alerte Prometheus `FastErrorBudgetBurn`.
- **14:22 UTC** : L'ingénieur d'astreinte commence l'investigation et isole le service de facturation.
- **14:35 UTC** : Identification du problème : migration de base de données sans `lock_timeout`.
- **14:48 UTC** : Rollback vers v2.4.0 validé.
- **15:02 UTC** : Trafic nominal rétabli, métriques vertes.

## 🔍 Cause Racine (Root Cause - 5 Pourquoi)
1. Pourquoi le service a-t-il planté ? La base de données ne répondait plus.
2. Pourquoi ne répondait-elle plus ? Toutes les connexions étaient bloquées.
3. Pourquoi étaient-elles bloquées ? Une migration `ALTER TABLE` a posé un verrou exclusif.
4. Pourquoi n'a-t-elle pas échoué proprement ? Aucun `lock_timeout` n'était configuré.
5. Pourquoi n'était-ce pas détecté en pré-production ? Les tests de charge ne simulaient pas d'accès concurrents pendant la migration.

## ✅ Actions Correctives (Preventive Action Items)
- [ ] Configurer `SET lock_timeout = '2s'` dans la pipeline de migration CI/CD.
- [ ] Ajouter un test de migration sous charge dans la suite k6.
- [ ] Automatiser le rollback si le taux d'erreur dépasse 1% pendant 3 minutes consécutives.
```

---

## 🛠️ 6. Outillage Déterministe CLI SRE & Observabilité

Deux scripts Python autonomes sont fournis dans le dossier `scripts/` :

### 1. Calculateur de SLO & Burn Rates Prometheus
```bash
python scripts/calc_slo_burn.py 99.9 --window 30
```
Fournit les minutes de panne autorisées, les seuils de burn rate 14.4x / 6x, et produit le bloc YAML Prometheus complet prêt à l'emploi.

### 2. Validateur de Logs Structurés ODD (Charity Majors)
```bash
python scripts/validate_structured_logs.py --log-file production.log
```
Vérifie la validité JSON des événements, la présence des champs obligatoires (`timestamp`, `level`, `event`), du `trace_id` de haute cardinalité et de la métrique `duration_ms`.
