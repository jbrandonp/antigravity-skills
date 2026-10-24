---
name: devops-infrastructure-as-code
description: >-
  Architect and implement declarative Infrastructure as Code (IaC) and containerization using Terraform/OpenTofu, Docker multi-stage builds, and Kubernetes (K8s/Helm). Enforces immutable infrastructure, remote state locking, least-privilege non-root containers, health probes, resource limits, and production Kubernetes manifests.
---

# 🚀 DevOps, Infrastructure as Code (IaC) & Container Engineering

> **Standard :** Production Cloud & Container Architecture SOTA 2026  
> **Core Axiom :** *"Every server, container, and network route must be declared in code, version-controlled, reproducible from scratch in minutes, and executed under strict least-privilege security."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Imagine que tu doives installer un serveur web :
- **La méthode "bricolage" (à bannir)** : Tu te connectes au serveur en SSH, tu tapes 50 commandes à la main (`apt install`, modifier des fichiers de config, configurer les pare-feux). Le jour où le serveur plante ou qu'il faut en installer un deuxième, tu as oublié la moitié de ce que tu as fait, et plus rien ne marche.
- **La méthode "DevOps & IaC" (Standard Pro)** : 
  1. **Terraform (Le Maçon Cloud)** : C'est un fichier texte qui décrit exactement tes machines, tes disques et tes réseaux. Tu tapes `terraform apply`, et AWS ou Google Cloud construit l'infrastructure complète en 2 minutes de manière 100% identique.
  2. **Docker (La Boîte Hermétique)** : Tu emballes ton application avec toutes ses dépendances dans un conteneur léger et sécurisé. Elle tourne exactement de la même façon sur ton PC portable que sur un serveur géant.
  3. **Kubernetes (Le Chef d'Orchestre)** : Il surveille tes conteneurs. Si un conteneur plante à 3h du matin, Kubernetes le redémarre instantanément. Si 10 000 utilisateurs arrivent d'un coup, il duplique automatiquement les conteneurs pour absorber la charge.

---

## 🏗️ 2. Les 3 Piliers de l'Infrastructure Moderne

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Terraform / OpenTofu (Provisioning d'Infra Cloud)        │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Docker Multi-Stage (Conteneurs légers, distroless & sûrs)│
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Kubernetes & Helm (Orchestration, Scalabilité & Probes)  │
 └─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 3. Guide Pratique & Templates de Production

### 1. Terraform : Architecture des Modules & Remote State
Ne jamais stocker le fichier `terraform.tfstate` en local. Toujours utiliser un bucket S3 / GCS distant avec verrouillage (DynamoDB / GCS locking) :

```hcl
# main.tf
terraform {
  required_version = ">= 1.8.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "my-company-terraform-state"
    key            = "prod/app/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

# Refactoring sans destruction de ressource de production (Terraform 1.1+)
# Évite de détruire et recréer une base de données lors d'un renommage
moved {
  from = aws_instance.legacy_web
  to   = aws_instance.api_server
}
```

### 2. Docker Multi-Stage Build : Ultra-Léger et Sans Privilèges Root
Ne jamais embarquer les compilateurs ou les outils de build dans l'image finale de production :

```dockerfile
# Étape 1 : Build & compilation
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv export --no-dev --format requirements-txt > requirements.txt
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Étape 2 : Image d'exécution minimale & sécurisée
FROM gcr.io/distroless/python3-debian12
WORKDIR /app
COPY --from=builder /install /usr/local
COPY src/ ./src/

# Exécution sous utilisateur non-root par défaut
USER 65534:65534
EXPOSE 8000
CMD ["-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Kubernetes Manifest de Production
Tout déploiement Kubernetes doit comporter :
- **Resource Requests & Limits** (CPU/Mémoire) pour éviter les saturations de nœuds (`OOMKilled`).
- **Liveness & Readiness Probes** pour la bascule de trafic sans coupure.
- **SecurityContext** durci (`readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  labels:
    app: api-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
      containers:
        - name: api
          image: myregistry.io/api-service:v1.2.0
          ports:
            - containerPort: 8000
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 2
            periodSeconds: 5
```

---

## 🎯 Commandes Essentielles

```bash
# Valider la syntaxe et formater le code Terraform
terraform fmt -check
terraform validate
terraform plan -out=tfplan

# Scanner une image Docker contre les vulnérabilités CVE avec Trivy
trivy image my-app:latest --severity HIGH,CRITICAL

# Déployer et vérifier le rollout sur Kubernetes
kubectl apply -f k8s/
kubectl rollout status deployment/api-service
```
