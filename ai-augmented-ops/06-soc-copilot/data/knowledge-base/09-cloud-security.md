# Cloud Security Operations — AWS and GCP
**Document type:** Runbook reference | **Owner:** Cloud Security | **Last reviewed:** 2025-03-15

## AWS environments
- Production: account ID 123456789012 (`meridian-prod`)
- Staging: account ID 234567890123 (`meridian-staging`)
- Security tooling: account ID 345678901234 (`meridian-security`)
- All accounts are members of the Meridian AWS Organisation; SCPs enforce baseline controls.

## Key controls
- **CloudTrail**: enabled in all regions, logs shipped to `meridian-security` account S3 bucket with CloudWatch alerts on high-risk API calls (e.g. `CreateUser`, `AttachUserPolicy`, `PutBucketPolicy`).
- **GuardDuty**: enabled in all accounts; findings routed to SIEM via EventBridge.
- **IAM Access Analyzer**: continuous; findings reviewed weekly.
- **No long-lived access keys**: enforced by SCP. All programmatic access via IAM roles and instance profiles.

## Alert response — GuardDuty finding
1. Retrieve finding detail from SIEM or GuardDuty console.
2. Identify the IAM principal: is it a service role or a human identity?
3. If `UnauthorizedAccess:IAMUser/ConsoleLogin` from unexpected geography: revoke sessions and rotate credentials.
4. If `Backdoor:EC2/C&CActivity`: isolate the instance (modify security group to deny-all) and preserve the instance state (snapshot before termination).
5. Escalate to cloud security team for root-cause analysis.

## GCP environments
- Meridian uses GCP for ML workloads only (project: `meridian-ml-prod`).
- Cloud Audit Logs forwarded to Chronicle SIEM.
- Org policy enforces no external IP on compute instances without explicit exception.
