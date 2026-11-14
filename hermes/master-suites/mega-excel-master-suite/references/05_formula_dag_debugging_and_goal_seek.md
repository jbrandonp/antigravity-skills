# 05 — Formula DAG Dependency Debugging & Goal Seek Protocol

## 🎯 Objective
Model the workbook as an in-memory Directed Acyclic Graph (DAG) of cell formulas to isolate error root causes in a single step and execute numerical sensitivity analysis (Goal Seek).

---

## 🕸️ DAG Graph Construction
The engine reads every formula across every worksheet and breaks references into edges:
- **Precedents:** `Cell -> Set[Cells it depends on]`
- **Dependents:** `Cell -> Set[Cells that depend on it]`

```text
    [ A1 (Input: 100) ] ───────┐
                               ▼
    [ B1 (Input: "Text") ] ─> [ C1 (=A1*B1 -> #VALUE!) ]
                               │
                               ▼
                              [ D1 (=C1+50 -> #VALUE!) ]
```

### Root-Cause Isolation Algorithm
When a cell (e.g. `D1`) reports `#VALUE!`:
1. The engine walks **backwards** along the DAG via Breadth-First Search (BFS).
2. It tests whether predecessor cells also exhibit the error.
3. It identifies the upstream junction (here `C1`, caused by multiplying string `B1`), pinpointing the exact origin rather than having the agent guess.

---

## 🎯 Headless Goal Seek (Secant / Bisection Solver)
Allows an agent to answer: *"What value must input cell X take for target formula cell Y to reach target value Z?"*

1. Identifies the variable cell $x$ and the objective formula $f(x)$.
2. Evaluates $f(x_0)$ and $f(x_1)$.
3. Computes next estimate via Secant method:
   $$x_{n+1} = x_n - f(x_n) \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$
4. Iterates until $|f(x) - \text{Target}| \le \text{Tolerance}$ ($10^{-3}$).
5. Writes the converged parameter back into the workbook.
