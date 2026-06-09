# Detection Notes — Lateral Movement
**Document type:** Detection engineering notes | **Owner:** Detection Engineering | **Last updated:** 2025-03-01

## Overview
This document summarises detection rules and data sources for lateral movement techniques
observed in Meridian's environment. Updated after each confirmed lateral movement incident.

## PsExec lateral movement (T1021.002)

**What we see:** `psexec.exe` spawning from unusual parent processes (not IT management
tools), or ADMIN$ share connections followed by remote service creation events.

**Detection rule:** `sigma-rule-lateral-psexec-v2.yml` (in the sigma-rules repository)
- Log source: Windows Security Event Log, Event ID 4648 (explicit credentials used) + 7045 (service installed)
- Key field: `ServiceName` matching `PSEXESVC` or random 8-char string
- False positive: legitimate sysadmin use from jump hosts (`MERIDIAN-JUMP-01`, `MERIDIAN-JUMP-02`)

**Tuning note:** Add a filter for source IPs in the jump host CIDR (`10.0.0.240/28`) to
suppress the false-positive storm from the IT team's scheduled maintenance scripts.

## WMI remote execution (T1047)

**What we see:** `WmiPrvSE.exe` spawning `cmd.exe` or `powershell.exe` with network
connections to the host immediately preceding it.

**Detection rule:** `sigma-rule-wmi-remote-exec-v1.yml`
- Log source: Sysmon Event ID 1 (process creation), parent `WmiPrvSE.exe`
- Filter: exclude `WmiPrvSE.exe → msiexec.exe` (Windows Update false positive)

## Log retention
- Windows Security events: 90 days in SIEM, 1 year in cold storage
- Sysmon events: 30 days in SIEM (volume constraint), 90 days cold
- Network flow logs: 180 days

## Known gaps
- No detection for WinRM-based lateral movement (T1021.006). Ticket: DET-2025-0041.
- PowerShell remoting (T1021.006 variant) produces insufficient logging without
  ScriptBlock logging enabled. Enforcement in progress; target completion: 2025-Q3.
