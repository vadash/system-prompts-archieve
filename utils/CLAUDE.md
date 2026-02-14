# PowerShell Script Testing Guidelines

## When running pwsh commands from Bash tool

**CRITICAL:** `${}` in PowerShell strings will be interpreted by bash before reaching pwsh.

### Wrong (causes syntax errors in bash):
```bash
pwsh -Command "Invoke-EscapeBackticks '${K?\"test\":\"fail\"}'"
# bash interprets ${K} as a variable → Error: K: test:fail
```

### Right (use -File with a script, or escape carefully):

**Option 1: Use -File (RECOMMENDED for tests)**
```bash
# Create a .ps1 file with your test
pwsh -File "C:\path\to\test.ps1"
```

**Option 2: Use single-quoted bash string with escaped ${**
```bash
pwsh -Command 'Invoke-EscapeBackticks ([char]96 + ''''${}'''' + ''K?testfail'')'
# Still error-prone - avoid this pattern
```

**Option 3: Here-string in .ps1 file (BEST)**
```powershell
# In test.ps1:
. "$PSScriptRoot\patch-prompts.ps1"

$bt = [char]96
$dlr = [char]36
$openBrace = [char]123
$closeBrace = [char]125

$input = $bt + $dlr + $openBrace + 'test' + $closeBrace
$result = Invoke-EscapeBackticks $input
```

## Pester Testing

**Old Pester (v3.4.0):** No `-OutputStyle` parameter
```bash
# Wrong
pwsh -Command "Invoke-Pester test.ps1 -OutputStyle Minimal"

# Right
pwsh -Command "Invoke-Pester test.ps1"
```

## File Writing for Tests

**Wrong:** Try to use Set-Content with `-Encoding Byte` (not supported in older PowerShell)

**Right:** Use .NET methods directly
```powershell
[System.IO.File]::WriteAllText(
    "$testDir\test.md",
    "inline ``code`` here",
    [System.Text.UTF8Encoding]::new($false)  # $false = no BOM
)
```

## Debugging String Issues

When you see unexpected output with special characters:
1. Write chars with their byte values: `$s.ToCharArray() | ForEach-Object { Write-Host "$($_)=[{0}]" -f ([int][char]$_) }`
2. Or create a .ps1 file to avoid shell interpretation issues
