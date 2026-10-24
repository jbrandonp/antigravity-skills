---
name: rag-vector-search-engineer
description: >-
  Design and implement production Retrieval-Augmented Generation (RAG) and semantic search architectures. Covers document chunking (semantic, recursive), vector embeddings, vector databases (pgvector, Qdrant), hybrid search (dense + BM25 sparse), Cohere/BGE reranking, and automated RAG evaluation (Ragas triad: faithfulness, answer relevance, context precision).
---

# 🧠 RAG, Vector Search & LLM Retrieval Engineering

> **Standard :** Advanced RAG & Semantic Search Architecture SOTA 2026  
> **Core Axiom :** *"Naive RAG (fixed-chunk + single cosine similarity) fails in production. High-precision RAG requires contextual chunking, hybrid search (dense embeddings + BM25 keyword search), Cross-Encoder reranking, and automated evaluation on the Ragas triad."*

---

## 🧒 1. Explication Pédagogique (Style 15 ans)

Le RAG (Retrieval-Augmented Generation), c'est donner **un livre ouvert à un élève pendant un examen** :
- **Sans RAG** : L'IA répond uniquement de mémoire. Si tu lui demandes un détail précis sur ton entreprise ou un contrat écrit hier, elle ne le sait pas et risque d'inventer n'importe quoi (c'est l'*hallucination*).
- **Le RAG Naïf (Ce que font les débutants)** : Découper le livre en morceaux bêtes de 500 mots et chercher les morceaux qui ressemblent à la question. Problème : une phrase coupée en deux perd tout son sens, et l'IA répond à côté de la plaque.
- **Le RAG Avancé (Standard Pro)** :
  1. **Découpage Sémantique (Contextual Chunking)** : On découpe par paragraphe logique et on ajoute le titre de la section devant chaque morceau.
  2. **Recherche Hybride** : On combine les mots-clés exacts (BM25 pour trouver un numéro de commande précis) et le sens des mots (Embeddings pour comprendre les synonymes).
  3. **Reranker (Le Juge Arbitre)** : Un second modèle relit les 20 morceaux trouvés et ne garde que les 3 plus pertinents.
  4. **Évaluation Ragas** : On teste automatiquement si l'IA invente des faits (*faithfulness*) et si sa réponse est claire.

---

## 🏗️ 2. Le Pipeline RAG Avancé SOTA 2026

```text
  [ Question Utilisateur ]
            │
            ├─────────────────────────────────────────┐
            ▼                                         ▼
   [ Recherche Dense ]                       [ Recherche Sparse ]
   (Embeddings text-embedding-3-small)       (BM25 Mots-clés exacts)
            │                                         │
            └────────────────────┬────────────────────┘
                                 ▼
                     [ RRF (Reciprocal Rank Fusion) ]
                     (Fusion des 20 meilleurs passages)
                                 ▼
                     [ Cross-Encoder Reranker ]
                     (Cohere Rerank v3 / BGE-Reranker-large)
                                 ▼
                     [ Top 3 Passages Pertinents ]
                                 ▼
                     [ Génération LLM avec Citations ]
```

---

## 🐘 3. Implémentation pgvector (PostgreSQL Vector Search)

Configuration de l'extension `vector` et de l'index HNSW (Hierarchical Navigable Small World) pour une recherche sous les 5 ms :

```sql
-- 1. Activation de l'extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Table de documents chunkés
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB NOT NULL,
    embedding vector(1536) -- Dimension pour OpenAI text-embedding-3-small
);

-- 3. Index HNSW pour recherche vectorielle ultra-rapide
CREATE INDEX idx_document_chunks_hnsw 
ON document_chunks 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 4. Requête de similarité Cosine avec filtre
SELECT content, metadata, 1 - (embedding <=> :query_vector) AS similarity
FROM document_chunks
WHERE metadata->>'category' = 'legal'
ORDER BY embedding <=> :query_vector
LIMIT 5;
```

---

## 🎯 4. Reranking avec Cohere en Python

```python
import cohere

co = cohere.Client(api_key="your-api-key")

def rerank_documents(query: str, documents: list[str], top_n: int = 3) -> list[str]:
    response = co.rerank(
        model="rerank-v3.5",
        query=query,
        documents=documents,
        top_n=top_n
    )
    return [documents[result.index] for result in response.results]
```

---

## 📊 5. Évaluation Automatique : La Triade Ragas

Pour mesurer mathématiquement la qualité d'un pipeline RAG avant mise en production :
1. **Fidélité (`Faithfulness`)** : Est-ce que chaque affirmation de la réponse découle strictement des documents fournis ? ($[0.0, 1.0]$, viser $\ge 0.90$).
2. **Pertinence de la Réponse (`Answer Relevancy`)** : La réponse répond-elle directement à la question sans divaguer ? ($[0.0, 1.0]$, viser $\ge 0.85$).
3. **Précision du Contexte (`Context Precision`)** : Les morceaux de texte utiles sont-ils bien classés en tête du prompt ? ($[0.0, 1.0]$, viser $\ge 0.85$).
