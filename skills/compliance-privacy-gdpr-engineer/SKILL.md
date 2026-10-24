---
name: compliance-privacy-gdpr-engineer
description: >-
  Audit and implement software privacy compliance, GDPR/RGPD regulations, open-source license compatibility, and European AI Act requirements. Enforces privacy-by-design, cookie consent architectures, right-to-erasure workflows, data processing registers, and license risk triage.
---

# ⚖️ Software Compliance, Privacy Engineering & GDPR / AI Act

> **Standard :** European GDPR / RGPD (2018), EU AI Act (2024/2026) & Open Source Legal Hygiene  
> **Core Axiom :** *"Privacy and legal compliance cannot be retrofitted on a finished product. Design software with privacy-by-design, enforce minimal data retention, verify third-party license compatibility, and document automated data erasure workflows."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Créer un logiciel sans respecter les lois de protection des données, c'est comme **ouvrir un restaurant sans respecter les normes d'hygiène** : tu risques des amendes géantes (jusqu'à 20 millions d'euros ou 4% du chiffre d'affaires mondial avec le RGPD !) et la fermeture de ton service.

- **Le RGPD (Règlement Général sur la Protection des Données)** : C'est la loi européenne qui dit que les données d'un utilisateur lui appartiennent. S'il te demande *"Supprimez toutes mes données personnelles"* (le *Droit à l'oubli*), ton code doit être capable d'effacer son compte et ses traces en un clic.
- **Privacy-by-Design (La Discrétion par Défaut)** : Tu ne collectes JAMAIS d'informations inutiles. Si ton application est une calculatrice, elle n'a pas besoin de demander la géolocalisation de l'utilisateur !
- **Les Licences Open Source (Ne pas se faire piéger)** : Si tu utilises une librairie sous licence **GPL-3.0** dans ton code propriétaire fermé, la licence te force légalement à rendre tout ton code source public et gratuit ! Tu dois savoir trier les licences permissives (**MIT, Apache 2.0**) et les licences virales (**GPL, AGPL**).
- **L'EU AI Act (La Régulation de l'IA)** : La nouvelle loi européenne qui classe les systèmes d'IA selon leur niveau de risque (Minime, Spécifique, Élevé, Inacceptable).

---

## 📋 2. Les 5 Piliers du RGPD Technique

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Minimisation des Données (Collecter le strict minimum)   │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Base Légale Claire (Consentement explicite ou contrat)   │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Droit à l'Effacement (Workflow automatisé de suppression)│
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Registre des Traitements (Article 30 du RGPD)            │
 ├─────────────────────────────────────────────────────────────┤
 │ 5. Analytics Privacy-First (Plausible / Umami sans cookies) │
 └─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 3. Implémentation du Droit à l'Effacement (Hard Delete vs Anonymisation)

Lorsqu'un utilisateur demande la suppression de ses données :
- **Données personnelles supprimées immédiatement** : Nom, prénom, email, téléphone, IP, photo.
- **Données de facturation (Obligation fiscale légale)** : Conservées 10 ans selon la loi, mais déconnectées de l'identité et archivées de façon chiffrée.

```python
# Workflow d'effacement conforme RGPD
async def process_gdpr_erasure_request(user_id: str, db_session):
    async with db_session.begin():
        # 1. Suppression des données personnelles directes
        await db_session.execute(
            delete(UserProfile).where(UserProfile.user_id == user_id)
        )
        await db_session.execute(
            delete(UserSessions).where(UserSessions.user_id == user_id)
        )
        
        # 2. Anonymisation des logs d'activité (conservation des métriques pures)
        await db_session.execute(
            update(ActivityLogs)
            .where(ActivityLogs.user_id == user_id)
            .values(user_id=None, ip_address="0.0.0.0", user_agent="ANONYMIZED")
        )
        
        # 3. Marquer le compte comme effacé dans le registre d'audit
        await record_audit_event(event="gdpr_erasure_completed", subject_id=user_id)
```

---

## 📜 4. Matrice de Triage des Licences Open Source

| Licence | Type | Utilisation Commerciale Propriétaire ? | Risque de Contamination |
|---|---|:---:|:---:|
| **MIT / ISC** | Très permissive | ✅ Oui, sans restriction | 🟢 Zéro risque |
| **Apache 2.0** | Permissive + Protection Brevet | ✅ Oui (mentionner la licence) | 🟢 Zéro risque |
| **BSD 2/3-Clause**| Permissive | ✅ Oui | 🟢 Zéro risque |
| **LGPL-3.0** | Copyleft faible | ⚠️ Oui, si lié dynamiquement (`shared library`) | 🟡 Risque modéré |
| **GPL-3.0** | Copyleft fort (Viral) | ❌ Non, force à ouvrir tout le code en GPL | 🔴 Risque critique |
| **AGPL-3.0** | Copyleft réseau (SaaS Viral)| ❌ Non, contamine tout code accédé par réseau | 🚨 Risque maximal |

---

## 🍪 5. Analytics Privacy-First (Sans Bannière de Cookies)

Pour respecter la vie privée et se dispenser légalement des bannières de cookies invasives, utiliser des solutions exemptées de consentement (CNIL / GDPR compliant) comme **Plausible Analytics** ou **Umami** :

```html
<!-- Script Plausible : Aucun cookie, aucune donnée personnelle stockée, 100% conforme RGPD sans bannière -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

---

## 🛠️ 6. Scanner Déterministe de Données Personnelles (PII)

Un scanner Python est inclus pour auditer automatiquement vos modèles et schémas de code :
```bash
python scripts/scan_pii_fields.py src/
```
Détecte les champs à risque (SSN, IBAN, santé, biométrie) et les données personnelles (email, IP, téléphone), et rappelle la mise en place obligatoire du droit à l'effacement.
