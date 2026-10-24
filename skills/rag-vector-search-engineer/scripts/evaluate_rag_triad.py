#!/usr/bin/env python3
"""RAG Triad Metric Evaluator (Faithfulness, Answer Relevance, Context Precision).

Evaluates RAG retrieval and generation quality against the Ragas Triad:
1. Faithfulness: Are answer claims mathematically supported by retrieved context?
2. Answer Relevance: Does the generated answer directly address the user query?
3. Context Precision: What percentage of retrieved context was relevant vs noise?
"""

import argparse
import json
import re
import sys


def tokenize_words(text: str) -> set[str]:
    # Extract lowercased alphanumeric tokens
    return set(re.findall(r"\b[a-zA-Z0-9_\u00C0-\u017F]{3,}\b", text.lower()))


def evaluate_rag_sample(query: str, context: str, answer: str) -> dict[str, float | str]:
    query_tokens = tokenize_words(query)
    context_tokens = tokenize_words(context)
    answer_tokens = tokenize_words(answer)

    # 1. Faithfulness: proportion of answer terms present in context
    if not answer_tokens:
        faithfulness = 0.0
    else:
        supported_tokens = answer_tokens.intersection(context_tokens)
        faithfulness = len(supported_tokens) / len(answer_tokens)

    # 2. Answer Relevance: overlap between answer and query
    if not query_tokens or not answer_tokens:
        answer_relevance = 0.0
    else:
        shared_query_terms = query_tokens.intersection(answer_tokens)
        answer_relevance = len(shared_query_terms) / len(query_tokens)

    # 3. Context Precision: proportion of context useful for query
    if not context_tokens:
        context_precision = 0.0
    else:
        useful_context_terms = context_tokens.intersection(query_tokens)
        context_precision = min(1.0, len(useful_context_terms) / max(1, len(query_tokens)))

    # Composite Score (harmonic mean / weighted average)
    composite = (faithfulness * 0.4) + (answer_relevance * 0.35) + (context_precision * 0.25)

    verdict = "PASS" if composite >= 0.65 else ("WARN" if composite >= 0.45 else "FAIL")

    return {
        "faithfulness": round(faithfulness, 3),
        "answer_relevance": round(answer_relevance, 3),
        "context_precision": round(context_precision, 3),
        "composite_score": round(composite, 3),
        "verdict": verdict
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG Triad Evaluator (Faithfulness, Relevance, Precision)")
    parser.add_argument("--query", help="User question string")
    parser.add_argument("--context", help="Retrieved context string")
    parser.add_argument("--answer", help="Generated LLM response string")
    parser.add_argument("--file", help="Path to JSON file containing {query, context, answer}")
    args = parser.parse_args()

    if args.file:
        try:
            data = json.loads(Path(args.file).read_text(encoding="utf-8"))
            query = data.get("query", "")
            context = data.get("context", "")
            answer = data.get("answer", "")
        except Exception as e:
            print(f"Error reading JSON file: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.query and args.context and args.answer:
        query, context, answer = args.query, args.context, args.answer
    else:
        # Default demonstrative sample
        query = "Comment configurer le mode WAL dans SQLite ?"
        context = "Pour activer le mode WAL dans SQLite, exécutez la commande PRAGMA journal_mode = WAL; avec un busy_timeout de 5000ms."
        answer = "Le mode WAL dans SQLite s'active via la commande PRAGMA journal_mode = WAL; accompagnée d'un timeout de 5000ms."

    results = evaluate_rag_sample(query, context, answer)

    print("=" * 65)
    print(" RAG Triad Quality Evaluation (Ragas Metric Standards)")
    print("=" * 65)
    print(f"Query   : {query[:80]}")
    print(f"Answer  : {answer[:80]}")
    print("-" * 65)
    print(f"1. Faithfulness (Groundedness) : {results['faithfulness'] * 100:.1f}%")
    print(f"2. Answer Relevance           : {results['answer_relevance'] * 100:.1f}%")
    print(f"3. Context Precision          : {results['context_precision'] * 100:.1f}%")
    print(f"-> Composite Quality Score    : {results['composite_score'] * 100:.1f}%")
    print(f"-> Verdict                    : [{results['verdict']}]")
    print("=" * 65)


if __name__ == "__main__":
    main()
