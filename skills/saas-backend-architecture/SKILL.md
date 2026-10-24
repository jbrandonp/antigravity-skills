---
name: saas-backend-architecture
description: >-
  Design and implement production SaaS backend services: OAuth2/OIDC, JWT & RBAC/ABAC authorization, Stripe Checkout & Billing subscriptions, webhook HMAC signature verification with idempotency keys, Redis caching & rate limiting, background job queues (BullMQ/Celery), and transactional email delivery (Resend).
---

# 💳 SaaS Backend Architecture & Revenue Systems

> **Standard :** Multi-Tenant SaaS Architecture SOTA 2026  
> **Core Axiom :** *"A SaaS platform must guarantee four invariants: multi-tenant isolation, cryptographic webhook verification with strict idempotency, resilient background jobs, and graceful rate-limited third-party integrations."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Créer le backend d'un logiciel SaaS (Software as a Service comme Netflix, Spotify ou Notion), c'est installer **les organes vitaux de ton business** :
1. **L'Authentification & Rôles (La Carte d'Accès)** : Savoir qui est connecté (via Google, GitHub ou email/mot de passe), et ce qu'il a le droit de faire (`Admin`, `Membre`, `Lecteur`).
2. **Le Système d'Abonnement Stripe (Le Guichet Automatique)** : Gérer les paiements récurrents mensuels, les cartes expirées, et couper l'accès si la personne arrête de payer.
3. **L'Idempotence des Webhooks (Le Carnet de Reçus)** : Quand Stripe envoie un message disant *"Paiement réussi pour Brandon"*, Internet peut avoir un hoquet et renvoyer le même message 3 fois. Grâce à la clé d'idempotence, ton serveur note le reçu la première fois et ignore les doublons pour ne jamais facturer deux fois le client !
4. **Les Files d'Attente en Arrière-Plan (La Cuisine Séparée)** : Quand un utilisateur clique sur *"Créer un compte"*, le serveur ne le fait pas attendre 5 secondes que l'e-mail parte. Il lui répond immédiatement *"Compte créé !"* et confie l'envoi de l'e-mail à un robot en tâche de fond (Redis + BullMQ/Celery).

---

## 🔐 2. Le Modèle d'Authentification & RBAC

```text
               [ Requête Utilisateur avec JWT Bearer ]
                                  |
                                  v
              +---------------------------------------+
              |   Validation Cryptographique (RS256)  |
              +---------------------------------------+
                                  |
                   +--------------+--------------+
                   |                             |
             [ Role: Admin ]              [ Role: Member ]
             - Gestion Facturation         - Lecture projets
             - Inviter membres             - Modification autorisée
             - Supprimer compte            - Facturation INTERDITE
```

---

## 💳 3. Intégration Robuste de Stripe & Idempotence

### Traitement Sécurisé des Webhooks Stripe
Ne jamais faire confiance à l'URL sans vérifier la signature HMAC de Stripe :

```python
import stripe
from fastapi import Request, HTTPException, Header

@app.post("/api/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature")
):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Signature invalide")

    event_id = event["id"]
    
    # 1. Vérification d'idempotence dans Redis
    if await redis.get(f"processed_event:{event_id}"):
        return {"status": "already_processed"}

    # 2. Routage de l'événement
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        await fulfill_order(session["client_reference_id"], session["customer"])

    elif event["type"] == "customer.subscription.deleted":
        sub = event["data"]["object"]
        await revoke_access(sub["customer"])

    # 3. Marquer l'événement comme traité pendant 24h
    await redis.setex(f"processed_event:{event_id}", 86400, "1")
    return {"status": "success"}
```

---

## 📨 4. Envoi d'E-mails Transactionnels (Resend)

Utiliser des modèles propres avec délivrabilité garantie (SPF, DKIM, DMARC) :

```typescript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function sendWelcomeEmail(userEmail: string, userName: string) {
  await resend.emails.send({
    from: 'Brandon <notifications@yourdomain.com>',
    to: userEmail,
    subject: 'Bienvenue sur la plateforme !',
    html: `<p>Bonjour <strong>${userName}</strong>,</p><p>Votre espace SaaS est prêt.</p>`,
    headers: {
      'X-Entity-Ref-ID': crypto.randomUUID()
    }
  });
}
```

---

## 🚦 5. Rate Limiting avec Redis (Token Bucket)

Pour protéger les endpoints sensibles (authentification, génération IA) contre les attaques par déni de service (DDoS) ou le scraping abusif :

```python
async def check_rate_limit(client_ip: str, limit: int = 10, window_sec: int = 60) -> bool:
    key = f"rate_limit:{client_ip}"
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, window_sec)
    return current <= limit
```
