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
