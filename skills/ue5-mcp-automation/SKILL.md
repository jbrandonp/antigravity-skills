---
name: ue5-mcp-automation
description: "Control Unreal Engine 5 programmatically from AI agents using the Model Context Protocol (MCP) and Python remote bridge. Automates actor manipulation, Blueprint generation, Node Graph pin wiring, UMG UI, and viewport camera automation via TCP socket 55557."
---

# Unreal Engine 5 MCP Automation Pipeline

Use this skill when an AI agent needs to programmatically inspect, manipulate, or construct assets inside an active Unreal Engine 5 editor session via the Model Context Protocol (MCP).

Based on the battle-tested `unreal-mcp` architecture (2,100+ stars), this bridge connects LLMs and coding agents directly to the Unreal Engine 5 editor through an internal TCP socket bridge (`127.0.0.1:55557`), eliminating manual editor clicks and enabling rapid autonomous level prototyping, Blueprint creation, node graph wiring, and viewport capture.

---

## 1. System Architecture & Prerequisites

The bridge consists of two communicating layers:
1. **Unreal MCP Host (Python stdio MCP server)**: Runs as an MCP server registered in Antigravity / Claude Code / Cursor. Translates standardized tool calls into JSON-RPC socket payloads.
2. **Unreal Engine Plugin / Editor Listener (C++ / Python Remote Execution)**: Listens on TCP port `55557` inside Unreal Engine 5.5 - 5.8, executing operations on the main editor thread via `FSlateApplication` or Python Remote Execution.

```
+-----------------------------------+       stdio JSON-RPC       +-----------------------------------+
|      AI Coding Agent (AGY)        | <------------------------> |     unreal-mcp Server (Python)    |
+-----------------------------------+                            +-----------------------------------+
                                                                                   |
                                                                       TCP Socket (127.0.0.1:55557)
                                                                                   v
                                                                 +-----------------------------------+
                                                                 |  Unreal Engine 5 Editor (Plugin)  |
                                                                 |   - World / Level Actors          |
                                                                 |   - Blueprint Node Graphs         |
                                                                 |   - Viewport & Screenshot Buffers |
                                                                 +-----------------------------------+
```

### Installation & MCP Configuration
Add the MCP server to your Antigravity or workspace MCP configuration (`mcp.json` or `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "unreal-mcp": {
      "command": "python",
      "args": ["-m", "unreal_mcp_server"],
      "env": {
        "UNREAL_HOST": "127.0.0.1",
        "UNREAL_PORT": "55557"
      }
    }
  }
}
```

---

## 2. Core Tool Catalog

### 2.1 — Level & Actor Tools (`actor_tools`)

| Tool | Parameters | Description |
|---|---|---|
| `get_actors_in_level` | None | Returns JSON array of all actors in current world with classes and transforms. |
| `find_actors_by_name` | `pattern: str` | Regex/substring match on actor label or internal name. |
| `create_actor` | `name: str, type: str, location: [float, 3], rotation: [float, 3], scale: [float, 3]` | Spawns primitive (CUBE, SPHERE, CYLINDER) or engine Actor class. |
| `set_actor_transform` | `name: str, location: [float, 3], rotation: [float, 3], scale: [float, 3]` | Updates World Transform coordinates with millimeter precision. |
| `delete_actor` | `name: str` | Removes an actor and cleans hierarchy dependencies. |
| `set_actor_material` | `actor_name: str, material_path: str, slot_index: int = 0` | Assigns Material / Material Instance (`/Game/...`) to mesh slot. |
| `attach_actor_to_actor` | `child_name: str, parent_name: str, socket_name: str = ""` | Attaches hierarchy maintaining world or relative offset. |

#### Example: Spawning an Arena Platform
```json
{
  "tool": "create_actor",
  "arguments": {
    "name": "ArenaFloor_01",
    "type": "CUBE",
    "location": [0.0, 0.0, -50.0],
    "rotation": [0.0, 0.0, 0.0],
    "scale": [50.0, 50.0, 1.0]
  }
}
```

---

### 2.2 — Blueprint Creation & Manipulation (`blueprint_tools`)

| Tool | Parameters | Description |
|---|---|---|
| `create_blueprint` | `name: str, parent_class: str, path: str = "/Game/Blueprints"` | Generates a new `UBlueprint` asset derived from `Actor`, `Character`, `GameModeBase`, etc. |
| `add_component_to_blueprint` | `blueprint_name: str, component_type: str, component_name: str, location: [float, 3], rotation: [float, 3], scale: [float, 3], component_properties: dict` | Adds `StaticMeshComponent`, `BoxComponent`, `NiagaraComponent`, etc. |
| `set_component_properties` | `blueprint_name: str, component_name: str, properties: dict` | Mutates component reflection properties (e.g. `CollisionProfileName: "BlockAll"`). |
| `spawn_blueprint_actor` | `blueprint_path: str, name: str, location: [float, 3], rotation: [float, 3]` | Instantiates a compiled Blueprint asset into the active level. |
| `compile_blueprint` | `blueprint_name: str` | Triggers `FKismetEditorUtilities::CompileBlueprint` and returns compilation errors. |

#### Example: Creating a Hazard Trigger Blueprint
```json
{
  "tool": "create_blueprint",
  "arguments": {
    "name": "BP_LavaHazard",
    "parent_class": "Actor",
    "path": "/Game/Gameplay/Hazards"
  }
}
```

---

### 2.3 — Node Graph & Wiring Tools (`node_tools`)

The most powerful capability: programmatically constructing Blueprint Visual Scripting graphs without manually dragging wires.

| Tool | Parameters | Description |
|---|---|---|
| `add_blueprint_event_node` | `blueprint_name: str, event_type: str, node_position: [int, 2]` | Adds lifecycle event (`BeginPlay`, `Tick`, `OnActorBeginOverlap`, `Destroyed`). |
| `add_blueprint_input_action_node` | `blueprint_name: str, action_name: str, node_position: [int, 2]` | Creates an Enhanced Input action event node (`IA_Jump`). |
| `add_blueprint_function_node` | `blueprint_name: str, function_name: str, target_class: str, node_position: [int, 2]` | Instantiates standard engine functions (`PrintString`, `ApplyDamage`, `SpawnEmitterAtLocation`). |
| `add_blueprint_variable` | `blueprint_name: str, variable_name: str, variable_type: str, default_value: any` | Adds typed variable (`Boolean`, `Integer`, `Float`, `Vector`, `Transform`, `ObjectReference`). |
| `connect_blueprint_nodes` | `blueprint_name: str, source_node_id: str, source_pin: str, target_node_id: str, target_pin: str` | Connects execution pins (`exec`) or data pins with schema validation. |
| `disconnect_blueprint_pins` | `blueprint_name: str, source_node_id: str, source_pin: str, target_node_id: str, target_pin: str` | Breaks specific pin links in the graph. |

#### Blueprint Graph Wiring Flow
```
[Event BeginPlay] (Output: then)
       |
       v
[Print String] (Input: execute, InString: "Hello UE5 MCP!")
```

```json
// Step 1: Create BeginPlay Event Node
{
  "tool": "add_blueprint_event_node",
  "arguments": {
    "blueprint_name": "BP_LavaHazard",
    "event_type": "BeginPlay",
    "node_position": [100, 100]
  }
} // Returns node_id: "K2Node_Event_0"

// Step 2: Create Print String Function Node
{
  "tool": "add_blueprint_function_node",
  "arguments": {
    "blueprint_name": "BP_LavaHazard",
    "function_name": "PrintString",
    "target_class": "KismetSystemLibrary",
    "node_position": [400, 100]
  }
} // Returns node_id: "K2Node_CallFunction_1"

// Step 3: Wire Execution Pin
{
  "tool": "connect_blueprint_nodes",
  "arguments": {
    "blueprint_name": "BP_LavaHazard",
    "source_node_id": "K2Node_Event_0",
    "source_pin": "then",
    "target_node_id": "K2Node_CallFunction_1",
    "target_pin": "execute"
  }
}
```

---

### 2.4 — Editor & Viewport Automation (`editor_tools`)

| Tool | Parameters | Description |
|---|---|---|
| `focus_viewport` | `target: str = None, location: [float, 3] = None, distance: float = 1000.0, orientation: [float, 3] = [0, 0, 0]` | Positions editor viewport camera to inspect spawned geometry. |
| `take_screenshot` | `filename: str = "screenshot.png", show_ui: bool = false, resolution: [int, 2] = [1920, 1080]` | Captures viewport buffer and saves PNG for visual verification. |
| `execute_console_command` | `command: str` | Sends command directly to UE5 editor console (`stat fps`, `viewmode unlit`, `r.Nanite 1`). |
| `run_python_script` | `script_content: str` | Directly executes raw `unreal.py` Python automation inside Unreal editor runtime. |

---

## 3. Autonomous Level-Building Workflow

When generating a game level or testing gameplay slices:

1. **Verify Socket Connectivity**:
   - Call `focus_viewport` or `get_actors_in_level`. If socket timeout occurs (`ECONNREFUSED 127.0.0.1:55557`), instruct user to launch Unreal Engine with the UnrealMCP plugin enabled.
2. **Greybox Construction**:
   - Spawn level boundaries, floor slabs, cover objects, and player starts using `create_actor`.
   - Use strict spatial coordinates ($X$ forward, $Y$ right, $Z$ up in UE5 centimeters).
3. **Blueprint Wiring**:
   - Create interactive actors (`create_blueprint`).
   - Add collision volumes and static meshes (`add_component_to_blueprint`).
   - Wire event logic (`add_blueprint_event_node`, `connect_blueprint_nodes`).
   - Compile and verify error-free compilation (`compile_blueprint`).
4. **Visual Ground-Truth Verification**:
   - Align camera with `focus_viewport(target="BP_LavaHazard", distance=600)`.
   - Capture render using `take_screenshot(filename="audit_hazard.png")`.
   - Inspect screenshot to verify actor alignment and lighting.

---

## 4. Safety Guardrails & Anti-Patterns

❌ **Anti-pattern: Sending raw C++ code to editor console without compilation.**
- *Fix*: Use `run_python_script` for dynamic script execution, or compile C++ modules using `Build.bat` before calling MCP tools.

❌ **Anti-pattern: Spawning actors without coordinate spacing (Z-fighting / stacking).**
- *Fix*: Always calculate bounding boxes and assign explicit non-zero transform offsets.

❌ **Anti-pattern: Forgetting to call `compile_blueprint` after modifying node pins.**
- *Fix*: Blueprint node modifications remain dirty until explicitly compiled. Always end Blueprint edits with `compile_blueprint`.

❌ **Anti-pattern: Blocking the main editor UI thread with synchronous long-running Python loops.**
- *Fix*: Offload batch processing to incremental ticks or asynchronous editor background tasks.
