#!/usr/bin/env python3
"""
scaffold_agent_architecture.py — Generate production-grade AI Agent Architecture specifications.
Conforms strictly to the Antigravity Agent Architecture Contract (7 core views).

Usage:
  python scaffold_agent_architecture.py --name NAME --role ROLE [--topology TOPOLOGY] [--tools TOOLS] [--output FILE]

Author: Antigravity Agentic Super Suite
"""

import os
import sys
import argparse
import re
from pathlib import Path
from typing import List

TOPOLOGIES = {
    "single_agent_loop": "Single Agent ReAct Loop (Think-Act-Observe with hard step cap)",
    "router_worker": "Router-Worker / Triage Gateway (Classifier routing to specialized handlers)",
    "orchestrator_subagents": "Orchestrator-Workers (Central planner fanning out subtasks)",
    "evaluator_optimizer": "Evaluator-Optimizer Loop (Generator paired with deterministic/model judge)",
    "state_machine": "Deterministic State Machine / Flow (Graph-based transitions with bounded agent nodes)"
}


def generate_mermaid_topology(name: str, topology: str, tools: List[str]) -> str:
    """Generate Mermaid flowchart diagram representing the agent architecture."""
    tool_nodes = "\n".join([f'            T_{i}["🔧 {t.strip()}"]' for i, t in enumerate(tools)]) if tools else '            T_0["🔧 Default Tools"]'
    
    if topology == "router_worker":
        return f"""```mermaid
flowchart TD
    User([👤 User / Client]) --> IngressGate["🛡️ Ingress & Auth Guardrail"]
    IngressGate --> Router["🧠 Triage / Intent Router"]
    
    subgraph Workers ["Specialized Workers"]
        W1["⚡ Quick Retrieval Worker"]
        W2["🔬 Deep Analysis Worker"]
        W3["💼 Action Execution Worker"]
    end
    
    Router -->|Intent: Simple Q&A| W1
    Router -->|Intent: Complex Research| W2
    Router -->|Intent: Mutation / Effect| W3
    
    subgraph ToolEcosystem ["Deterministic Tools & APIs"]
{tool_nodes}
    end
    
    W2 -.-> ToolEcosystem
    W3 -->|Pre-execution Policy Check| PolicyGate{{"⚖️ Policy & Human Approval"}}
    PolicyGate -->|Approved| ToolEcosystem
    
    W1 --> EgressFilter["🧹 Egress Redaction & Output Guardrail"]
    W2 --> EgressFilter
    W3 --> EgressFilter
    EgressFilter --> User
```"""
    elif topology == "orchestrator_subagents":
        return f"""```mermaid
flowchart TD
    User([👤 User / Client]) --> Ingress["🛡️ Input Sanitization Gate"]
    Ingress --> Orchestrator["🧠 Central Orchestrator / Planner"]
    
    subgraph Subagents ["Isolated Subagent Team"]
        A1["🔍 Researcher Agent"]
        A2["💻 Code & Exec Agent"]
        A3["📊 Synthesis Agent"]
    end
    
    Orchestrator -->|Decompose & Delegate| A1
    Orchestrator -->|Decompose & Delegate| A2
    Orchestrator -->|Decompose & Delegate| A3
    
    subgraph ToolBelt ["Tool Boundaries"]
{tool_nodes}
    end
    
    A1 -.-> ToolBelt
    A2 -.-> ToolBelt
    
    A1 -->|Partial Result| Orchestrator
    A2 -->|Partial Result| Orchestrator
    A3 -->|Final Synthesis| VerificationGate{{"✅ Acceptance Gate"}}
    VerificationGate -->|Pass| Egress["Output Delivery"]
    VerificationGate -->|Fail / Budget Left| Orchestrator
    Egress --> User
```"""
    else:  # single_agent_loop / default
        return f"""```mermaid
flowchart TD
    User([👤 User / Client]) --> Ingress["🛡️ Ingress Gate (Auth & Sanitize)"]
    Ingress --> AgentCore["🧠 Agent Core: {name}"]
    
    subgraph AgentLoop ["Bounded ReAct Loop (Max N Iterations)"]
        AgentCore --> Thought["🤔 Reason / Plan Next Action"]
        Thought --> ToolCallProposal{{"❓ Action Proposal"}}
        ToolCallProposal --> PolicyCheck{{"⚖️ Deterministic Policy Gate"}}
        PolicyCheck -->|Allowed| ExecTool["⚙️ Execute Tool"]
        PolicyCheck -->|Denied / Escalate| Escalation["🚨 Fallback / Human Queue"]
        ExecTool --> ToolResult["👁️ Observe Result & Update Context"]
        ToolResult --> StepCounter{{"🔢 Step & Budget Limit Check"}}
        StepCounter -->|Within Budget| AgentCore
        StepCounter -->|Exhausted| Escalation
    end
    
    subgraph ToolEcosystem ["Registered Deterministic Tools"]
{tool_nodes}
    end
    ExecTool -.-> ToolEcosystem
    
    Thought -->|Task Finished| FinalReview["🔍 Output Validator"]
    FinalReview --> Egress["📤 Delivery to User"]
    Escalation --> Egress
    Egress --> User
```"""


def generate_mermaid_sequence(name: str) -> str:
    """Generate Mermaid sequence diagram illustrating the request lifecycle."""
    return f"""```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Client / User
    participant Gate as 🛡️ Security / Ingress Gate
    participant Agent as 🧠 {name} Engine
    participant Policy as ⚖️ Policy & Rate Limiter
    participant Tool as ⚙️ Deterministic Tool
    participant Storage as 💾 State & Memory Store

    User->>Gate: Submit Prompt / Instruction
    Gate->>Gate: Validate Auth, Sanitize Input, Check Quota
    Gate->>Agent: Dispatch Clean Task Context
    
    loop Bounded Execution Cycle (Max Iterations)
        Agent->>Storage: Read State & Short-Term Memory
        Agent->>Agent: Plan Step / Produce Tool Call
        Agent->>Policy: Submit Tool Call for Admissibility Check
        alt Policy Denied or Unsafe
            Policy-->>Agent: Action Rejected (Violation Reason)
            Agent->>Agent: Formulate Alternative or Escalation
        else Policy Approved
            Policy->>Tool: Execute Authorized Operation
            Tool-->>Policy: Return Raw Typed Output
            Policy-->>Agent: Pass Scrubbed Observation
            Agent->>Storage: Persist Step Log & State Delta
        end
    end
    
    Agent->>Gate: Final Answer Candidate
    Gate->>Gate: Validate Output Constraints & PII Redaction
    Gate-->>User: Deliver Verified Response & Provenance
```"""


def build_specification(
    name: str,
    role: str,
    topology: str,
    model: str,
    tools: List[str],
    max_steps: int,
    timeout_sec: int,
    budget_usd: float
) -> str:
    """Build complete Markdown agent architecture document conforming to the 7 contract views."""
    top_label = TOPOLOGIES.get(topology, topology)
    mermaid_top = generate_mermaid_topology(name, topology, tools)
    mermaid_seq = generate_mermaid_sequence(name)
    tools_list = [t.strip() for t in tools if t.strip()]

    tools_rows = ""
    for t in tools_list:
        tools_rows += f"| `{t}` | Core operational capability | Input parameters | Deterministic result | `read-only` | Pre-call permission gate |\n"
    if not tools_rows:
        tools_rows = "| `system_search` | Domain knowledge retrieval | Query string | Search snippets | `read-only` | Automated |\n"

    return f"""# 🏛️ AI Agent Architecture Specification: {name}

> **Standard :** Antigravity Agent Architecture Contract v2.0  
> **Status :** ARCHITECTURAL_DESIGN (Pre-Implementation Baseline)  
> **Topology :** `{topology}` — {top_label}  
> **Target Model :** `{model}`

---

## 1. Task and Requirements Criteria

### 1.1 Mission & Value Proposition
- **Agent Identifier :** `{name}`
- **Core Mission / Role :** {role}
- **Primary Stakeholders :** End-users, Domain Developers, System Operators.
- **Success Criteria :** 
  1. Complete target tasks within allocated resource bounds with verifiable outputs.
  2. Zero policy or security violations (deterministic rejection of out-of-bounds actions).
  3. 100% idempotency and auditability on all state mutations.

### 1.2 Requirements Traceability Matrix
| R-ID | Requirement Description | Source | Architectural Decision | Verification Check |
| :--- | :--- | :--- | :--- | :--- |
| `REQ-01` | Core task execution ({role}) | User Spec | Implements `{topology}` pattern | Eval suite test scenario |
| `REQ-02` | Hard operational limits | Invariant | Max `{max_steps}` steps, `{timeout_sec}s` timeout, `${budget_usd:.2f}` cap | Runtime step interceptor |
| `REQ-03` | Deterministic policy enforcement | Security Standard | Programmatic pre-call validator (Zero-Trust) | Unit test permission bypass |
| `REQ-04` | External write idempotency | Architecture Contract | Mandatory idempotency keys & reconciliation | Duplicate request test |
| `REQ-05` | Graceful failure & escalation | UX / Safety | Controlled fallback outcome on budget exhaustion | Mock timeout test |

---

## 2. Structure and Boundaries

### 2.1 Component Topology Diagram
{mermaid_top}

### 2.2 Component Responsibilities Map
| Component | Primary Responsibility | Strict Non-Responsibilities | Evidence / Technology |
| :--- | :--- | :--- | :--- |
| **Ingress Gate** | Auth verification, rate limiting, prompt injection defense | Does not formulate task plan | Middleware / WAF |
| **Agent Core (`{name}`)** | Reasoning, sub-task planning, model interaction | Does not directly mutate DB without tool | Model `{model}` |
| **Deterministic Policy Gate** | Pre-call admissibility, argument schema typing, budget checks | Does not alter business intent | Python SDK Interceptor |
| **Tool Ecosystem** | Executes concrete deterministic actions & API requests | Never relies on probabilistic LLM logic | Typed Python Tools / MCP |
| **State & Memory Store** | Append-only audit log, short-term conversational context | Does not store untrusted secrets in prompt | SQLite / Redis |
| **Egress Redactor** | Validates structured output schema, strips PII/credentials | Does not retry failed jobs | Pydantic V2 / JSON Schema |

---

## 3. Execution, State, and Stopping Invariants

### 3.1 Request & Execution Sequence Flow
{mermaid_seq}

### 3.2 The Four Environment Functions
| Function | Owner | Verifiable Mechanism | Failure Mode Handling |
| :--- | :--- | :--- | :--- |
| **Translation** | Ingress Gateway | Validates schema & injects authenticated user context | Rejects invalid requests with HTTP 400 |
| **Execution** | Runtime Dispatcher | Invokes typed tools in isolated sandbox | Catches unhandled tool errors, returns structured err |
| **Observation** | Tool Interceptor | Normalizes output, truncates oversized data, scrubs PII | Marks status `UNKNOWN` if output malformed |
| **Correction** | Agent Loop Controller | Decides continuation vs escalation based on explicit error | Bounded retry (max 2) before human escalation |

### 3.3 Mandatory Operational Limits
| Control Field | Hard Enforcement Limit | Enforcing Authority | Failure / Stopping Outcome |
| :--- | :--- | :--- | :--- |
| **Max Iterations** | `{max_steps}` iterations | Runtime Step Counter | Terminate loop, return partial summary + escalation |
| **Total Task Timeout** | `{timeout_sec}` seconds | Async Watchdog Timer | Cancel background tasks, return HTTP 504 status |
| **Total Budget Cap** | `${budget_usd:.2f}` USD | Centralized atomic budget reservation pool | Halt immediately upon budget depletion |
| **Consecutive Identical Calls** | 2 identical parameter sets | Loop Breaker Guard | Abort with `LOOP_DETECTED` warning |
| **Max Concurrent Workers** | 3 parallel sub-tasks | Thread/Worker Pool with atomic budget shares | Queue excess requests with backpressure |
| **Execution Guardrail** | Synchronous pre-call gate | Pre-execution Policy Gate | Immediate rejection before an external effect |

---

## 4. Context, Knowledge, and Memory Architecture

### 4.1 Token Budget Distribution
```text
┌────────────────────────────────────────────────────────┐
│ System Instructions & Persona       : ~1,500 tokens    │
├────────────────────────────────────────────────────────┤
│ Tool Definitions & Schemas          : ~1,000 tokens    │
├────────────────────────────────────────────────────────┤
│ Working Conversation / History      : ~4,000 tokens    │
├────────────────────────────────────────────────────────┤
│ Retrieved RAG / Knowledge Evidence  : ~3,000 tokens    │
├────────────────────────────────────────────────────────┤
│ Model Generation & Reasoning Reserve: ~2,500 tokens    │
└────────────────────────────────────────────────────────┘
Total Window Footprint: ~12,000 tokens (Safely fits standard 32k/128k context)
```

### 4.2 Compaction & Memory Hierarchy
- **Working Memory :** Ephemeral memory buffer for current session. Compacted via high-density summarization when history exceeds 8,000 tokens.
- **Episodic Memory :** Key task outcomes and user preferences stored in external store with explicit user/tenant isolation.
- **Procedural Memory Admission :** Candidate memory updates require explicit change authority approval before being promoted to active procedures.
- **Critical Invariant :** Authorization tokens and active transaction IDs are **never** stored in raw prompt memory.

---

## 5. Tool Contracts and Authority Matrix

### 5.1 Registered Capabilities
| Tool Name | Scope & Purpose | Input Schema | Output Schema | Side-Effect Type | Pre-Execution Guardrail |
| :--- | :--- | :--- | :--- | :--- | :--- |
{tools_rows}

### 5.2 Idempotency, Pagination, and Write Operations Contract
- Every mutating tool invocation **must** supply a deterministic `idempotency_key` (e.g., `hash(task_id + step_index)`).
- If an external call times out, the tool enters `EFFECT_UNKNOWN` state: the agent **must not** blindly re-execute without querying the downstream resource to confirm execution status.
- Tool responses enforce pagination and explicit truncation indicators (`has_more`, `total_count`) to eliminate silent data truncation.

---

## 6. Threat Model and Failure Mitigations

| Threat Vector | Attack Scenario | Trust Boundary | Mitigation Mechanism | Residual Risk & Owner |
| :--- | :--- | :--- | :--- | :--- |
| **Prompt Injection** | Malicious payload in user input or retrieved docs | Ingress Gate | Strict separation of System prompt vs User data | Monitored by Ops |
| **Tool Abuse / SSRF** | Model attempts to call internal `169.254.169.254` | Tool Sandbox | IP whitelisting & non-root container with network isolation | SecOps |
| **Runaway Costs** | Infinite reasoning / retry loop | Runtime Counter | Hard cap at `${budget_usd:.2f}` and `{max_steps}` steps | Architect |
| **Data Leakage** | Agent returns private API keys in output | Egress Gate | Egress redaction proxy scanning and PII scrubber before delivery | App Owner |
| **Cancellation Race** | Job cancelled while call in-flight | Dispatcher | Explicit tracking: task cancellation is not an automatic rollback | Core Engine |

---

## 7. Quality Verification, Economics & Evaluation Gates

### 7.1 Quality Gate Criteria (CI/CD Pipeline)
An agent architecture is considered ready for implementation only when it satisfies:
- **Minimal Viable Complexity :** The architecture is justified against a simpler predefined workflow or single-call baseline.
- **Independent Evaluation Split :** Testing is conducted on an unpolluted independent holdout validation set separated from tuning data.
- **Non-Compensable Security Gates :** Authorization, tenant access, and safety checks are hard binary gates; high response quality never compensates for an access violation.
- **Accuracy / Task Completion :** $\\ge 90\\%$ on synthetic evaluation benchmark.
- **Safety / Injection Rejection :** $100\\%$ on adversarial security eval cases.
- **Zero Runaway Incidents :** $0$ executions exceeding `{max_steps}` steps or `${budget_usd:.2f}` budget.
- **Latency SLO :** $p95 \\le 15.0\\text{{s}}$ per completed task.
"""


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    parser = argparse.ArgumentParser(
        description="Scaffold an AI Agent Architecture specification adhering to the 7 Contract Views."
    )
    parser.add_argument("--name", type=str, required=True, help="Agent system name (e.g., SupportTriageAgent)")
    parser.add_argument("--role", type=str, required=True, help="High-level mission and responsibility statement")
    parser.add_argument(
        "--topology",
        choices=list(TOPOLOGIES.keys()),
        default="single_agent_loop",
        help="Architectural topology pattern"
    )
    parser.add_argument("--model", type=str, default="claude-3-5-sonnet", help="Target LLM model")
    parser.add_argument("--tools", type=str, default="", help="Comma-separated list of tool names")
    parser.add_argument("--max-steps", type=int, default=10, help="Maximum allowed loop iterations")
    parser.add_argument("--timeout-sec", type=int, default=60, help="Total execution timeout in seconds")
    parser.add_argument("--budget-usd", type=float, default=0.50, help="Hard financial limit per task")
    parser.add_argument("--output", type=str, default="AGENT_ARCHITECTURE.md", help="Output file path")

    args = parser.parse_args()

    tools_list = [t.strip() for t in args.tools.split(",") if t.strip()]
    spec_content = build_specification(
        name=args.name,
        role=args.role,
        topology=args.topology,
        model=args.model,
        tools=tools_list,
        max_steps=args.max_steps,
        timeout_sec=args.timeout_sec,
        budget_usd=args.budget_usd
    )

    out_p = Path(args.output)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with open(out_p, "w", encoding="utf-8") as f:
        f.write(spec_content)

    print(f"✓ Agent Architecture specification scaffolded successfully: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
