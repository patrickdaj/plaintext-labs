# Meridian Financial — Incident Brief
**Case ID:** MFI-2024-0315  
**Classification:** Confidential — Internal Use Only  
**Prepared by:** IR Team Lead  
**Date:** 2024-03-15

---

## Executive Summary

On 15 March 2024, Meridian Financial's security operations centre detected anomalous activity
originating from developer workstation WORKSTATION-04. Investigation confirmed a multi-stage
intrusion: phishing email → endpoint compromise → credential extraction → cloud pivot. The
attacker created a backdoor IAM user and assumed a production deployment role before the
account was revoked. Estimated dwell time: 4 hours and 34 minutes.

---

## Timeline

| Time (UTC)   | Event                                                                                  | Phase              |
|--------------|----------------------------------------------------------------------------------------|--------------------|
| 13:47        | Phishing email received by developer `mfin\dev-svc01` (PDF attachment)                | Preparation gap    |
| 13:51        | Developer opens PDF; malicious macro executes                                          | Detection & Analysis |
| 14:18        | SIEM alert fires: Event ID 4698 (scheduled task creation) on WORKSTATION-04           | Detection & Analysis |
| 14:22        | **[UNKNOWN]** — what did the SOC analyst do at alert receipt?                         | Detection & Analysis |
| 14:35        | Attacker begins CloudTrail API reconnaissance from IP 198.51.100.42                   | Detection & Analysis |
| 14:38        | Attacker creates backdoor IAM user `svc-backup-restore` with AdministratorAccess       | Detection & Analysis |
| 15:52        | Attacker assumes `MeridianProdDeploy` role via `svc-backup-restore`                   | Detection & Analysis |
| 16:18        | SOC supervisor escalates alert to IR team lead                                         | Detection & Analysis |
| 16:22        | IR team lead declares incident; begins live response on WORKSTATION-04                 | Containment        |
| 16:34        | WORKSTATION-04 isolated from network (4hr 16min after initial alert)                  | Containment        |
| 16:40        | **[UNKNOWN]** — what cloud containment action was taken (or missed)?                  | Containment        |
| 17:10        | Velociraptor hunt confirms compromise isolated to WORKSTATION-04; no lateral movement  | Containment        |
| 17:30        | Disk image and memory capture of WORKSTATION-04 initiated                              | Containment        |
| 18:15        | Developer account `dev-svc01` password reset and MFA reset                            | Eradication        |
| 18:30        | Scheduled task `\MicrosoftEdgeUpdateTaskUser` removed from WORKSTATION-04             | Eradication        |
| 18:45        | `svchost32.exe` and `/tmp/.s` removed from WORKSTATION-04                             | Eradication        |
| 19:00        | C2 domain `update-cdn82.net` blocked at perimeter firewall                             | Eradication        |
| 19:15        | **[UNKNOWN]** — what IAM eradication steps were performed (or missed)?                | Eradication        |
| 20:00        | WORKSTATION-04 reimaged from baseline                                                  | Recovery           |
| 20:30        | Developer account restored; MFA verified                                               | Recovery           |
| 21:22        | System returned to production                                                          | Recovery           |

---

## Response Actions Taken

### Detection & Analysis
- SIEM alert reviewed and escalated (2hr 27min after alert)
- Live response with Velociraptor: process list, network connections, recent files
- Memory and disk capture of WORKSTATION-04
- Network forensics on PCAP from perimeter sensor (identified C2 session)
- EVTX triage with Hayabusa: Event IDs 4698, 4688, 4624 correlated

### Containment
- WORKSTATION-04 network isolated
- Velociraptor fleet hunt: 47 other endpoints cleared

### Eradication
- Attacker binary (`svchost32.exe`) removed
- Persistence mechanism (scheduled task) removed
- Developer account rotated
- C2 domain blocked at firewall

### Recovery
- Workstation reimaged
- User account restored

---

## Gaps Identified (preliminary)

1. **Detection delay:** 2hr 27min from alert to escalation. The SIEM alert was triaged at
   level 2 and not immediately escalated; the escalation policy requires supervisor review
   before IR team engagement.

2. **Missing notification:** Legal and privacy team were not notified until 19:45 (3hr 27min
   after incident declaration). Regulatory obligation in Meridian's jurisdiction requires
   notification within 4 hours of incident confirmation — this was nearly missed.

3. **Eradication scope question:** The eradication checklist addressed endpoint artifacts and
   the developer account. The CloudTrail evidence from module 10 shows a second IAM identity
   was created (`svc-backup-restore`) with AdministratorAccess, and a production role
   (`MeridianProdDeploy`) was assumed. The incident brief does not explicitly list the
   eradication actions for these cloud artifacts.

---

## Open Questions for Post-Incident Review

1. Why did the phishing email bypass the email security gateway? Was DMARC/DKIM enforcement
   configured? Was the PDF attachment scanned before delivery?
2. What would have detected the attack earlier — at the phishing stage, the scheduled task
   creation, or the C2 outbound connection?
3. What single control would have highest probability of stopping a repeat of this attack chain?

---

*This brief is a fictional training document. All organisations, individuals, IP addresses, and
domain names are synthetic. Any resemblance to real incidents is coincidental.*
