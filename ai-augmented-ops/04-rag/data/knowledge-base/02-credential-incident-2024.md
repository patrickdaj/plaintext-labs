# Post-Incident Report — Meridian Credential Incident (2024-Q2)
**Classification:** Internal — Restricted | **Date:** 2024-06-18 | **Author:** IR Team Lead

## Executive summary
On 2024-06-12, Meridian's SIEM detected anomalous authentication patterns from three finance
department accounts. Investigation confirmed that credentials had been compromised via a
targeted phishing campaign. No customer data was exfiltrated. Incident was contained within
4 hours of detection.

## Timeline
| Time (UTC) | Event |
|-----------|-------|
| 09:14 | SIEM alert: impossible travel — user `jsmith@meridian.fin` authenticated from London and New York within 22 minutes |
| 09:19 | SOC analyst confirms alert, opens P2 incident ticket INC-2024-0612-001 |
| 09:31 | Two additional accounts (`aparker`, `rliu`) show same pattern |
| 09:45 | Identity team revokes sessions and resets passwords for all three accounts |
| 10:02 | Phishing email recovered from quarantine; link pointed to credential harvesting page at `meridian-secure-login.net` (not affiliated with Meridian) |
| 11:20 | Forensic review of mailbox access logs confirms no forwarding rules, no data download |
| 13:30 | Incident closed; all three accounts restored with MFA enforced |

## Root cause
Phishing email with a convincing internal-branding template delivered to finance team.
Three users entered credentials on the harvesting page. MFA was not enforced at the time
on the finance department SSO profile.

## Containment procedure applied
1. Identify all accounts with suspicious authentication in the 24-hour window.
2. Immediately revoke active sessions via Azure AD "Revoke all sessions."
3. Force password reset for compromised accounts.
4. Check for mailbox forwarding rules and OAuth application consent grants.
5. Preserve mailbox audit logs to forensic storage (90-day retention).
6. Notify affected users and their managers.

## Lessons learned
- MFA was not enforced on all SSO profiles. **Remediation:** MFA mandatory for all SSO
  profiles by 2024-07-31.
- Detection relied on the impossible-travel alert. No phishing-link click alert existed.
  **Remediation:** Deploy URL filtering logs to SIEM; alert on clicks to newly registered domains.

## ATT&CK mapping
- T1566.002 — Phishing: Spearphishing Link
- T1078 — Valid Accounts
- T1539 — Steal Web Session Cookie (not confirmed but plausible given session reuse pattern)

## Artifacts
- Phishing URL: `hxxps://meridian-secure-login[.]net/auth` (defanged)
- Sender domain: `meridian-fin-support[.]com` (look-alike, registered 2024-06-10)
