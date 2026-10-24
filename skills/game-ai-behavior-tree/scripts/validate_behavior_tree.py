# -*- coding: utf-8 -*-
"""
validate_behavior_tree.py - Game AI Behavior Tree Validator
Verifie la structure hierarchique, la presence de feuilles et l absence de boucles infinies.
"""

import argparse
from typing import TypedDict, List, Dict, Optional, Tuple

class BTNode(TypedDict, total=False):
    id: str
    node_type: str  # "Selector", "Sequence", "Decorator", "Action", "Condition"
    name: str
    children: List[str]
    blackboard_reads: List[str]
    blackboard_writes: List[str]

DEMO_BEHAVIOR_TREE: Dict[str, BTNode] = {
    "root": {
        "id": "root",
        "node_type": "Selector",
        "name": "RootSelector",
        "children": ["combat_seq", "patrol_seq"],
    },
    "combat_seq": {
        "id": "combat_seq",
        "node_type": "Sequence",
        "name": "EngageInCombat",
        "children": ["has_target_cond", "attack_action"],
    },
    "has_target_cond": {
        "id": "has_target_cond",
        "node_type": "Condition",
        "name": "IsTargetVisible?",
        "blackboard_reads": ["target_player"],
    },
    "attack_action": {
        "id": "attack_action",
        "node_type": "Action",
        "name": "ExecuteMeleeAttack",
        "blackboard_reads": ["target_player"],
    },
    "patrol_seq": {
        "id": "patrol_seq",
        "node_type": "Sequence",
        "name": "PatrolWaypoints",
        "children": ["move_to_waypoint"],
    },
    "move_to_waypoint": {
        "id": "move_to_waypoint",
        "node_type": "Action",
        "name": "NavigateNextWaypoint",
        "blackboard_writes": ["current_waypoint"],
    },
}

def audit_tree(tree: Dict[str, BTNode], root_id: str) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if root_id not in tree:
        return False, [f"Noeud racine '{root_id}' introuvable."]

    visited: List[str] = []
    def traverse(node_id: str, path: List[str]) -> None:
        if node_id in path:
            errors.append(f"Boucle infinie detectee dans l arbre : {' -> '.join(path + [node_id])}")
            return
        node = tree.get(node_id)
        if not node:
            errors.append(f"Noeud enfant reference '{node_id}' non defini.")
            return

        visited.append(node_id)
        children = node.get("children", [])
        if node["node_type"] in ("Selector", "Sequence") and not children:
            errors.append(f"Noeud composite '{node_id}' ({node['node_type']}) n a aucun enfant.")

        for child in children:
            traverse(child, path + [node_id])

    traverse(root_id, [])
    unreachable = [k for k in tree.keys() if k not in visited]
    if unreachable:
        errors.append(f"Noeuds orphelins inatteignables : {unreachable}")

    return (len(errors) == 0), errors

def main():
    parser = argparse.ArgumentParser(description="Game AI Behavior Tree Validator")
    parser.add_argument("--demo", action="store_true", help="Valider l arbre d IA de demonstration")
    args = parser.parse_args()

    print("=" * 65)
    print("      GAME AI BEHAVIOR TREE (VALIDATEUR HIERARCHIQUE SOTA)      ")
    print("=" * 65)

    is_valid, errors = audit_tree(DEMO_BEHAVIOR_TREE, "root")

    print(f"Total Noeuds dans l Arbre : {len(DEMO_BEHAVIOR_TREE)}")
    print(f"Racine : {DEMO_BEHAVIOR_TREE['root']['name']}")
    print("-" * 65)

    if is_valid:
        print("[OK] Arbre de comportement parfaitement valide, acyclique et connexe.")
        print("Structure executee :")
        for nid, n in DEMO_BEHAVIOR_TREE.items():
            ch = f"-> Enfants: {', '.join(n.get('children', []))}" if n.get("children") else "[Action/Feuille]"
            print(f"  [{n['node_type']:<9}] {n['name']:<22} {ch}")
    else:
        print("[X] Erreurs structurelles detectees :")
        for err in errors:
            print(f"  - {err}")

    print("=" * 65)

if __name__ == "__main__":
    main()