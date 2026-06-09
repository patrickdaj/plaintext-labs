# CIS Windows 11 Benchmark — Level 1 Subset

*Source: CIS Microsoft Windows 11 Enterprise Benchmark v3.0.0 (2024)*
*Controls selected for lab demonstration: high-value, automatable via PowerShell/LGPO.*

---

## Section 1 — Account Policies

### 1.1 — Password Policy

| CIS ID | Control | Recommended Value | Automation |
|--------|---------|-------------------|-----------|
| 1.1.1 | Enforce password history | 24 or more | PowerShell (secedit) |
| 1.1.2 | Maximum password age | 365 days or fewer | PowerShell (secedit) |
| 1.1.4 | Minimum password length | 14 or more characters | PowerShell (secedit) |
| 1.1.5 | Password must meet complexity | Enabled | PowerShell (secedit) |

### 1.2 — Account Lockout Policy

| CIS ID | Control | Recommended Value | Automation |
|--------|---------|-------------------|-----------|
| 1.2.1 | Account lockout duration | 15 or more minutes | PowerShell (secedit) |
| 1.2.2 | Account lockout threshold | 5 or fewer invalid attempts | PowerShell (secedit) |
| 1.2.3 | Reset lockout counter after | 15 or more minutes | PowerShell (secedit) |

---

## Section 2 — Local Policies

### 2.2 — User Rights Assignment

| CIS ID | Control | Recommended Value | Automation |
|--------|---------|-------------------|-----------|
| 2.2.21 | Deny access from network: Guests, Local account | Guests, Local account | LGPO |
| 2.2.26 | Deny log on locally: Guests | Guests | LGPO |
| 2.2.41 | Log on as service: specific accounts only | [MANUAL] — list service accounts |

### 2.3 — Security Options

| CIS ID | Control | Recommended Value | Automation |
|--------|---------|-------------------|-----------|
| 2.3.7.1 | Interactive logon: Do not display last username | Enabled | Registry |
| 2.3.7.4 | Interactive logon: Machine inactivity limit | 900 seconds or fewer | Registry |
| 2.3.10.6 | Network security: Do not store LAN Manager hash | Enabled | Registry |
| 2.3.11.5 | Network security: LAN Manager auth level | NTLMv2 only | Registry |
| 2.3.15.2 | Shutdown: Allow system to be shut down without logon | Disabled | Registry |

---

## Section 9 — Windows Firewall (MANUAL)

| CIS ID | Control | Recommended Value | Automation |
|--------|---------|-------------------|-----------|
| 9.1.1 | Domain firewall: on | On | PowerShell (netsh) |
| 9.1.2 | Domain firewall: inbound default | Block | PowerShell (netsh) |
| 9.2.1 | Private firewall: on | On | PowerShell (netsh) |
| 9.3.1 | Public firewall: on | On | PowerShell (netsh) |

---

## Section 18 — Administrative Templates

### 18.4 — MS Security Guide

| CIS ID | Control | Recommended Value | Automation |
|--------|---------|-------------------|-----------|
| 18.4.3 | Configure SMB v1 server | Disabled | Registry |
| 18.4.9 | NetBT NodeType: Peer-Peer | P-node (2) | Registry |

### 18.9 — Windows Components

| CIS ID | Control | Recommended Value | Automation |
|--------|---------|-------------------|-----------|
| 18.9.12.1 | Turn off AutoPlay | All drives | Registry |
| 18.9.59.2 | PowerShell: Script Block Logging | Enabled | Registry |
| 18.9.59.3 | PowerShell: Transcription | Enabled | Registry |

---

## [MANUAL] Controls requiring interactive configuration

These three controls **cannot** be set via PowerShell alone and require the Group Policy
editor (gpedit.msc) or LGPO with a specific GPO backup:

1. **CIS 2.2.41 — Log on as a service**: Open gpedit.msc → Computer Configuration →
   Windows Settings → Security Settings → Local Policies → User Rights Assignment →
   "Log on as a service". Remove any accounts not in the approved service account list.
   Approved accounts: listed in your organisation's service account inventory.

2. **CIS 18.9.47.5 — Windows Search: Control indexing encrypted files**: Requires LGPO GPO
   import from the CIS GPO backup package. Download from CIS SecureSuite (member access).

3. **CIS 19.7.26.1 — Prevent downloading enclosures from RSS feeds**: Requires user-level GPO
   (HKCU). Set via gpedit.msc under User Configuration → Administrative Templates →
   Windows Components → RSS Feeds.
