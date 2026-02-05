#!/usr/bin/env pwsh
<#
.SYNOPSIS
Install ayga-mcp-client in a clean virtual environment (Claude Desktop compatible)

.DESCRIPTION
Creates and configures a Python virtual environment specifically for ayga-mcp-client
to avoid dependency conflicts with other packages on your system.

.EXAMPLE
./setup-ayga-mcp.ps1

.NOTES
- Creates venv in: $env:USERPROFILE\.mcp\ayga-venv
- For Claude Desktop: Add to claude_desktop_config.json
- For VS Code: Add to mcp.json configuration
#>

param(
    [string]$VenvPath = "$env:USERPROFILE\.mcp\ayga-venv",
    [string]$ApiKey = ""
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 ayga-mcp-client Setup for Claude Desktop/Copilot" -ForegroundColor Cyan
Write-Host "=" * 70
Write-Host ""

# Step 1: Create venv directory
Write-Host "📁 Step 1: Creating virtual environment..." -ForegroundColor Yellow
Write-Host "   Location: $VenvPath"

if (Test-Path $VenvPath) {
    Write-Host "   ⚠️  Directory exists. Removing old venv..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $VenvPath
}

# Create parent directory
$VenvParent = Split-Path $VenvPath
if (-not (Test-Path $VenvParent)) {
    New-Item -ItemType Directory -Path $VenvParent -Force | Out-Null
}

# Create venv
python -m venv $VenvPath

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Virtual environment created" -ForegroundColor Green
Write-Host ""

# Step 2: Activate venv
Write-Host "🔌 Step 2: Activating virtual environment..." -ForegroundColor Yellow

$ActivateScript = "$VenvPath\Scripts\Activate.ps1"
if (-not (Test-Path $ActivateScript)) {
    Write-Host "❌ Activation script not found" -ForegroundColor Red
    exit 1
}

& $ActivateScript

Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Step 3: Upgrade pip
Write-Host "📦 Step 3: Upgrading pip and setuptools..." -ForegroundColor Yellow

python -m pip install --upgrade pip setuptools wheel 2>&1 | Where-Object { $_ -match "Successfully installed|Requirement already satisfied|Upgrade|already" } | ForEach-Object { Write-Host "   $_" }

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Warning: pip upgrade had issues, continuing..." -ForegroundColor Yellow
}

Write-Host "✅ pip upgraded" -ForegroundColor Green
Write-Host ""

# Step 4: Install ayga-mcp-client with latest version
Write-Host "🔍 Step 4: Installing ayga-mcp-client..." -ForegroundColor Yellow

# Install with --no-deps first to see what conflicts exist
Write-Host "   Installing dependencies..." -ForegroundColor Gray

python -m pip install "ayga-mcp-client>=1.4.1" 2>&1 | ForEach-Object {
    if ($_ -match "Successfully installed|Requirement already satisfied|Upgrading") {
        Write-Host "   ✅ $_" -ForegroundColor Green
    }
    elseif ($_ -match "ERROR|error") {
        Write-Host "   ❌ $_" -ForegroundColor Red
    }
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install ayga-mcp-client" -ForegroundColor Red
    exit 1
}

Write-Host "✅ ayga-mcp-client installed successfully" -ForegroundColor Green
Write-Host ""

# Step 5: Verify installation
Write-Host "✔️  Step 5: Verifying installation..." -ForegroundColor Yellow

$VerifyResult = python -c "import ayga_mcp_client; print(ayga_mcp_client.__version__ if hasattr(ayga_mcp_client, '__version__') else 'installed')" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Package imported successfully: $VerifyResult" -ForegroundColor Green
}
else {
    Write-Host "   ⚠️  Could not verify: $VerifyResult" -ForegroundColor Yellow
}

Write-Host "✅ Installation verified" -ForegroundColor Green
Write-Host ""

# Step 6: Show configuration instructions
Write-Host "=" * 70
Write-Host "📋 CONFIGURATION INSTRUCTIONS" -ForegroundColor Cyan
Write-Host "=" * 70
Write-Host ""

$PythonExe = "$VenvPath\Scripts\python.exe"
$ModuleExe = "-m ayga_mcp_client"

Write-Host "1️⃣  For Claude Desktop:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Edit: %APPDATA%\Claude\claude_desktop_config.json" -ForegroundColor Gray
Write-Host ""
Write-Host "   Add this configuration:" -ForegroundColor Gray
Write-Host ""

$Config = @"
{
  "mcpServers": {
    "ayga": {
      "command": "$PythonExe",
      "args": ["$ModuleExe"],
      "env": {
        "REDIS_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
"@

Write-Host $Config -ForegroundColor Cyan
Write-Host ""

Write-Host "2️⃣  For VS Code Copilot:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Edit: %APPDATA%\Code\User\mcp.json" -ForegroundColor Gray
Write-Host ""
Write-Host "   Add this configuration:" -ForegroundColor Gray
Write-Host ""

$VsConfig = @"
{
  "servers": {
    "ayga": {
      "type": "stdio",
      "command": "$PythonExe",
      "args": ["$ModuleExe"],
      "env": {
        "REDIS_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
"@

Write-Host $VsConfig -ForegroundColor Cyan
Write-Host ""

Write-Host "3️⃣  Get your API key:" -ForegroundColor Yellow
Write-Host "   🌐 https://redis.ayga.tech" -ForegroundColor Gray
Write-Host "   📧 Contact: support@ayga.tech" -ForegroundColor Gray
Write-Host ""

# Step 7: Test the installation
Write-Host "=" * 70
Write-Host "🧪 TESTING INSTALLATION" -ForegroundColor Cyan
Write-Host "=" * 70
Write-Host ""

Write-Host "Running ayga-mcp-client..." -ForegroundColor Yellow

# Create a simple test to show server is working
$TestCode = @"
import asyncio
from ayga_mcp_client.server import create_mcp_server

async def test():
    try:
        server = create_mcp_server("test")
        print("✅ Server created successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

asyncio.run(test())
"@

$TestResult = python -c $TestCode 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host $TestResult -ForegroundColor Green
}
else {
    Write-Host $TestResult -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 70
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "=" * 70
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Replace YOUR_API_KEY_HERE with your actual API key"
Write-Host "2. Restart Claude Desktop or VS Code"
Write-Host "3. The ayga MCP server will be available in your AI tools"
Write-Host ""
Write-Host "To reactivate venv in future:" -ForegroundColor Gray
Write-Host "  & '$ActivateScript'" -ForegroundColor DarkGray
Write-Host ""
