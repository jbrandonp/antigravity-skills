---
name: systematic-debugging
description: Investigate and resolve complex bugs using the Anthropic SWE-bench Systematic Debugging standard. Enforces root-cause investigation, deterministic reproduction scripts, difference analysis, and regression guards before applying code fixes.
---

# Systematic Debugging (SWE-bench & Anthropic Standard)

The premier debugging framework for AI coding agents derived from **SWE-bench** state-of-the-art benchmarks and **Anthropic** research.

The Iron Law of Debugging: **No code modification without a verified reproduction script and root-cause evidence first.** Trial-and-error symptom patching is strictly forbidden.

---

## 🔬 The 4-Phase Diagnostic Cycle

```text
 ┌─────────────────────────────────────────────────────────────┐
 │ Phase 1: Evidence Gate & Deterministic Reproduction         │
 ├─────────────────────────────────────────────────────────────┤
 │ Phase 2: Differential & Pattern Analysis                    │
 ├─────────────────────────────────────────────────────────────┤
 │ Phase 3: Minimal Causal Patch Implementation                │
 ├─────────────────────────────────────────────────────────────┤
 │ Phase 4: Verification & Regression Guard                    │
 └─────────────────────────────────────────────────────────────┘
```

### Phase 1: The Evidence Gate
- **Never guess or assume.** Read the exact stack trace, file path, line number, and exception type.
- **Create a Reproduction Script**: Write an isolated test case or script (`repro_issue.py`) that reliably fails on the current codebase.
- Verify that Phase 1 is **RED**: the script reproduces the symptom with exit code != 0.

### Phase 2: Differential Analysis
- Inspect recent changes using `git diff HEAD~1` or examine surrounding working components.
- Trace variables backward from the failure point to locate the exact divergent state.
- Formulate a falsifiable hypothesis explaining *why* the defect occurs.

### Phase 3: Minimal Causal Patch
- Fix the *cause*, not the *symptom*. Do not wrap broken code in defensive `try/except: pass` blocks.
- Apply the minimal contiguous diff required. Refuse broad, speculative refactoring.

### Phase 4: Verification & Regression Guard
- Re-run the reproduction script: verify it turns **GREEN** (exit code 0).
- Run the full workspace test suite to ensure adjacent components have not regressed.
- Delete the temporary reproduction script or convert it into a permanent regression test.

---

## 🛠️ Deterministic Tooling

```bash
# Execute reproduction script and verify red/green transition
python scripts/generate_reproduction_harness.py --script repro_bug.py

# Run with automated timeout and trace capture
python scripts/generate_reproduction_harness.py --script repro_bug.py --timeout 10
```