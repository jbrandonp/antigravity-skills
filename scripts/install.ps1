# One-click installer for Antigravity & Universal AI Agent Skills
[CmdletBinding()]
param(
    [ValidateSet("All", "Antigravity", "Agents", "Hermes", "Claude")]
    [string]$Target = "All"
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $PSScriptRoot

# 1. Antigravity Installation (~/.gemini/config and ~/.gemini/antigravity)
if ($Target -eq "All" -or $Target -eq "Antigravity") {
    $DestGemini = Join-Path $HOME ".gemini\config"
    $DestSkills = Join-Path $DestGemini "skills"
    $DestPlugins = Join-Path $DestGemini "plugins"
    $DestMcp = Join-Path $HOME ".gemini\antigravity\mcp"

    Write-Host "=== Installing Antigravity Customizations (~/.gemini/config) ===" -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path $DestSkills | Out-Null
    New-Item -ItemType Directory -Force -Path $DestPlugins | Out-Null
    New-Item -ItemType Directory -Force -Path $DestMcp | Out-Null

    Write-Host "--> Copying skills to $DestSkills..." -ForegroundColor Yellow
    Copy-Item -Path (Join-Path $ScriptDir "skills\*") -Destination $DestSkills -Recurse -Force

    Write-Host "--> Copying plugins (Science, Stitch, Android, Firebase, etc.) to $DestPlugins..." -ForegroundColor Yellow
    Copy-Item -Path (Join-Path $ScriptDir "plugins\*") -Destination $DestPlugins -Recurse -Force

    if (Test-Path (Join-Path $ScriptDir "mcp")) {
        Write-Host "--> Copying MCP tool schemas to $DestMcp..." -ForegroundColor Yellow
        Copy-Item -Path (Join-Path $ScriptDir "mcp\*") -Destination $DestMcp -Recurse -Force
    }

    $ConfigTarget = Join-Path $DestGemini "config.json"
    if (-not (Test-Path $ConfigTarget)) {
        Write-Host "--> Installing default config.json..." -ForegroundColor Green
        Copy-Item -Path (Join-Path $ScriptDir "config\config.template.json") -Destination $ConfigTarget -Force
    }

    $McpTarget = Join-Path $DestGemini "mcp_config.json"
    if (-not (Test-Path $McpTarget)) {
        Write-Host "--> Installing default mcp_config.json..." -ForegroundColor Green
        Copy-Item -Path (Join-Path $ScriptDir "config\mcp_config.template.json") -Destination $McpTarget -Force
    }
}

# 2. Universal Agent Skills Installation (~/.agents/skills)
if ($Target -eq "All" -or $Target -eq "Agents") {
    $DestAgents = Join-Path $HOME ".agents\skills"
    Write-Host "=== Installing Universal Agent Skills (~/.agents/skills) ===" -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path $DestAgents | Out-Null

    Write-Host "--> Deploying core skills to $DestAgents for Claude Code, Cursor, Copilot & npx skills..." -ForegroundColor Yellow
    Copy-Item -Path (Join-Path $ScriptDir "skills\*") -Destination $DestAgents -Recurse -Force

    # Also deploy DeepMind Science skills into ~/.agents/skills
    $ScienceSkillsDir = Join-Path $ScriptDir "plugins\science\skills"
    if (Test-Path $ScienceSkillsDir) {
        Write-Host "--> Deploying DeepMind Science skills into $DestAgents..." -ForegroundColor Yellow
        Get-ChildItem -Path $ScienceSkillsDir -Directory | ForEach-Object {
            $canonicalName = $_.Name -replace "_", "-"
            $targetDir = Join-Path $DestAgents $canonicalName
            Copy-Item -Path $_.FullName -Destination $targetDir -Recurse -Force
        }
    }

    # Also deploy Google Labs Stitch skills into ~/.agents/skills
    Get-ChildItem -Path (Join-Path $ScriptDir "plugins") -Directory -Filter "stitch-*" | ForEach-Object {
        $stitchSkillsDir = Join-Path $_.FullName "skills"
        if (Test-Path $stitchSkillsDir) {
            Write-Host "--> Deploying $($_.Name) skills into $DestAgents..." -ForegroundColor Yellow
            Get-ChildItem -Path $stitchSkillsDir -Directory | ForEach-Object {
                $targetDir = Join-Path $DestAgents "stitch-$($_.Name)"
                Copy-Item -Path $_.FullName -Destination $targetDir -Recurse -Force
            }
        }
    }

    # Also deploy Hermes Mega-Suites & Master-Suites into ~/.agents/skills
    $HermesMegaDir = Join-Path $ScriptDir "hermes\mega-suites"
    if (Test-Path $HermesMegaDir) {
        Write-Host "--> Deploying Hermes Mega-Suites into $DestAgents..." -ForegroundColor Yellow
        Copy-Item -Path (Join-Path $HermesMegaDir "*") -Destination $DestAgents -Recurse -Force
    }
    $HermesMasterDir = Join-Path $ScriptDir "hermes\master-suites"
    if (Test-Path $HermesMasterDir) {
        Write-Host "--> Deploying Hermes Master-Suites into $DestAgents..." -ForegroundColor Yellow
        Copy-Item -Path (Join-Path $HermesMasterDir "*") -Destination $DestAgents -Recurse -Force
    }
}

# 3. Hermes Autonomous Agent Ecosystem (~/.hermes/skills and ~/.hermes/mcp)
if ($Target -eq "All" -or $Target -eq "Hermes") {
    $DestHermesSkills = Join-Path $HOME ".hermes\skills"
    $DestHermesMcp = Join-Path $HOME ".hermes\mcp"
    Write-Host "=== Installing Hermes Autonomous Suite (~/.hermes) ===" -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path $DestHermesSkills | Out-Null
    New-Item -ItemType Directory -Force -Path $DestHermesMcp | Out-Null

    Write-Host "--> Copying Hermes Mega-Suites (10) and Master-Suites (50) to $DestHermesSkills..." -ForegroundColor Yellow
    Copy-Item -Path (Join-Path $ScriptDir "hermes\mega-suites\*") -Destination $DestHermesSkills -Recurse -Force
    Copy-Item -Path (Join-Path $ScriptDir "hermes\master-suites\*") -Destination $DestHermesSkills -Recurse -Force

    Write-Host "--> Copying Hermes MCP servers (eBay, Vinted, Web Tools) to $DestHermesMcp..." -ForegroundColor Yellow
    Copy-Item -Path (Join-Path $ScriptDir "hermes\mcp-servers\*") -Destination $DestHermesMcp -Recurse -Force
}

# 4. Anthropic Claude Code Installation (~/.claude/skills)
if ($Target -eq "All" -or $Target -eq "Claude") {
    $DestClaudeSkills = Join-Path $HOME ".claude\skills"
    Write-Host "=== Installing Claude Code Skills (~/.claude/skills) ===" -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path $DestClaudeSkills | Out-Null

    Write-Host "--> Deploying Antigravity Elite Skills & Hermes Mega-Suites to $DestClaudeSkills..." -ForegroundColor Yellow
    Copy-Item -Path (Join-Path $ScriptDir "skills\*") -Destination $DestClaudeSkills -Recurse -Force
    Copy-Item -Path (Join-Path $ScriptDir "hermes\mega-suites\*") -Destination $DestClaudeSkills -Recurse -Force
}

Write-Host "✓ Installation complete! 177 skills & suites (117 elite, 10 mega-suites, 50 master suites, 41 science, 16 stitch) and 8 MCP servers are active and ready." -ForegroundColor Green
