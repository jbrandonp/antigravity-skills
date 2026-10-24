#!/usr/bin/env python3
"""A2A Bus MCP Server — Point d'échange direct entre agents Giga Factory.

Expose les outils MCP que les agents Hermes peuvent appeler pour :
- S'enregistrer (register_agent)
- Envoyer des messages directs (send_message)
- Lire leurs messages en attente (get_pending)
- Répondre (respond_message)
- Découvrir les autres agents (discover_agents)
- Obtenir les stats du bus (bus_stats)

Usage: python a2a_bus_server.py
Le serveur écoute sur stdin/stdout (stdio transport MCP).
"""

import json
import os
import sys
import datetime
import uuid
import threading
import time
from datetime import timezone

UTC = timezone.utc

def _now():
    """Return current UTC time as ISO 8601 string."""
    return datetime.datetime.now(UTC).isoformat().replace("+00:00", "Z")

# === CONFIG ===
BUS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workspace", "giga-a2a-bus.json")
LOCK_PATH = BUS_PATH + ".lock"
os.makedirs(os.path.dirname(BUS_PATH), exist_ok=True)

# === BUS CORE ===

def _load_bus():
    if os.path.exists(BUS_PATH):
        with open(BUS_PATH, "r") as f:
            return json.load(f)
    return {
        "a2a_bus_version": 1,
        "last_updated": _now(),
        "agents": {},
        "messages": [],
        "pending_deliveries": [],
        "stats": {"total_messages": 0, "completed": 0, "in_flight": 0, "failed": 0, "avg_completion_ms": 0}
    }

def _save_bus(bus):
    bus["last_updated"] = _now()
    with open(BUS_PATH, "w") as f:
        json.dump(bus, f, indent=2)

def _update_stats(bus):
    total = len(bus["messages"])
    completed = sum(1 for m in bus["messages"] if m["status"] == "completed")
    failed = sum(1 for m in bus["messages"] if m["status"] == "failed")
    in_flight = sum(1 for m in bus["messages"] if m["status"] == "pending")
    bus["stats"] = {
        "total_messages": total,
        "completed": completed,
        "in_flight": in_flight,
        "failed": failed,
        "avg_completion_ms": 0  # simplified for now
    }
    return bus["stats"]

# === TOOL IMPLEMENTATIONS ===

def tool_register_agent(params):
    name = params.get("name", "")
    description = params.get("description", "")
    capabilities = params.get("capabilities", {})
    
    if not name:
        return {"error": "Agent name is required"}
    
    bus = _load_bus()
    bus["agents"][name] = {
        "card": {
            "name": name,
            "description": description or f"Agent {name}",
            "url": f"hermes://skill/{name}",
            "capabilities": capabilities,
            "status": "idle"
        },
        "registered_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    _save_bus(bus)
    
    return {
        "result": {
            "agent": name,
            "status": "registered",
            "agents_count": len(bus["agents"])
        }
    }

def tool_send_message(params):
    sender = params.get("sender", "")
    recipient = params.get("recipient", "")
    task_type = params.get("task_type", "generic")
    payload = params.get("payload", {})
    priority = params.get("priority", "normal")
    
    if not sender or not recipient:
        return {"error": "Both sender and recipient are required"}
    
    bus = _load_bus()
    msg_id = f"msg_{uuid.uuid4().hex[:8]}"
    timestamp = _now()
    
    msg = {
        "id": msg_id,
        "protocol": "a2a",
        "jsonrpc": "2.0",
        "method": "tasks/send",
        "sender": sender,
        "recipient": recipient,
        "task_id": f"task_{msg_id}",
        "status": "pending",
        "type": "request",
        "priority": priority,
        "payload": {"type": task_type, "content": payload},
        "metadata": {
            "hop_count": 0,
            "created_at": timestamp
        },
        "created_at": timestamp,
        "completed_at": None
    }
    
    bus["messages"].append(msg)
    bus["pending_deliveries"].append({"msg_id": msg_id, "recipient": recipient})
    _update_stats(bus)
    _save_bus(bus)
    
    return {
        "result": {
            "message_id": msg_id,
            "sender": sender,
            "recipient": recipient,
            "task_type": task_type,
            "status": "pending"
        }
    }

def tool_get_pending_messages(params):
    agent_name = params.get("agent_name", "")
    
    if not agent_name:
        return {"error": "agent_name is required"}
    
    bus = _load_bus()
    pending = []
    for msg in bus["messages"]:
        if msg["recipient"] == agent_name and msg["status"] == "pending":
            pending.append(msg)
    
    return {
        "result": {
            "agent": agent_name,
            "pending_count": len(pending),
            "messages": pending
        }
    }

def tool_respond_message(params):
    msg_id = params.get("message_id", "")
    response = params.get("response", {})
    status = params.get("status", "completed")
    
    if not msg_id:
        return {"error": "message_id is required"}
    
    bus = _load_bus()
    for msg in bus["messages"]:
        if msg["id"] == msg_id:
            msg["status"] = status
            msg["response"] = response
            msg["completed_at"] = _now()
            
            bus["pending_deliveries"] = [d for d in bus["pending_deliveries"] if d["msg_id"] != msg_id]
            
            _update_stats(bus)
            _save_bus(bus)
            
            return {
                "result": {
                    "message_id": msg_id,
                    "status": status,
                    "completed": True
                }
            }
    
    return {"error": f"Message {msg_id} not found"}

def tool_discover_agents(params):
    needed_capability = params.get("needed_capability", None)
    status_filter = params.get("status", None)
    
    bus = _load_bus()
    agents = {}
    
    for name, info in bus["agents"].items():
        if status_filter and info["card"].get("status") != status_filter:
            continue
        if needed_capability:
            triggers = info["card"]["capabilities"].get("triggers", [])
            if needed_capability not in triggers:
                continue
        agents[name] = info
    
    return {
        "result": {
            "agents": agents,
            "count": len(agents)
        }
    }

def tool_bus_stats(params=None):
    bus = _load_bus()
    return {
        "result": {
            "stats": bus["stats"],
            "agents_count": len(bus["agents"]),
            "messages_count": len(bus["messages"]),
            "pending_count": len(bus["pending_deliveries"])
        }
    }

def tool_register_pipeline_agents(params):
    """Enregistre tous les agents Giga Factory standards en une seule commande."""
    project_type = params.get("project_type", "saas")
    
    default_agents = {
        "giga-market-persona": {
            "description": "Génère des personas clients détaillés",
            "capabilities": {"inputs": ["market_segment", "product_type"], "outputs": ["persona_profile"], "triggers": ["market.persona.needed"]}
        },
        "giga-market-tam": {
            "description": "Calcule TAM/SAM/SOM",
            "capabilities": {"inputs": ["market_data", "segment"], "outputs": ["tam_som_sam"], "triggers": ["market.tam.needed"]}
        },
        "giga-brand-tone": {
            "description": "Définit le ton et la voix de marque",
            "capabilities": {"inputs": ["brand_values", "target_audience"], "outputs": ["tone_guide"], "triggers": ["brand.tone.needed"]}
        },
        "giga-finance-model": {
            "description": "Construit des modèles financiers",
            "capabilities": {"inputs": ["revenue_assumptions", "cost_structure"], "outputs": ["financial_model"], "triggers": ["finance.model.needed"]}
        },
        "giga-legal-structure": {
            "description": "Définit la structure juridique",
            "capabilities": {"inputs": ["business_type", "jurisdiction"], "outputs": ["legal_structure"], "triggers": ["legal.structure.needed"]}
        },
        "giga-domain-check": {
            "description": "Vérifie la disponibilité des noms de domaine",
            "capabilities": {"inputs": ["brand_name", "tlds"], "outputs": ["domain_availability"], "triggers": ["domain.check.needed"]}
        }
    }
    
    bus = _load_bus()
    registered = []
    for name, info in default_agents.items():
        if name not in bus["agents"]:
            bus["agents"][name] = {
                "card": {
                    "name": name,
                    "description": info["description"],
                    "url": f"hermes://skill/{name}",
                    "capabilities": info["capabilities"],
                    "status": "idle"
                },
                "registered_at": _now()
            }
            registered.append(name)
    
    _save_bus(bus)
    
    return {
        "result": {
            "registered": registered,
            "total_agents": len(bus["agents"])
        }
    }

# === MCP PROTOCOL IMPLEMENTATION ===

TOOL_DEFINITIONS = [
    {
        "name": "register_agent",
        "description": "Enregistrer un agent dans le bus A2A avec ses capacités",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Nom de l'agent"},
                "description": {"type": "string", "description": "Description des capacités"},
                "capabilities": {"type": "object", "description": "Capacités (inputs, outputs, triggers)"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "send_message",
        "description": "Envoyer un message A2A direct d'un agent à un autre",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sender": {"type": "string", "description": "Nom de l'agent expéditeur"},
                "recipient": {"type": "string", "description": "Nom de l'agent destinataire"},
                "task_type": {"type": "string", "description": "Type de tâche"},
                "payload": {"type": "object", "description": "Contenu du message"},
                "priority": {"type": "string", "enum": ["low", "normal", "high"]}
            },
            "required": ["sender", "recipient"]
        }
    },
    {
        "name": "get_pending_messages",
        "description": "Récupérer les messages en attente pour un agent",
        "inputSchema": {
            "type": "object",
            "properties": {
                "agent_name": {"type": "string", "description": "Nom de l'agent"}
            },
            "required": ["agent_name"]
        }
    },
    {
        "name": "respond_message",
        "description": "Répondre à un message A2A reçu",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message_id": {"type": "string", "description": "ID du message"},
                "response": {"type": "object", "description": "Réponse"},
                "status": {"type": "string", "enum": ["completed", "failed"]}
            },
            "required": ["message_id", "response"]
        }
    },
    {
        "name": "discover_agents",
        "description": "Découvrir les agents disponibles et leurs capacités",
        "inputSchema": {
            "type": "object",
            "properties": {
                "needed_capability": {"type": "string", "description": "Filtrer par capacité nécessaire"},
                "status": {"type": "string", "description": "Filtrer par statut"}
            }
        }
    },
    {
        "name": "bus_stats",
        "description": "Obtenir les statistiques du bus A2A",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "register_pipeline_agents",
        "description": "Enregistrer tous les agents Giga Factory standards",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_type": {"type": "string", "description": "Type de projet"}
            }
        }
    }
]

TOOL_HANDLERS = {
    "register_agent": tool_register_agent,
    "send_message": tool_send_message,
    "get_pending_messages": tool_get_pending_messages,
    "respond_message": tool_respond_message,
    "discover_agents": tool_discover_agents,
    "bus_stats": tool_bus_stats,
    "register_pipeline_agents": tool_register_pipeline_agents
}

def handle_mcp_request(request):
    """Handle a single MCP JSON-RPC request."""
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2025-03-26",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "giga-a2a-bus",
                    "version": "1.0.0"
                }
            }
        }
    
    elif method == "notifications/initialized":
        return None  # no response for notifications
    
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": TOOL_DEFINITIONS
            }
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        
        if tool_name in TOOL_HANDLERS:
            try:
                result = TOOL_HANDLERS[tool_name](tool_args)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Tool not found: {tool_name}"
                }
            }
    
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }


def main():
    """Main loop: read JSON-RPC requests from stdin, write responses to stdout."""
    # Signal startup
    sys.stderr.write("A2A Bus MCP Server started\n")
    sys.stderr.flush()
    
    buffer = ""
    for line in sys.stdin:
        buffer += line
        try:
            request = json.loads(buffer)
            buffer = ""
        except json.JSONDecodeError:
            continue
        
        if isinstance(request, list):
            responses = [handle_mcp_request(r) for r in request]
            responses = [r for r in responses if r is not None]
            if responses:
                response = json.dumps(responses)
                sys.stdout.write(f"{response}\n")
                sys.stdout.flush()
        else:
            response_data = handle_mcp_request(request)
            if response_data is not None:
                response = json.dumps(response_data)
                sys.stdout.write(f"{response}\n")
                sys.stdout.flush()

if __name__ == "__main__":
    main()
