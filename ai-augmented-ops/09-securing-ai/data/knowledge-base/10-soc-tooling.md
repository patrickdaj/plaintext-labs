# SOC Tooling Reference
**Document type:** Reference | **Owner:** Security Operations | **Last reviewed:** 2025-04-01

## SIEM — Splunk Enterprise Security
- Version: 7.3.1
- Data ingestion: ~120 GB/day
- Retention: 90 days hot (indexed), 1 year warm (cold bucket), 3 years frozen (S3)
- Key index: `main` (raw events), `notable` (ES notables), `risk` (Risk Framework scores)

## EDR — CrowdStrike Falcon
- Coverage: 98% of managed endpoints (2% are OT/IoT excluded by policy)
- RTR (remote response): enabled for SOC analysts; requires manager approval for full disk access
- Isolation: SOC analysts can isolate any endpoint without approval (P1/P2 response)

## Threat intelligence — Recorded Future
- Feeds updated every 4 hours
- IOC types ingested: IP, domain, hash, CVE, vulnerability
- Integration: IOCs auto-enriched in SIEM via lookup table (`threat_intel` lookup)
- Analyst access: `https://app.recordedfuture.com` (SSO via Okta)

## Ticketing — ServiceNow ITSM
- All incidents open a ServiceNow ticket automatically from SIEM notable
- IR tickets use the `Security Incident` table; SLA tracking automated
- Playbook workflows trigger on ticket creation for P1/P2

## Network monitoring — Zeek + Suricata
- Zeek: passive analysis of all inter-zone traffic; logs to SIEM
- Suricata: IDS in alert mode on perimeter and Finance VLAN; blocks only on confirmed C2 signatures
- PCAP retention: 7 days full PCAP (storage constraint), 90 days metadata only
