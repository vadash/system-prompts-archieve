# Implementation Plan - patch-prompts.ps1

> **Reference:** `docs/designs/2026-02-14-patch-prompts-design.md`
> **Execution:** Use `executing-plans` skill.

## Prerequisites

- Pester 3.4.0+ (already installed, verify with `Get-Module -ListAvailable Pester`)
- Run tests: `powershell -c "Invoke-Pester utils/patch-prompts.Tests.ps1 -Verbose"`

## Architecture Note: Testability

The script is split into **functions** (dot-sourceable by tests) and a **main block** (guarded so it only runs when executed directly, not dot-sourced). This is the standard PowerShell pattern for testable scripts.

```
utils/
  patch-prompts.ps1          # Functions + guarded main
  patch-prompts.Tests.ps1    # Pester tests
```

---

### Task 1: Backtick Escaping Function + Tests

**Goal:** Create and test the core `Invoke-EscapeBackticks` function that escapes unescaped backticks in a string.

**Step 1: Write the Failing Test**
- File: `utils/patch-prompts.Tests.ps1`
- Code:
  ```powershell
  # Dot-source the script to import functions
  . "$PSScriptRoot\patch-prompts.ps1"

  Describe "Invoke-EscapeBackticks" {
      It "escapes a single unescaped backtick" {
          $result = Invoke-EscapeBackticks 'Hello `world`'
          $result | Should Be 'Hello \`world\`'
      }

      It "does NOT double-escape already-escaped backticks" {
          $result = Invoke-EscapeBackticks 'Already \`escaped\`'
          $result | Should Be 'Already \`escaped\`'
      }

      It "escapes triple backticks (code fences)" {
          $result = Invoke-EscapeBackticks '```python'
          $result | Should Be '\`\`\`python'
      }

      It "handles mixed escaped and unescaped" {
          $result = Invoke-EscapeBackticks 'mix \`ok` and `raw\`'
          $result | Should Be 'mix \`ok\` and \`raw\`'
      }

      It "returns unchanged string with no backticks" {
          $result = Invoke-EscapeBackticks 'no backticks here'
          $result | Should Be 'no backticks here'
      }

      It "handles empty string" {
          $result = Invoke-EscapeBackticks ''
          $result | Should Be ''
      }
  }
  ```

**Step 2: Run Test (Red)**
- Command: `powershell -c "Invoke-Pester utils/patch-prompts.Tests.ps1 -Verbose"`
- Expect: Fail — function `Invoke-EscapeBackticks` not found

**Step 3: Implementation (Green)**
- File: `utils/patch-prompts.ps1`
- Action: Create script with the function. Use regex negative lookbehind to only escape unescaped backticks.
- Code:
  ```powershell
  #!/usr/bin/env pwsh
  # --- Functions (dot-sourceable for testing) ---

  function Invoke-EscapeBackticks {
      param([string]$Text)
      if (-not $Text) { return $Text }
      # Negative lookbehind: match ` not preceded by \
      return [regex]::Replace($Text, '(?<!\\)`', '\`')
  }

  # --- Main execution (only when run directly, not dot-sourced) ---
  # Guard: $MyInvocation.InvocationName is "." when dot-sourced
  if ($MyInvocation.InvocationName -ne ".") {
      # Main logic goes here in later tasks
      Write-Host "patch-prompts: not yet implemented" -ForegroundColor Yellow
  }
  ```

**Step 4: Verify (Green)**
- Command: `powershell -c "Invoke-Pester utils/patch-prompts.Tests.ps1 -Verbose"`
- Expect: All 6 tests PASS

**Step 5: Git Commit**
- `git add utils/patch-prompts.ps1 utils/patch-prompts.Tests.ps1`
- `git commit -m "feat: add Invoke-EscapeBackticks with Pester tests"`

---

### Task 2: Line Ending Fix Function + Tests

**Goal:** Create and test `Invoke-FixLineEndings` that converts CRLF to LF in a string.

**Step 1: Write the Failing Test**
- File: `utils/patch-prompts.Tests.ps1` (append to existing)
- Code:
  ```powershell
  Describe "Invoke-FixLineEndings" {
      It "converts CRLF to LF" {
          $result = Invoke-FixLineEndings "line1`r`nline2`r`n"
          $result | Should Be "line1`nline2`n"
      }

      It "leaves LF-only content unchanged" {
          $result = Invoke-FixLineEndings "line1`nline2`n"
          $result | Should Be "line1`nline2`n"
      }

      It "handles mixed CRLF and LF" {
          $result = Invoke-FixLineEndings "crlf`r`nlf`nmore`r`n"
          $result | Should Be "crlf`nlf`nmore`n"
      }

      It "handles empty string" {
          $result = Invoke-FixLineEndings ''
          $result | Should Be ''
      }
  }
  ```

**Step 2: Run Test (Red)**
- Command: `powershell -c "Invoke-Pester utils/patch-prompts.Tests.ps1 -Verbose"`
- Expect: Fail — function `Invoke-FixLineEndings` not found

**Step 3: Implementation (Green)**
- File: `utils/patch-prompts.ps1`
- Action: Add function after `Invoke-EscapeBackticks`:
  ```powershell
  function Invoke-FixLineEndings {
      param([string]$Text)
      if (-not $Text) { return $Text }
      return $Text -replace "`r`n", "`n"
  }
  ```

**Step 4: Verify (Green)**
- Command: `powershell -c "Invoke-Pester utils/patch-prompts.Tests.ps1 -Verbose"`
- Expect: All 10 tests PASS (6 + 4)

**Step 5: Git Commit**
- `git add utils/patch-prompts.ps1 utils/patch-prompts.Tests.ps1`
- `git commit -m "feat: add Invoke-FixLineEndings with Pester tests"`

---

### Task 3: File Collection Function + Tests

**Goal:** Create and test `Get-PatchableFiles` that recursively finds text files, skipping binaries and ignored directories.

**Step 1: Write the Failing Test**
- File: `utils/patch-prompts.Tests.ps1` (append)
- Code:
  ```powershell
  Describe "Get-PatchableFiles" {
      $testDir = Join-Path $TestDrive "patchtest"

      BeforeEach {
          # Create test directory structure
          New-Item -ItemType Directory -Path $testDir -Force | Out-Null
          New-Item -ItemType Directory -Path "$testDir\.git" -Force | Out-Null
          New-Item -ItemType Directory -Path "$testDir\sub" -Force | Out-Null

          # Text files (should be found)
          "hello" | Set-Content "$testDir\readme.md"
          "world" | Set-Content "$testDir\sub\notes.txt"

          # Binary file (should be skipped)
          [byte[]]@(0,1,2) | Set-Content "$testDir\image.png" -Encoding Byte

          # File inside .git (should be skipped)
          "gitfile" | Set-Content "$testDir\.git\config"
      }

      It "finds text files recursively" {
          $files = Get-PatchableFiles -Path $testDir
          $files.Count | Should Be 2
      }

      It "skips .git directory" {
          $files = Get-PatchableFiles -Path $testDir
          ($files | Where-Object { $_.FullName -like "*\.git\*" }).Count | Should Be 0
      }

      It "skips binary extensions" {
          $files = Get-PatchableFiles -Path $testDir
          ($files | Where-Object { $_.Extension -eq ".png" }).Count | Should Be 0
      }
  }
  ```

**Step 2: Run Test (Red)**
- Command: `powershell -c "Invoke-Pester utils/patch-prompts.Tests.ps1 -Verbose"`
- Expect: Fail — function `Get-PatchableFiles` not found

**Step 3: Implementation (Green)**
- File: `utils/patch-prompts.ps1`
- Action: Add function. Reuse the binary extensions and skip-dirs lists from the old `fix-line-endings.ps1`:
  ```powershell
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
  ```

**Step 4: Verify (Green)**
- Command: `powershell -c "Invoke-Pester utils/patch-prompts.Tests.ps1 -Verbose"`
- Expect: All 13 tests PASS (6 + 4 + 3)

**Step 5: Git Commit**
- `git add utils/patch-prompts.ps1 utils/patch-prompts.Tests.ps1`
- `git commit -m "feat: add Get-PatchableFiles with Pester tests"`

---

### Task 4: Fixer Pipeline + Main Script Integration

**Goal:** Wire up the fixer array, main execution block, and `-Path` parameter with interactive fallback.

**Step 1: Write the Failing Test**
- File: `utils/patch-prompts.Tests.ps1` (append)
- Code:
  ```powershell
  Describe "Invoke-Fixers (integration)" {
      $testDir = Join-Path $TestDrive "integration"

      BeforeEach {
          New-Item -ItemType Directory -Path $testDir -Force | Out-Null
          # MD file with unescaped backticks AND CRLF
          [System.IO.File]::WriteAllText(
              "$testDir\test.md",
              "inline `code` here`r`n",
              [System.Text.UTF8Encoding]::new($false)
          )
          # TXT file with only CRLF (no backtick issue)
          [System.IO.File]::WriteAllText(
              "$testDir\plain.txt",
              "line1`r`nline2`r`n",
              [System.Text.UTF8Encoding]::new($false)
          )
      }

      It "escapes backticks in .md files" {
          Invoke-Fixers -Path $testDir
          $content = [System.IO.File]::ReadAllText("$testDir\test.md")
          $content | Should Match ([regex]::Escape('\`'))
          $content | Should Not Match '(?<!\\)`'
      }

      It "fixes line endings in all files" {
          Invoke-Fixers -Path $testDir
          $mdContent = [System.IO.File]::ReadAllText("$testDir\test.md")
          $txtContent = [System.IO.File]::ReadAllText("$testDir\plain.txt")
          $mdContent | Should Not Match "`r"
          $txtContent | Should Not Match "`r"
      }

      It "does not double-escape on second run" {
          Invoke-Fixers -Path $testDir
          Invoke-Fixers -Path $testDir  # run again
          $content = [System.IO.File]::ReadAllText("$testDir\test.md")
          # Should have \` not \\`
          $content | Should Not Match ([regex]::Escape('\\`'))
      }
  }
  ```

**Step 2: Run Test (Red)**
- Command: `powershell -c "Invoke-Pester utils/patch-prompts.Tests.ps1 -Verbose"`
- Expect: Fail — function `Invoke-Fixers` not found

**Step 3: Implementation (Green)**
- File: `utils/patch-prompts.ps1`
- Action: Add `Invoke-Fixers` function and complete the main block.
- Key code for `Invoke-Fixers`:
  ```powershell
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
  ```
- Main block (update the guard):
  ```powershell
  if ($MyInvocation.InvocationName -ne ".") {
      param([string]$Path)

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
  ```
  **Note:** `param()` must be at the top of the script, not inside the guard. Restructure so `param` is the first statement after the shebang, and the guard wraps only the execution logic.

**Step 4: Verify (Green)**
- Command: `powershell -c "Invoke-Pester utils/patch-prompts.Tests.ps1 -Verbose"`
- Expect: All 16 tests PASS (6 + 4 + 3 + 3)

**Step 5: Git Commit**
- `git add utils/patch-prompts.ps1 utils/patch-prompts.Tests.ps1`
- `git commit -m "feat: add fixer pipeline and main execution block"`

---

### Task 5: Delete Old Script + Final Verification

**Goal:** Remove `utils/fix-line-endings.ps1` and run full test suite.

**Step 1: Delete**
- Command: `git rm utils/fix-line-endings.ps1`

**Step 2: Verify nothing breaks**
- Command: `powershell -c "Invoke-Pester utils/patch-prompts.Tests.ps1 -Verbose"`
- Expect: All 16 tests PASS

**Step 3: Manual smoke test**
- Command: `powershell -c ".\utils\patch-prompts.ps1 -Path 'C:\Users\vadash\.tweakcc\system-prompts-archieve'"`
- Expect: See output listing fixed files, no errors

**Step 4: Git Commit**
- `git rm utils/fix-line-endings.ps1`
- `git add -A && git commit -m "refactor: remove fix-line-endings.ps1, absorbed into patch-prompts"`
