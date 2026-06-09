# Runbook — Ransomware Response
**Document type:** Runbook | **Owner:** Security Operations | **Last reviewed:** 2025-02-20

## When to use this runbook
Activate when: (a) ransomware note or encrypted files observed on any endpoint, or (b) EDR
alerts to mass file encryption behaviour.

## Severity: Always P1

## Immediate containment (first 15 minutes)
1. **Do not power off the affected host** — volatile memory may contain the encryption key.
   Use EDR to isolate the host at the network layer (block all inbound/outbound except IR VPN).
2. Identify the "patient zero" host by reviewing EDR process tree for the ransomware executable.
3. Check for lateral movement: query EDR for any SMB/RDP connections *from* the patient zero
   host in the 4-hour window before the encryption event.
4. Escalate to CISO immediately per the P1 escalation path.
5. Notify Legal and Communications — do not communicate externally without approval.

## Investigation
1. Pull the ransomware binary if present; submit to internal malware sandbox.
2. Check threat intelligence feeds for the ransom note template / file extension.
3. Identify the initial access vector: phishing, RDP exposure, vulnerable service.
4. Determine blast radius: which file shares / backup systems are accessible from patient zero?

## Eradication and recovery
1. Restore from clean backup. Verify backup integrity *before* wiping the host.
2. Patch or close the initial access vector before restoring to network.
3. Reset credentials for any account used on the affected host.
4. Update EDR detection rules with indicators from this incident.

## Do NOT
- Do not pay the ransom without CISO and General Counsel approval and law enforcement notification.
- Do not wipe the host before IR team has taken a forensic image.
- Do not trust any "decryptor" provided by the threat actor without vendor validation.

## ATT&CK techniques commonly observed
- T1486 — Data Encrypted for Impact
- T1490 — Inhibit System Recovery (shadow copy deletion)
- T1070.001 — Indicator Removal: Clear Windows Event Logs
