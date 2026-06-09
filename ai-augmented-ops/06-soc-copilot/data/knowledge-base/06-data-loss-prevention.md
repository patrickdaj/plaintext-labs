# Runbook — Data Loss Prevention Alert Response
**Document type:** Runbook | **Owner:** Security Operations | **Last reviewed:** 2024-12-05

## Overview
Meridian's DLP platform monitors email, web uploads, and USB devices for sensitive data patterns
(PII, PCI data, internally classified documents). This runbook covers the response to a DLP alert.

## Alert types and default severity
| Alert type | Default severity | Notes |
|-----------|-----------------|-------|
| Credit card numbers in outbound email | P2 | Auto-block; review in 30 min |
| SSN in email or upload | P2 | Auto-block |
| Internally classified document uploaded to personal cloud storage | P2 | |
| Large file to USB device | P3 | Review context; IT provisioned USB devices may be legitimate |
| Bulk email to external domain | P3 | Check for mailing list vs. exfiltration pattern |

## Investigation steps
1. Identify the user and their manager. Pull HR context (any recent disciplinary action? resignation submitted?).
2. Review the content: was it actually sensitive? DLP false-positives on patterns like test data or sanitised samples.
3. Check for other DLP events from the same user in the past 30 days.
4. If insider threat pattern suspected: escalate to HR and Legal before contacting the user.

## Data retention for DLP events
- DLP alert metadata: 2 years.
- Content captures: 90 days in restricted access storage.

## Regulatory notes
- PCI DSS: card number events must be logged and the incident reported to the compliance team.
- GDPR (where applicable): personal data incidents may require notification to the DPO.
