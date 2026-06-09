# CI/CD Security Review Checklist

Apply this checklist to every GitHub Actions workflow before merging.

## Trigger security
- [ ] Is `pull_request_target` used? If so, does the workflow check out and execute PR code? (CRITICAL: this allows secret exfiltration)
- [ ] Does the workflow use `pull_request` (not `pull_request_target`) for PR code scanning?

## Permissions
- [ ] Is there a `permissions:` block at the job level (not just workflow level)?
- [ ] Are permissions scoped to the minimum required? (`contents: read` for checkout; `pull-requests: write` only where needed)
- [ ] Is `permissions: write-all` used? (RED FLAG — must be reviewed)

## Third-party actions
- [ ] Are all `uses:` actions pinned to a full SHA commit hash (not a tag like `@v2` or `@latest`)?
- [ ] Has the pinned SHA been verified against the action's release history?

## Secrets
- [ ] Are secrets passed as environment variables to commands (not as CLI arguments)?
- [ ] Does any `run:` step print or `echo` a secret value?
- [ ] Are computed values derived from secrets also treated as secrets?

## Code execution
- [ ] Does the workflow run scripts from the PR branch? (Verify this is intentional and safe)
- [ ] Are any `run:` blocks constructed from user-controlled inputs? (script injection risk)

## TODO: Add items for the two findings not in this checklist (unpinned actions, secret-in-log)
