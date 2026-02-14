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

function Get-PatchableFiles {
    param([string]$Path)

    $binaryExtensions = @(
        '.exe', '.dll', '.so', '.dylib', '.bin', '.dat',
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.zip', '.tar', '.gz', '.rar', '.7z',
        '.mp3', '.mp4', '.avi', '.mov', '.wav', '.flac',
        '.ttf', '.otf', '.woff', '.woff2', '.eot',
        '.pyc', '.class', '.jar', '.war', '.ear'
    )
    $skipDirs = @('.git', '.svn', 'node_modules', 'vendor', 'target', 'bin', 'obj')

    Get-ChildItem -Path $Path -Recurse -File | Where-Object {
        foreach ($dir in $skipDirs) {
            if ($_.FullName -like "*\$dir\*") { return $false }
        }
        $ext = $_.Extension.ToLower()
        return $ext -notin $binaryExtensions
    }
}

# --- Main execution (only when run directly, not dot-sourced) ---
# Guard: $MyInvocation.InvocationName is "." when dot-sourced
if ($MyInvocation.InvocationName -ne ".") {
    # Main logic goes here in later tasks
    Write-Host "patch-prompts: not yet implemented" -ForegroundColor Yellow
}
