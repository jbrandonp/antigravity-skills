# One-click installer for Antigravity & Universal AI Agent Skills
[CmdletBinding()]
param(
    [ValidateSet("All", "Antigravity", "Agents")]
    [string]$Target = "All"
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $PSScriptRoot

# 1. Antigravity Installation (~/.gemini/config)
if ($Target -eq "All" -or $Target -eq "Antigravity") {
    $DestGemini = Join-Path $HOME ".gemini\config"
    $DestSkills = Join-Path $DestGemini "skills"
    $DestPlugins = Join-Path $DestGemini "plugins"

    Write-Host "=== Installing Antigravity Customizations (~/.gemini/config) ===" -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path $DestSkills | Out-Null
    New-Item -ItemType Directory -Force -Path $DestPlugins | Out-Null

    Write-Host "--> Copying skills to $DestSkills..." -ForegroundColor Yellow
    Copy-Item -Path (Join-Path $ScriptDir "skills\*") -Destination $DestSkills -Recurse -Force

    Write-Host "--> Copying plugins to $DestPlugins..." -ForegroundColor Yellow
    Copy-Item -Path (Join-Path $ScriptDir "plugins\*") -Destination $DestPlugins -Recurse -Force

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

    Write-Host "--> Deploying skills to $DestAgents for Claude Code, Cursor, Copilot & npx skills..." -ForegroundColor Yellow
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
}

Write-Host "✓ Installation complete! All skills and plugins are active and ready." -ForegroundColor Green
