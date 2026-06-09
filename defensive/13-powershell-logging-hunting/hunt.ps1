# Teaching hunt harness for Defensive Module 13 — PowerShell Logging & Hunting.
# Reads bundled Script Block Logging (Event ID 4104) records and flags the script blocks
# that carry known PowerShell-abuse indicators. The point isn't this script — it's learning
# which FIELDS and PATTERNS matter, so you can write the hunt yourself (and as a Sigma rule).
param(
    [string]$Path = '/lab/data/scriptblock-4104.json'
)

# High-signal indicators an analyst recognises on sight. Each is (name, regex, note).
$indicators = @(
    @{ Name = 'RemoteDownload';   Pattern = 'Download(String|Data|File)';                     Note = 'pulls a payload over the network (Net.WebClient)' }
    @{ Name = 'InMemoryExec';     Pattern = '\b(IEX|Invoke-Expression)\b';                     Note = 'executes a string in memory — nothing written to disk' }
    @{ Name = 'Base64Payload';    Pattern = 'FromBase64String';                                Note = 'decodes an embedded Base64 payload at runtime' }
    @{ Name = 'AmsiTamper';       Pattern = 'amsiInitFailed|AmsiUtils';                        Note = 'disables AMSI so later payloads are not scanned' }
    @{ Name = 'CharObfuscation';  Pattern = '(\[char\]\d+\s*\+\s*){3,}';                       Note = 'rebuilds a command from [char] codes to dodge string matching' }
    @{ Name = 'EncodedCommand';   Pattern = '-e(nc|ncodedcommand)\b';                          Note = 'ran from a Base64 -EncodedCommand blob' }
)

$events = Get-Content -Raw $Path | ConvertFrom-Json
Write-Output "Loaded $($events.Count) Event ID 4104 script-block records from $Path`n"

$flagged = 0
foreach ($e in $events) {
    $hits = foreach ($i in $indicators) {
        if ($e.ScriptBlockText -match $i.Pattern) { $i }
    }
    if ($hits) {
        $flagged++
        $snippet = $e.ScriptBlockText
        if ($snippet.Length -gt 90) { $snippet = $snippet.Substring(0, 90) + '...' }
        Write-Output "[SUSPICIOUS] $($e.TimeCreated)  $($e.Computer)  $($e.UserId)"
        Write-Output "   script : $snippet"
        Write-Output "   matched: $((($hits | ForEach-Object { $_.Name }) -join ', '))"
        foreach ($h in $hits) { Write-Output "      - $($h.Name): $($h.Note)" }
        Write-Output ""
    }
}

Write-Output "Verdict: $flagged of $($events.Count) script blocks are suspicious; the rest are routine admin activity."
Write-Output "Note the borderline case: a download that saves to disk from an INTERNAL host is not flagged here — context (internal vs external, save-to-disk vs IEX) is the hunt judgement you own."
