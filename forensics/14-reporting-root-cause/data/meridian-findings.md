# Meridian Financial — Raw Forensic Findings
**Case ID:** MFI-2024-0315  
**Status:** Pre-report notes — NOT a finished report  
**Prepared by:** IR Team  
**Date collected:** 2024-03-15 through 2024-03-16

These are the raw findings from the Meridian investigation, covering modules 08–12.
Use these to complete the formal incident report (report-template.md).

---

## From Module 08 — Live Response (Velociraptor)

- **Process anomaly:** PID 3847 `svchost32.exe` with PPID 3201 (bash) — anomalous parent/child.
  Image path: `/tmp/svchost32.exe` (not a system path).
- **Network connection:** PID 3847 has ESTABLISHED TCP connection to `198.51.100.42:4444`.
- **Files:** `/tmp/svchost32.exe` written at 2024-03-15T14:21:55Z (52,224 bytes).
  `/tmp/.s` (hidden dot-file, 0 bytes) written at 2024-03-15T14:22:41Z.
- **Scope assessment:** Velociraptor hunt over 47 additional endpoints returned no further
  anomalies. Compromise appears isolated to WORKSTATION-04.

## From Module 09 — Network Forensics (Zeek + tshark)

- **DNS query:** `update-cdn82.net` → resolved to `198.51.100.42` at 2024-03-15T14:20:01Z.
- **HTTP session:** GET `/update.bin` to `198.51.100.42:80` at 2024-03-15T14:21:40Z.
  Response: HTTP 200, Content-Type: `application/octet-stream`, 52,224 bytes transferred.
- **File hash (conn.log/files.log):** MD5 `aabbccdd1122334455667788aabbccdd` (synthetic).
  NOTE: This hash is synthetic. In production, submit to VirusTotal before citing.
- **No TLS sessions** observed to `198.51.100.42` (cleartext C2).

## From Module 10 — Log & Cloud Forensics (Hayabusa + CloudTrail)

### Endpoint (EVTX)
- **Event 4698** at 14:18:03Z: Scheduled task `\MicrosoftEdgeUpdateTaskUser` created by
  `MFIN\dev-svc01`. Task action: execute `/tmp/svchost32.exe`.
- **Event 4688** at 14:18:45Z: `WINWORD.EXE` spawned `cmd.exe`.
- **Event 4688** at 14:19:12Z: `cmd.exe` spawned `powershell.exe -w hidden -EncodedCommand [base64]`.
- **Event 4624** at 14:20:01Z: Network logon (Type 3) from `10.0.0.50` as `dev-svc01`.
- **Event 4663** at 14:21:55Z: `powershell.exe` wrote `/tmp/svchost32.exe`.

### Cloud (CloudTrail)
- **14:35:02Z:** `dev-svc01` → `GetCallerIdentity` from `198.51.100.42` (attacker IP).
- **14:35:18Z–14:36:05Z:** `dev-svc01` → `ListUsers`, `ListRoles`, `ListAttachedUserPolicies`
  (IAM reconnaissance, 3 calls in 47 seconds).
- **14:38:12Z:** `dev-svc01` → `CreateUser` for `svc-backup-restore`.
- **14:38:45Z:** `dev-svc01` → `AttachUserPolicy` with `arn:aws:iam::aws:policy/AdministratorAccess`
  to `svc-backup-restore`.
- **14:39:02Z:** `dev-svc01` → `CreateAccessKey` for `svc-backup-restore` (key ID: `AKIA999NEWKEY0001`).
- **15:52:17Z:** `svc-backup-restore` → `AssumeRole` for `MeridianProdDeploy`.

## From Module 11 — Anti-Forensics

- **Timestomped file:** `svchost32.exe` SI mtime set to 2019-06-15T00:00:00Z.
  FN attribute creation time: 2024-03-15T14:21:55Z. Delta: 4 years, 9 months.
  Method: `touch -t 201906150000` or Win32 `SetFileTime` API equivalent.

## From Module 12 — Malware Artifacts

- **CAPA profile (hypothetical):** scheduled task persistence (T1053.005), HTTP C2 (T1071.001),
  DLL injection (T1055.001), VM check (T1497.001), runtime API resolution (T1027).
- **YARA match:** `MeridianDropper_C2_Domain` rule fires on embedded string `update-cdn82.net`.
- **Sample not submitted to sandboxing** — analysis limited to static triage in this engagement.

---

## IOC Summary (raw)

| Type | Value |
|------|-------|
| IP | 198.51.100.42 |
| Domain | update-cdn82.net |
| URI | http://update-cdn82.net/update.bin |
| File path | /tmp/svchost32.exe |
| File path | /tmp/.s |
| File MD5 | aabbccdd1122334455667788aabbccdd (synthetic) |
| IAM user | svc-backup-restore |
| IAM key | AKIA999NEWKEY0001 |
| IAM role assumed | arn:aws:iam::123456789012:role/MeridianProdDeploy |
| Scheduled task | \MicrosoftEdgeUpdateTaskUser |

---

*These are training notes using a fictional scenario. All IP addresses, domains, and hashes are synthetic.*
