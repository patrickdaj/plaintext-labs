# Meridian Financial — Incident Response Overview
**Document type:** Runbook | **Owner:** Security Operations | **Last reviewed:** 2025-01-15

## Purpose
This document defines Meridian Financial's incident response lifecycle and the responsibilities
of each team during a declared security incident.

## Incident severity levels

| Level | Definition | Response SLA |
|-------|-----------|-------------|
| P1 — Critical | Active data exfiltration, ransomware, confirmed account takeover of privileged account | 15 minutes to first responder on call |
| P2 — High | Suspected compromise, C2 communication confirmed, lateral movement observed | 1 hour |
| P3 — Medium | Malware detected (not active), phishing landing confirmed, policy violation | 4 hours |
| P4 — Low | Suspicious activity under investigation, no confirmed compromise | Next business day |

## Lifecycle phases
1. **Detect** — alert fires in SIEM or EDR; SOC analyst reviews.
2. **Triage** — analyst confirms true positive, assigns severity, opens an IR ticket.
3. **Contain** — isolate affected systems; revoke credentials if indicated.
4. **Investigate** — root cause analysis; determine blast radius.
5. **Eradicate** — remove malware, close attack path, reset credentials.
6. **Recover** — restore systems from clean backups; validate integrity.
7. **Post-incident review** — complete within 5 business days; update runbooks.

## Escalation path
- **P1/P2**: On-call SOC analyst → SOC Manager → CISO (within 15 min for P1).
- Legal and Communications must be notified for any incident involving customer PII.
- Ransomware events require CISO and General Counsel approval before any communication with threat actors.

## Key contacts
Refer to the internal on-call roster in ServiceNow. Do not store personal contact details in this document.
