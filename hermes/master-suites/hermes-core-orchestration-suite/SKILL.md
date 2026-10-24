---
name: hermes-core-orchestration-suite
description: >-
  Hermes Agent Master Orchestration Suite: Core agent runtime guidelines, prompt engineering, Kanban task management, roadmap planning, MCP ecosystem integration, and recursive self-evolution.
version: 2.0.0
tags:
  - hermes
  - agent-orchestration
  - kanban
  - mcp
  - self-evolution
  - planning
merged_member_skills:
  - hermes-agent (01_Hermes_Skills_Core_Library\autonomous-ai-agents\hermes-agent\SKILL.md)
  - hermes-agent (02_Grok_Hermes_Skills\hermes-agent\SKILL.md)
  - hermes-agent-skill-authoring (02_Grok_Hermes_Skills\hermes-agent-skill-authoring\SKILL.md)
  - hermes-evolution (03_OpenClaw_Hermes_Evolution\SKILL.md)
  - hermes-kanban-orchestrator (02_Grok_Hermes_Skills\hermes-kanban-orchestrator\SKILL.md)
  - hermes-mcp-ecosystem (02_Grok_Hermes_Skills\hermes-mcp-ecosystem\SKILL.md)
  - hermes-memory-github-sync (01_Hermes_Skills_Core_Library\devops\hermes-memory-github-sync\SKILL.md)
  - hermes-plan (02_Grok_Hermes_Skills\hermes-plan\SKILL.md)
  - hermes-plugin-development (01_Hermes_Skills_Core_Library\hermes\hermes-plugin-development\SKILL.md)
  - hermes-powerpoint (02_Grok_Hermes_Skills\hermes-powerpoint\SKILL.md)
  - hermes-self-evolution (02_Grok_Hermes_Skills\hermes-self-evolution\SKILL.md)
  - hermes-web-ui (01_Hermes_Skills_Core_Library\hermes\hermes-web-ui\SKILL.md)
---

# Hermes Core Orchestration Suite

> **Master Suite Consolidée :** Regroupe et unifie **12 compétences spécialisées** de l'écosystème Hermes en une référence modulaire et cohérente.


## 🎯 Quand Déclencher cette Master Suite (Triggers)
Cette suite doit être activée dès que l'utilisateur mentionne l'un des mots-clés, frameworks, outils ou objectifs liés aux modules inclus ci-dessous.
Chaque module peut être exécuté individuellement ou orchestré en séquence selon la tâche demandée.

---
## 📋 Vue d'Ensemble & Sommaire des Modules

1. **[hermes-agent](#module-1-hermes-agent)** : Complete guide to using and extending Hermes Agent — CLI usage, setup, configuration, spawning additional agents, gateway platforms, skills, voice, tools, profiles, and a concise contributor reference. Load this skill when helping users configure Hermes, troubleshoot issues, spawn agent instances, or make code contributions.
2. **[hermes-agent](#module-2-hermes-agent)** : Configure, extend, or contribute to Hermes Agent. Open-source AI agent framework (Nous Research) for terminal, messaging, IDEs. Self-improving via skills, persistent memory, multi-platform gateway, provider-agnostic. Direct port of the Hermes autonomous-ai-agents/hermes-agent skill adapted for Grok Build (run_terminal_command for all hermes CLI, write for configs/scripts, 1password for secrets, background for spawning, cross-refs to claude-code/codex/opencode, github-*, mcp, etc.).
3. **[hermes-agent-skill-authoring](#module-3-hermes-agent-skill-authoring)** : >
4. **[hermes-evolution](#module-4-hermes-evolution)** : Carefully distill user corrections, stated preferences, reusable workflows, and high-cost pitfalls into user-approved updates to AGENTS.md, TOOLS.md, MEMORY.md, or managed SKILL.md files. Only trigger at the end of significant turns in the main session; by default most turns should skip.
5. **[hermes-kanban-orchestrator](#module-5-hermes-kanban-orchestrator)** : >
6. **[hermes-mcp-ecosystem](#module-6-hermes-mcp-ecosystem)** : >
7. **[hermes-memory-github-sync](#module-7-hermes-memory-github-sync)** : Set up automatic GitHub sync for Hermes Agent memory, skills, and config using git + macOS launchd. Runs every 30 minutes in the background. Covers repo init, .gitignore pitfalls, token extraction, and launchd plist setup.
8. **[hermes-plan](#module-8-hermes-plan)** : >
9. **[hermes-plugin-development](#module-9-hermes-plugin-development)** : Create Hermes plugins that hook into the agent lifecycle (post_llm_call, pre_tool_call, on_session_end, etc.). Covers plugin structure, available hooks, and macOS notification pattern.
10. **[hermes-powerpoint](#module-10-hermes-powerpoint)** : >
11. **[hermes-self-evolution](#module-11-hermes-self-evolution)** : >
12. **[hermes-web-ui](#module-12-hermes-web-ui)** : 启动、配置和排查 hermes-web-ui 面板，包括 Node.js 版本要求和 nvm 持久化配置。

---

## Module 1: `hermes-agent`

- **Origine :** `01_Hermes_Skills_Core_Library\autonomous-ai-agents\hermes-agent\SKILL.md`
- **Rôle / Objectif :** Complete guide to using and extending Hermes Agent — CLI usage, setup, configuration, spawning additional agents, gateway platforms, skills, voice, tools, profiles, and a concise contributor reference. Load this skill when helping users configure Hermes, troubleshoot issues, spawn agent instances, or make code contributions.

## Hermes Agent

Hermes Agent is an open-source AI agent framework by Nous Research that runs in your terminal, messaging platforms, and IDEs. It belongs to the same category as Claude Code (Anthropic), Codex (OpenAI), and OpenClaw — autonomous coding and task-execution agents that use tool calling to interact with your system. Hermes works with any LLM provider (OpenRouter, Anthropic, OpenAI, DeepSeek, local models, and 15+ others) and runs on Linux, macOS, and WSL.

What makes Hermes different:

- **Self-improving through skills** — Hermes learns from experience by saving reusable procedures as skills. When it solves a complex problem, discovers a workflow, or gets corrected, it can persist that knowledge as a skill document that loads into future sessions. Skills accumulate over time, making the agent better at your specific tasks and environment.
- **Persistent memory across sessions** — remembers who you are, your preferences, environment details, and lessons learned. Pluggable memory backends (built-in, Honcho, Mem0, and more) let you choose how memory works.
- **Multi-platform gateway** — the same agent runs on Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email, and 10+ other platforms with full tool access, not just chat.
- **Provider-agnostic** — swap models and providers mid-workflow without changing anything else. Credential pools rotate across multiple API keys automatically.
- **Profiles** — run multiple independent Hermes instances with isolated configs, sessions, skills, and memory.
- **Extensible** — plugins, MCP servers, custom tools, webhook triggers, cron scheduling, and the full Python ecosystem.

People use Hermes for software development, research, system administration, data analysis, content creation, home automation, and anything else that benefits from an AI agent with persistent context and full system access.

**This skill helps you work with Hermes Agent effectively** — setting it up, configuring features, spawning additional agent instances, troubleshooting issues, finding the right commands and settings, and understanding how the system works when you need to extend or contribute to it.

**Docs:** https://hermes-agent.nousresearch.com/docs/

### Quick Start

```bash
## Install
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

## Interactive chat (default)
hermes

## Single query
hermes chat -q "What is the capital of France?"

## Setup wizard
hermes setup

## Change model/provider
hermes model

## Check health
hermes doctor
```

---

### CLI Reference

#### Global Flags

```
hermes [flags] [command]

  --version, -V             Show version
  --resume, -r SESSION      Resume session by ID or title
  --continue, -c [NAME]     Resume by name, or most recent session
  --worktree, -w            Isolated git worktree mode (parallel agents)
  --skills, -s SKILL        Preload skills (comma-separate or repeat)
  --profile, -p NAME        Use a named profile
  --yolo                    Skip dangerous command approval
  --pass-session-id         Include session ID in system prompt
```

No subcommand defaults to `chat`.

#### Chat

```
hermes chat [flags]
  -q, --query TEXT          Single query, non-interactive
  -m, --model MODEL         Model (e.g. anthropic/claude-sonnet-4)
  -t, --toolsets LIST       Comma-separated toolsets
  --provider PROVIDER       Force provider (openrouter, anthropic, nous, etc.)
  -v, --verbose             Verbose output
  -Q, --quiet               Suppress banner, spinner, tool previews
  --checkpoints             Enable filesystem checkpoints (/rollback)
  --source TAG              Session source tag (default: cli)
```

#### Configuration

```
hermes setup [section]      Interactive wizard (model|terminal|gateway|tools|agent)
hermes model                Interactive model/provider picker
hermes config               View current config
hermes config edit          Open config.yaml in $EDITOR
hermes config set KEY VAL   Set a config value
hermes config path          Print config.yaml path
hermes config env-path      Print .env path
hermes config check         Check for missing/outdated config
hermes config migrate       Update config with new options
hermes login [--provider P] OAuth login (nous, openai-codex)
hermes logout               Clear stored auth
hermes doctor [--fix]       Check dependencies and config
hermes status [--all]       Show component status
```

#### Tools & Skills

```
hermes tools                Interactive tool enable/disable (curses UI)
hermes tools list           Show all tools and status
hermes tools enable NAME    Enable a toolset
hermes tools disable NAME   Disable a toolset

hermes skills list          List installed skills
hermes skills search QUERY  Search the skills hub
hermes skills install ID    Install a skill
hermes skills inspect ID    Preview without installing
hermes skills config        Enable/disable skills per platform
hermes skills check         Check for updates
hermes skills update        Update outdated skills
hermes skills uninstall N   Remove a hub skill
hermes skills publish PATH  Publish to registry
hermes skills browse        Browse all available skills
hermes skills tap add REPO  Add a GitHub repo as skill source
```

#### MCP Servers

```
hermes mcp serve            Run Hermes as an MCP server
hermes mcp add NAME         Add an MCP server (--url or --command)
hermes mcp remove NAME      Remove an MCP server
hermes mcp list             List configured servers
hermes mcp test NAME        Test connection
hermes mcp configure NAME   Toggle tool selection
```

#### Gateway (Messaging Platforms)

```
hermes gateway run          Start gateway foreground
hermes gateway install      Install as background service
hermes gateway start/stop   Control the service
hermes gateway restart      Restart the service
hermes gateway status       Check status
hermes gateway setup        Configure platforms
```

Supported platforms: Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, Matrix, Mattermost, Home Assistant, DingTalk, Feishu, WeCom, BlueBubbles (iMessage), Weixin (WeChat), API Server, Webhooks. Open WebUI connects via the API Server adapter.

Platform docs: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/

#### Sessions

```
hermes sessions list        List recent sessions
hermes sessions browse      Interactive picker
hermes sessions export OUT  Export to JSONL
hermes sessions rename ID T Rename a session
hermes sessions delete ID   Delete a session
hermes sessions prune       Clean up old sessions (--older-than N days)
hermes sessions stats       Session store statistics
```

#### Cron Jobs

```
hermes cron list            List jobs (--all for disabled)
hermes cron create SCHED    Create: '30m', 'every 2h', '0 9 * * *'
hermes cron edit ID         Edit schedule, prompt, delivery
hermes cron pause/resume ID Control job state
hermes cron run ID          Trigger on next tick
hermes cron remove ID       Delete a job
hermes cron status          Scheduler status
```

#### Webhooks

```
hermes webhook subscribe N  Create route at /webhooks/<name>
hermes webhook list         List subscriptions
hermes webhook remove NAME  Remove a subscription
hermes webhook test NAME    Send a test POST
```

#### Profiles

```
hermes profile list         List all profiles
hermes profile create NAME  Create (--clone, --clone-all, --clone-from)
hermes profile use NAME     Set sticky default
hermes profile delete NAME  Delete a profile
hermes profile show NAME    Show details
hermes profile alias NAME   Manage wrapper scripts
hermes profile rename A B   Rename a profile
hermes profile export NAME  Export to tar.gz
hermes profile import FILE  Import from archive
```

#### Credential Pools

```
hermes auth add             Interactive credential wizard
hermes auth list [PROVIDER] List pooled credentials
hermes auth remove P INDEX  Remove by provider + index
hermes auth reset PROVIDER  Clear exhaustion status
```

#### Other

```
hermes insights [--days N]  Usage analytics
hermes update               Update to latest version
hermes pairing list/approve/revoke  DM authorization
hermes plugins list/install/remove  Plugin management
hermes honcho setup/status  Honcho memory integration (requires honcho plugin)
hermes memory setup/status/off  Memory provider config
hermes completion bash|zsh  Shell completions
hermes acp                  ACP server (IDE integration)
hermes claw migrate         Migrate from OpenClaw
hermes uninstall            Uninstall Hermes
```

---

### Slash Commands (In-Session)

Type these during an interactive chat session.

#### Session Control
```
/new (/reset)        Fresh session
/clear               Clear screen + new session (CLI)
/retry               Resend last message
/undo                Remove last exchange
/title [name]        Name the session
/compress            Manually compress context
/stop                Kill background processes
/rollback [N]        Restore filesystem checkpoint
/background <prompt> Run prompt in background
/queue <prompt>      Queue for next turn
/resume [name]       Resume a named session
```

#### Configuration
```
/config              Show config (CLI)
/model [name]        Show or change model
/provider            Show provider info
/personality [name]  Set personality
/reasoning [level]   Set reasoning (none|minimal|low|medium|high|xhigh|show|hide)
/verbose             Cycle: off → new → all → verbose
/voice [on|off|tts]  Voice mode
/yolo                Toggle approval bypass
/skin [name]         Change theme (CLI)
/statusbar           Toggle status bar (CLI)
```

#### Tools & Skills
```
/tools               Manage tools (CLI)
/toolsets            List toolsets (CLI)
/skills              Search/install skills (CLI)
/skill <name>        Load a skill into session
/cron                Manage cron jobs (CLI)
/reload-mcp          Reload MCP servers
/plugins             List plugins (CLI)
```

#### Gateway
```
/approve             Approve a pending command (gateway)
/deny                Deny a pending command (gateway)
/restart             Restart gateway (gateway)
/sethome             Set current chat as home channel (gateway)
/update              Update Hermes to latest (gateway)
/platforms (/gateway) Show platform connection status (gateway)
```

#### Utility
```
/branch (/fork)      Branch the current session
/btw                 Ephemeral side question (doesn't interrupt main task)
/fast                Toggle priority/fast processing
/browser             Open CDP browser connection
/history             Show conversation history (CLI)
/save                Save conversation to file (CLI)
/paste               Attach clipboard image (CLI)
/image               Attach local image file (CLI)
```

#### Info
```
/help                Show commands
/commands [page]     Browse all commands (gateway)
/usage               Token usage
/insights [days]     Usage analytics
/status              Session info (gateway)
/profile             Active profile info
```

#### Exit
```
/quit (/exit, /q)    Exit CLI
```

---

### Key Paths & Config

```
~/.hermes/config.yaml       Main configuration
~/.hermes/.env              API keys and secrets
$HERMES_HOME/skills/        Installed skills
~/.hermes/sessions/         Session transcripts
~/.hermes/logs/             Gateway and error logs
~/.hermes/auth.json         OAuth tokens and credential pools
~/.hermes/hermes-agent/     Source code (if git-installed)
```

Profiles use `~/.hermes/profiles/<name>/` with the same layout.

#### Config Sections

Edit with `hermes config edit` or `hermes config set section.key value`.

| Section | Key options |
|---------|-------------|
| `model` | `default`, `provider`, `base_url`, `api_key`, `context_length` |
| `agent` | `max_turns` (90), `tool_use_enforcement` |
| `terminal` | `backend` (local/docker/ssh/modal), `cwd`, `timeout` (180) |
| `compression` | `enabled`, `threshold` (0.50), `target_ratio` (0.20) |
| `display` | `skin`, `tool_progress`, `show_reasoning`, `show_cost` |
| `stt` | `enabled`, `provider` (local/groq/openai/mistral) |
| `tts` | `provider` (edge/elevenlabs/openai/minimax/mistral/neutts) |
| `memory` | `memory_enabled`, `user_profile_enabled`, `provider` |
| `security` | `tirith_enabled`, `website_blocklist` |
| `delegation` | `model`, `provider`, `base_url`, `api_key`, `max_iterations` (50), `reasoning_effort` |
| `smart_model_routing` | `enabled`, `cheap_model` |
| `checkpoints` | `enabled`, `max_snapshots` (50) |

Full config reference: https://hermes-agent.nousresearch.com/docs/user-guide/configuration

#### Providers

20+ providers supported. Set via `hermes model` or `hermes setup`.

| Provider | Auth | Key env var |
|----------|------|-------------|
| OpenRouter | API key | `OPENROUTER_API_KEY` |
| Anthropic | API key | `ANTHROPIC_API_KEY` |
| Nous Portal | OAuth | `hermes auth` |
| OpenAI Codex | OAuth | `hermes auth` |
| GitHub Copilot | Token | `COPILOT_GITHUB_TOKEN` |
| Google Gemini | API key | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| DeepSeek | API key | `DEEPSEEK_API_KEY` |
| xAI / Grok | API key | `XAI_API_KEY` |
| Hugging Face | Token | `HF_TOKEN` |
| Z.AI / GLM | API key | `GLM_API_KEY` |
| MiniMax | API key | `MINIMAX_API_KEY` |
| MiniMax CN | API key | `MINIMAX_CN_API_KEY` |
| Kimi / Moonshot | API key | `KIMI_API_KEY` |
| Alibaba / DashScope | API key | `DASHSCOPE_API_KEY` |
| Xiaomi MiMo | API key | `XIAOMI_API_KEY` |
| Kilo Code | API key | `KILOCODE_API_KEY` |
| AI Gateway (Vercel) | API key | `AI_GATEWAY_API_KEY` |
| OpenCode Zen | API key | `OPENCODE_ZEN_API_KEY` |
| OpenCode Go | API key | `OPENCODE_GO_API_KEY` |
| Qwen OAuth | OAuth | `hermes login --provider qwen-oauth` |
| Custom endpoint | Config | `model.base_url` + `model.api_key` in config.yaml |
| GitHub Copilot ACP | External | `COPILOT_CLI_PATH` or Copilot CLI |

Full provider docs: https://hermes-agent.nousresearch.com/docs/integrations/providers

#### Toolsets

Enable/disable via `hermes tools` (interactive) or `hermes tools enable/disable NAME`.

| Toolset | What it provides |
|---------|-----------------|
| `web` | Web search and content extraction |
| `browser` | Browser automation (Browserbase, Camofox, or local Chromium) |
| `terminal` | Shell commands and process management |
| `file` | File read/write/search/patch |
| `code_execution` | Sandboxed Python execution |
| `vision` | Image analysis |
| `image_gen` | AI image generation |
| `tts` | Text-to-speech |
| `skills` | Skill browsing and management |
| `memory` | Persistent cross-session memory |
| `session_search` | Search past conversations |
| `delegation` | Subagent task delegation |
| `cronjob` | Scheduled task management |
| `clarify` | Ask user clarifying questions |
| `messaging` | Cross-platform message sending |
| `search` | Web search only (subset of `web`) |
| `todo` | In-session task planning and tracking |
| `rl` | Reinforcement learning tools (off by default) |
| `moa` | Mixture of Agents (off by default) |
| `homeassistant` | Smart home control (off by default) |

Tool changes take effect on `/reset` (new session). They do NOT apply mid-conversation to preserve prompt caching.

---

### Voice & Transcription

#### STT (Voice → Text)

Voice messages from messaging platforms are auto-transcribed.

Provider priority (auto-detected):
1. **Local faster-whisper** — free, no API key: `pip install faster-whisper`
2. **Groq Whisper** — free tier: set `GROQ_API_KEY`
3. **OpenAI Whisper** — paid: set `VOICE_TOOLS_OPENAI_KEY`
4. **Mistral Voxtral** — set `MISTRAL_API_KEY`

Config:
```yaml
stt:
  enabled: true
  provider: local        # local, groq, openai, mistral
  local:
    model: base          # tiny, base, small, medium, large-v3
```

#### TTS (Text → Voice)

| Provider | Env var | Free? |
|----------|---------|-------|
| Edge TTS | None | Yes (default) |
| ElevenLabs | `ELEVENLABS_API_KEY` | Free tier |
| OpenAI | `VOICE_TOOLS_OPENAI_KEY` | Paid |
| MiniMax | `MINIMAX_API_KEY` | Paid |
| Mistral (Voxtral) | `MISTRAL_API_KEY` | Paid |
| NeuTTS (local) | None (`pip install neutts[all]` + `espeak-ng`) | Free |

Voice commands: `/voice on` (voice-to-voice), `/voice tts` (always voice), `/voice off`.

---

### Spawning Additional Hermes Instances

Run additional Hermes processes as fully independent subprocesses — separate sessions, tools, and environments.

#### When to Use This vs delegate_task

| | `delegate_task` | Spawning `hermes` process |
|-|-----------------|--------------------------|
| Isolation | Separate conversation, shared process | Fully independent process |
| Duration | Minutes (bounded by parent loop) | Hours/days |
| Tool access | Subset of parent's tools | Full tool access |
| Interactive | No | Yes (PTY mode) |
| Use case | Quick parallel subtasks | Long autonomous missions |

#### One-Shot Mode

```
terminal(command="hermes chat -q 'Research GRPO papers and write summary to ~/research/grpo.md'", timeout=300)

## Background for long tasks:
terminal(command="hermes chat -q 'Set up CI/CD for ~/myapp'", background=true)
```

#### Interactive PTY Mode (via tmux)

Hermes uses prompt_toolkit, which requires a real terminal. Use tmux for interactive spawning:

```
## Start
terminal(command="tmux new-session -d -s agent1 -x 120 -y 40 'hermes'", timeout=10)

## Wait for startup, then send a message
terminal(command="sleep 8 && tmux send-keys -t agent1 'Build a FastAPI auth service' Enter", timeout=15)

## Read output
terminal(command="sleep 20 && tmux capture-pane -t agent1 -p", timeout=5)

## Send follow-up
terminal(command="tmux send-keys -t agent1 'Add rate limiting middleware' Enter", timeout=5)

## Exit
terminal(command="tmux send-keys -t agent1 '/exit' Enter && sleep 2 && tmux kill-session -t agent1", timeout=10)
```

#### Multi-Agent Coordination

```
## Agent A: backend
terminal(command="tmux new-session -d -s backend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t backend 'Build REST API for user management' Enter", timeout=15)

## Agent B: frontend
terminal(command="tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t frontend 'Build React dashboard for user management' Enter", timeout=15)

## Check progress, relay context between them
terminal(command="tmux capture-pane -t backend -p | tail -30", timeout=5)
terminal(command="tmux send-keys -t frontend 'Here is the API schema from the backend agent: ...' Enter", timeout=5)
```

#### Session Resume

```
## Resume most recent session
terminal(command="tmux new-session -d -s resumed 'hermes --continue'", timeout=10)

## Resume specific session
terminal(command="tmux new-session -d -s resumed 'hermes --resume 20260225_143052_a1b2c3'", timeout=10)
```

#### Tips

- **Prefer `delegate_task` for quick subtasks** — less overhead than spawning a full process
- **Use `-w` (worktree mode)** when spawning agents that edit code — prevents git conflicts
- **Set timeouts** for one-shot mode — complex tasks can take 5-10 minutes
- **Use `hermes chat -q` for fire-and-forget** — no PTY needed
- **Use tmux for interactive sessions** — raw PTY mode has `\r` vs `\n` issues with prompt_toolkit
- **For scheduled tasks**, use the `cronjob` tool instead of spawning — handles delivery and retry

---

### Troubleshooting

#### Voice not working
1. Check `stt.enabled: true` in config.yaml
2. Verify provider: `pip install faster-whisper` or set API key
3. In gateway: `/restart`. In CLI: exit and relaunch.

#### Tool not available
1. `hermes tools` — check if toolset is enabled for your platform
2. Some tools need env vars (check `.env`)
3. `/reset` after enabling tools

#### Model/provider issues
1. `hermes doctor` — check config and dependencies
2. `hermes login` — re-authenticate OAuth providers
3. Check `.env` has the right API key
4. **Copilot 403**: `gh auth login` tokens do NOT work for Copilot API. You must use the Copilot-specific OAuth device code flow via `hermes model` → GitHub Copilot.

#### Changes not taking effect
- **Tools/skills:** `/reset` starts a new session with updated toolset
- **Config changes:** In gateway: `/restart`. In CLI: exit and relaunch.
- **Code changes:** Restart the CLI or gateway process

#### Skills not showing
1. `hermes skills list` — verify installed
2. `hermes skills config` — check platform enablement
3. Load explicitly: `/skill name` or `hermes -s name`

#### Gateway issues
Check logs first:
```bash
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20
```

Common gateway problems:
- **Gateway dies on SSH logout**: Enable linger: `sudo loginctl enable-linger $USER`
- **Gateway dies on WSL2 close**: WSL2 requires `systemd=true` in `/etc/wsl.conf` for systemd services to work. Without it, gateway falls back to `nohup` (dies when session closes).
- **Gateway crash loop**: Reset the failed state: `systemctl --user reset-failed hermes-gateway`

#### Platform-specific issues
- **Discord bot silent**: Must enable **Message Content Intent** in Bot → Privileged Gateway Intents.
- **Slack bot only works in DMs**: Must subscribe to `message.channels` event. Without it, the bot ignores public channels.
- **Windows HTTP 400 "No models provided"**: Config file encoding issue (BOM). Ensure `config.yaml` is saved as UTF-8 without BOM.

#### Auxiliary models not working
If `auxiliary` tasks (vision, compression, session_search) fail silently, the `auto` provider can't find a backend. Either set `OPENROUTER_API_KEY` or `GOOGLE_API_KEY`, or explicitly configure each auxiliary task's provider:
```bash
hermes config set auxiliary.vision.provider <your_provider>
hermes config set auxiliary.vision.model <model_name>
```

---

### Where to Find Things

| Looking for... | Location |
|----------------|----------|
| Config options | `hermes config edit` or [Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) |
| Available tools | `hermes tools list` or [Tools reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference) |
| Slash commands | `/help` in session or [Slash commands reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands) |
| Skills catalog | `hermes skills browse` or [Skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) |
| Provider setup | `hermes model` or [Providers guide](https://hermes-agent.nousresearch.com/docs/integrations/providers) |
| Platform setup | `hermes gateway setup` or [Messaging docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) |
| MCP servers | `hermes mcp list` or [MCP guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) |
| Profiles | `hermes profile list` or [Profiles docs](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) |
| Cron jobs | `hermes cron list` or [Cron docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) |
| Memory | `hermes memory status` or [Memory docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) |
| Env variables | `hermes config env-path` or [Env vars reference](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) |
| CLI commands | `hermes --help` or [CLI reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) |
| Gateway logs | `~/.hermes/logs/gateway.log` |
| Session files | `~/.hermes/sessions/` or `hermes sessions browse` |
| Source code | `~/.hermes/hermes-agent/` |

---

### Contributor Quick Reference

For occasional contributors and PR authors. Full developer docs: https://hermes-agent.nousresearch.com/docs/developer-guide/

#### Project Layout

```
hermes-agent/
├── run_agent.py          # AIAgent — core conversation loop
├── model_tools.py        # Tool discovery and dispatch
├── toolsets.py           # Toolset definitions
├── cli.py                # Interactive CLI (HermesCLI)
├── hermes_state.py       # SQLite session store
├── agent/                # Prompt builder, context compression, memory, model routing, credential pooling, skill dispatch
├── hermes_cli/           # CLI subcommands, config, setup, commands
│   ├── commands.py       # Slash command registry (CommandDef)
│   ├── config.py         # DEFAULT_CONFIG, env var definitions
│   └── main.py           # CLI entry point and argparse
├── tools/                # One file per tool
│   └── registry.py       # Central tool registry
├── gateway/              # Messaging gateway
│   └── platforms/        # Platform adapters (telegram, discord, etc.)
├── cron/                 # Job scheduler
├── tests/                # ~3000 pytest tests
└── website/              # Docusaurus docs site
```

Config: `~/.hermes/config.yaml` (settings), `~/.hermes/.env` (API keys).

#### Adding a Tool (3 files)

**1. Create `tools/your_tool.py`:**
```python
import json, os
from tools.registry import registry

def check_requirements() -> bool:
    return bool(os.getenv("EXAMPLE_API_KEY"))

def example_tool(param: str, task_id: str = None) -> str:
    return json.dumps({"success": True, "data": "..."})

registry.register(
    name="example_tool",
    toolset="example",
    schema={"name": "example_tool", "description": "...", "parameters": {...}},
    handler=lambda args, **kw: example_tool(
        param=args.get("param", ""), task_id=kw.get("task_id")),
    check_fn=check_requirements,
    requires_env=["EXAMPLE_API_KEY"],
)
```

**2. Add to `toolsets.py`** → `_HERMES_CORE_TOOLS` list.

Auto-discovery: any `tools/*.py` file with a top-level `registry.register()` call is imported automatically — no manual list needed.

All handlers must return JSON strings. Use `get_hermes_home()` for paths, never hardcode `~/.hermes`.

#### Adding a Slash Command

1. Add `CommandDef` to `COMMAND_REGISTRY` in `hermes_cli/commands.py`
2. Add handler in `cli.py` → `process_command()`
3. (Optional) Add gateway handler in `gateway/run.py`

All consumers (help text, autocomplete, Telegram menu, Slack mapping) derive from the central registry automatically.

#### Agent Loop (High Level)

```
run_conversation():
  1. Build system prompt
  2. Loop while iterations < max:
     a. Call LLM (OpenAI-format messages + tool schemas)
     b. If tool_calls → dispatch each via handle_function_call() → append results → continue
     c. If text response → return
  3. Context compression triggers automatically near token limit
```

#### Testing

```bash
python -m pytest tests/ -o 'addopts=' -q   # Full suite
python -m pytest tests/tools/ -q            # Specific area
```

- Tests auto-redirect `HERMES_HOME` to temp dirs — never touch real `~/.hermes/`
- Run full suite before pushing any change
- Use `-o 'addopts='` to clear any baked-in pytest flags

#### Commit Conventions

```
type: concise subject line

Optional body.
```

Types: `fix:`, `feat:`, `refactor:`, `docs:`, `chore:`

#### Key Rules

- **Never break prompt caching** — don't change context, tools, or system prompt mid-conversation
- **Message role alternation** — never two assistant or two user messages in a row
- Use `get_hermes_home()` from `hermes_constants` for all paths (profile-safe)
- Config values go in `config.yaml`, secrets go in `.env`
- New tools need a `check_fn` so they only appear when requirements are met


---

## Module 2: `hermes-agent`

- **Origine :** `02_Grok_Hermes_Skills\hermes-agent\SKILL.md`
- **Rôle / Objectif :** Configure, extend, or contribute to Hermes Agent. Open-source AI agent framework (Nous Research) for terminal, messaging, IDEs. Self-improving via skills, persistent memory, multi-platform gateway, provider-agnostic. Direct port of the Hermes autonomous-ai-agents/hermes-agent skill adapted for Grok Build (run_terminal_command for all hermes CLI, write for configs/scripts, 1password for secrets, background for spawning, cross-refs to claude-code/codex/opencode, github-*, mcp, etc.).

## Hermes Agent

Hermes Agent is an open-source AI agent framework by Nous Research that runs in your terminal, messaging platforms, and IDEs. It belongs to the same category as Claude Code (Anthropic), Codex (OpenAI), and OpenCode — autonomous coding and task-execution agents that use tool calling to interact with your system. Hermes works with any LLM provider (OpenRouter, Anthropic, OpenAI, DeepSeek, local models, xAI/Grok, and 15+ others) and runs on Linux, macOS, Windows, and WSL.

What makes Hermes different:

- **Self-improving through skills** — Hermes learns from experience by saving reusable procedures as skills. When it solves a complex problem, discovers a workflow, or gets corrected, it can persist that knowledge as a skill document that loads into future sessions. Skills accumulate over time, making the agent better at your specific tasks and environment.
- **Persistent memory across sessions** — remembers who you are, your preferences, environment details, and lessons learned. Pluggable memory backends (built-in, Honcho, Mem0, and more) let you choose how memory works.
- **Multi-platform gateway** — the same agent runs on Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email, and 10+ other platforms with full tool access, not just chat.
- **Provider-agnostic** — swap models and providers mid-workflow without changing anything else. Credential pools rotate across multiple API keys automatically.
- **Profiles** — run multiple independent Hermes instances with isolated configs, sessions, skills, and memory.
- **Extensible** — plugins, MCP servers, custom tools, webhook triggers, cron scheduling, and the full Python ecosystem.

People use Hermes for software development, research, system administration, data analysis, content creation, home automation, and anything else that benefits from an AI agent with persistent context and full system access.

**This skill helps you work with Hermes Agent effectively** — setting it up, configuring features, spawning additional agent instances, troubleshooting issues, finding the right commands and settings, and understanding how the system works when you need to extend or contribute to it.

**Docs:** https://hermes-agent.nousresearch.com/docs/

### Quick Start (Grok-adapted)

```pwsh
## Install (if not already)
run_terminal_command "curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash"

## Interactive chat (default)
run_terminal_command "hermes"

## Single query
run_terminal_command "hermes chat -q \"What is the capital of France?\""

## Setup wizard
run_terminal_command "hermes setup"

## Change model/provider
run_terminal_command "hermes model"

## Check health
run_terminal_command "hermes doctor"
```

For Grok: All "hermes ..." commands are executed via `run_terminal_command`. For background/long-running: add `background=true`. For interactive spawning: use background + follow-up commands (Grok terminal supports this; tmux if you need real PTY for complex TUI).

### CLI Reference (via run_terminal_command)

#### Global Flags

```pwsh
run_terminal_command "hermes [flags] [command]"

## Examples:
run_terminal_command "hermes --version"
run_terminal_command "hermes --resume SESSION"
run_terminal_command "hermes --continue [NAME]"
run_terminal_command "hermes --worktree"  # Isolated git worktree mode (parallel agents)
run_terminal_command "hermes --skills SKILL"  # Preload skills (comma-separate or repeat)
run_terminal_command "hermes --profile NAME"  # Use a named profile
run_terminal_command "hermes --yolo"  # Skip dangerous command approval
```

No subcommand defaults to `chat`.

#### Chat

```pwsh
run_terminal_command "hermes chat [flags]"
## -q, --query TEXT          Single query, non-interactive
## -m, --model MODEL         Model (e.g. anthropic/claude-sonnet-4 or xai/grok-...)
## -t, --toolsets LIST       Comma-separated toolsets
## --provider PROVIDER       Force provider (openrouter, anthropic, nous, xai, etc.)
## -v, --verbose             Verbose output
## -Q, --quiet               Suppress banner, spinner, tool previews
## --checkpoints             Enable filesystem checkpoints (/rollback)
## --source TAG              Session source tag (default: cli)
```

#### Configuration

```pwsh
run_terminal_command "hermes setup [section]"      # Interactive wizard (model|terminal|gateway|tools|agent)
run_terminal_command "hermes model"                # Interactive model/provider picker
run_terminal_command "hermes config"               # View current config
run_terminal_command "hermes config edit"          # Open config.yaml in $EDITOR (use write/search_replace for Grok edits)
run_terminal_command "hermes config set KEY VAL"   # Set a config value
run_terminal_command "hermes config path"          # Print config.yaml path
run_terminal_command "hermes config env-path"      # Print .env path
run_terminal_command "hermes config check"         # Check for missing/outdated config
run_terminal_command "hermes config migrate"       # Update config with new options
run_terminal_command "hermes auth"                 # Interactive credential manager
run_terminal_command "hermes auth add PROVIDER"    # Add OAuth or API-key credential (e.g. nous, openai-codex, qwen-oauth, xai)
run_terminal_command "hermes auth list"            # List stored credentials
run_terminal_command "hermes auth remove PROVIDER" # Remove a stored credential
run_terminal_command "hermes doctor [--fix]"       # Check dependencies and config
run_terminal_command "hermes status [--all]"       # Show component status
```

**Grok note:** Use `1password` skill to manage secrets in .env before running hermes commands. For editing configs, prefer `write` or `search_replace` on the files in ~/.hermes/ (or profile dirs), then run hermes commands.

#### Tools & Skills

```pwsh
run_terminal_command "hermes tools"                # Interactive tool enable/disable (curses UI)
run_terminal_command "hermes tools list"           # Show all tools and status
run_terminal_command "hermes tools enable NAME"    # Enable a toolset
run_terminal_command "hermes tools disable NAME"   # Disable a toolset

run_terminal_command "hermes skills list"          # List installed skills
run_terminal_command "hermes skills search QUERY"  # Search the skills hub
run_terminal_command "hermes skills install ID"    # Install a skill (ID can be a hub identifier OR a direct https://…/SKILL.md URL; pass --name to override)
run_terminal_command "hermes skills inspect ID"    # Preview without installing
run_terminal_command "hermes skills config"        # Enable/disable skills per platform
run_terminal_command "hermes skills check"         # Check for updates
run_terminal_command "hermes skills update"        # Update outdated skills
run_terminal_command "hermes skills uninstall N"   # Remove a hub skill
run_terminal_command "hermes skills publish PATH"  # Publish to registry
run_terminal_command "hermes skills browse"        # Browse all available skills
run_terminal_command "hermes skills tap add REPO"  # Add a GitHub repo as skill source
```

**Grok integration:** Grok has its own skills system (many Hermes skills already ported here, e.g. claude-code, codex, opencode, github-*, etc.). You can load Hermes skills via the CLI if you have Hermes installed, or use the ported Grok versions directly. For cross-use, the skill files are compatible Markdown.

#### MCP Servers

```pwsh
run_terminal_command "hermes mcp serve"            # Run Hermes as an MCP server
run_terminal_command "hermes mcp add NAME --url URL or --command CMD"  # Add an MCP server
run_terminal_command "hermes mcp remove NAME"      # Remove an MCP server
run_terminal_command "hermes mcp list"             # List configured servers
run_terminal_command "hermes mcp test NAME"        # Test connection
run_terminal_command "hermes mcp configure NAME"   # Toggle tool selection
```

See the ported `hermes-mcp-ecosystem` skill for details on MCP in Grok context.

#### Gateway (Messaging Platforms)

```pwsh
run_terminal_command "hermes gateway run"          # Start gateway foreground
run_terminal_command "hermes gateway install"      # Install as background service
run_terminal_command "hermes gateway start/stop"   # Control the service
run_terminal_command "hermes gateway restart"      # Restart the service
run_terminal_command "hermes gateway status"       # Check status
run_terminal_command "hermes gateway setup"        # Configure platforms
```

Supported platforms: Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, Matrix, Mattermost, Home Assistant, DingTalk, Feishu, WeCom, BlueBubbles (iMessage), Weixin (WeChat), API Server, Webhooks. Open WebUI connects via the API Server adapter.

For Grok: If you have Hermes gateway running, you can interact with it via terminal or the platform. Grok itself can run similar gateway patterns via its own tools.

#### Sessions

```pwsh
run_terminal_command "hermes sessions list"        # List recent sessions
run_terminal_command "hermes sessions browse"      # Interactive picker
run_terminal_command "hermes sessions export OUT"  # Export to JSONL
run_terminal_command "hermes sessions rename ID T" # Rename a session
run_terminal_command "hermes sessions delete ID"   # Delete a session
run_terminal_command "hermes sessions prune --older-than N"  # Clean up old sessions
run_terminal_command "hermes sessions stats"       # Session store statistics
```

#### Cron Jobs

```pwsh
run_terminal_command "hermes cron list"            # List jobs (--all for disabled)
run_terminal_command "hermes cron create SCHED 'prompt'"  # Create: '30m', 'every 2h', '0 9 * * *'
run_terminal_command "hermes cron edit ID"         # Edit schedule, prompt, delivery
run_terminal_command "hermes cron pause/resume ID" # Control job state
run_terminal_command "hermes cron run ID"          # Trigger on next tick
run_terminal_command "hermes cron remove ID"       # Delete a job
run_terminal_command "hermes cron status"          # Scheduler status
```

#### Webhooks

```pwsh
run_terminal_command "hermes webhook subscribe NAME"  # Create route at /webhooks/<name>
run_terminal_command "hermes webhook list"         # List subscriptions
run_terminal_command "hermes webhook remove NAME"  # Remove a subscription
run_terminal_command "hermes webhook test NAME"    # Send a test POST
```

#### Profiles

```pwsh
run_terminal_command "hermes profile list"         # List all profiles
run_terminal_command "hermes profile create NAME --clone ..."  # Create (--clone, --clone-all, --clone-from)
run_terminal_command "hermes profile use NAME"     # Set sticky default
run_terminal_command "hermes profile delete NAME"  # Delete a profile
run_terminal_command "hermes profile show NAME"    # Show details
run_terminal_command "hermes profile alias NAME"   # Manage wrapper scripts
run_terminal_command "hermes profile rename A B"   # Rename a profile
run_terminal_command "hermes profile export NAME"  # Export to tar.gz
run_terminal_command "hermes profile import FILE"  # Import from archive
```

#### Credential Pools

```pwsh
run_terminal_command "hermes auth add"             # Interactive credential wizard
run_terminal_command "hermes auth list [PROVIDER]" # List pooled credentials
run_terminal_command "hermes auth remove P INDEX"  # Remove by provider + index
run_terminal_command "hermes auth reset PROVIDER"  # Clear exhaustion status
```

Use `1password` skill to securely manage the actual keys/tokens referenced here.

#### Other

```pwsh
run_terminal_command "hermes insights [--days N]"  # Usage analytics
run_terminal_command "hermes update"               # Update to latest version
run_terminal_command "hermes pairing list/approve/revoke"  # DM authorization
run_terminal_command "hermes plugins list/install/remove"  # Plugin management
run_terminal_command "hermes honcho setup/status"  # Honcho memory integration
run_terminal_command "hermes memory setup/status/off"  # Memory provider config
run_terminal_command "hermes completion bash|zsh"  # Shell completions
run_terminal_command "hermes acp"                  # ACP server (IDE integration)
run_terminal_command "hermes claw migrate"         # Migrate from OpenClaw
run_terminal_command "hermes uninstall"            # Uninstall Hermes
```

### Slash Commands (In-Session)

Type these during an interactive chat session (via run_terminal_command "hermes" or equivalent). New commands land fairly often; if something below looks stale, run `/help` in-session.

#### Session Control
```
/new (/reset)        Fresh session
/clear               Clear screen + new session (CLI)
/retry               Resend last message
/undo                Remove last exchange
/title [name]        Name the session
/compress            Manually compress context
/stop                Kill background processes
/rollback [N]        Restore filesystem checkpoint
/snapshot [sub]      Create or restore state snapshots of Hermes config/state (CLI)
/background <prompt> Run prompt in background
/queue <prompt>      Queue for next turn
/steer <prompt>      Inject a message after the next tool call without interrupting
/agents (/tasks)     Show active agents and running tasks
/resume [name]       Resume a named session
/goal [text|sub]     Set a standing goal Hermes works on across turns until achieved
                     (subcommands: status, pause, resume, clear)
/redraw              Force a full UI repaint (CLI)
```

#### Configuration
```
/config              Show config (CLI)
/model [name]        Show or change model
/personality [name]  Set personality
/reasoning [level]   Set reasoning (none|minimal|low|medium|high|xhigh|show|hide)
/verbose             Cycle: off → new → all → verbose
/voice [on|off|tts]  Voice mode
/yolo                Toggle approval bypass
/busy [sub]          Control what Enter does while Hermes is working (CLI)
                     (subcommands: queue, steer, interrupt, status)
/indicator [style]   Pick the TUI busy-indicator style (CLI)
                     (styles: kaomoji, emoji, unicode, ascii)
/footer [on|off]     Toggle gateway runtime-metadata footer on final replies
/skin [name]         Change theme (CLI)
/statusbar           Toggle status bar (CLI)
```

#### Tools & Skills
```
/tools               Manage tools (CLI)
/toolsets            List toolsets (CLI)
/skills              Search/install skills (CLI)
/skill <name>        Load a skill into session
/reload-skills       Re-scan ~/.hermes/skills/ for added/removed skills
/reload              Reload .env variables into the running session (CLI)
/reload-mcp          Reload MCP servers
/cron                Manage cron jobs (CLI)
/curator [sub]       Background skill maintenance (status, run, pin, archive, …)
/kanban [sub]        Multi-profile collaboration board (tasks, links, comments)
/plugins             List plugins (CLI)
```

#### Gateway
```
/approve             Approve a pending command (gateway)
/deny                Deny a pending command (gateway)
/restart             Restart gateway (gateway)
/sethome             Set current chat as home channel (gateway)
/update              Update Hermes to latest (gateway)
/topic [sub]         Enable or inspect Telegram DM topic sessions (gateway)
/platforms (/gateway) Show platform connection status (gateway)
```

#### Utility
```
/branch (/fork)      Branch the current session
/fast                Toggle priority/fast processing
/browser             Open CDP browser connection
/history             Show conversation history (CLI)
/save                Save conversation to file (CLI)
/copy [N]            Copy the last assistant response to clipboard (CLI)
/paste               Attach clipboard image (CLI)
/image               Attach local image file (CLI)
```

#### Info
```
/help                Show commands
/commands [page]     Browse all commands (gateway)
/usage               Token usage
/insights [days]     Usage analytics
/gquota              Show Google Gemini Code Assist quota usage (CLI)
/status              Session info (gateway)
/profile             Active profile info
/debug               Upload debug report (system info + logs) and get shareable links
```

#### Exit
```
/quit (/exit, /q)    Exit CLI
```

### Key Paths & Config (Grok note: use run_terminal_command "hermes config path" etc.)

```
~/.hermes/config.yaml       Main configuration
~/.hermes/.env              API keys and secrets (under $HERMES_HOME if set)
$HERMES_HOME/skills/        Installed skills (Grok can read these for cross-porting)
~/.hermes/sessions/         Gateway routing index, request dumps, *.jsonl transcripts
~/.hermes/state.db          Canonical session store (SQLite + FTS5)
~/.hermes/logs/             Gateway and error logs
~/.hermes/auth.json         OAuth tokens and credential pools
~/.hermes/hermes-agent/     Source code (if git-installed)
```

Profiles use `~/.hermes/profiles/<name>/` with the same layout.

For Grok: Manage these files with `write`, `read_file`, `search_replace`. Use `1password` for .env secrets.

#### Config Sections

Edit with `hermes config edit` or `hermes config set section.key value` (via terminal), or directly with Grok file tools.

| Section | Key options |
|---------|-------------|
| `model` | `default`, `provider`, `base_url`, `api_key`, `context_length` |
| `agent` | `max_turns` (90), `tool_use_enforcement` |
| `terminal` | `backend` (local/docker/ssh/modal), `cwd`, `timeout` (180) |
| `compression` | `enabled`, `threshold` (0.50), `target_ratio` (0.20) |
| `display` | `skin`, `tool_progress`, `show_reasoning`, `show_cost` |
| `stt` | `enabled`, `provider` (local/groq/openai/mistral) |
| `tts` | `provider` (edge/elevenlabs/openai/minimax/mistral/neutts) |
| `memory` | `memory_enabled`, `user_profile_enabled`, `provider` |
| `security` | `tirith_enabled`, `website_blocklist` |
| `delegation` | `model`, `provider`, `base_url`, `api_key`, `max_iterations` (50), `reasoning_effort` |
| `checkpoints` | `enabled`, `max_snapshots` (50) |

Full config reference: https://hermes-agent.nousresearch.com/docs/user-guide/configuration

#### Providers

20+ providers supported. Set via `hermes model` or `hermes setup`.

| Provider | Auth | Key env var |
|----------|------|-------------|
| OpenRouter | API key | `OPENROUTER_API_KEY` |
| Anthropic | API key | `ANTHROPIC_API_KEY` |
| Nous Portal | OAuth | `hermes auth` |
| OpenAI Codex | OAuth | `hermes auth` |
| GitHub Copilot | Token | `COPILOT_GITHUB_TOKEN` |
| Google Gemini | API key | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| DeepSeek | API key | `DEEPSEEK_API_KEY` |
| xAI / Grok | API key | `XAI_API_KEY` |
| Hugging Face | Token | `HF_TOKEN` |
| Z.AI / GLM | API key | `GLM_API_KEY` |
| MiniMax | API key | `MINIMAX_API_KEY` |
| MiniMax CN | API key | `MINIMAX_CN_API_KEY` |
| Kimi / Moonshot | API key | `KIMI_API_KEY` |
| Alibaba / DashScope | API key | `DASHSCOPE_API_KEY` |
| Xiaomi MiMo | API key | `XIAOMI_API_KEY` |
| Kilo Code | API key | `KILOCODE_API_KEY` |
| OpenCode Zen | API key | `OPENCODE_ZEN_API_KEY` |
| OpenCode Go | API key | `OPENCODE_GO_API_KEY` |
| Qwen OAuth | OAuth | `hermes auth add qwen-oauth` |
| Custom endpoint | Config | `model.base_url` + `model.api_key` in config.yaml |
| GitHub Copilot ACP | External | `COPILOT_CLI_PATH` or Copilot CLI |

Full provider docs: https://hermes-agent.nousresearch.com/docs/integrations/providers

**Grok note:** xAI/Grok is directly supported as a provider. Use `XAI_API_KEY` and set via `hermes model` or config. Grok Build can also run Hermes with Grok as the backend.

#### Toolsets

Enable/disable via `hermes tools` (interactive) or `hermes tools enable/disable NAME`.

| Toolset | What it provides |
|---------|------------------|
| `web` | Web search and content extraction |
| `search` | Web search only (subset of `web`) |
| `browser` | Browser automation (Browserbase, Camofox, or local Chromium) |
| `terminal` | Shell commands and process management |
| `file` | File read/write/search/patch |
| `code_execution` | Sandboxed Python execution |
| `vision` | Image analysis |
| `image_gen` | AI image generation |
| `video` | Video analysis and generation |
| `tts` | Text-to-speech |
| `skills` | Skill browsing and management |
| `memory` | Persistent cross-session memory |
| `session_search` | Search past conversations |
| `delegation` | Subagent task delegation |
| `cronjob` | Scheduled task management |
| `clarify` | Ask user clarifying questions |
| `messaging` | Cross-platform message sending |
| `todo` | In-session task planning and tracking |
| `kanban` | Multi-agent work-queue tools (gated to workers) |
| `debugging` | Extra introspection/debug tools (off by default) |
| `safe` | Minimal, low-risk toolset for locked-down sessions |
| `spotify` | Spotify playback and playlist control |
| `homeassistant` | Smart home control (off by default) |
| `discord` | Discord integration tools |
| `discord_admin` | Discord admin/moderation tools |
| `feishu_doc` | Feishu (Lark) document tools |
| `feishu_drive` | Feishu (Lark) drive tools |
| `yuanbao` | Yuanbao integration tools |
| `rl` | Reinforcement learning tools (off by default) |
| `moa` | Mixture of Agents (off by default) |

Full enumeration lives in `toolsets.py` as the `TOOLSETS` dict; `_HERMES_CORE_TOOLS` is the default bundle most platforms inherit from.

Tool changes take effect on `/reset` (new session). They do NOT apply mid-conversation to preserve prompt caching.

**Grok note:** Many of these toolsets map to Grok tools (web_fetch/open_page for web, run_terminal_command for terminal, read_file/write/search_replace for file, image_gen for image_gen, etc.). When running Hermes via terminal in Grok, the Hermes tools layer on top.

### Security & Privacy Toggles

Common "why is Hermes doing X to my output / tool calls / commands?" toggles — and the exact commands to change them. Most of these need a fresh session (`/reset` in chat, or start a new `hermes` invocation) because they're read once at startup.

#### Secret redaction in tool output

Secret redaction is **on by default** — tool output (terminal stdout, `read_file`, web content, subagent summaries, etc.) is scanned for strings that look like API keys, tokens, and secrets before it enters the conversation context and logs. Leave it enabled for normal use:

```bash
hermes config set security.redact_secrets true       # keep enabled globally
```

**Restart required.** `security.redact_secrets` is snapshotted at import time — toggling it mid-session will NOT take effect for the running process. Tell the user to change it in config from a terminal, then start a new session. This is deliberate — it prevents an LLM from flipping the toggle on itself mid-task.

Disable only when you deliberately need raw credential-like strings for debugging or redactor development:

```bash
hermes config set security.redact_secrets false
```

#### PII redaction in gateway messages

Separate from secret redaction. When enabled, the gateway hashes user IDs and strips phone numbers from the session context before it reaches the model:

```bash
hermes config set privacy.redact_pii true    # enable
hermes config set privacy.redact_pii false   # disable (default)
```

#### Command approval prompts

By default (`approvals.mode: manual`), Hermes prompts the user before running shell commands flagged as destructive (`rm -rf`, `git reset --hard`, etc.). The modes are:

- `manual` — always prompt (default)
- `smart` — use an auxiliary LLM to auto-approve low-risk commands, prompt on high-risk
- `off` — skip all approval prompts (equivalent to `--yolo`)

```bash
hermes config set approvals.mode smart       # recommended middle ground
hermes config set approvals.mode off         # bypass everything (not recommended)
```

Per-invocation bypass without changing config:
- `hermes --yolo …`
- `export HERMES_YOLO_MODE=1`

Note: YOLO / `approvals.mode: off` does NOT turn off secret redaction. They are independent.

#### Shell hooks allowlist

Some shell-hook integrations require explicit allowlisting before they fire. Managed via `~/.hermes/shell-hooks-allowlist.json` — prompted interactively the first time a hook wants to run.

#### Disabling the web/browser/image-gen tools

To keep the model away from network or media tools entirely, open `hermes tools` and toggle per-platform. Takes effect on next session (`/reset`). See the Tools & Skills section above.

### Voice & Transcription

#### STT (Voice → Text)

Voice messages from messaging platforms are auto-transcribed.

Provider priority (auto-detected):
1. **Local faster-whisper** — free, no API key: `pip install faster-whisper`
2. **Groq Whisper** — free tier: set `GROQ_API_KEY`
3. **OpenAI Whisper** — paid: set `VOICE_TOOLS_OPENAI_KEY`
4. **Mistral Voxtral** — set `MISTRAL_API_KEY`

Config:
```yaml
stt:
  enabled: true
  provider: local        # local, groq, openai, mistral
  local:
    model: base          # tiny, base, small, medium, large-v3
```

#### TTS (Text → Voice)

| Provider | Env var | Free? |
|----------|---------|-------|
| Edge TTS | None | Yes (default) |
| ElevenLabs | `ELEVENLABS_API_KEY` | Free tier |
| OpenAI | `VOICE_TOOLS_OPENAI_KEY` | Paid |
| MiniMax | `MINIMAX_API_KEY` | Paid |
| Mistral (Voxtral) | `MISTRAL_API_KEY` | Paid |
| NeuTTS (local) | None (`pip install neutts[all]` + `espeak-ng`) | Free |

Voice commands: `/voice on` (voice-to-voice), `/voice tts` (always voice), `/voice off`.

### Spawning Additional Hermes Instances (Grok-adapted)

Run additional Hermes processes as fully independent subprocesses — separate sessions, tools, and environments.

#### When to Use This vs delegate_task

| | `delegate_task` | Spawning `hermes` process |
|-|-----------------|--------------------------|
| Isolation | Separate conversation, shared process | Fully independent process |
| Duration | Minutes (bounded by parent loop) | Hours/days |
| Tool access | Subset of parent's tools | Full tool access |
| Interactive | No | Yes (PTY mode via background) |
| Use case | Quick parallel subtasks | Long autonomous missions |

#### One-Shot Mode

```pwsh
run_terminal_command "hermes chat -q 'Research GRPO papers and write summary to ~/research/grpo.md'" timeout=300

## Background for long tasks:
run_terminal_command "hermes chat -q 'Set up CI/CD for ~/myapp'" background=true
```

#### Interactive PTY Mode (via tmux or Grok background)

Hermes uses prompt_toolkit, which requires a real terminal. Use tmux for interactive spawning if needed, or rely on Grok's run_terminal_command background mode + follow-ups.

```pwsh
## Start (example with tmux for full TUI if Grok terminal needs it)
run_terminal_command "tmux new-session -d -s agent1 -x 120 -y 40 'hermes'" timeout=10

## Wait for startup, then send a message
run_terminal_command "sleep 8 && tmux send-keys -t agent1 'Build a FastAPI auth service' Enter" timeout=15

## Read output
run_terminal_command "sleep 20 && tmux capture-pane -t agent1 -p" timeout=5

## Send follow-up
run_terminal_command "tmux send-keys -t agent1 'Add rate limiting middleware' Enter" timeout=5

## Exit
run_terminal_command "tmux send-keys -t agent1 '/exit' Enter && sleep 2 && tmux kill-session -t agent1" timeout=10
```

#### Multi-Agent Coordination

```pwsh
## Agent A: backend
run_terminal_command "tmux new-session -d -s backend -x 120 -y 40 'hermes -w'" timeout=10
run_terminal_command "sleep 8 && tmux send-keys -t backend 'Build REST API for user management' Enter" timeout=15

## Agent B: frontend
run_terminal_command "tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'" timeout=10
run_terminal_command "sleep 8 && tmux send-keys -t frontend 'Build React dashboard for user management' Enter" timeout=15

## Check progress, relay context between them
run_terminal_command "tmux capture-pane -t backend -p | tail -30" timeout=5
run_terminal_command "tmux send-keys -t frontend 'Here is the API schema from the backend agent: ...' Enter" timeout=5
```

#### Session Resume

```pwsh
## Resume most recent session
run_terminal_command "tmux new-session -d -s resumed 'hermes --continue'" timeout=10

## Resume specific session
run_terminal_command "tmux new-session -d -s resumed 'hermes --resume 20260225_143052_a1b2c3'" timeout=10
```

#### Tips

- **Prefer `delegate_task` for quick subtasks** — less overhead than spawning a full process (if using Hermes).
- **Use `-w` (worktree mode)** when spawning agents that edit code — prevents git conflicts.
- **Set timeouts** for one-shot mode — complex tasks can take 5-10 minutes.
- **Use `hermes chat -q` for fire-and-forget** — no PTY needed.
- **Use tmux for interactive sessions** — raw PTY mode has `\r` vs `\n` issues with prompt_toolkit (adapt to Grok background if possible).
- **For scheduled tasks**, use the `cronjob` tool instead of spawning — handles delivery and retry.

### Durable & Background Systems

Four systems run alongside the main conversation loop. Quick reference here; full developer notes live in `AGENTS.md`, user-facing docs under `website/docs/user-guide/features/`.

#### Delegation (`delegate_task`)

Synchronous subagent spawn — the parent waits for the child's summary before continuing its own loop. Isolated context + terminal session.

- **Single:** `delegate_task(goal, context, toolsets)`.
- **Batch:** `delegate_task(tasks=[{goal, ...}, ...])` runs children in parallel, capped by `delegation.max_concurrent_children` (default 3).
- **Roles:** `leaf` (default; cannot re-delegate) vs `orchestrator` (can spawn its own workers, bounded by `delegation.max_spawn_depth`).
- **Not durable.** If the parent is interrupted, the child is cancelled. For work that must outlive the turn, use `cronjob` or `terminal(background=True, notify_on_complete=True)` in Hermes context.

Config: `delegation.*` in `config.yaml`.

**Grok note:** Use `spawn_subagent` for similar delegation patterns in Grok Build. For Hermes-specific, run via terminal.

#### Cron (scheduled jobs)

Durable scheduler — `cron/jobs.py` + `cron/scheduler.py`. Drive it via the `cronjob` tool, the `hermes cron` CLI (`list`, `add`, `edit`, `pause`, `resume`, `run`, `remove`), or the `/cron` slash command.

- **Schedules:** duration (`"30m"`, `"2h"`), "every" phrase (`"every monday 9am"`), 5-field cron (`"0 9 * * *"`), or ISO timestamp.
- **Per-job knobs:** `skills`, `model`/`provider` override, `script` (pre-run data collection; `no_agent=True` makes the script the whole job), `context_from` (chain job A's output into job B), `workdir` (run in a specific dir with its `AGENTS.md` / `CLAUDE.md` loaded), multi-platform delivery.
- **Invariants:** 3-minute hard interrupt per run, `.tick.lock` file prevents duplicate ticks across processes, cron sessions pass `skip_memory=True` by default, and cron deliveries are framed with a header/footer instead of being mirrored into the target gateway session (keeps role alternation intact).

User docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron

#### Curator (skill lifecycle)

Background maintenance for agent-created skills. Tracks usage, marks idle skills stale, archives stale ones, keeps a pre-run tar.gz backup so nothing is lost.

- **CLI:** `hermes curator <verb>` — `status`, `run`, `pause`, `resume`, `pin`, `unpin`, `archive`, `restore`, `prune`, `backup`, `rollback`.
- **Slash:** `/curator <subcommand>` mirrors the CLI.
- **Scope:** only touches skills with `created_by: "agent"` provenance. Bundled + hub-installed skills are off-limits. **Never deletes** — max destructive action is archive. Pinned skills are exempt from every auto-transition and every LLM review pass.
- **Telemetry:** sidecar at `~/.hermes/skills/.usage.json` holds per-skill `use_count`, `view_count`, `patch_count`, `last_activity_at`, `state`, `pinned`.

Config: `curator.*` (`enabled`, `interval_hours`, `min_idle_hours`, `stale_after_days`, `archive_after_days`, `backup.*`).

User docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/curator

#### Kanban (multi-agent work queue)

Durable SQLite board for multi-profile / multi-worker collaboration. Users drive it via `hermes kanban <verb>`; dispatcher-spawned workers see a focused `kanban_*` toolset gated by `HERMES_KANBAN_TASK`, and orchestrator profiles can opt into the broader `kanban` toolset. Normal sessions still have zero `kanban_*` schema footprint unless configured.

- **CLI verbs (common):** `init`, `create`, `list` (alias `ls`), `show`, `assign`, `link`, `unlink`, `comment`, `complete`, `block`, `unblock`, `archive`, `tail`. Less common: `watch`, `stats`, `runs`, `log`, `dispatch`, `daemon`, `gc`.
- **Worker/orchestrator toolset:** `kanban_show`, `kanban_complete`, `kanban_block`, `kanban_heartbeat`, `kanban_comment`, `kanban_create`, `kanban_link`; profiles that explicitly enable the `kanban` toolset outside a dispatcher-spawned task also get `kanban_list` and `kanban_unblock` for board routing.
- **Dispatcher** runs inside the gateway by default (`kanban.dispatch_in_gateway: true`) — reclaims stale claims, promotes ready tasks, atomically claims, spawns assigned profiles. Auto-blocks a task after `failure_limit` consecutive spawn failures (default 2; configurable via `kanban.failure_limit` or per-task `max_retries`).
- **Isolation:** board is the hard boundary (workers get `HERMES_KANBAN_BOARD` pinned in env); tenant is a soft namespace within a board for workspace-path + memory-key isolation.

User docs: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban

**Grok note:** Cross-ref the ported `hermes-kanban-orchestrator` and `kanban-worker` skills for similar multi-agent patterns in Grok Build.

### Windows-Specific Quirks (keep as-is from source, highly relevant)

Hermes runs natively on Windows (PowerShell, cmd, Windows Terminal, git-bash mintty, VS Code integrated terminal). Most of it just works, but a handful of differences between Win32 and POSIX have bitten us — document new ones here as you hit them so the next person (or the next session) doesn't rediscover them from scratch.

#### Input / Keybindings

**Alt+Enter doesn't insert a newline.** Windows Terminal intercepts Alt+Enter at the terminal layer to toggle fullscreen — the keystroke never reaches prompt_toolkit. Use **Ctrl+Enter** instead. Windows Terminal delivers Ctrl+Enter as LF (`c-j`), distinct from plain Enter (`c-m` / CR), and the CLI binds `c-j` to newline insertion on `win32` only (see `_bind_prompt_submit_keys` + the Windows-only `c-j` binding in `cli.py`).

Side effect: the raw Ctrl+J keystroke also inserts a newline on Windows — unavoidable, because Windows Terminal collapses Ctrl+Enter and Ctrl+J to the same keycode at the Win32 console API layer. No conflicting binding existed for Ctrl+J on Windows, so this is a harmless side effect.

mintty / git-bash behaves the same (fullscreen on Alt+Enter) unless you disable Alt+Fn shortcuts in Options → Keys. Easier to just use Ctrl+Enter.

**Diagnosing keybindings.** Run `python scripts/keystroke_diagnostic.py` (repo root) to see exactly how prompt_toolkit identifies each keystroke in the current terminal. Answers questions like "does Shift+Enter come through as a distinct key?" (almost never — most terminals collapse it to plain Enter) or "what byte sequence is my terminal sending for Ctrl+Enter?" This is how the Ctrl+Enter = c-j fact was established.

#### Config / Files

**HTTP 400 "No models provided" on first run.** `config.yaml` was saved with a UTF-8 BOM (common when Windows apps write it). Re-save as UTF-8 without BOM. `hermes config edit` writes without BOM; manual edits in Notepad are the usual culprit.

#### `execute_code` / Sandbox

**WinError 10106** ("The requested service provider could not be loaded or initialized") from the sandbox child process — it can't create an `AF_INET` socket, so the loopback-TCP RPC fallback fails before `connect()`. Root cause is usually **not** a broken Winsock LSP; it's Hermes's own env scrubber dropping `SYSTEMROOT` / `WINDIR` / `COMSPEC` from the child env. Python's `socket` module needs `SYSTEMROOT` to locate `mswsock.dll`. Fixed via the `_WINDOWS_ESSENTIAL_ENV_VARS` allowlist in `tools/code_execution_tool.py`. If you still hit it, echo `os.environ` inside an `execute_code` block to confirm `SYSTEMROOT` is set. Full diagnostic recipe in `references/execute-code-sandbox-env-windows.md`.

#### Testing / Contributing

**`scripts/run_tests.sh` doesn't work as-is on Windows** — it looks for POSIX venv layouts (`.venv/bin/activate`). The Hermes-installed venv at `venv/Scripts/` has no pip or pytest either (stripped for install size). Workaround: install `pytest + pytest-xdist + pyyaml` into a system Python 3.11 user site, then invoke pytest directly with `PYTHONPATH` set:

```bash
"/c/Program Files/Python311/python" -m pip install --user pytest pytest-xdist pyyaml
export PYTHONPATH="$(pwd)"
"/c/Program Files/Python311/python" -m pytest tests/foo/test_bar.py -v --tb=short -n 0
```

Use `-n 0`, not `-n 4` — `pyproject.toml`'s default `addopts` already includes `-n`, and the wrapper's CI-parity guarantees don't apply off POSIX.

**POSIX-only tests need skip guards.** Common markers already in the codebase:
- Symlinks — elevated privileges on Windows
- `0o600` file modes — POSIX mode bits not enforced on NTFS by default
- `signal.SIGALRM` — Unix-only (see `tests/conftest.py::_enforce_test_timeout`)
- Winsock / Windows-specific regressions — `@pytest.mark.skipif(sys.platform != "win32", ...)`

Use the existing skip-pattern style (`sys.platform == "win32"`) to stay consistent with the rest of the suite.

#### Path / Filesystem

**Line endings.** Git may warn `LF will be replaced by CRLF the next time Git touches it`. Cosmetic — the repo's `.gitattributes` normalizes. Don't let editors auto-convert committed POSIX-newline files to CRLF.

**Forward slashes work almost everywhere.** `C:/Users/...` is accepted by every Hermes tool and most Windows APIs. Prefer forward slashes in code and logs — avoids shell-escaping backslashes in bash.

### Troubleshooting (Grok note: run all via `run_terminal_command "hermes ..."` or equivalent file reads)

#### Voice not working
1. Check `stt.enabled: true` in config.yaml
2. Verify provider: `pip install faster-whisper` or set API key
3. In gateway: `/restart`. In CLI: exit and relaunch.

#### Tool not available
1. `hermes tools` — check if toolset is enabled for your platform
2. Some tools need env vars (check `.env`)
3. `/reset` after enabling tools

#### Model/provider issues
1. `hermes doctor` — check config and dependencies
2. `hermes auth` — re-authenticate OAuth providers (or `hermes auth add <provider>`)
3. Check `.env` has the right API key
4. **Copilot 403**: `gh auth login` tokens do NOT work for Copilot API. You must use the Copilot-specific OAuth device code flow via `hermes model` → GitHub Copilot.

#### Changes not taking effect
- **Tools/skills:** `/reset` starts a new session with updated toolset
- **Config changes:** In gateway: `/restart`. In CLI: exit and relaunch.
- **Code changes:** Restart the CLI or gateway process

#### Skills not showing
1. `hermes skills list` — verify installed
2. `hermes skills config` — check platform enablement
3. Load explicitly: `/skill name` or `hermes -s name`

#### Gateway issues
Check logs first:
```bash
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20
```

Common gateway problems:
- **Gateway dies on SSH logout**: Enable linger: `sudo loginctl enable-linger $USER`
- **Gateway dies on WSL2 close**: WSL2 requires `systemd=true` in `/etc/wsl.conf` for systemd services to work. Without it, gateway falls back to `nohup` (dies when session closes).
- **Gateway crash loop**: Reset the failed state: `systemctl --user reset-failed hermes-gateway`

#### Platform-specific issues
- **Discord bot silent**: Must enable **Message Content Intent** in Bot → Privileged Gateway Intents.
- **Slack bot only works in DMs**: Must subscribe to `message.channels` event. Without it, the bot ignores public channels.
- **Windows-specific issues** (`Alt+Enter` newline, WinError 10106, UTF-8 BOM config, test suite, line endings): see the dedicated **Windows-Specific Quirks** section above.

#### Auxiliary models not working
If `auxiliary` tasks (vision, compression, session_search) fail silently, the `auto` provider can't find a backend. Either set `OPENROUTER_API_KEY` or `GOOGLE_API_KEY`, or explicitly configure each auxiliary task's provider:
```bash
hermes config set auxiliary.vision.provider <your_provider>
hermes config set auxiliary.vision.model <model_name>
```

### Where to Find Things

| Looking for... | Location |
|----------------|----------|
| Config options | `hermes config edit` or [Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration) |
| Available tools | `hermes tools list` or [Tools reference](https://hermes-agent.nousresearch.com/docs/reference/tools-reference) |
| Slash commands | `/help` in session or [Slash commands reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands) |
| Skills catalog | `hermes skills browse` or [Skills catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) |
| Provider setup | `hermes model` or [Providers guide](https://hermes-agent.nousresearch.com/docs/integrations/providers) |
| Platform setup | `hermes gateway setup` or [Messaging docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) |
| MCP servers | `hermes mcp list` or [MCP guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) |
| Profiles | `hermes profile list` or [Profiles docs](https://hermes-agent.nousresearch.com/docs/user-guide/profiles) |
| Cron jobs | `hermes cron list` or [Cron docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) |
| Memory | `hermes memory status` or [Memory docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) |
| Env variables | `hermes config env-path` or [Env vars reference](https://hermes-agent.nousresearch.com/docs/reference/environment-variables) |
| CLI commands | `hermes --help` or [CLI reference](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) |
| Gateway logs | `~/.hermes/logs/gateway.log` |
| Session files | `hermes sessions browse` (reads state.db) |
| Source code | `~/.hermes/hermes-agent/` |

### Contributor Quick Reference

For occasional contributors and PR authors. Full developer docs: https://hermes-agent.nousresearch.com/docs/developer-guide/

#### Project Layout

```
hermes-agent/
├── run_agent.py          # AIAgent — core conversation loop
├── model_tools.py        # Tool discovery and dispatch
├── toolsets.py           # Toolset definitions
├── cli.py                # Interactive CLI (HermesCLI)
├── hermes_state.py       # SQLite session store
├── agent/                # Prompt builder, context compression, memory, model routing, credential pooling, skill dispatch
├── hermes_cli/           # CLI subcommands, config, setup, commands
│   ├── commands.py       # Slash command registry (CommandDef)
│   ├── config.py         # DEFAULT_CONFIG, env var definitions
│   └── main.py           # CLI entry point and argparse
├── tools/                # One file per tool
│   └── registry.py       # Central tool registry
├── gateway/              # Messaging gateway
│   └── platforms/        # Platform adapters (telegram, discord, etc.)
├── cron/                 # Job scheduler
├── tests/                # ~3000 pytest tests
└── website/              # Docusaurus docs site
```

Config: `~/.hermes/config.yaml` (settings), `~/.hermes/.env` (API keys) — both under `$HERMES_HOME` when it is set.

#### Adding a Tool (3 files)

**1. Create `tools/your_tool.py`:** (use `write` tool in Grok to create the file)

```python
import json, os
from tools.registry import registry

def check_requirements() -> bool:
    return bool(os.getenv("EXAMPLE_API_KEY"))

def example_tool(param: str, task_id: str = None) -> str:
    return json.dumps({"success": True, "data": "..."})

registry.register(
    name="example_tool",
    toolset="example",
    schema={"name": "example_tool", "description": "...", "parameters": {...}},
    handler=lambda args, **kw: example_tool(
        param=args.get("param", ""), task_id=kw.get("task_id")),
    check_fn=check_requirements,
    requires_env=["EXAMPLE_API_KEY"],
)
```

**2. Add to `toolsets.py`** → `_HERMES_CORE_TOOLS` list.

Auto-discovery: any `tools/*.py` file with a top-level `registry.register()` call is imported automatically — no manual list needed.

All handlers must return JSON strings. Use `get_hermes_home()` for paths, never hardcode `~/.hermes`.

#### Adding a Slash Command

1. Add `CommandDef` to `COMMAND_REGISTRY` in `hermes_cli/commands.py`
2. Add handler in `cli.py` → `process_command()`
3. (Optional) Add gateway handler in `gateway/run.py`

All consumers (help text, autocomplete, Telegram menu, Slack mapping) derive from the central registry automatically.

#### Agent Loop (High Level)

```
run_conversation():
  1. Build system prompt
  2. Loop while iterations < max:
     a. Call LLM (OpenAI-format messages + tool schemas)
     b. If tool_calls → dispatch each via handle_function_call() → append results → continue
     c. If text response → return
  3. Context compression triggers automatically near token limit
```

#### Testing

```bash
python -m pytest tests/ -o 'addopts=' -q   # Full suite
python -m pytest tests/tools/ -q            # Specific area
```

- Tests auto-redirect `HERMES_HOME` to temp dirs — never touch real `~/.hermes/`
- Run full suite before pushing any change
- Use `-o 'addopts='` to clear any baked-in pytest flags

**Windows contributors:** `scripts/run_tests.sh` currently looks for POSIX venvs (`.venv/bin/activate` / `venv/bin/activate`) and will error out on Windows where the layout is `venv/Scripts/activate` + `python.exe`. The Hermes-installed venv at `venv/Scripts/` also has no `pip` or `pytest` — it's stripped for end-user install size. Workaround: install pytest + pytest-xdist + pyyaml into a system Python 3.11 user site (`/c/Program Files/Python311/python -m pip install --user pytest pytest-xdist pyyaml`), then run tests directly:

```bash
export PYTHONPATH="$(pwd)"
"/c/Program Files/Python311/python" -m pytest tests/tools/test_foo.py -v --tb=short -n 0
```

Use `-n 0` (not `-n 4`) because `pyproject.toml`'s default `addopts` already includes `-n`, and the wrapper's CI-parity story doesn't apply off-POSIX.

**Cross-platform test guards:** tests that use POSIX-only syscalls need a skip marker. Common ones already in the codebase:
- Symlink creation → `@pytest.mark.skipif(sys.platform == "win32", reason="Symlinks require elevated privileges on Windows")` (see `tests/cron/test_cron_script.py`)
- POSIX file modes (0o600, etc.) → `@pytest.mark.skipif(sys.platform.startswith("win"), reason="POSIX mode bits not enforced on Windows")` (see `tests/hermes_cli/test_auth_toctou_file_modes.py`)
- `signal.SIGALRM` → Unix-only (see `tests/conftest.py::_enforce_test_timeout`)
- Live Winsock / Windows-specific regression tests → `@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific regression")`

**Monkeypatching `sys.platform` is not enough** when the code under test also calls `platform.system()` / `platform.release()` / `platform.mac_ver()`. Those functions re-read the real OS independently, so a test that sets `sys.platform = "linux"` on a Windows runner will still see `platform.system() == "Windows"` and route through the Windows branch. Patch all three together:

```python
monkeypatch.setattr(sys, "platform", "linux")
monkeypatch.setattr(platform, "system", lambda: "Linux")
monkeypatch.setattr(platform, "release", lambda: "6.8.0-generic")
```

See `tests/agent/test_prompt_builder.py::TestEnvironmentHints` for a worked example.

#### Extending the system prompt's execution-environment block

Factual guidance about the host OS, user home, cwd, terminal backend, and shell (bash vs. PowerShell on Windows) is emitted from `agent/prompt_builder.py::build_environment_hints()`. This is also where the WSL hint and per-backend probe logic live. The convention:
- **Local terminal backend** → emit host info (OS, `$HOME`, cwd) + Windows-specific notes (hostname ≠ username, `terminal` uses bash not PowerShell).
- **Remote terminal backend** (anything in `_REMOTE_TERMINAL_BACKENDS`: `docker, singularity, modal, daytona, ssh, managed_modal`) → **suppress** host info entirely and describe only the backend. A live `uname`/`whoami`/`pwd` probe runs inside the backend via `tools.environments.get_environment(...).execute(...)`, cached per process in `_BACKEND_PROBE_CACHE`, with a static fallback if the probe times out.
- **Key fact for prompt authoring:** when `TERMINAL_ENV != "local"`, *every* file tool (`read_file`, `write_file`, `patch`, `search_files`) runs inside the backend container, not on the host. The system prompt must never describe the host in that case — the agent can't touch it.

Full design notes, the exact emitted strings, and testing pitfalls:
`references/prompt-builder-environment-hints.md`.

**Refactor-safety pattern (POSIX-equivalence guard):** when you extract inline logic into a helper that adds Windows/platform-specific behavior, keep a `_legacy_<name>` oracle function in the test file that's a verbatim copy of the old code, then parametrize-diff against it. Example: `tests/tools/test_code_execution_windows_env.py::TestPosixEquivalence`. This locks in the invariant that POSIX behavior is bit-for-bit identical and makes any future drift fail loudly with a clear diff.

#### Commit Conventions

```
type: concise subject line

Optional body.
```

Types: `fix:`, `feat:`, `refactor:`, `docs:`, `chore:`

#### Key Rules

- **Never break prompt caching** — don't change context, tools, or system prompt mid-conversation
- **Message role alternation** — never two assistant or two user messages in a row
- Use `get_hermes_home()` from `hermes_constants` for all paths (profile-safe)
- Config values go in `config.yaml`, secrets go in `.env`
- New tools need a `check_fn` so they only appear when requirements are met

---

### Grok Build Tool Mapping & Adaptation

- **All Hermes CLI commands**: Execute via `run_terminal_command "hermes ..."` (pwsh compatible). For long-running or interactive: use `background=true` and follow up with additional calls to monitor/poll/send input/kill.
- **Spawning additional agents**: Use `run_terminal_command` with `background=true`, `workdir`, `timeout`. For full TUI interactivity, combine with tmux if needed (as in the source), or rely on Grok terminal's background + capture capabilities. Use git worktrees (`run_terminal_command "git worktree add ... "`) for isolated parallel agents (cross-ref `claude-code`, `codex`, `opencode` ports for the same pattern).
- **Configs, .env, skills, sessions**: Manage files with `read_file`, `write`, `search_replace`. Use `1password` skill to inject secrets into .env or env vars before running hermes commands (e.g., `$env:OPENROUTER_API_KEY = (op read ...)`).
- **Skills**: Hermes skills are Markdown files (many already ported to Grok's `~/.grok/skills/`). You can install Hermes skills via the CLI if you have Hermes, or directly use/adapt the Grok-ported versions. For cross-loading, the format is similar.
- **MCP**: See the dedicated `hermes-mcp-ecosystem` skill (ported). Run MCP-related hermes commands via terminal.
- **Gateway / messaging**: If you have the Hermes gateway installed, control it via `run_terminal_command "hermes gateway ..."`. For similar multi-platform in Grok, look at available messaging patterns or build via terminal scripts.
- **Cron / scheduled**: Use `run_terminal_command "hermes cron ..."` or the `cronjob` tool if available in Hermes. For Grok-native, use external schedulers + terminal.
- **Kanban / multi-agent**: Cross-ref the ported `hermes-kanban-orchestrator` and `kanban-worker` skills for Grok-native implementation of similar durable work queues.
- **Curator / skill lifecycle**: Hermes-specific; in Grok, use `todo_write` for task tracking and manual curation of skills in `~/.grok/skills/`.
- **Windows/pwsh**: The source's detailed quirks section is directly applicable — keep it. Use pwsh syntax in all `run_terminal_command` calls. For tests/contributing to Hermes while using Grok, follow the Windows notes (e.g., pytest via system Python, skip guards).
- **Delegation & sub-agents**: In Hermes context, use the CLI. In pure Grok, use `spawn_subagent` tool for parallel sub-agents (see Grok's delegation patterns).
- **Verification**: After any hermes command or spawn, capture output with follow-up terminal calls, inspect files with `read_file`, test changes with `run_terminal_command "git diff"`, etc.
- **No direct "hermes" MCP in Grok by default**: If needed, install Hermes and run its MCP server via terminal, or use Grok's native tools + ported skills.

### Pitfalls & Windows Notes (from source, adapted)

See the full "Windows-Specific Quirks" and "Troubleshooting" sections above — they are copied faithfully as they are highly relevant when running Hermes (or contributing to it) from a Windows/Grok environment.

Key recurring ones:
- Restart required for many config/tool changes (`/reset` or new hermes invocation).
- Secret redaction is always on unless explicitly disabled in config (and restarted).
- Subscriptions/renewals, gateway linger on Windows/WSL.
- PATH/binary resolution for hermes/opencode/etc.
- Git worktrees for safe parallel edits.
- Use `1password` for all keys to avoid .env leaks.

### Verification Checklist

- [ ] `hermes doctor` / `hermes status` passes.
- [ ] Auth providers listed and tokens healthy.
- [ ] Tools/skills enabled as expected (check with `hermes tools list`, `hermes skills list`).
- [ ] New session (`hermes chat` or `/reset`) picks up changes.
- [ ] For spawns: isolated workdirs, git status clean, outputs captured.
- [ ] Windows: forward slashes, no BOM in configs, correct pytest skips if contributing.
- [ ] Security: redaction active, approvals mode appropriate, no leaked secrets in logs.

### Post-Execution

- Deliver exact `run_terminal_command` invocations used + their outputs.
- For config/skills changes: the files written/edited via `write`/`search_replace`, and the hermes commands to reload.
- For spawns/parallel agents: the worktree paths, session IDs, and summarized outcomes (files changed, commits, PRs).
- Provide any helper scripts written (e.g., tmux wrappers, batch spawners).
- Suggest next: install a specific Hermes skill via CLI, spawn a long-running agent for a task, set up a cron for maintenance, or contribute a new tool/skill back to Hermes (using the contributor section).
- Log patterns to lessons (e.g., "worktree + background spawn for isolated feature work; always follow with github-pr-workflow").
- Confidence: on successful setup/spawn/operation + any manual steps the user still needs (e.g., Azure consents for gateway, tmux install, specific provider keys).

This is a high-fidelity, comprehensive port of the Hermes hermes-agent (meta) skill. The CLI surface, slash commands, config, tools/skills/MCP/gateway/cron/kanban/curator details, spawning patterns, Windows quirks, troubleshooting, and contributor guide are preserved as faithfully as possible. Only the execution mechanics and integration points were adapted to Grok Build's `run_terminal_command`, `write`/`search_replace`/`read_file`, `1password`, `spawn_subagent`, background jobs, and the ecosystem of already-ported skills (claude-code, codex, opencode, github-*, mcp, kanban, etc.).

Hermes Agent is the "source of truth" for many of the skills we've ported — this meta-skill lets you run the original Hermes CLI/tools directly from Grok when you have it installed, while using the Grok-native ports for day-to-day work. Perfect for users who want the best of both (Grok's native capabilities + Hermes' extensible gateway/skills ecosystem).

Install Hermes if you haven't (via the quick start), manage secrets with 1password, use worktrees for safety, and treat `run_terminal_command "hermes ..."` as your bridge. For pure Grok flows, lean on the ported equivalents.

**Never break prompt caching in Hermes sessions. Always use git worktrees for parallel edits. Restart after tool/config changes. Verify with doctor/status. Log everything useful.**

Continue the sweep for any remaining unported items in .hermes or other locations (e.g., specific sub-skills in bevy, android, or custom giga ones not yet covered). The exhaustive one-by-one porting is well underway — many dozens completed with high fidelity. 

If a specific remaining skill or category is next, provide the path and I'll read/port it immediately.


---

## Module 3: `hermes-agent-skill-authoring`

- **Origine :** `02_Grok_Hermes_Skills\hermes-agent-skill-authoring\SKILL.md`
- **Rôle / Objectif :** >

## hermes-agent-skill-authoring — How to Write Great Skills

This skill exists so that when you (or an agent) create new skills, they are **actually usable** by agents: clear triggers, focused scope, strong examples, explicit gates, good references, and testable where possible.

### Skill Anatomy (the ideal structure)

A good skill usually contains most or all of these:

- **Frontmatter / Metadata** (YAML block at the top)
  - `name`, `description`, `version`, `author`, `license`
  - `tags`, `related_skills`, `category`
  - `triggers` / `negative_triggers` (what user language should activate or avoid this skill)
  - Any execution hints (temperature, max tokens, required toolsets, etc.)

- **Core Description / When to Use**
  - Clear one-paragraph (or short) explanation of the skill's purpose.
  - Explicit "use this when..." and "do not use this when..." lists.

- **Prerequisites / Setup**
  - What the environment or user must have (auth, tools, permissions, specific skills loaded first).

- **Main Content / Phases / Playbook**
  - The actual instructions, broken into clear, numbered or named phases/steps.
  - For each step: inputs, outputs, principles, quality gates, common pitfalls, code/examples.
  - Strong preference for **concrete, copy-pasteable** examples over vague advice.

- **Quality Gates / Checklists** (very important)
  - Explicit, machine- or human-checkable lists of what "done" looks like for this skill.
  - These are what prevent the skill from producing sloppy output.

- **References / Further Reading**
  - Links or local `references/` files (official docs, papers, good examples, "why we do it this way").

- **Scripts / Tooling** (when relevant)
  - Small, focused helper scripts that the skill can invoke (or that the user can run).
  - Clear usage and expected outputs.

- **Tests / Validation** (when relevant)
  - For skills that produce code, artifacts, or decisions that can be automatically or semi-automatically checked.

- **Integration Notes**
  - How this skill is meant to be combined with others (handoff points, shared context, common patterns).

### Writing Principles (enforce these when authoring)

- **Small and focused** — A skill should do one thing well. If it has 15 unrelated phases, it probably wants to be several skills + an orchestrator.
- **Trigger-driven** — Good `triggers` make the right skill activate at the right time. Negative triggers prevent misuse.
- **Gates over vibes** — Prefer explicit checklists and verifiable criteria ("exactly 3 taglines, 5-8 words each") over "make it good."
- **Copy-paste friendly** — The consumer of the skill (human or agent) should be able to take the examples and run with them with minimal rewriting.
- **Versioned & dated** — Skills move with their underlying platforms (Bevy versions, Android API levels, Godot 4 changes, etc.). Note the versions they target.
- **Composable** — Design so that higher-level skills (giga-*, research-paper-writing, etc.) can call or depend on lower-level ones cleanly.
- **Honest about limitations** — Say what the skill does **not** do, or where it needs human review.

### Anatomy of a Great SKILL.md (for Grok Build)

When writing for this environment:

- Frontmatter with `name`, `description`, `metadata.short-description`, `tags`, `related`.
- Clear "When to Use" and "Usage in Grok Build" sections (how the user invokes it and what I will actually do with Grok tools).
- Explicit mapping from the skill's steps to Grok capabilities (`read_file`, `write`, `run_terminal_command`, `grep`, `spawn_subagent`, `web_search`, image tools, etc.).
- Quality gates written so they can be checked in a Grok session (run this command, inspect that file, produce this table, etc.).
- "Post-execution" or handoff steps where relevant (log to lessons, version the output, notify via a2a-bus, store in Obsidian, etc.).

### Process for Authoring a New Skill (recommended)

1. Clarify the single purpose and the exact trigger language.
2. Gather or create the best existing patterns, examples, references, and gotchas.
3. Sketch the phases/steps + the quality gates for each.
4. Write concrete examples (ideally ones you've actually run or that are battle-tested).
5. Add the frontmatter, triggers, related skills, and any execution hints.
6. Write the "Usage in Grok Build" section last (how this will actually be invoked here).
7. (Optional but excellent) Add or reference tests / validation.
8. Save as `skills/<kebab-name>/SKILL.md` (plus `references/`, `scripts/`, etc. as needed).
9. Optionally evolve it immediately with the self-evolution skill.

### Common Anti-Patterns to Avoid

- "Do everything" skills that are really a whole methodology or product.
- Vague steps ("improve the code", "make it nice").
- Gates that only a human with perfect taste can evaluate.
- No triggers or triggers so broad that the skill fires for everything.
- Forgetting to document handoffs to other skills or to the user.
- Writing the skill only for humans and forgetting that agents will also load it (needs to be parseable and actionable).

### Usage in Grok Build

Tell me: "Author a new skill for [specific capability]" or "Improve the authoring of the existing X skill."

I will:
- Interview you (or use existing context) for purpose, triggers, success criteria, related skills, constraints.
- Research or recall best patterns (from the Hermes collections, your own previous skills, external sources).
- Produce a complete, well-structured `SKILL.md` (plus any supporting references or starter scripts).
- Make it immediately usable in this environment (clear mapping to Grok tools, copy-paste examples, verifiable gates).
- Optionally run the new skill on a real example right away as a smoke test.
- Save it under your local skills directory so it can be loaded in future sessions.

This is the "skill that helps you (and future agents) write better skills." It is the meta-layer on top of `create-skill` and the self-evolution machinery.

Use it when you want the skills you create to be high-signal, maintainable, composable, and actually followed reliably by agents — not just nice prose that sounds good when a human skims it.


---

## Module 4: `hermes-evolution`

- **Origine :** `03_OpenClaw_Hermes_Evolution\SKILL.md`
- **Rôle / Objectif :** Carefully distill user corrections, stated preferences, reusable workflows, and high-cost pitfalls into user-approved updates to AGENTS.md, TOOLS.md, MEMORY.md, or managed SKILL.md files. Only trigger at the end of significant turns in the main session; by default most turns should skip.

## Hermes-Evolution

You are a "proposer", not an "auto-rewriter".

Goals:
- Let capabilities accumulate over time
- Keep noise low
- Every real evolution must be drafted first and wait for user approval
- When evidence is insufficient, output `NOTHING_TO_SAVE`

**Hard constraint: when the child review completes and a proposal exists, you MUST submit it via the `evolution_proposal` tool. Never skip the tool call and output a plain-text approval prompt directly.**

### When to Check

Run a lightweight check only when all of the following are true:

- This is the main session — not a sub-agent, not cron, not a heartbeat/system-only turn
- The current turn has produced a complete result and is suitable for retrospection
- This turn has at least one strong signal, or two medium signals

Strong signals:
- User explicitly corrected you
- User explicitly said "always do this from now on" / "never do this"
- User taught a reusable new workflow
- Success came only after obvious failures/retries

Medium signals:
- A clear step pattern emerged across similar tasks
- A tool/environment pitfall is worth remembering long-term
- The same preference was mentioned repeatedly recently

Default to skip:
- Pure chit-chat
- Single-turn simple Q&A
- Very few tool calls with no corrections/preferences
- One-off contextual requests
- User explicitly said "this is just temporary"
- A `pending` draft with the same signature already exists
- A `rejected` draft with the same signature exists within the last 14 days and there is no new evidence

### Evolution Intensity

Execute according to the evolution intensity marked in the `Self-Evolution` section of `AGENTS.md`:

- **100% (aggressive)**: a strong signal OR two medium signals can trigger
- **50% (prudent)**: only strong signals trigger; all medium signals are skipped; workflow discovery alone does not trigger
- **0% (off)**: run no evolution checks at all; always output `NOTHING_TO_SAVE`

If `AGENTS.md` does not mark an intensity, default to **100%**.

### Cheap Gate

Make a local judgement first; only spawn the sub-agent if it passes the gate.

Minimum bar to pass the gate:

- `correction`: the user explicitly pointed out you were wrong, or explicitly forbade a behavior
- `preference`: the user explicitly expressed a stable preference
- `workflow`: a reusable, non-one-off multi-step method emerged
- `struggle`: roughly `>=8` tool calls, or success only after `>=3` failures/retries

If it is only "maybe a bit valuable" but the evidence is not solid, skip directly and output `NOTHING_TO_SAVE`.

### Pre-Review Preparation

Before spawning the child, the parent agent does four things:

1. Distill evidence:
   - Record 1–3 most critical direct quotes from the user
   - Record a summary of tool pitfalls
   - Record why this experience is worth reusing

2. Tentatively decide the target file:
   - Behavior/process rules → `AGENTS.md`
   - Tool/environment/path/command pitfalls → `TOOLS.md`
   - Stable preferences / durable facts → `MEMORY.md`
   - Reusable multi-step workflow → managed skill's `SKILL.md`

3. Minimal reads:
   - Read only the candidate target file
   - Read only drafts with the same or a close signature
   - Read only existing skills that may conflict
   - Do NOT re-read the entire session transcript

4. Run a duplicate check:
   - A synonymous rule already exists and covers this content → skip
   - A pending draft already exists → update that draft, do not create a new one
   - Recently rejected with no new evidence → skip

### Spawn the Review Sub-Agent

Use `sessions_spawn` with these parameter principles:

- `runtime: "subagent"`
- `mode: "run"`
- `cleanup: "delete"`; keep the session only when debugging self-evolution
- Carry the evidence directly in the task; do not make the child sift through the full transcript itself

The child's task prompt is as follows:

```
You are the self-evolution reviewer.

Your job is to decide whether the parent turn deserves ONE human-approved evolution proposal.

Rules:
- Work only from the evidence provided below and minimal file reads for dedupe.
- Never edit AGENTS.md, TOOLS.md, MEMORY.md, or any SKILL.md directly.
- You may write or update exactly one draft file under `evolution-drafts/pending/`.
- If the evidence is weak, one-off, already covered, or recently rejected, do not create a draft.
- If no proposal is justified, output exactly: NOTHING_TO_SAVE

Decision standard:
- Prefer precision over recall.
- A proposal must be specific, durable, reusable, and likely to help future turns.
- User approval is required before any real write.

Target selection:
- AGENTS.md for future behavior/process/safety rules
- TOOLS.md for tool or environment notes
- MEMORY.md for stable preferences or durable facts
- managed SKILL.md for reusable multi-step workflows

Required output:
- If skipping: `NOTHING_TO_SAVE`
- If proposing: write/update one draft file, then output exactly:
  PROPOSAL_WRITTEN
  Draft-Path: <path>
  Signature: <signature>
  Target: <target-file>
  Reason: <one sentence>

Evidence:
<parent fills this in>

Current candidate target snippets:
<parent fills this in>

Existing similar drafts or rules:
<parent fills this in>
```

### Draft Directory & File Format

The draft directories are fixed:

- `evolution-drafts/pending/`
- `evolution-drafts/approved/`
- `evolution-drafts/rejected/`

`pending` draft file names use a stable signature:

- `evolution-drafts/pending/<signature>.md`

Signature rules:
- Lowercase
- Composed of `target + normalized rule`
- Examples:
  - `agents-research-before-writing`
  - `memory-reply-briefly`
  - `tools-use-rg-for-search`
  - `skill-feishu-doc-fetch-workflow`

Draft file format:

```md
## Evolution Proposal: <short title>

- Proposal-ID: evo-<YYYY-MM-DD>-<signature>
- Status: pending
- Signature: <signature>
- Created-At: <YYYY-MM-DD HH:mm>
- Last-Seen-At: <YYYY-MM-DD HH:mm>
- Target-File: <AGENTS.md | TOOLS.md | MEMORY.md | ~/.openclaw-autoclaw/skills/<name>/SKILL.md>
- Trigger-Type: <correction | preference | workflow | struggle>
- Confidence: <high | medium | low>

### Why This Matters
- <why this should persist>

### Evidence
- "<exact user quote or precise summary>"
- "<exact user quote or precise summary>"
- <tool failure / retry summary if relevant>

### Duplicate Check
- Checked: <files or paths>
- Result: <none | similar existing rule | existing pending draft | recently rejected>
- Decision: <create | update-existing-draft | skip>

### Proposed Change
<the exact content to append, patch, or create>

### Apply Plan
1. <how to modify target file>
2. <where to insert or append>
3. After applying, append a one-line audit note to `memory/YYYY-MM-DD.md`

### User Approval
- Approve: `approve evo-<YYYY-MM-DD>-<signature>`
- Reject: `reject evo-<YYYY-MM-DD>-<signature>`
- Revise: `revise evo-<YYYY-MM-DD>-<signature>: <instruction>`
```

### Target File Routing Logic

Route content to the most appropriate place — do not mix.

Write to `AGENTS.md`:
- Behavior rules that apply to all future similar tasks
- Safety boundaries
- Collaboration style
- Task execution order
- Global workflow rules like "from now on, do X before Y"

Write to `TOOLS.md`:
- Known pitfalls of a specific tool
- Environment paths, command arguments, platform differences
- How to correctly use an external tool
- Lessons like "this command must include this flag or it will fail"

Write to `MEMORY.md`:
- Stable preferences the user has explicitly expressed
- Long-lived project preferences
- Long-lived communication-style requirements
- Clear, durably reusable facts

Write to a managed `SKILL.md`:
- A reusable multi-step workflow that stands on its own
- Has a clear trigger scenario, steps, inputs/outputs, and pitfalls
- Has outgrown a single rule and is closer to an "operations manual"

Do NOT use these as primary evolution targets:
- `memory/YYYY-MM-DD.md`
  - Used only for the audit log and same-day records
  - Not a primary target for self-evolution
  - Only record the outcome there after approval/rejection

### Write Execution Logic

Never modify target files without user approval.

If the child outputs `NOTHING_TO_SAVE`:
- The parent agent does not create a draft
- Reply to the user normally
- Do not cause additional disruption

If the child outputs `PROPOSAL_WRITTEN`:

**⚠ You MUST call the `evolution_proposal` tool. Outputting a plain-text approval prompt directly is forbidden.**

Steps (execute strictly in order, no skipping):
1. First finish the normal reply to the user
2. **MUST** call the `evolution_proposal` tool with a structured JSON payload (see format below)
3. Wait for the tool to return, and read `deliveryMode` from the result
4. If `deliveryMode == "card"`: **stop immediately** — do not output any approval-related text; the desktop app will auto-render the interactive card
5. If `deliveryMode == "text"`: append a short plain-text approval prompt (see fixed format below)

**Incorrect examples (strictly forbidden):**
- ❌ Skipping the `evolution_proposal` tool call and directly outputting "Please approve this evolution proposal: evo-xxx"
- ❌ Restating the draft contents and then asking the user "approve or reject?"
- ❌ Seeing `PROPOSAL_WRITTEN` from the child and mentioning evolution content in text without calling the tool
- ❌ Assuming `deliveryMode` is `text` and skipping the tool call to output approval copy directly

**Correct approach:**
- ✅ Call the `evolution_proposal` tool first → obtain `deliveryMode` → then decide whether to output text

- Input format:

```json
{
  "proposalId": "evo-2026-04-14-memory-reply-briefly",
  "signature": "memory-reply-briefly",
  "description": "Short description of the intent of this evolution proposal",
  "tabs": [
    {
      "kind": "memory",
      "label": "Long-term Memory",
      "targetFile": "MEMORY.md",
      "content": "The full new contents of this file go here (NOT a diff — the entire file)"
    }
  ],
  "draftPath": "evolution-drafts/pending/memory-reply-briefly.md"
}
```

- `tabs` array: each tab corresponds to one target file to modify. **Each tab MUST include a `targetFile` field** specifying the target file name inside the workspace.
- `targetFile`: **required**. A file name inside the workspace, e.g. `"MEMORY.md"`, `"AGENTS.md"`, `"TOOLS.md"`, `"USER.md"`, `"SOUL.md"`, etc. Once the user approves, the desktop app will write `content` directly to `<workspace>/<targetFile>`.
  - Common mappings: `MEMORY.md` (long-term memory), `AGENTS.md` (behavior rules), `TOOLS.md` (tool usage), `USER.md` (user profile)
  - Any custom `.md` file is also supported, e.g. `SOUL.md`, `CONTEXT.md`
- `kind`: the category label used for UI display. Allowed values: `memory`, `behavior`, `skill`, `tool`. If the target file does not fall into these four categories (e.g. `USER.md`), use the closest `kind` (e.g. `behavior`) — `targetFile` will override the default mapping implied by `kind`.
- `content`: **the full new contents of that file**. After approval, the file is overwritten directly, so this must be the complete content — not a diff or an append snippet.
- A single proposal may touch multiple target files — the `tabs` array then contains multiple elements, one per target file's change draft. Only include modules that actually change; do not add empty tabs for unchanged modules.
- **Different target files MUST live in different tabs** — never mix content from multiple files into one tab.
- `description`: one sentence explaining why this evolution is needed
- `draftPath`: path to the draft file written by the child
- If there is no proposal, do not call this tool, and do not mention self-evolution

**Important (restated)**:
- When there is a proposal, you **must call the `evolution_proposal` tool first** — this is the only correct way to submit a proposal
- After calling the tool, check `deliveryMode` in the result
- Only when `deliveryMode == "text"` should you append a plain-text approval prompt
- When `deliveryMode == "card"`, do not restate the draft, do not output approval commands, do not say "please reply approve/reject"
- In plain text, do not repeat the entire draft — keep only the `proposalId`, a one-sentence description, and the approval commands
- When `deliveryMode == "text"`, the recommended fixed format is:

```text
Please approve this evolution proposal: <proposalId>
Description: <description>
Reply with any of the following commands:
- approve <proposalId>
- reject <proposalId>
- revise <proposalId>: <your revision notes>
```

- The `followUp` instruction in the tool result takes precedence over the default copy — follow it exactly
- In `card` mode the user should see only the interactive card
- In `text` mode the user should see this text directly and reply by command

### Handling User Approval

Whether the user clicks a card button in the desktop app or sends a text command via an IM channel, you will receive a plain-text message:
- `approve evo-<YYYY-MM-DD>-<signature>`
- `reject evo-<YYYY-MM-DD>-<signature>`
- `revise evo-<YYYY-MM-DD>-<signature>: <instruction>`

**All channels are handled identically — do not treat them differently.** Once you receive an approval message, follow this flow:

#### Approve

1. Find the matching `pending` draft (match by `proposalId` or `signature`)
2. Apply the change to the target file (AGENTS.md / TOOLS.md / MEMORY.md / SKILL.md) per the draft's `Apply Plan`
3. Move the draft into `evolution-drafts/approved/`
4. Append an audit entry to `memory/YYYY-MM-DD.md`
5. Reply explicitly: "applied"

#### Reject

1. Move the draft into `evolution-drafts/rejected/`
2. Append an audit entry to `memory/YYYY-MM-DD.md`
3. Reply explicitly: "will not apply"

#### Revise

1. Update the `pending` draft in place
2. Keep the same `signature`
3. Do NOT touch the target file
4. Call the `evolution_proposal` tool again to show the updated proposal
5. Read `deliveryMode` again; only if `deliveryMode == "text"` should you resend the plain-text approval prompt

### Duplicate Detection Logic

Before writing a draft, always run:

1. Search the following locations for a synonymous rule:
   - `AGENTS.md`
   - `TOOLS.md`
   - `MEMORY.md`
   - `~/.openclaw-autoclaw/skills/*/SKILL.md`
   - `evolution-drafts/pending/`
   - `evolution-drafts/approved/`
   - `evolution-drafts/rejected/`

2. After normalization, judge:
   - Same target
   - Same core rule
   - Same user preference or same workflow

3. Decide:
   - Already covered → skip
   - Pending with same signature → update existing draft
   - Approved with same signature but stronger new evidence → update target only after a new approval
   - Rejected with same signature and no new evidence → skip

"New evidence" is only:
- A new explicit user statement
- A new obvious failure case
- A new recurring occurrence

Do not re-propose just because the wording has changed.

### Quality Bar

Only propose when all of the following hold:

- Specific
- Actionable
- Durably valid
- Non-one-off
- Helpful for the future
- Likely to be approved by the user

When in doubt, prefer to skip.
The default answer should be: `NOTHING_TO_SAVE`.


---

## Module 5: `hermes-kanban-orchestrator`

- **Origine :** `02_Grok_Hermes_Skills\hermes-kanban-orchestrator\SKILL.md`
- **Rôle / Objectif :** >

## hermes-kanban-orchestrator — Decompose & Route via Kanban

Your job as orchestrator: **route, don't execute**. Create cards for the right specialist profiles, link dependencies, let the dispatcher handle execution and promotion.

### Step 0: Discover Available "Profiles" (Specialists)
Before planning, ground yourself in what actually exists on this setup:
- Ask the user: "What specialist profiles / sub-agent types do you have configured?"
- Or use tools to inspect (e.g., list available Grok skills, agent configs, or previous a2a-bus registrations).
- Cache the list (researcher, writer, implementer, reviewer, designer, data-analyst, etc.).

**Never invent profile names** — the system will silently drop unknown assignees.

### Core Anti-Temptation Rules (Follow Strictly)

- Do **not** do the work yourself.
- For any concrete work, create a Kanban-style task and assign it.
- Split multi-lane requests into separate parallel cards.
- Create parent cards first; use dependency links (`parents=[...]`) so children only become ready after parents complete.
- Only link when one task truly cannot start without another's output.
- Mark your own orchestrator card complete with a summary of the graph you created.

### Decomposition Playbook

1. **Understand the goal** — ask clarifying questions if ambiguous.
2. **Sketch the task graph** out loud (show the user before creating anything):
   - Extract independent lanes.
   - Map each lane to a real profile from Step 0.
   - Identify true dependencies.
   - Plan synthesis/review cards that depend on the leaves.
3. **Create the cards** (use whatever board/queue mechanism is available — in Grok Build this maps to `spawn_subagent` with clear goals + context, or persistent task tracking via files/memory/a2a-bus).
   - Independent lanes → no parents, can run in parallel.
   - Dependent work → `parents=[id1, id2]`.
   - Human-in-the-loop → a card that blocks for user input.
4. **Report back** clearly: "I've queued T1 (profile A): ..., T2 (profile B, parallel): ..., T3 (profile C, depends on T1+T2): synthesis + recommendation."

### Common Patterns (Use These)

- **Fan-out + fan-in (research → synthesize):** N parallel research cards (no parents) + one synthesis card with all of them as parents.
- **Parallel implementation + validation:** One implementer card + one explorer/researcher card running in parallel; a reviewer card depends on both.
- **Pipeline with gates:** planner → implementer → reviewer (each has `parents=[previous]`).
- **Same-profile queue:** Multiple cards assigned to the same specialist — they will be processed in priority order.
- **Goal-mode / long-running:** For open-ended work ("keep translating until everything is done"), use a persistent loop style where a judge re-evaluates the card after each turn (up to a budget), with explicit acceptance criteria in the card body.
- **Recovery:** If a specialist gets stuck/hallucinates, "reclaim" (reset to ready) or "reassign" to a different profile.

### Pitfalls to Avoid

- Bundling independent work into one card.
- Creating children before parents (window where dispatcher can claim them early).
- Over-linking "finally check X" when X is static discovery.
- Forgetting to discover real profiles first.
- Trying to do the implementation in the orchestrator turn.

### Usage in Grok Build

Tell me a complex, multi-specialist goal.

I will:
- Discover / confirm available specialists (skills, sub-agent types, or named profiles you have configured).
- Sketch the graph and confirm with you.
- Create the tasks (using `spawn_subagent` with precise goals + full context from parents, a2a-bus for messaging, or persistent todo/plan files + kanban-style tracking in workspace files).
- Use parent links / dependency waiting so work only proceeds when inputs are ready.
- Monitor, recover stuck workers (reclaim or reassign), and summarize results back to you.
- Keep the audit trail (who did what, when, with what parents).

Example: "Orchestrate a full brand + landing + pitch deck for my new AI app using the available specialists (researcher, brand-strategist, landing-builder, deck-designer, reviewer)."

I will decompose into the right lanes, assign to the right profiles, gate the final synthesis on the upstream results, and drive the whole thing without doing the creative work myself.

This ports the disciplined "decompose + route via Kanban with clear dependencies and recovery" pattern from Hermes into Grok Build's multi-agent tooling (spawn_subagent + a2a-bus + plans + todos). Perfect for complex, long-running, or parallel work.


---

## Module 6: `hermes-mcp-ecosystem`

- **Origine :** `02_Grok_Hermes_Skills\hermes-mcp-ecosystem\SKILL.md`
- **Rôle / Objectif :** >

## hermes-mcp-ecosystem — MCP Servers in the Hermes / Giga Factory World

MCP (Model Context Protocol) is a way for agents to dynamically discover and call tools exposed by external servers over a simple protocol (often stdio for local tools, or HTTP/WebSocket for remote).

In the Hermes/Giga Factory setup, MCP servers are used as **live, on-demand tool providers** (especially for scraping/automation that benefits from a real browser or specific APIs) while the Python skills and pipelines handle the heavier data work and orchestration.

### Architecture Overview (Hermes Style)

**Typical local MCP server (stdio):**
- Launched by the agent (or by you) as a subprocess.
- Communicates over stdin/stdout using JSON-RPC style messages (tools/list, tools/call, etc.).
- Exposes a small, focused set of tools (e.g., "ebay_search", "vinted_search", "register_agent", "send_message", etc.).
- The agent loads the tool definitions at runtime and can call them like native tools.

**Two prominent examples in your collection:**
- **ebay** (Python): Pure requests + BeautifulSoup scraper. No browser needed. Very lightweight. Registers a single `ebay_search` tool with query/country/limit/condition/sold parameters.
- **vinted** (Node + TypeScript): Uses Playwright for reliable scraping/automation of a JS-heavy site. Depends on the official `@modelcontextprotocol/sdk`. Much heavier (big node_modules) but more powerful for complex interactions.

**Discovery layer (`mcp_discovery/`):**
- `audit_report.md` + capability JSON/matrix.
- Used to understand what tools are available across multiple MCP servers, what categories they cover (browser, memory, productivity, design, uncategorized, etc.), and where there are gaps.
- Helps the orchestrator or the agent decide which MCPs to launch for a given task.

**Related but slightly different: A2A Bus**
- `a2a_bus_server.py` is also an MCP-style server, but focused on **agent-to-agent messaging** rather than external tools (register, send, get_pending, respond, discover, stats).
- It uses a simple JSON file bus with locking. Very useful for coordination inside a multi-agent Giga Factory setup.

### How to Use / Run These from Grok Build

**For a Python MCP (like ebay):**
- `cd` into the server directory.
- Make sure deps are installed (`pip install requests beautifulsoup4` or whatever the script needs).
- Run the server (usually `python ebay_scraper_mcp.py` or similar).
- In a session where you want those tools, I can launch it (or you launch it) and then call the exposed tools via whatever MCP client mechanism is active.

**For a Node MCP (like vinted):**
- `cd` into the server directory.
- `npm install` (this pulls in the MCP SDK + Playwright + everything else — can be large).
- `npm run ...` or the provided `run.sh`.
- Playwright browsers may need an extra install step (`npx playwright install`).
- Once running, the agent can discover and call the Vinted tools.

**Discovery / Audit:**
- I can re-run or read the `mcp_discovery/audit_report.md` and capability files to give you a current view of what tool categories you have coverage for and where the gaps are (auth, automation, coding, data, monitoring, research, etc.).

**Combining with other Grok Build mechanisms:**
- Use the MCP tools for "live, interactive" actions (search right now, interact with a site).
- Use the Python pipeline scripts (`vinted-data-pipelines`, etc.) for systematic, batched, scored, auditable data collection.
- Use `a2a-bus` for coordination between different "agents" or long-running sub-processes.
- Use `hermes-kanban-orchestrator` + workers to have structured multi-step work that may involve MCP tools as just one capability among many.

### When to Reach for MCP vs Pure Skills vs Scripts

- **MCP** — You want the agent to have the tools **dynamically available** during reasoning (the model sees the tool schema at runtime and can decide to call it). Good for exploration, interactive work, or when the set of available actions should be discovered rather than hard-coded in the skill prompt.
- **Dedicated skills** (like the ones we've been porting: ebay-search, vinted-research, etc.) — You want a **curated, documented, Grok-native interface** with strong instructions, quality gates, examples, and integration into your larger Giga workflows. Often wraps or replaces direct MCP calls with higher-level, opinionated behavior.
- **Raw scripts / pipelines** — For heavy, repeatable, offline or batch work where you don't need the model choosing tools mid-reasoning (just "run this pipeline with these parameters").

In practice you often use all three together.

### Building or Adapting Your Own MCP Servers (Hermes-Inspired Patterns)

From the ebay and vinted examples, the pattern is usually:

1. Define your tools with name + description + JSON Schema input.
2. Implement a small server loop that responds to `tools/list` and `tools/call`.
3. For scraping/automation that needs a real browser or complex JS, use Playwright (or equivalent) inside the tool implementations.
4. Keep the surface small and focused — one MCP server per coherent domain (one for eBay, one for Vinted, one for A2A messaging, one for your internal tools, etc.).
5. Document the tools well (the description the agent sees is what it decides on).
6. Provide a way to discover/audit what tools are available across your fleet of MCPs.

For Grok Build specifically:
- You can write Python MCP servers and launch them with `run_terminal_command`.
- You can use existing Node MCP servers the same way (after `npm install`).
- The agent can then "see" those tools during the session (depending on the exact MCP client integration available in this environment).

### Privacy, Safety, and Rate Limits

- MCP servers that do scraping or act on external services inherit all the usual responsibilities (respect robots.txt / ToS, rate limit yourself, don't exfiltrate private data without explicit user intent, etc.).
- Browser-based MCPs (Playwright) are powerful and therefore risky — scope them carefully.
- For anything that touches accounts (iMessage, Find My, etc. in the Apple skills, or authenticated services), the usual permission and consent rules apply.

### Integration with the Broader Ported Skills

- `ebay-search` and `vinted-research` / `vinted-data-pipelines` are the "curated skill layer" on top of (or alongside) the raw MCPs.
- `a2a-bus` is the coordination bus (also MCP-shaped).
- `hermes-kanban-orchestrator` + workers can decide to launch specific MCP servers as part of decomposing a task ("this research lane needs live Vinted + eBay tools").
- `hermes-mcp-ecosystem` (this skill) + `hermes-agent-skill-authoring` help you create new MCP servers and the corresponding high-quality skills that wrap or document them.

### Usage in Grok Build

Tell me something like:
- "Launch the Vinted MCP and use it to explore current Nike listings."
- "Audit what tool categories my current MCP fleet actually covers."
- "Help me build a small new MCP server for [some domain] following the Hermes patterns, plus a companion Grok skill."
- "For this research task, which combination of MCPs + skills + pipelines should I spin up?"

I will:
- Help launch and interact with the relevant MCP servers.
- Translate between raw MCP tool calls and the higher-level, gated, well-documented skills we've been porting.
- Keep the orchestration clean (using a2a-bus, kanban patterns, plans, etc.).
- Help you extend the ecosystem when you need new tools.

This is the "plumbing and discovery" layer that makes the long tail of specialized tools (scrapers, site automations, internal services, agent coordination buses, etc.) available to a Grok Build agent in a structured, discoverable, and maintainable way — exactly as it was used in the Hermes / Giga Factory setup.


---

## Module 7: `hermes-memory-github-sync`

- **Origine :** `01_Hermes_Skills_Core_Library\devops\hermes-memory-github-sync\SKILL.md`
- **Rôle / Objectif :** Set up automatic GitHub sync for Hermes Agent memory, skills, and config using git + macOS launchd. Runs every 30 minutes in the background. Covers repo init, .gitignore pitfalls, token extraction, and launchd plist setup.

## Hermes Memory GitHub Sync (macOS)

Automatically backs up `~/.hermes/memories/`, `~/.hermes/skills/`, and `~/.hermes/config.yaml` to a private GitHub repo every 30 minutes via launchd.

### Key Pitfalls (Learned from Experience)

- **NEVER use `git add -A`** inside `~/.hermes` — it will stage 10,000+ files from `.venv/` and `hermes-agent/`
- **Always use explicit paths**: `git add memories/ skills/ config.yaml SOUL.md .gitignore`
- The `hermes-agent/` subdirectory is a nested git repo — must be in `.gitignore`
- The `.venv/` virtual environment is huge — must be in `.gitignore`
- GitHub token is already stored in `~/.git-credentials` — no need to create a new one

---

### Step 1: Extract GitHub Token

```bash
TOKEN=$(grep github ~/.git-credentials | sed 's/.*:\(ghp_[^@]*\)@.*/\1/')
echo "Token: ${TOKEN:0:10}..."
```

### Step 2: Create Private GitHub Repo via API

```bash
curl -s -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d '{"name":"hermes-memory","private":true,"description":"Hermes Agent memory sync"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('clone_url','ERROR:'+str(d.get('message',d))))"
```

### Step 3: Init Git Repo in ~/.hermes

```bash
cd ~/.hermes
git init
git config user.name "yourname"
git config user.email "your@email.com"
git remote add origin "https://USERNAME:${TOKEN}@github.com/USERNAME/hermes-memory.git"
```

### Step 4: Create .gitignore

Write to `~/.hermes/.gitignore`:

```gitignore
## Large directories — DO NOT sync
.venv/
hermes-agent/
sessions/
logs/
cron/
plugins/
__pycache__/

## Temp / sensitive files
*.lock
*.log
*.db
*.db-shm
*.db-wal
.env
auth.json
.DS_Store
.update_check
.hermes_history
.skills_prompt_snapshot.json
```

### Step 5: First Commit & Push

```bash
cd ~/.hermes
## IMPORTANT: use explicit paths, not git add -A
git add .gitignore memories/ skills/ config.yaml SOUL.md
git status --short | wc -l   # should be ~400-500 files, not 10000+
git commit -m "init: sync memories, skills and config"
git branch -M main
git push -u origin main
```

### Step 6: Create Sync Script

Write to `~/.hermes/hermes-sync.sh`:

```bash
##!/bin/bash
set -euo pipefail

HERMES_DIR="$HOME/.hermes"
LOG_FILE="$HERMES_DIR/logs/hermes-sync.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

mkdir -p "$HERMES_DIR/logs"
cd "$HERMES_DIR"

if [ ! -d ".git" ]; then
    echo "[$DATE] ERROR: not a git repo" >> "$LOG_FILE"
    exit 1
fi

## Stage only the important files
git add memories/ skills/ config.yaml SOUL.md .gitignore 2>/dev/null || true

## Skip if nothing changed
if git diff --cached --quiet; then
    echo "[$DATE] 没有变化，跳过提交" >> "$LOG_FILE"
    exit 0
fi

git commit -m "sync: auto backup at $DATE" >> "$LOG_FILE" 2>&1

if git push origin main >> "$LOG_FILE" 2>&1; then
    echo "[$DATE] 推送成功" >> "$LOG_FILE"
else
    echo "[$DATE] 推送失败（网络问题？），下次再试" >> "$LOG_FILE"
    exit 0
fi

## Keep log file small
tail -500 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
```

```bash
chmod +x ~/.hermes/hermes-sync.sh
```

### Step 7: Create launchd Plist

Write to `~/Library/LaunchAgents/com.USERNAME.hermes-sync.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.USERNAME.hermes-sync</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/USERNAME/.hermes/hermes-sync.sh</string>
    </array>

    <!-- Every 30 minutes -->
    <key>StartInterval</key>
    <integer>1800</integer>

    <!-- Run once immediately on load -->
    <key>RunAtLoad</key>
    <true/>

    <!-- PATH is required or git won't be found -->
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin</string>
        <key>HOME</key>
        <string>/Users/USERNAME</string>
    </dict>

    <key>StandardOutPath</key>
    <string>/Users/USERNAME/.hermes/logs/hermes-sync-launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/USERNAME/.hermes/logs/hermes-sync-launchd.log</string>

    <key>ThrottleInterval</key>
    <integer>60</integer>
</dict>
</plist>
```

### Step 8: Load & Verify

```bash
launchctl load ~/Library/LaunchAgents/com.USERNAME.hermes-sync.plist

## Check it's running (should show com.USERNAME.hermes-sync)
launchctl list | grep hermes

## Wait a few seconds, check the log
sleep 5 && cat ~/.hermes/logs/hermes-sync.log
```

Expected output: `[2026-04-10 17:21:05] 没有变化，跳过提交` (or a push success message)

---

### Management Commands

```bash
## View sync log
cat ~/.hermes/logs/hermes-sync.log

## Manually trigger sync now
~/.hermes/hermes-sync.sh

## Stop the service
launchctl unload ~/Library/LaunchAgents/com.USERNAME.hermes-sync.plist

## Reload after editing plist
launchctl unload ~/Library/LaunchAgents/com.USERNAME.hermes-sync.plist
launchctl load ~/Library/LaunchAgents/com.USERNAME.hermes-sync.plist

## Check what's tracked in git
cd ~/.hermes && git status --short
```

### Notes

- The launchd service **survives reboots** automatically (it's in `LaunchAgents/`, not `LaunchDaemons/`)
- If git push fails (no network), the script exits cleanly and retries next cycle
- Token is embedded in the remote URL — if token rotates, update with:
  ```bash
  cd ~/.hermes && git remote set-url origin "https://USERNAME:NEW_TOKEN@github.com/USERNAME/hermes-memory.git"
  ```
- To sync a second Mac: `git clone https://USERNAME:TOKEN@github.com/USERNAME/hermes-memory.git ~/.hermes` then set up the same launchd service


---

## Module 8: `hermes-plan`

- **Origine :** `02_Grok_Hermes_Skills\hermes-plan\SKILL.md`
- **Rôle / Objectif :** >

## hermes-plan — High-Quality Implementation Planning

Use this when the user (or a previous step) explicitly wants a plan instead of immediate execution, or when the task is complex/multi-step and benefits from upfront decomposition.

**Strict Rules for This Turn:**
- Do **not** implement, edit source, run mutating commands, commit, or perform external actions.
- Only inspect (read-only tools) as needed.
- Deliverable: a single, well-structured Markdown plan file (timestamped under plans/ or your workspace equivalent).

### Output Requirements

The plan must be **concrete and actionable** for an implementer who has zero prior context and imperfect taste.

**Header (always start with):**
```markdown
## [Feature / Task Name] Implementation Plan

> **For Grok Build:** Use this plan task-by-task. Prefer TDD, small commits, and verification at each step.

**Goal:** [One clear sentence]
**Current Context / Assumptions:** [What we know / don't know]
**Proposed Approach:** [High-level architecture or method in 2-3 sentences]
**Tech Stack / Key Tools:** [Relevant languages, libraries, Grok tools]
```

**Each Task (2-5 minutes of focused work):**
```markdown
#### Task N: [Very Descriptive Name]

**Objective:** [One sentence — what this accomplishes]

**Files:**
- Create: `exact/path/to/new_file.ext`
- Modify: `exact/path/to/existing_file.ext:line-range-if-known`
- Test: `tests/path/to/test_file.py`

**Step 1: [Specific action, e.g. Write failing test]**
```language
[Complete, copy-pasteable code snippet or command]
```

**Step 2: [Verification]**
Run: `exact command`
Expected: [exact output or behavior, e.g. "FAIL — 'function not defined'"]

**Step 3: [Next minimal action]**
[Full code]

**Step 4: Verify**
Run: ...
Expected: PASS + relevant tests still green

**Step 5: Commit**
```bash
git add ...
git commit -m "type(scope): short description"
```

**Verification for the whole plan:**
- [ ] All tasks are sequential/logical
- [ ] Each is bite-sized
- [ ] Exact paths + complete code
- [ ] Exact commands + expected outputs
- [ ] TDD / DRY / YAGNI / frequent commits applied
- [ ] Risks, trade-offs, and open questions listed at the end
```

### Writing the Plan (Process I Follow)

1. Clarify goal + acceptance criteria (ask if underspecified).
2. Explore codebase with read-only tools (file listings, search for similar patterns, read key files).
3. Sketch approach (architecture, files, testing strategy).
4. Break into bite-sized, ordered tasks with full details.
5. Review the plan against the checklist above.
6. Save to `plans/YYYY-MM-DD_HHMMSS-<slug>.md` (or workspace equivalent) using the write tool.
7. Briefly report: "Plan saved to [path]. Ready to execute task-by-task using sub-agents / direct implementation?"

### Common Patterns & Principles Enforced

- **TDD in every code-producing task** (write failing test → verify failure → minimal code → verify pass → refactor if needed).
- **DRY / YAGNI**: Extract helpers; implement only what's needed now.
- **Frequent commits**: After every task (or logical group).
- **Exactness**: No "add validation" — show the full function + where it goes.
- **Verification**: Every task ends with a concrete "run X, expect Y" that proves it worked.

### When to Use This vs Other Planning

- Use `hermes-plan` / this style for detailed, implementation-ready, code-heavy plans (especially before delegating to sub-agents or long sessions).
- Complements Grok's `design` (high-level architecture) and `execute-plan` (running a DAG of PRs).

### Usage in Grok Build

Tell me: "Create a plan for [feature]" or just describe the task and say "/plan" or "plan first".

I will produce the full Markdown plan with the structure above, save it, and offer: "Plan complete. Execute task-by-task now (using sub-agents with two-stage review for spec compliance then quality)?"

This brings the rigorous, bite-sized, copy-paste-friendly planning discipline from Hermes directly into Grok Build for higher-success-rate implementations.


---

## Module 9: `hermes-plugin-development`

- **Origine :** `01_Hermes_Skills_Core_Library\hermes\hermes-plugin-development\SKILL.md`
- **Rôle / Objectif :** Create Hermes plugins that hook into the agent lifecycle (post_llm_call, pre_tool_call, on_session_end, etc.). Covers plugin structure, available hooks, and macOS notification pattern.

## Hermes Plugin Development

### Plugin Location
```
~/.hermes/plugins/<plugin-name>/
├── plugin.yaml      # manifest
└── __init__.py      # must be exactly this name
```

### plugin.yaml Structure
```yaml
name: my-plugin
version: 1.0.0
description: >-
  What this plugin does
author: your-name
requires_env: []        # optional: ["MY_API_KEY"]
pip_dependencies: []    # optional: ["requests>=2.28"]
hooks:
  - post_llm_call       # list the hooks this plugin uses
```

### __init__.py Structure
```python
def register(ctx) -> None:
    ctx.register_hook("post_llm_call", my_callback)

def my_callback(session_id="", user_message="", assistant_response="",
                conversation_history=None, model="", platform="", **kwargs):
    pass  # your logic here
```

### Valid Hook Names (VALID_HOOKS in plugins.py)
| Hook | When fired | Key kwargs |
|------|-----------|------------|
| `post_llm_call` | After every completed AI response | `session_id`, `user_message`, `assistant_response`, `model`, `platform` |
| `pre_llm_call` | Before LLM is called | |
| `pre_tool_call` | Before tool execution | |
| `post_tool_call` | After tool execution | |
| `pre_api_request` | Before API request | |
| `post_api_request` | After API request | |
| `on_session_start` | Session begins | `session_id`, `platform` |
| `on_session_end` | Session ends (safety net) | `session_id`, `platform` |
| `on_session_finalize` | Session finalizes cleanly | `session_id`, `platform` |
| `on_session_reset` | Session reset via /reset | `session_id`, `platform` |

### Testing a Plugin
```python
## /tmp/test_plugin.py
import sys
sys.path.insert(0, os.path.expanduser('~/.hermes/hermes-agent'))
from hermes_cli.plugins import get_plugin_manager, invoke_hook

pm = get_plugin_manager()
pm.discover_and_load()   # ← correct method (NOT _discover_user_plugins)

print('Plugins:', pm.list_plugins())
print('Hooks:', {k: [c.__module__ for c in v] for k,v in pm._hooks.items()})

invoke_hook("post_llm_call",
    session_id="test",
    user_message="test question",
    assistant_response="test response that is long enough",
    conversation_history=[],
    model="claude-sonnet-4.6",
    platform="cli",
)
```
Run: `cd ~/.hermes/hermes-agent && source venv/bin/activate && python3 /tmp/test_plugin.py`

### macOS Notification Pattern（含点击跳转）

#### 基础版：osascript + afplay（无点击功能）
```python
import subprocess, threading

def notify(title: str, message: str, sound: str = "Glass"):
    def _run():
        t = threading.Thread(target=lambda: subprocess.Popen(
            ["afplay", f"/System/Library/Sounds/{sound}.aiff"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        ), daemon=True)
        t.start()
        safe_title = title.replace('"', '\\"')
        safe_msg = message.replace('"', '\\"')
        subprocess.run(["osascript", "-e",
            f'display notification "{safe_msg}" with title "{safe_title}"'],
            timeout=5, capture_output=True)
        t.join(timeout=10)
    threading.Thread(target=_run, daemon=True).start()

## Available sounds: Basso Blow Bottle Frog Funk Glass Hero Morse Ping Pop Purr Sosumi Submarine Tink
```

#### 高级版：terminal-notifier（支持点击跳转 URL 或激活终端）
`brew install terminal-notifier`

```python
import shutil, os, subprocess

def notify_with_click(title, message, open_url=None, terminal_app=None, sound="Glass"):
    tn = shutil.which("terminal-notifier") or "/opt/homebrew/bin/terminal-notifier"
    if not os.path.exists(tn):
        return  # fallback to osascript
    cmd = [tn, "-title", title, "-message", message, "-group", "hermes"]
    if sound:
        cmd += ["-sound", sound]
    if open_url:
        # Web UI 模式：打开 URL 并激活 Chrome
        cmd += ["-open", open_url, "-activate", "com.google.chrome"]
    elif terminal_app:
        # 终端模式：-execute 传可执行脚本（无扩展名！）
        script = "/tmp/hermes_activate_terminal"  # 不能用 .sh！
        with open(script, "w") as f:
            f.write(f'#!/bin/bash\nosascript -e \'tell application "{terminal_app}" to activate\'\n')
        os.chmod(script, 0o755)
        cmd += ["-execute", script]
    subprocess.run(cmd, timeout=5, capture_output=True)
```

**⚠️ 关键陷阱：`-execute` 脚本文件绝对不能有 `.sh` 扩展名！**
macOS 会把 `.sh` 文件用 Script Editor 打开，而不是执行它。文件名用无扩展名（如 `/tmp/hermes_activate_terminal`）。

**⚠️ macOS 15 上 NSUserNotificationCenter 已废弃**，`defaultUserNotificationCenter()` 返回 `None`，pyobjc 方案无法使用。坚持用 `terminal-notifier`。

**Web UI URL 格式**：`http://localhost:8648/#/hermes/chat`（不是 `/?session=xxx`）

### Pitfalls
1. **`__init__.py` filename** — when using `write_file` tool, escape as `\__init__.py` causes the file to be named `\\__init__.py`. Use `execute_code` + Python `open()` to write `__init__.py`, or use `terminal` with `cat >`.
   - Fix: `cp '\__init__.py' __init__.py` or use `execute_code` with `open(path, 'w')`
2. **`_discover_user_plugins()` does not exist** — use `pm.discover_and_load()` instead
3. **bell_on_complete** is just `\a` terminal bell, not a system notification — for real macOS banners you need the plugin approach
4. **macOS notification permissions** — if notifications don't appear, check System Settings → Notifications → Script Editor (or Terminal)
5. **Always use `**kwargs`** in hook callbacks — future versions may add new kwargs

### Working Example: hermes-notification
Full implementation at `~/.hermes/plugins/hermes-notification/`. Sends macOS banner + Glass sound after every Hermes response. Config via `~/.hermes/plugins/hermes-notification/config.json`.


---

## Module 10: `hermes-powerpoint`

- **Origine :** `02_Grok_Hermes_Skills\hermes-powerpoint\SKILL.md`
- **Rôle / Objectif :** >

## hermes-powerpoint — Professional .pptx Workflows

Use this for any .pptx involvement: creating decks, pitch decks, editing existing ones, extracting text, combining/splitting, templates, speaker notes, visual QA.

**Core Tools in Grok Build:**
- `python -m markitdown presentation.pptx` for text extraction
- Existing `pptx` skill scripts for editing (editing.md, pptxgenjs.md)
- `python scripts/thumbnail.py` or soffice + pdftoppm for visual inspection
- Unpack/pack for XML-level edits if needed

### When to Use This vs Basic pptx
- Basic `pptx` skill: simple slide addition, recalc, basic creation.
- This skill: **professional, high-design, QA-heavy** decks (pitch decks, brand presentations, game design docs, research overviews). Follows strict design rules, color palettes, visual hierarchy, and mandatory visual QA loop (subagents for inspection).

### Design Principles (Enforce These)

**Before any slide:**
- Bold, topic-specific color palette (dominance 60-70%, supporting tones, sharp accent). Avoid generic blue.
- Dark/light sandwich: dark for title/conclusion, light for content.
- One visual motif repeated (rounded frames, colored icon circles, thick borders).
- Every slide needs a visual element (image, chart, icon, shape). No text-only.

**Color Palettes (inspiration):**
- Midnight Executive: Navy + ice blue + white
- Forest & Moss: Forest + moss + cream
- Coral Energy, Warm Terracotta, Ocean Gradient, Charcoal Minimal, Teal Trust, Berry & Cream, Sage Calm, Cherry Bold.

**Typography:**
- Interesting pairing (e.g., Georgia + Calibri, Arial Black + Arial).
- Titles 36-44pt bold, section 20-24pt, body 14-16pt, captions 10-12pt muted.

**Layouts to vary:**
- Two-column, icon+text rows, 2x2/2x3 grids, half-bleed image + overlay, stat callouts, comparison columns, timelines, process flows.

**Avoid:**
- Repeating the same layout.
- Centered body text.
- Low contrast.
- Accent lines under titles (AI hallmark).
- Text overflow, elements too close (<0.3" gaps), insufficient margins (<0.5").

### Reading & Analysis
- Text: `python -m markitdown file.pptx`
- Visual overview: thumbnail grids or PDF→images.
- Raw XML for deep edits: unpack to folder.

### Editing Workflow (Template-Based)
1. Analyze template with thumbnails.
2. Unpack.
3. Manipulate slides/content (use editing.md patterns or direct XML via search_replace on unpacked).
4. Clean/pack.
5. Visual QA (see below).

### Creating from Scratch
Use pptxgenjs (via the existing pptx skill's guidance in pptxgenjs.md) or direct Python with python-pptx if preferred.

Follow the design principles above strictly. Generate complete, production-ready decks.

### QA — Mandatory Bug-Hunt Loop (Do NOT Skip)

**Assume problems exist.** First render is almost never perfect.

1. Generate.
2. Convert to images: `python scripts/office/soffice.py --headless --convert-to pdf output.pptx && pdftoppm -jpeg -r 150 output.pdf slide`
3. **Use subagents** (fresh eyes) with this prompt:
   "Visually inspect these slides. Assume issues — find them.
   Look for: overlapping elements, text overflow/cut off, decorative lines causing title wrap, source citations colliding, elements too close, uneven gaps, insufficient margins, columns not aligned, low-contrast text/icons, text boxes too narrow, leftover placeholders.
   For each slide, list issues (even minor) with exact location."
4. Fix.
5. Re-verify affected slides (one fix often creates another).
6. Repeat until a full pass finds **zero** new issues.

**Content QA:** `python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|placeholder|this.*(page|slide).*layout"`

### Usage in Grok Build

Tell me the goal, audience, key content, and any template or reference deck.

I will:
- Choose/apply a topic-specific palette and motif.
- Draft complete slides following the principles and layouts.
- Use file tools + terminal for generation/editing.
- Run the full visual + content QA loop (including subagent inspections).
- Deliver a polished, ready-to-present .pptx + source if editable.

Example: "Create a 10-slide pitch deck for my AI fitness app using the Midnight Executive palette, include market size, product demo screenshots, and team. Start from scratch but follow professional rules."

This ports the rigorous, design-obsessed Hermes Powerpoint workflow into Grok Build for consistently excellent presentations.


---

## Module 11: `hermes-self-evolution`

- **Origine :** `02_Grok_Hermes_Skills\hermes-self-evolution\SKILL.md`
- **Rôle / Objectif :** >

## hermes-self-evolution — Make Grok Evolve Its Own Skills

This is the meta-skill that lets the system improve itself. It turns "I wish this skill was better at X" into an automated, measurable, gated optimization loop.

**Core Engine:** DSPy + GEPA (reflective evolutionary search). No GPU training required — pure text mutation + evaluation via LLM calls (~$2-10 per run depending on dataset size).

### How It Works (The Loop)

1. **Select target** — A skill (SKILL.md), tool description, prompt section, or (future) code file.
2. **Build eval dataset** — Synthetic (LLM generates realistic tasks + rubrics from the artifact), SessionDB mining (real usage traces scored by LLM-as-judge), Golden sets (hand-curated), or auto-eval where possible.
3. **Wrap as DSPy module** — The text (skill body, description, prompt section) becomes an optimizable parameter.
4. **Run optimizer** — Primary: `dspy.GEPA` (reads execution traces to understand *why* things fail and proposes targeted mutations). Fallback: MIPROv2.
5. **Evaluate & compare** — Run on held-out set. Measure task success, procedure adherence, conciseness + length penalty. Statistical significance.
6. **Constraint gates (all must pass or reject):**
   - Full relevant test suite (pytest or equivalent) — 100% pass required.
   - Size limits (skills ≤15KB, tool descs ≤500 chars, prompt sections no >20% growth).
   - Semantic preservation (no drift from original purpose).
   - Caching compatibility (changes only take effect on new sessions).
7. **Deploy with approval** — Save evolved version + metrics + diff. Human (or you) reviews and accepts. Git-style lineage for rollback.

### Phases (Current Status & Roadmap)

- **Phase 1 (Skills)** — Fully implemented. Evolve SKILL.md bodies. CLI: `python -m evolution.skills.evolve_skill --skill <name> --iterations 10 --eval-source synthetic|sessiondb|golden`.
- **Phase 2 (Tool descriptions)** — Planned (optimize the `description` fields agents see when choosing tools).
- **Phase 3 (System prompt sections)** — Planned (MEMORY_GUIDANCE, SKILLS_GUIDANCE, tool usage rules, etc.).
- **Phase 4 (Code)** — Planned (Darwinian Evolver for tool implementations — higher risk, stricter gates).
- **Phase 5 (Continuous loop)** — Planned (monitor performance over time, auto-trigger when metrics drop, scheduled benchmark runs).

### Guardrails & Important Principles

- **Human review required** for deployment (never auto-commit).
- Benchmarks (TBLite-style, YC-Bench, etc.) are **gates**, not the fitness function. Fitness is task-specific (did this skill do its job better?).
- Holdout sets prevent overfitting.
- Every evolved artifact gets a full before/after report (scores, size delta, constraints, time, cost).
- Works on real session history (your actual Grok conversations) or synthetic data.

### Usage in Grok Build

**Basic (evolve one of your skills):**
"Use hermes-self-evolution to improve the `giga-landing-page` skill. Use 8 iterations, sessiondb for eval data, run the relevant tests."

I will:
- Load the current SKILL.md.
- Build or load an eval dataset (synthetic tasks + rubrics, or mine your past landing-page sessions).
- Run GEPA (or fallback).
- Validate constraints + holdout.
- Produce the evolved version + diff + metrics table + recommendation.
- Save outputs (evolved_skill.md, baseline, metrics.json, diff) under an `evolution_output/` or similar.
- Ask for approval before overwriting the live skill.

**Advanced:**
- Evolve tool descriptions across a category.
- Evolve a specific section of the system prompt ("improve how I decide when to use sub-agents").
- Mine a particular set of past sessions for high-signal failures/successes.
- Set up a recurring "skill audit + propose evolutions" cron-style task.
- Combine with `create-skill` (generate a new skill) then immediately evolve it.

**With your existing Grok skills:**
- Point it at any of the ported Hermes skills (giga-*, github-*, systematic-debugging, research-paper-writing, etc.).
- Use it on Grok-native skills (check-work, design, etc.) or the ones you create.
- The constraint system can call your test commands, run linters, size checks, etc.

### Implementation Notes for This Port

The original is a standalone Python package (`evolution/` with core/dataset_builder/fitness/constraints, skills/evolve_skill + skill_module).
In Grok Build we adapt it to:
- Use Grok's `run_terminal_command` to execute the evolution scripts or equivalent Python snippets.
- Use file tools (`read_file`, `write`, `search_replace`) to load/save SKILL.md and outputs.
- Leverage `spawn_subagent` for parallel evaluation of candidates if desired.
- Store datasets, outputs, and lineage in the workspace (or a dedicated `evolution/` folder).
- The core GEPA/DSPy logic can be run via installed packages or by calling out to the original repo if you have it cloned.

**To bootstrap:** If you have the `hermes-agent-self-evolution` package or the scripts, I can run them directly. Otherwise I can implement a lightweight in-Grok version of the loop (synthetic dataset generation + iterative refinement with explicit constraints and holdout scoring) that achieves the same spirit.

This is the ultimate meta-skill: it turns Grok Build into a self-improving system that gets better at the exact tasks you care about (your giga pipelines, research, code review, brand work, etc.) by learning from real usage. Highly recommended to run periodically on your most-used custom skills.


---

## Module 12: `hermes-web-ui`

- **Origine :** `01_Hermes_Skills_Core_Library\hermes\hermes-web-ui\SKILL.md`
- **Rôle / Objectif :** 启动、配置和排查 hermes-web-ui 面板，包括 Node.js 版本要求和 nvm 持久化配置。

## hermes-web-ui

hermes-web-ui 是 Hermes Agent 的浏览器图形界面，默认端口 8648，通过 hermes api_server（默认端口 8642）与 agent 通信。

启动成功后输出带 token 的完整访问地址，格式：
  http://localhost:8648/#/?token=<your_token>

### 常用命令

  start / stop / status / restart

日志位置：HOME/.hermes-web-ui/server.log

### 已知问题：node:sqlite 报错导致启动失败

#### 症状

日志报 ERR_UNKNOWN_BUILTIN_MODULE: No such built-in module: node:sqlite

#### 原因

hermes-web-ui 依赖 node:sqlite，该内置模块在 Node.js v22.5.0 才引入，v20 及以下会直接崩溃。

#### 修复步骤

1. 安装并切换 Node.js v22（通过 nvm）
2. 重装 hermes-web-ui（让 bin shebang 指向新 node 路径）
3. 验证 which hermes-web-ui 输出路径含 v22
4. 再次 start

#### 持久化 nvm 版本

在 .zshrc 中 nvm 加载行之后追加：
  nvm use 22 --silent

同时执行：
  nvm alias default 22

--silent 参数避免每次开终端打印版本提示。

### 开机自启动（macOS LaunchAgent）

plist 路径：`~/Library/LaunchAgents/ai.hermes.web-ui.plist`

#### 常见问题：plist 启动失败（exit code 1）

**原因1**：plist 里写的是旧版 node（如 v20）路径，但 hermes-web-ui 需要 v22+。  
检查：`launchctl list | grep hermes.web-ui` 看 exit code，exit code=1 即失败。  
修复：把 ProgramArguments 和 PATH 里的 node 路径改成 v22：
```
/Users/<用户名>/.nvm/versions/node/v22.x.x/bin/hermes-web-ui
```
查 v22 实际路径：`ls ~/.nvm/versions/node/v22*/bin/hermes-web-ui`

**原因2**：`hermes-web-ui start` 在服务已运行时返回 exit code 1（"already running"），LaunchAgent 会认为失败并不断重试。  
修复：用包装脚本替代直接调用：

```bash
## ~/.hermes/scripts/start-web-ui.sh
##!/bin/bash
HERMES_WEB_UI="/Users/<用户名>/.nvm/versions/node/v22.x.x/bin/hermes-web-ui"
if "$HERMES_WEB_UI" status 2>&1 | grep -q "is running"; then
    exit 0
fi
"$HERMES_WEB_UI" start
exit 0
```

plist ProgramArguments 改为：
```xml
<array>
    <string>/bin/bash</string>
    <string>/Users/<用户名>/.hermes/scripts/start-web-ui.sh</string>
</array>
```

重载 plist：
```bash
launchctl unload ~/Library/LaunchAgents/ai.hermes.web-ui.plist
launchctl load ~/Library/LaunchAgents/ai.hermes.web-ui.plist
launchctl list | grep hermes.web-ui  # exit code 应为 0
```

### api_server 配置（hermes 侧）

相关配置在 hermes config.yaml 的 platforms.api_server 节点下：
  enabled, host, port, key（token）, cors_origins

修改后执行 hermes gateway restart 生效。


---
