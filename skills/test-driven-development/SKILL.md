---
name: test-driven-development
description: >-
  Enforce strict Test-Driven Development (TDD) using the Red-Green-Refactor cycle combined with generative property-based testing and invariant fuzzing inspired by Hypothesis and QuickCheck. Forbids writing production code without a failing test, validates test failure semantics, and generates randomized edge-case inputs (surrogate Unicode, boundary numbers, empty sequences) to discover hidden boundary bugs.
---

# Test-Driven Development (Strict TDD Standard)

A disciplined engineering methodology developed to eliminate regression, enforce testability, and produce minimal, clean architectures.

The Golden Rule of TDD: **Write no production code until you have written a failing automated test that proves the feature is missing or the bug exists.**

---

## 🚦 The Red-Green-Refactor Triad

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. RED Phase: Write minimal test that FAILS for the right reason │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. GREEN Phase: Write MINIMAL production code to make it pass   │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. REFACTOR Phase: Clean up duplication, enforce typing & DRY  │
 └─────────────────────────────────────────────────────────────┘
```

### 1. The RED Phase
- Write an isolated unit test exercising the desired function or bugfix.
- Run the test suite: verify the test **fails**.
- **Crucial**: Verify it fails with the *expected* failure (e.g. `AssertionError` or `AttributeError: function not defined`), not a broken syntax or import error.

### 2. The GREEN Phase
- Implement the simplest possible code that satisfies the test.
- Do not write speculative extra logic or unrequested features.
- Re-run test suite: verify all tests pass.

### 3. The REFACTOR Phase
- Improve code readability, remove duplicate logic (DRY), and enforce strict types without `any`.
- Re-run test suite after every small refactor to guarantee zero behavioral regressions.

---

## 🛠️ Tooling 1 : Vérificateur de Cycle Red-Green-Refactor

```bash
# Verify test suite pass/fail metrics and execution status
python scripts/tdd_cycle_checker.py --test-dir tests/

# Run specific test file in TDD mode
python scripts/tdd_cycle_checker.py --test-file tests/test_pricing.py
```

---

## 🧪 Module Complémentaire : Fuzzing d'Invariants & Tests aux Limites Aléatoires (Property-Based Testing)

# Property-Based Testing (Hypothesis & Invariant Standard)

Elevates software verification beyond static example assertions (`assert add(2, 3) == 5`) to **invariant properties** that must hold true for *any* valid input $x \in X$.

---

## 🎲 The 4 Universal Property Patterns

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ 1. Roundtrip Invariant: decode(encode(x)) == x              │
 ├─────────────────────────────────────────────────────────────┤
 │ 2. Idempotence Invariant: f(f(x)) == f(x)                   │
 ├─────────────────────────────────────────────────────────────┤
 │ 3. Invariant Preservation: len(sort(xs)) == len(xs)         │
 ├─────────────────────────────────────────────────────────────┤
 │ 4. Monotonicity Invariant: a <= b ==> f(a) <= f(b)          │
 └─────────────────────────────────────────────────────────────┘
```

### Pattern 1: Roundtrip (Serialization / Deserialization)
- If you convert an object to JSON, SQLite row, or binary, decoding it must reproduce the exact original value.

### Pattern 2: Idempotence (Formatting / Cleaning / Normalization)
- A text sanitizer, price normalizer, or database migration must be safe to run twice: `clean(clean(text)) == clean(text)`.

### Pattern 3: Invariant Preservation
- A data transformer or filter must never drop primary keys or corrupt numeric totals.

### Pattern 4: Extreme Boundary Fuzzing
- Feed functions extreme values:
  - Numbers: `0`, `-1`, `2**31 - 1`, `float('inf')`, `float('nan')`.
  - Strings: `""`, `\x00` (null byte), `\uFFFF`, RTL Arabic text, SQL injection strings.
  - Lists: empty list, single element, 10,000 identical items.

---

## 🛠️ Tooling 2 : Fuzzer d'Invariants & Tests de Propriétés (Hypothesis)

```bash
# Run invariant fuzzer across sample algorithms
python scripts/run_property_fuzzer.py --demo

# Test custom mathematical function
python scripts/run_property_fuzzer.py --iterations 500
```
