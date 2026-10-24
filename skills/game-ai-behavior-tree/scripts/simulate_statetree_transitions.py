# -*- coding: utf-8 -*-
"""
simulate_statetree_transitions.py - Unreal Engine 5 StateTree Simulator
Simulateur d'arbres d'etats hierarchiques avec evaluateurs et transitions conditionnelles.
"""

from typing import Dict, List, Optional, TypedDict

class BlackboardContext(TypedDict):
    health_percent: float
    target_distance: float
    has_line_of_sight: bool
    is_alarm_triggered: bool

class StateTransition(TypedDict):
    target_state: str
    condition_name: str
    priority: int

class StateTreeNode(TypedDict):
    state_id: str
    parent_state: Optional[str]
    active_task: str
    transitions: List[StateTransition]

class StateTreeSimulationResult(TypedDict):
    current_state: str
    executed_task: str
    transition_triggered: Optional[str]

def evaluate_transition_condition(condition_name: str, ctx: BlackboardContext) -> bool:
    """Verifie si la condition logique de transition est remplie."""
    if condition_name == "IsLowHealth":
        return ctx["health_percent"] < 25.0
    elif condition_name == "HasTargetInRange":
        return ctx["target_distance"] < 15.0 and ctx["has_line_of_sight"]
    elif condition_name == "TargetLost":
        return ctx["target_distance"] > 30.0 or not ctx["has_line_of_sight"]
    elif condition_name == "AlarmActive":
        return ctx["is_alarm_triggered"]
    return False

def tick_statetree(
    current_state: str,
    nodes: Dict[str, StateTreeNode],
    ctx: BlackboardContext
) -> StateTreeSimulationResult:
    """Execute un tick de la machine StateTree et evalue les transitions par priorite."""
    node = nodes.get(current_state)
    if not node:
        return {"current_state": "Invalid", "executed_task": "None", "transition_triggered": None}

    # Trier les transitions par priorite decroissante
    sorted_transitions = sorted(node["transitions"], key=lambda t: t["priority"], reverse=True)

    for trans in sorted_transitions:
        if evaluate_transition_condition(trans["condition_name"], ctx):
            next_state = trans["target_state"]
            next_node = nodes[next_state]
            return {
                "current_state": next_state,
                "executed_task": next_node["active_task"],
                "transition_triggered": trans["condition_name"]
            }

    return {
        "current_state": current_state,
        "executed_task": node["active_task"],
        "transition_triggered": None
    }

def build_demo_statetree() -> Dict[str, StateTreeNode]:
    """Construit un arbre d'etats hierarchique de garde de securite."""
    return {
        "Patrol": {
            "state_id": "Patrol",
            "parent_state": None,
            "active_task": "Task_FollowPatrolSpline",
            "transitions": [
                {"target_state": "EngageCombat", "condition_name": "HasTargetInRange", "priority": 10},
                {"target_state": "InvestigateAlarm", "condition_name": "AlarmActive", "priority": 5}
            ]
        },
        "EngageCombat": {
            "state_id": "EngageCombat",
            "parent_state": None,
            "active_task": "Task_ShootTargetRanged",
            "transitions": [
                {"target_state": "RetreatToCover", "condition_name": "IsLowHealth", "priority": 20},
                {"target_state": "Patrol", "condition_name": "TargetLost", "priority": 5}
            ]
        },
        "RetreatToCover": {
            "state_id": "RetreatToCover",
            "parent_state": None,
            "active_task": "Task_FindSafeCoverAndHeal",
            "transitions": [
                {"target_state": "EngageCombat", "condition_name": "HasTargetInRange", "priority": 1}
            ]
        },
        "InvestigateAlarm": {
            "state_id": "InvestigateAlarm",
            "parent_state": None,
            "active_task": "Task_MoveToAlarmSource",
            "transitions": [
                {"target_state": "EngageCombat", "condition_name": "HasTargetInRange", "priority": 10}
            ]
        }
    }

def run_self_test() -> int:
    """Verifie les transitions automatiques de StateTree."""
    print("Execution du self-test StateTree AI UE5...")
    tree = build_demo_statetree()

    ctx: BlackboardContext = {
        "health_percent": 100.0,
        "target_distance": 50.0,
        "has_line_of_sight": False,
        "is_alarm_triggered": False
    }

    # 1. En patrouille normale
    res1 = tick_statetree("Patrol", tree, ctx)
    assert res1["current_state"] == "Patrol", f"Expected Patrol, got {res1['current_state']}"

    # 2. Cible reperee dans le champ de tir
    ctx["target_distance"] = 10.0
    ctx["has_line_of_sight"] = True
    res2 = tick_statetree("Patrol", tree, ctx)
    assert res2["current_state"] == "EngageCombat", f"Expected EngageCombat, got {res2['current_state']}"

    # 3. Blessure critique -> Repli d'urgence
    ctx["health_percent"] = 15.0
    res3 = tick_statetree("EngageCombat", tree, ctx)
    assert res3["current_state"] == "RetreatToCover", f"Expected RetreatToCover, got {res3['current_state']}"

    print(f"[PASS] StateTree teste : Transition reussie vers {res3['current_state']} (Tache active : {res3['executed_task']})")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run_self_test())