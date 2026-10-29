# Weekly refresh: 2026-10-29

Review the changes below. To change a score, tag or note, edit `curation/overrides.yaml` in this PR; overrides beat Claude's first pass.

| Candidates | IT-relevant | Passed gate | Scored by Claude this run | Needs review |
|---|---|---|---|---|
| 898 | 682 | 184 | 60 | 0 |

## IT Ops lens changes

- ⬆️ **jmpsec/osctrl** entered at #1
- ⬆️ **pnp/powershell** entered at #2
- ⬆️ **GAM-team/GAM** entered at #3
- ⬆️ **taylorwilsdon/google_workspace_mcp** entered at #4
- ⬆️ **Installomator/Installomator** entered at #5
- ⬆️ **maester365/maester** entered at #6
- ⬆️ **autopkg/autopkg** entered at #7
- ⬆️ **googleworkspace/cli** entered at #8
- ⬆️ **Microsoft365DSC/Microsoft365DSC** entered at #9
- ⬆️ **microsoft/shell-intune-samples** entered at #10
- ⬆️ **PSAppDeployToolkit/PSAppDeployToolkit** entered at #11
- ⬆️ **jkroepke/openvpn-auth-oauth2** entered at #12
- ⬆️ **MichaelGrafnetter/DSInternals** entered at #13
- ⬆️ **Micke-K/IntuneManagement** entered at #14
- ⬆️ **SkipToTheEndpoint/OpenIntuneBaseline** entered at #15

## Scored by Claude this run

| Repo | Fit | Tags | Trust | Why for sysadmins |
|---|---|---|---|---|
| [yuezk/GlobalProtect-openconnect](https://github.com/yuezk/GlobalProtect-openconnect) | 2 | identity, endpoint, network | pilot | Open-source GlobalProtect VPN client for Linux/macOS/BSD with SAML SSO (Okta/Entra), FIDO2 and cert auth, plus HIP reports. Useful for supporting Linux users on Palo Alto VPNs. |
| [agentic-community/mcp-gateway-registry](https://github.com/agentic-community/mcp-gateway-registry) | 2 | identity, security, automation, agent | production | Central gateway and registry for MCP servers and agents, with Entra ID/Okta/Keycloak OAuth, scoped access control, and audit logging. Useful for IT teams governing which agent tools staff can reach. |
| [tngan/samlify](https://github.com/tngan/samlify) | 1 | identity | pilot | Node.js library for building SAML service providers or identity providers. Useful if you write internal apps that need to SSO against Okta or Entra ID, but it is a developer building block, not an admin tool. |
| [okta/terraform-provider-okta](https://github.com/okta/terraform-provider-okta) | 3 | identity, automation | production | Official Okta-maintained Terraform provider for managing Okta users, groups, apps, and policies as code, letting you version-control and review identity configuration changes. |
| [vgrem/office365-rest-python-client](https://github.com/vgrem/office365-rest-python-client) | 2 | identity, saas, automation | pilot | Python SDK for SharePoint REST and Microsoft Graph that lets you script M365 admin tasks such as SharePoint site and permission reports, OneDrive files, Teams, and Entra ID users and groups. |
| [pnp/cli-microsoft365](https://github.com/pnp/cli-microsoft365) | 3 | identity, saas, automation | pilot | Cross-platform CLI for administering a Microsoft 365 tenant (SharePoint Online, Teams, Entra ID, OneDrive, Power Platform, Purview) from bash or PowerShell, with JSON output and JMESPath queries for scripting. |
| [EdiWang/Moonglade](https://github.com/EdiWang/Moonglade) | 0 | identity | pilot | A self-hosted personal blog platform in ASP.NET Core. It supports Entra ID/OIDC sign-in, but it does not automate or improve any IT administration task. |
| [jkroepke/openvpn-auth-oauth2](https://github.com/jkroepke/openvpn-auth-oauth2) | 3 | identity, security, network | pilot | Adds OIDC SSO to OpenVPN servers using Entra ID, Okta, Google Workspace or Keycloak, replacing static VPN credentials with your IdP login and MFA policies. |
| [CompassSecurity/EntraFalcon](https://github.com/CompassSecurity/EntraFalcon) | 3 | identity, security, automation | pilot | Read-only PowerShell assessment of Entra ID that flags privileged objects, risky app permissions, users without MFA, Conditional Access gaps and PIM assignments, with output as HTML reports. |
| [vibber-ai/fastapi-azure-auth](https://github.com/vibber-ai/fastapi-azure-auth) | 1 | identity | pilot | Python library for adding Entra ID token validation to FastAPI apps. Useful if you build internal IT tools or APIs that need Entra SSO and role or scope checks, but it is a developer building block rather than an admin tool. |
| [Orange-Cyberdefense/GOAD](https://github.com/Orange-Cyberdefense/GOAD) | 1 | identity, security, network, automation | pilot | Builds an intentionally vulnerable Active Directory lab (multi-forest, SCCM) for practicing attack techniques. Useful for testing AD detections and hardening, not for production admin. |
| [S1ckB0y1337/Active-Directory-Exploitation-Cheat-Sheet](https://github.com/S1ckB0y1337/Active-Directory-Exploitation-Cheat-Sheet) | 2 | identity, security | experimental | AD attack/enumeration cheat sheet useful for sysadmins to understand and test their own Active Directory for Kerberoasting, delegation abuse, ACL weaknesses, and hardening priorities. |
| [Pennyw0rth/NetExec](https://github.com/Pennyw0rth/NetExec) | 2 | identity, security, network | pilot | Pentest tool (successor to CrackMapExec) for auditing Active Directory and Windows networks over SMB, LDAP, WinRM and similar protocols, e.g. finding weak credentials, open shares and misconfigurations. |
| [lazywinadmin/PowerShell](https://github.com/lazywinadmin/PowerShell) | 2 | identity, endpoint, saas, network, automation | experimental | A collection of PowerShell functions for Active Directory, SCCM, Exchange/O365, Azure and VMware admin tasks. It is useful as a script library, but each script needs review and adaptation before use. |
| [AutomatedLab/AutomatedLab](https://github.com/AutomatedLab/AutomatedLab) | 2 | identity, saas, network, automation | pilot | PowerShell framework to spin up Hyper-V or Azure test labs with AD, PKI, Exchange, SQL and ConfigMgr. Useful for testing GPOs, migrations and changes before production, but it does not manage production systems. |
| [lefayjey/linWinPwn](https://github.com/lefayjey/linWinPwn) | 2 | identity, security | pilot | Offensive AD pentesting wrapper (BloodHound, impacket, kerberoast, certipy). Sysadmins can use it to audit their own AD for weaknesses like ZeroLogon, noPac, ASREPRoast and ADCS misconfigs. |
| [lkarlslund/Adalanche](https://github.com/lkarlslund/Adalanche) | 3 | identity, security | pilot | Collects Active Directory ACLs, group memberships and Windows machine data to graph who can effectively reach Domain Admin. It also flags delegation errors, kerberoastable accounts and AD CS misconfigurations. |
| [m14r41/PentestingEverything](https://github.com/m14r41/PentestingEverything) | 1 | security, agent | pilot | A pentesting knowledge base and checklists covering network, Wi-Fi, AD, cloud, and configuration review. Useful as reference when hardening infrastructure or preparing for an external assessment, but it does not automate admin tasks. |
| [dromara/MaxKey](https://github.com/dromara/MaxKey) | 2 | identity, security | production | Self-hosted open-source IdP providing SSO (SAML, OIDC, CAS), MFA, SCIM provisioning and AD/LDAP account management. An alternative to Okta/Entra, but it requires running and maintaining a Java/MySQL stack. |
| [MichaelGrafnetter/DSInternals](https://github.com/MichaelGrafnetter/DSInternals) | 3 | identity, security, automation | pilot | PowerShell module for Active Directory password auditing (shared and breached passwords via Test-PasswordQuality), key credential audits, LAPS and BitLocker key recovery, and DC recovery from IFM backups. |
| [jm33-m0/emp3r0r](https://github.com/jm33-m0/emp3r0r) | 0 | identity | pilot | This is an offensive C2/post-exploitation and malware framework for red teaming, not a tool for administering identity, endpoints, SaaS, or networks. |
| [The-Viper-One/PsMapExec](https://github.com/The-Viper-One/PsMapExec) | 1 | security | experimental | Offensive post-exploitation framework for Active Directory, useful for red-team testing but not a routine admin task. Could inform defensive hardening. |
| [ASCIT31/Dark-Moon](https://github.com/ASCIT31/Dark-Moon) | 2 | security, automation | production | Autonomous AI penetration testing across web, AD, cloud, K8s and CI/CD, runnable on a local LLM for self-hosted vulnerability assessment of your own infrastructure. |
| [dirkjanm/ROADtools](https://github.com/dirkjanm/ROADtools) | 3 | identity, security | pilot | Dumps and explores all Entra ID/Azure AD data into a queryable offline database for security review and access analysis; useful for blue-team audits of tenant configuration. |
| [maester365/maester](https://github.com/maester365/maester) | 3 | identity, saas, security, automation | production | PowerShell framework that runs automated security configuration checks against Entra ID and Microsoft 365 tenants (Conditional Access, Exchange, etc.) and reports drift, with CI/CD and Teams/email notifications. |
| [pnp/powershell](https://github.com/pnp/powershell) | 3 | identity, saas, automation, agent | production | Widely used PowerShell module with 900+ cmdlets for administering SharePoint Online, Teams and other Microsoft 365 workloads, e.g. site provisioning, permissions reports and bulk changes. |
| [dotnet/dev-proxy](https://github.com/dotnet/dev-proxy) | 1 | automation | production | Developer tool that intercepts HTTP calls to simulate API errors and throttling, including Microsoft Graph rate limits. It can help test whether internal Graph automation scripts handle 429s and retries. |
| [microsoftgraph/msgraph-sdk-javascript](https://github.com/microsoftgraph/msgraph-sdk-javascript) | 1 | identity, saas, automation | production | Official JavaScript/TypeScript SDK for Microsoft Graph, a building block for custom scripts that query or manage Entra ID users, groups, and Microsoft 365 data such as mail and OneDrive. |
| [LETHAL-FORENSICS/Microsoft-Analyzer-Suite](https://github.com/LETHAL-FORENSICS/Microsoft-Analyzer-Suite) | 3 | identity, saas, security, automation | pilot | Analyzes Entra ID sign-in/audit logs, M365 Unified Audit Log, MFA status, OAuth grants, mailbox permissions and transport rules exported by Microsoft-Extractor-Suite, for incident response and tenant review. |
| [HotCakeX/Harden-Windows-Security](https://github.com/HotCakeX/Harden-Windows-Security) | 2 | endpoint, security | pilot | Hardens Windows using Microsoft-supported settings (Defender, BitLocker, firewall, WDAC). AppControl Manager helps build and deploy App Control for Business policies. Useful for baseline and application-allowlisting work. |
| [PSAppDeployToolkit/PSAppDeployToolkit](https://github.com/PSAppDeployToolkit/PSAppDeployToolkit) | 3 | endpoint, patching, automation | pilot | PowerShell framework for packaging and deploying Windows apps through Intune, ConfigMgr or Tanium, with standard install/uninstall workflows, user prompts, deferrals and logging. |
| [Microsoft365DSC/Microsoft365DSC](https://github.com/Microsoft365DSC/Microsoft365DSC) | 3 | identity, endpoint, saas, security, automation | production | Exports, deploys and monitors Microsoft 365 tenant configuration (Entra ID, Exchange, Intune, Teams, SharePoint, Defender) as PowerShell DSC code, so you can back it up and catch configuration drift. |
| [Micke-K/IntuneManagement](https://github.com/Micke-K/IntuneManagement) | 3 | endpoint, security, automation | pilot | Exports, backs up, documents, compares and migrates Intune policies and profiles, including assignments, between tenants via Graph, with a UI or silent batch mode. |
| [SkipToTheEndpoint/OpenIntuneBaseline](https://github.com/SkipToTheEndpoint/OpenIntuneBaseline) | 3 | endpoint, security | pilot | Ready-made Intune security baseline policies for Windows, Windows 365 and macOS, mapped to CIS, NCSC and Essential Eight, for hardening managed devices without building every policy by hand. |
| [microsoft/shell-intune-samples](https://github.com/microsoft/shell-intune-samples) | 3 | endpoint, patching, security, automation | production | Microsoft-maintained shell script samples for Intune-managed macOS and Linux: app installs, device config, custom attributes and Linux custom compliance checks. |
| [HarmVeenstra/Powershellisfun](https://github.com/HarmVeenstra/Powershellisfun) | 2 | identity, endpoint, patching, saas, security, network, automation | pilot | Collection of blog-backed PowerShell scripts for Intune printer/WinGet deployment, AD permission reports, Exchange permission copying, M365 license reports and MFA setup. Each needs per-script review and adaptation. |
| [Macjutsu/super](https://github.com/Macjutsu/super) | 3 | endpoint, patching, security | pilot | Enforces macOS and Apple software updates with user dialogs, deferrals, deadlines, and restarts, and can run Jamf Pro policies. Covers a recurring Mac patch-compliance task. |
| [deploymenttheory/terraform-provider-jamfpro](https://github.com/deploymenttheory/terraform-provider-jamfpro) | 3 | endpoint, patching, automation | production | Terraform provider that manages Jamf Pro configuration (policies, groups, profiles, apps) as code, enabling version control, change review, drift detection and replication across tenants. |
| [micromdm/micromdm](https://github.com/micromdm/micromdm) | 2 | endpoint, automation | pilot | Open-source API-driven Apple MDM server for enrolling Macs/iOS devices via DEP and pushing commands, but v1 is in maintenance mode with support ending 2025; NanoMDM is the successor. |
| [fleetdm/fleet](https://github.com/fleetdm/fleet) | 3 | endpoint, patching, security, automation | pilot | Open-source MDM and osquery-based device management for macOS, Windows, Linux, iOS and Android: inventory, software deployment and patching, CIS benchmark checks, and GitOps-managed config. |
| [zinggAI/zingg](https://github.com/zinggAI/zingg) | 1 | endpoint | production | Spark-based ML entity resolution for customer/master data. It is a data engineering tool, though it could help dedupe messy asset or user records merged from multiple HR/IT systems. |
| [datacleaner/DataCleaner](https://github.com/datacleaner/DataCleaner) | 1 | automation | experimental | General data quality and profiling desktop tool. Sysadmins could use it to profile and deduplicate exported directory or asset inventory data, but it is not IT-admin specific. |
| [h-mdm/hmdm-server](https://github.com/h-mdm/hmdm-server) | 2 | endpoint, patching | pilot | Self-hosted open-source Android MDM: QR enrollment, app deployment, device groups and configuration. Useful for Android fleets or kiosks outside Intune, but key lockdown features are in the paid edition. |
| [xxh/xxh](https://github.com/xxh/xxh) | 1 | automation | experimental | Carries your local shell (zsh, fish, xonsh, bash) and dotfiles to remote Linux hosts over SSH without root. It is a convenience for admins working on Linux servers, and it does not automate any admin task. |
| [chainguard-dev/osquery-defense-kit](https://github.com/chainguard-dev/osquery-defense-kit) | 2 | endpoint, security | experimental | Ships 250+ osquery detection, policy and incident-response queries for macOS and Linux fleets, tuned to return zero rows normally so they can drive alerts in a SIEM or fleet manager. |
| [jmpsec/osctrl](https://github.com/jmpsec/osctrl) | 3 | endpoint, security, automation, agent | production | Self-hosted osquery fleet manager for running distributed queries across endpoints, carving files, alerting on node state, and tracking posture mapped to SOC 2/ISO 27001. Includes an MCP server for fleet inspection. |
| [googleworkspace/cli](https://github.com/googleworkspace/cli) | 3 | identity, saas, automation, agent | production | A CLI built from Google's Discovery Service that covers every Workspace API, Admin included. Use it to script user, group, Drive and Gmail admin tasks with JSON output, and it ships agent skills for LLM-driven management. |
| [googleworkspace/apps-script-samples](https://github.com/googleworkspace/apps-script-samples) | 2 | saas, automation | experimental | Official Google Apps Script samples, including Admin SDK directory and domain management, Drive activity, and Gmail examples, that Workspace admins can adapt into scripts for user, group and Drive tasks. |
| [googleworkspace/apps-script-oauth2](https://github.com/googleworkspace/apps-script-oauth2) | 1 | saas, automation | pilot | Apps Script library that handles OAuth2 token flows and refresh. Useful as a building block when Google Workspace admin scripts need to call third-party APIs such as Okta or Slack. |
| [googleworkspace/python-samples](https://github.com/googleworkspace/python-samples) | 1 | saas, automation | pilot | Official Python quickstart samples for Google Workspace APIs, including Admin SDK Directory and Reports. Useful as starting code for scripting user listings or audit log pulls, but not a finished tool. |
| [googleworkspace/google-chat-samples](https://github.com/googleworkspace/google-chat-samples) | 1 | saas, automation | experimental | Developer samples for building Google Chat apps and bots. Useful as a starting point for IT teams building helpdesk bots or webhook alerts into Google Chat, but they are not admin tooling. |
| [googleworkspace/node-samples](https://github.com/googleworkspace/node-samples) | 1 | saas, automation | pilot | Official Node.js code samples for Google Workspace APIs (Drive, Slides, etc.), useful as reference snippets when writing custom Workspace admin scripts. |
| [SharePoint/sp-dev-docs](https://github.com/SharePoint/sp-dev-docs) | 1 | saas | pilot | Source for Microsoft's SharePoint developer docs (SPFx, site scripts, list formatting). Mostly developer-focused, but site templates and column formatting docs help SharePoint admins. |
| [cyb3rmik3/KQL-threat-hunting-queries](https://github.com/cyb3rmik3/KQL-threat-hunting-queries) | 2 | security | pilot | Collection of KQL hunting and detection queries for Microsoft Sentinel and Defender XDR, useful for M365 security teams writing hunts or analytics rules. Currently being rebuilt, so content may be in flux. |
| [kesslernity/awesome-copilot-studio-agents](https://github.com/kesslernity/awesome-copilot-studio-agents) | 1 | saas | experimental | A library of prompt instruction blocks for M365 Copilot declarative agents, mostly aimed at business users (writing, PM, HR). M365 admins rolling out Copilot could use it as starter content for users. |
| [zitadel/zitadel](https://github.com/zitadel/zitadel) | 2 | identity | production | Self-hostable IdP providing SSO (OIDC/SAML), MFA, passkeys, SCIM and LDAP federation. Mainly for app developers and B2B platforms, but usable as an internal IdP alternative to Keycloak or Okta. |
| [casdoor/casdoor](https://github.com/casdoor/casdoor) | 2 | identity, agent | production | Self-hosted IdP providing SSO via OIDC, SAML, CAS, LDAP and SCIM with MFA, federating to Google Workspace and Entra ID. Useful for internal apps or labs, but it is an alternative IdP rather than a tool for managing Okta or Entra. |
| [kanidm/kanidm](https://github.com/kanidm/kanidm) | 2 | identity, security, network | production | Self-hosted identity provider with OIDC SSO, passkeys, RADIUS for VPN/Wi-Fi, SSH key distribution and Linux login. An alternative to FreeIPA/Keycloak, not a tool for managing Okta or Entra ID. |
| [kdeldycke/awesome-iam](https://github.com/kdeldycke/awesome-iam) | 1 | identity, security | pilot | Curated reading list on IAM concepts (SSO, MFA, SAML, SCIM, passkeys, zero trust). It's aimed mostly at developers building auth, but useful background for admins designing identity policy. |
| [sebadob/rauthy](https://github.com/sebadob/rauthy) | 2 | identity, security | pilot | Self-hosted OIDC/OAuth2 identity provider with passkey MFA, SCIM, audit events, and a PAM module for Linux host logins. A lightweight Keycloak alternative for SSO on internal apps and servers. |

## Not found on GitHub

Fix or remove these in `curation/`:

- snipe/snipe-it

## Fetch problems

GitHub returned errors for 685 repo(s). They are still ranked, but their stars gained is unknown this week.

- `Resource not accessible by integration`

The built-in Actions token can't read this. Add a `GH_PAT` repository secret (a fine-grained token with read-only access to public repositories) and re-run the refresh.
