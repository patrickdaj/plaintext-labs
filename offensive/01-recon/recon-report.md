# Recon Report — meridian-financial.com
Date: 2026-06-08

## Scope
Target: `meridian-financial.com` and all subdomains. Passive recon only.
Authorization: Meridian Financial lab exercise (fictional estate).

## Asset inventory

| Hostname | IP | ASN | Stack | Score | Notes |
|----------|-----|-----|-------|-------|-------|
| vpn.meridian-financial.com | 198.51.100.50 | AS6939 | Nginx, Fortinet FortiGate SSL-VPN | 90 | FortiGate VPN portal — check for CVE-2023-27997 / CVE-2024-21762 |
| jira.meridian-financial.com | 185.166.143.50 | AS18679 | Nginx 1.24.0, Atlassian Jira 9.4.0 | 90 | Jira 9.4.0 — check CVE-2023-22515 (broken access control, auth bypass) |
| dev.meridian-financial.com | 198.51.100.55 | AS6939 | Apache 2.4.52, Django/4.2 | 85 | Dev environment — Apache 2.4.52 (CVE-2021-41773 patched, but 2.4.52 still vulnerable to mod_sed) |
| backups.meridian-financial.com | 52.216.100.20 | AS16509 | AWS S3 | 70 | S3 bucket accessible — check for public read/listObject permissions |
| api.meridian-financial.com | 54.239.28.1 | AS16509 | AWS ALB, Swagger UI 4.18.1 | 70 | Swagger UI exposed — API documentation accessible without auth |
| portal.meridian-financial.com | 104.21.45.13 | AS13335 | Nginx 1.18.0, React | 50 | Client-facing financial portal — JWT auth, React SPA |
| www.meridian-financial.com | 104.21.45.12 | AS13335 | Cloudflare, WordPress 6.4.3 | 20 |  |
| staging.meridian-financial.com | 198.51.100.55 | AS6939 | Apache 2.4.52, Django/4.2 | 10 | Basic auth — 401; possibly same stack as dev |

## Top priority targets

### vpn.meridian-financial.com  (score 90/100)
FortiGate VPN portal — check for CVE-2023-27997 / CVE-2024-21762

### jira.meridian-financial.com  (score 90/100)
Jira 9.4.0 — check CVE-2023-22515 (broken access control, auth bypass)

### dev.meridian-financial.com  (score 85/100)
Dev environment — Apache 2.4.52 (CVE-2021-41773 patched, but 2.4.52 still vulnerable to mod_sed)

### backups.meridian-financial.com  (score 70/100)
S3 bucket accessible — check for public read/listObject permissions

### api.meridian-financial.com  (score 70/100)
Swagger UI exposed — API documentation accessible without auth

### portal.meridian-financial.com  (score 50/100)
Client-facing financial portal — JWT auth, React SPA

## Sources
- Certificate Transparency: https://crt.sh/?q=%.meridian-financial.com
- DNS: passive enumeration (no zone transfer attempted)
- Tech stack: HTTP banner/header analysis

## Next steps
- Active scan of top-priority targets (authorization confirmed).
- Verify S3 bucket public access policy.
- Check FortiGate VPN and Jira for identified CVEs.