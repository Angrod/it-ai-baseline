---
name: offboard-user
description: Offboarding runbook across Okta, Google Workspace, Microsoft 365, Jamf and Snipe-IT, with a dry-run plan and a confirmation before every write. Use when asked to offboard, deprovision, terminate or disable a departing employee's accounts and devices.
---

# Offboard a user

An example L4 skill for the AI-Ready Baseline. The agent and the helpdesk follow the same steps, so this doubles as documentation.

## Inputs (ask for any that are missing)
- User's primary email, their manager's email, and the last working day / effective time.
- Whether it is a standard departure or an urgent termination (urgent means do sessions and lockout first, immediately).
- Who receives Drive files and mail (defaults to the manager).

## Rules
- **Plan first.** Before running anything, print the full plan as a numbered list of exact commands or API calls, with the user and devices resolved. Wait for "go".
- **Confirm every write** individually. Never batch-confirm destructive steps (wipe, delete).
- Prefer suspend/disable over delete. Deletion is out of scope for this skill.
- Log each step with its timestamp and result, and paste the log into the ticket at the end.
- If any step fails, stop and report. Don't improvise around it.

## Steps
1. **Okta**: suspend the user (`POST /api/v1/users/{id}/lifecycle/suspend`) and clear sessions (`DELETE /api/v1/users/{id}/sessions`). Deactivation, which triggers SCIM deprovisioning, happens after the data-transfer steps.
2. **Google Workspace (GAM)**: confirm syntax with `gam help` for your GAM version before first use.
   - `gam user <email> signout`
   - `gam user <email> transfer drive <manager>`
   - `gam update user <email> suspended on`
3. **Microsoft 365** (Graph PowerShell / Exchange Online):
   - `Revoke-MgUserSignInSession -UserId <upn>`
   - `Set-Mailbox -Identity <upn> -Type Shared`, then grant the manager access
   - `Update-MgUser -UserId <upn> -AccountEnabled:$false`
4. **Jamf Pro**: find the user's computers and mobile devices. Send a Lock Computer command only with explicit confirmation and a recorded passcode. Never wipe without a second confirmation that names the serial number.
5. **Snipe-IT**: check the user's assets back in (`POST /api/v1/hardware/{id}/checkin`) with a note referencing the ticket.
6. **Okta (final)**: deactivate the user (`POST /api/v1/users/{id}/lifecycle/deactivate`) so SCIM deprovisions downstream apps. Then list any apps that still show an assignment.
7. **Report**: a checklist of every step with its status, plus anything left for a human (licenses to reclaim, shared-drive ownership, vendor accounts outside SSO).
