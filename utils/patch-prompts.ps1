#!/usr/bin/env pwsh
param([string]$Path)

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

function Invoke-Fixers {
    param([string]$Path)

    $fixers = @(
        [PSCustomObject]@{
            Name   = "Escape backticks"
            Filter = "*.md"
            Action = {
                param($filePath)
                $content = [System.IO.File]::ReadAllText($filePath)
                $fixed = Invoke-EscapeBackticks $content
                if ($fixed -ne $content) {
                    [System.IO.File]::WriteAllText($filePath, $fixed)
                    return $true
                }
                return $false
            }
        },
        [PSCustomObject]@{
            Name   = "Fix line endings"
            Filter = "*"
            Action = {
                param($filePath)
                $bytes = [System.IO.File]::ReadAllBytes($filePath)
                $hasCRLF = $false
                for ($i = 0; $i -lt ($bytes.Length - 1); $i++) {
                    if ($bytes[$i] -eq 13 -and $bytes[$i + 1] -eq 10) {
                        $hasCRLF = $true; break
                    }
                }
                if ($hasCRLF) {
                    $content = [System.IO.File]::ReadAllText($filePath)
                    $fixed = Invoke-FixLineEndings $content
                    [System.IO.File]::WriteAllText($filePath, $fixed)
                    return $true
                }
                return $false
            }
        }
    )

    $allFiles = Get-PatchableFiles -Path $Path
    Write-Host "Found $($allFiles.Count) files." -ForegroundColor Cyan

    foreach ($fixer in $fixers) {
        $matchingFiles = $allFiles | Where-Object {
            $fixer.Filter -eq "*" -or $_.Name -like $fixer.Filter
        }
        $fixedCount = 0
        Write-Host "`n[$($fixer.Name)] Processing $($matchingFiles.Count) files..." -ForegroundColor Cyan

        foreach ($file in $matchingFiles) {
            try {
                $wasFixed = & $fixer.Action $file.FullName
                if ($wasFixed) {
                    $fixedCount++
                    $relPath = $file.FullName.Substring($Path.Length + 1)
                    Write-Host "  [FIXED] $relPath" -ForegroundColor Green
                }
            } catch {
                Write-Host "  [ERROR] $($file.FullName): $_" -ForegroundColor Red
            }
        }

        Write-Host "  $fixedCount file(s) fixed." -ForegroundColor White
    }
}

# --- Main execution (only when run directly, not dot-sourced) ---
# Guard: $MyInvocation.InvocationName is "." when dot-sourced
if ($MyInvocation.InvocationName -ne ".") {
    if (-not $Path) {
        $Path = Read-Host "Enter directory path to patch"
    }

    if (-not (Test-Path $Path -PathType Container)) {
        Write-Host "Error: '$Path' is not a valid directory." -ForegroundColor Red
        exit 1
    }

    $Path = (Resolve-Path $Path).Path
    Write-Host "Scanning '$Path'..." -ForegroundColor Cyan
    Invoke-Fixers -Path $Path
    Write-Host "`nDone." -ForegroundColor Green
}
