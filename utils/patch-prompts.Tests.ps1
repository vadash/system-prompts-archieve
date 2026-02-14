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

    It "escapes template literal syntax `${ to `${" {
        $result = Invoke-EscapeBackticks '`${K?"test":"fail"}'
        # Escapes both backtick (` → \`) and template literal (${ → \${)
        $result | Should Be '\`\${K?"test":"fail"}'
    }

    It "does NOT double-escape already-escaped `${" {
        $result = Invoke-EscapeBackticks '\\`\${already}'
        # Both already escaped, should remain unchanged
        $result | Should Be '\\`\${already}'
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

Describe "Invoke-Fixers (integration)" {
    $testDir = Join-Path $TestDrive "integration"

    BeforeEach {
        New-Item -ItemType Directory -Path $testDir -Force | Out-Null
        # MD file with unescaped backticks AND CRLF
        # Use escaped backticks to create literal backticks in file
        [System.IO.File]::WriteAllText(
            "$testDir\test.md",
            "inline ``code`` here`r`n",
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
