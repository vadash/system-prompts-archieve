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
