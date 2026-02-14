#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Convert Windows line endings (CRLF) to Unix (LF) recursively.

.DESCRIPTION
    Recursively processes all text files in the current directory and subfolders,
    replacing CRLF (\r\n) with LF (\n) line endings.

.EXAMPLE
    .\fix-line-endings.ps1
#>

$ErrorActionPreference = "Continue"

# Counters
$filesProcessed = 0
$filesSkipped = 0
$totalFiles = 0

# Get current directory
$rootPath = $PWD.Path

Write-Host "Scanning '$rootPath' for files with CRLF endings..." -ForegroundColor Cyan

# Find all files, skip common binary extensions and directories
$files = Get-ChildItem -Path $rootPath -Recurse -File | Where-Object {
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

    # Skip by directory
    foreach ($dir in $skipDirs) {
        if ($_.FullName -like "*\$dir\*") { return $false }
    }

    # Skip by extension
    $ext = $_.Extension.ToLower()
    return $ext -notin $binaryExtensions
}

$totalFiles = $files.Count

if ($totalFiles -eq 0) {
    Write-Host "No files found to process." -ForegroundColor Yellow
    exit 0
}

Write-Host "Found $totalFiles files. Checking for CRLF..." -ForegroundColor Cyan

foreach ($file in $files) {
    try {
        # Read file as raw bytes to detect line endings
        $content = [System.IO.File]::ReadAllBytes($file.FullName)

        # Check if file contains CRLF
        $hasCRLF = $false
        for ($i = 0; $i -lt ($content.Length - 1); $i++) {
            if ($content[$i] -eq 13 -and $content[$i + 1] -eq 10) {
                $hasCRLF = $true
                break
            }
        }

        if ($hasCRLF) {
            # Convert CRLF to LF
            $text = [System.IO.File]::ReadAllText($file.FullName)
            $fixedText = $text -replace "`r`n", "`n"
            [System.IO.File]::WriteAllText($file.FullName, $fixedText)
            $filesProcessed++
            Write-Host "  [FIXED] $($file.FullName.Substring($rootPath.Length + 1))" -ForegroundColor Green
        } else {
            $filesSkipped++
        }
    }
    catch {
        Write-Host "  [ERROR] $($file.FullName): $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Total files scanned: $totalFiles" -ForegroundColor White
Write-Host "  Files fixed:         $filesProcessed" -ForegroundColor Green
Write-Host "  Files skipped:       $filesSkipped" -ForegroundColor Gray
