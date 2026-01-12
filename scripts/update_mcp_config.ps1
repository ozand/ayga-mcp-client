# Update VS Code mcp.json - Change 'redis-api' to 'ayga-mcp-client'

$mcpConfigPath = "$env:APPDATA\Code\User\mcp.json"

Write-Host "Updating VS Code MCP configuration..." -ForegroundColor Cyan
Write-Host "File: $mcpConfigPath`n" -ForegroundColor Gray

if (-not (Test-Path $mcpConfigPath)) {
    Write-Host "Error: mcp.json not found at $mcpConfigPath" -ForegroundColor Red
    exit 1
}

# Backup original
$backupPath = "$mcpConfigPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $mcpConfigPath $backupPath
Write-Host "✓ Backup created: $backupPath" -ForegroundColor Green

# Read config
$content = Get-Content $mcpConfigPath -Raw

# Check if redis-api or ayga-mcp-client exists
$oldName = $null
if ($content -match '"redis-api"') {
    $oldName = "redis-api"
}
elseif ($content -match '"ayga-mcp-client"') {
    $oldName = "ayga-mcp-client"
}

if (-not $oldName) {
    Write-Host "`n⚠️  No known server name found in config" -ForegroundColor Yellow
    Write-Host "Current servers in config:" -ForegroundColor Gray
    
    # Show current servers
    $json = $content | ConvertFrom-Json
    $json.servers.PSObject.Properties.Name | ForEach-Object {
        Write-Host "  - $_" -ForegroundColor White
    }
    
    exit 0
}

# Replace with 'ayga' (short name)
$newContent = $content -replace "`"$oldName`"", '"ayga"'

# Save updated config
Set-Content -Path $mcpConfigPath -Value $newContent -NoNewline

Write-Host "✓ Updated server name: '$oldName' → 'ayga'" -ForegroundColor Green

# Verify change
$verifyContent = Get-Content $mcpConfigPath -Raw
if ($verifyContent -match '"ayga"') {
    Write-Host "✓ Verification: Change applied successfully" -ForegroundColor Green
}
else {
    Write-Host "✗ Verification failed!" -ForegroundColor Red
    # Restore backup
    Copy-Item $backupPath $mcpConfigPath -Force
    Write-Host "✓ Restored from backup" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Reload VS Code window: Ctrl+Shift+P → 'Developer: Reload Window'" -ForegroundColor White
Write-Host "2. Test with: @ayga list_parsers" -ForegroundColor White
Write-Host "`nUsage changed to short name:" -ForegroundColor Gray
Write-Host "  @ayga search_perplexity query=\"test\"" -ForegroundColor White
Write-Host "  @ayga translate_google_translate query=\"Hello\" to_language=\"ru\"" -ForegroundColor White
