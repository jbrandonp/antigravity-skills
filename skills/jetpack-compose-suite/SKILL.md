---
name: jetpack-compose-suite
description: "Comprehensive Android Jetpack Compose Master Suite: Architecture, Modern Authoring, Refactoring, Performance, and Automated Codebase Auditing & Diagnostic Scoring (Kotlin 2.0+ / Strong Skipping Mode). Unifies deep authoring patterns (state, side effects, Navigation 3, Paging 3, lifecycle coroutines, animations, KMP boundaries) with strict repository diagnostic audits (0-100 rubric, compiler metrics, splash launch UX, and compose-reports gradle script). Use when writing, reviewing, or auditing Jetpack Compose codebases."
license: MIT
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, Agent
argument-hint: "[focus area, e.g. 'audit', 'state', 'effects', 'navigation', 'paging', 'performance', 'animation', 'scoring']"
metadata:
  author: "Ivan Morgillo & Antigravity Suite"
  version: "5.0.0"
---

# Jetpack Compose Master Suite: Architecture, Authoring & Diagnostic Auditing

This skill provides the definitive standard for Android Jetpack Compose engineering. It unites:
1. **Modern Authoring & Architectural Guidelines**: Deep reference guides covering state, side effects, Navigation 3, lifecycle collection, performance stability, and Kotlin idioms.
2. **Automated Repository Diagnostic Auditing**: Systematic evidence-based codebase auditing, scoring (0-100 rubric), compiler metric reporting, and launch UX verification.

**Target baseline (unless project specifies otherwise):**
- Kotlin `2.0.20+` with Compose Compiler `1.5.4+` (Strong Skipping Mode default).
- Jetpack Compose BOM current, Material 3, `androidx.lifecycle` with `collectAsStateWithLifecycle()`.
- Navigation 3 (`androidx.navigation3`) or Navigation 2.8+ type-safe destinations.
- Coroutines + Flow async primitives (no RxJava or blocking thread calls).

---

## 1. Modern Authoring & Review Guidelines (`references/`)

When writing, reviewing, or refactoring Jetpack Compose code, consult the authoritative references:

- **State & Data Flow (`references/state.md`)**: Single source of truth, hoist mutable state, state hoisting rules, remember vs rememberSaveable.
- **Side Effects (`references/effects.md`)**: Proper selection of `LaunchedEffect`, `DisposableEffect`, `produceState`, `snapshotFlow`, and `rememberUpdatedState`.
- **Performance & Stability (`references/performance.md`)**: Strong skipping mode, lambda modifiers, deferred state reads (`derivedStateOf`), lazy layout keys, eliminating recomposition loops.
- **Modifiers (`references/modifiers.md`)**: Modifier order discipline, `Modifier.Node` over soft-deprecated `composed { }`, lambda modifiers for layout/draw phases.
- **Navigation (`references/navigation.md`)**: Navigation 3 vs Navigation 2.8 type-safe DSL, back stack management, deep links, and result passing.
- **Coroutines & Lifecycle (`references/concurrency.md`)**: Safe lifecycle-aware collection with `collectAsStateWithLifecycle()`, cancellation handling.
- **Flow Architecture (`references/flows.md`)**: `StateFlow` vs `SharedFlow`, `stateIn(WhileSubscribed(5000))`, backpressure handling.
- **Composable Component API (`references/component-api.md`)**: Slot APIs, parameter ordering, default parameters, preview annotations.
- **Animation (`references/animation.md`)**: Declarative vs imperative animation, `Animatable`, `spring` vs `tween`, `AnimatedVisibility`, `AnimatedContent`.
- **Paging 3 (`references/paging.md`)**: `collectAsLazyPagingItems`, stable keys, load state error & retry management.
- **Focus & Hardware Keys (`references/focus.md`)**: `@FocusRequester`, TV / D-pad focus traversal, keyboard shortcuts.
- **KMP Boundaries (`references/kmp.md`)**: Compose Multiplatform expectations, native platform view wrappers.
- **UI Testing (`references/testing.md`)**: ComposeTestRule, semantics trees, assertions, screenshot testing.

---

## 2. Codebase Diagnostic Auditing & Scoring (`references/`)

When auditing a repository or rating Compose architecture quality:

1. **Compiler Metrics**:
   - Run compiler reports using `scripts/compose-reports.init.gradle` to extract stability and restartability metrics.
   - Analyze restartable but non-skippable composables.

2. **Systematic Search Playbook (`references/search-playbook.md`)**:
   - Grep for soft-deprecated APIs (`composed { }`, `accompanist`, `observeAsState`).
   - Grep for state smells (unhoisted `mutableStateOf`, `var` state in data classes).
   - Grep for side-effect smells (raw coroutines in `@Composable`, missing `rememberUpdatedState`).

3. **Scoring Engine (`references/scoring.md`)**:
   Score the codebase across the 4 core dimensions (0-10 each, weighted to 0-100 total):
   - **Performance**: Stability, deferred reads, lazy keys.
   - **State Management**: Unidirectional data flow, persistence.
   - **Side Effects**: Correct effect handler choice, zero leaks.
   - **Composable API Quality**: Slot APIs, modifier parameter conventions.

4. **Audit Report Template (`references/report-template.md`)**:
   - Emit an executive summary, score breakdown, critical findings with code diffs, and prioritized remediation actions.

---

## Scripts & Tools

- `scripts/compose-reports.init.gradle`: Gradle initialization script for generating Compose compiler stability reports.
'''

Path = r"C:\Users\brand\.gemini\config\skills\jetpack-compose-suite\SKILL.md"
