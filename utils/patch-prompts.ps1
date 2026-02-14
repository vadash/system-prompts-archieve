#!/usr/bin/env pwsh
# --- Functions (dot-sourceable for testing) ---

function Invoke-EscapeBackticks {
    param([string]$Text)
    if (-not $Text) { return $Text }
    # Negative lookbehind: match ` not preceded by \
    return [regex]::Replace($Text, '(?<!\\)`', '\`')
}

function Invoke-FixLineEndings {
    param([string]$Text)
    if (-not $Text) { return $Text }
    return $Text -replace "`r`n", "`n"
}

# --- Main execution (only when run directly, not dot-sourced) ---
# Guard: $MyInvocation.InvocationName is "." when dot-sourced
if ($MyInvocation.InvocationName -ne ".") {
    # Main logic goes here in later tasks
    Write-Host "patch-prompts: not yet implemented" -ForegroundColor Yellow
}
