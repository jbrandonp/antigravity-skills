# One-click installer for Antigravity Skills & Plugins on Windows PowerShell
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$DestGemini = Join-Path $HOME ".gemini\config"
$DestSkills = Join-Path $DestGemini "skills"
$DestPlugins = Join-Path $DestGemini "plugins"

Write-Host "=== Installing Antigravity Skills & Plugins ===" -ForegroundColor Cyan

New-Item -ItemType Directory -Force -Path $DestSkills | Out-Null
New-Item -ItemType Directory -Force -Path $DestPlugins | Out-Null

$ScriptDir = Split-Path -Parent $PSScriptRoot

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

Write-Host "✓ Installation complete! Restart Google Antigravity to load all customizations." -ForegroundColor Green
