# Network Segmentation — Security Architecture Reference
**Document type:** Architecture reference | **Owner:** Network Security | **Last reviewed:** 2025-01-20

## Zone overview

| Zone | VLAN | Purpose | Internet access |
|------|------|---------|----------------|
| Corporate | 10 | Staff workstations | Via proxy only |
| Finance | 20 | Finance applications, trading systems | Blocked |
| Production | 30 | Customer-facing services | Inbound only (load balancer) |
| DMZ | 40 | Publicly accessible services | Full (managed) |
| Management | 100 | Jump hosts, monitoring | None |
| Guest | 200 | Visitor WiFi | Direct (isolated) |

## Inter-zone rules (summary)
- Finance → Production: blocked. Finance systems do not communicate directly with production APIs.
- Corporate → Production: blocked except via the API gateway (`prod-gw-01`).
- Management → all zones: allowed for management protocols (SSH 22, RDP 3389, SNMP) from jump hosts only.
- Any zone → Management: blocked.
- Guest → all internal zones: blocked.

## Jump hosts
- `MERIDIAN-JUMP-01` (10.0.0.241) — Windows, RDP for Windows server administration.
- `MERIDIAN-JUMP-02` (10.0.0.242) — Linux, SSH for Linux and cloud administration.
All jump host sessions are logged to PAM and recorded. Session duration limit: 8 hours.

## Detection notes
Unexpected inter-zone traffic (e.g., Finance → DMZ direct, Corporate → Finance on non-HTTP ports)
should be treated as a lateral movement indicator and triaged under the lateral movement runbook.
