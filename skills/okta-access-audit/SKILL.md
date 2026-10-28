---
name: okta-access-audit
description: Read-only Okta hygiene audit that reports stale users, deprovisioned users still holding app assignments, empty or ownerless groups, admin-role sprawl, and unassigned apps. Use when asked to audit Okta, review access, find stale or inactive accounts, or prepare evidence for an access review. Never changes anything in Okta.
---

# Okta access audit (read-only)

An example L4 skill for the AI-Ready Baseline. Copy it into `~/.claude/skills/` or a repo's `.claude/skills/` and adjust the thresholds.

## Ground rules
- **Read-only.** Use the Okta MCP server (`okta/okta-mcp-server`) or the Okta Management API with an API client granted only `okta.users.read`, `okta.groups.read`, `okta.apps.read`, `okta.roles.read` and `okta.logs.read`.
- If a step needs any write scope, stop and say so instead of asking for more access.
- Work against a preview org first. Name the org in the report header.

## Checks
1. **Stale users**: ACTIVE users whose `lastLogin` is older than 90 days, or who never logged in and were created more than 14 days ago.
2. **Deprovisioned but assigned**: DEPROVISIONED or SUSPENDED users who still have app assignments.
3. **Groups**: Okta-mastered groups with zero members, and group rules that are INACTIVE or target a deleted attribute.
4. **Admin sprawl**: everyone holding Super Admin or Org Admin, with each one's last login. Flag more than 3 super admins.
5. **Unassigned apps**: ACTIVE apps with no user or group assignments.
6. **Recent risky events** (last 7 days of System Log): `user.account.privilege.grant`, `policy.lifecycle.update`, `application.policy.sign_on.deny_access` spikes.

## Output
A markdown report with one section per check: counts first, then a table (user/group/app, the fact that flagged it, a suggested action). End with the three highest-impact fixes.
The suggested actions are suggestions only. The admin applies them in Okta, or through a separate skill that confirms each write.
