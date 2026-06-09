# Runbook — Phishing Response
**Document type:** Runbook | **Owner:** Security Operations | **Last reviewed:** 2025-01-30

## Trigger
User reports a suspicious email, or email security gateway quarantines a message with a malicious
link or attachment.

## Triage (15 minutes)
1. Retrieve the email from quarantine or from the user's mailbox using the Exchange admin tools.
2. Identify: sender domain, reply-to address, all embedded URLs (defang before documenting).
3. Check whether any user has *clicked* the link — query URL filtering logs for the domain.
4. If a user clicked: escalate to credential incident runbook (document 02). Otherwise P3.

## Containment
1. Remove the email from all mailboxes using `Search-Mailbox -DeleteContent` or equivalent.
2. Block the sender domain and all embedded domains in the email security gateway.
3. Submit the URL and attachment hash to threat intelligence platform for enrichment.
4. If attachment: submit to sandbox; preserve a copy in forensic evidence store.

## Notification
- Notify the reporting user with thanks and a one-paragraph explanation (trust-building).
- If 10+ recipients: draft an all-staff notification via Communications. Do not send without CISO review.

## ATT&CK mapping
- T1566.001 — Phishing: Spearphishing Attachment
- T1566.002 — Phishing: Spearphishing Link
