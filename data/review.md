# Weekly refresh: 2026-11-09

Review the changes below. To change a score, tag or note, edit `curation/overrides.yaml` in this PR; overrides beat Claude's first pass.

| Candidates | IT-relevant | Passed gate | Scored by Claude this run | Needs review |
|---|---|---|---|---|
| 1301 | 706 | 203 | 14 | 0 |

## Scored by Claude this run

| Repo | Fit | Tags | Trust | Why for sysadmins |
|---|---|---|---|---|
| [yuezk/GlobalProtect-openconnect](https://github.com/yuezk/GlobalProtect-openconnect) | 2 | identity, network | pilot | Third-party GlobalProtect VPN client for Linux/BSD/macOS with SAML SSO, MFA, and HIP reports. Useful for supporting Linux users on a Palo Alto VPN that has no official client option. |
| [jm33-m0/emp3r0r](https://github.com/jm33-m0/emp3r0r) | 0 | identity, agent | pilot | This is an offensive C2/post-exploitation and malware framework for red teaming, not a tool for administering identity, endpoints, SaaS, or networks. |
| [Badgerati/Pode](https://github.com/Badgerati/Pode) | 1 | automation | pilot | PowerShell web framework for wrapping existing admin scripts in REST APIs or small internal web tools, with Windows/Azure AD auth and cron-style scheduled tasks. It is a building block, not a ready-made admin tool. |
| [HelpCode-ai/anythingmcp](https://github.com/HelpCode-ai/anythingmcp) | 1 | automation, agent | production | Self-hosted MCP gateway that exposes REST, SOAP, SQL and file shares to AI clients with RBAC and audit logs. Its connectors focus on ERP and e-commerce, so for IT admins it is mainly a platform for building agents, not a sysadmin tool. |
| [IainKay/ram-altman](https://github.com/IainKay/ram-altman) | 0 | automation | experimental | A parody bash script that emails a daily joke about unused RAM. Its /proc/meminfo accounting is correct, but it is not a practical memory monitoring tool for IT work. |
| [Windshiftapp/core](https://github.com/Windshiftapp/core) | 2 | automation, helpdesk, agent | production | Self-hosted Jira/JSM alternative with service desk queues, SLAs, request portal, knowledge base and asset/CMDB register; could host IT ticketing and asset tracking with LDAP/OIDC SSO. |
| [capture0x/AdStrike](https://github.com/capture0x/AdStrike) | 1 | identity, security, agent | experimental | Offensive AD red-team framework; useful for authorized pentesting/AD security validation, but it's an attack tool rather than a day-to-day sysadmin operations tool. |
| [pocket-id/pocket-id](https://github.com/pocket-id/pocket-id) | 2 | identity, security | production | Self-hosted OIDC/OAuth 2.0 provider with passkey-only sign-in, useful for adding SSO and phishing-resistant MFA to internal or self-hosted apps without the complexity of Keycloak. |
| [bridgecrewio/checkov-action](https://github.com/bridgecrewio/checkov-action) | 1 | security, automation | pilot | GitHub Action that runs Checkov to scan Terraform, CloudFormation, Kubernetes and container images for misconfigurations; useful for IT teams managing infrastructure-as-code in GitHub repos. |
| [bivlked/amneziawg-installer](https://github.com/bivlked/amneziawg-installer) | 1 | network, automation | pilot | One-command Bash installer for a self-hosted AmneziaWG (obfuscated WireGuard) VPN server on Ubuntu/Debian with client QR codes. It suits personal or anti-censorship use more than corporate remote access. |
| [hashicorp/terraform-provider-azurerm](https://github.com/hashicorp/terraform-provider-azurerm) | 2 | network, automation | production | Official Terraform provider for managing Azure infrastructure as code, such as resource groups, virtual networks and VMs. It is useful for teams running Azure infrastructure, though it is cloud-infra focused rather than Entra/Intune admin. |
| [open-policy-agent/opa](https://github.com/open-policy-agent/opa) | 1 | security, automation | production | General-purpose policy engine (Rego) for authorization and compliance checks across Kubernetes, Terraform, Docker and SSH/sudo. Mostly a platform/DevOps building block; it does not directly cover mainstream IT admin stacks. |
| [google/osv-scanner](https://github.com/google/osv-scanner) | 2 | security | production | Scans source dependencies, container images and Linux OS packages for known vulnerabilities using OSV.dev. Useful for vulnerability checks on internal scripts, tools and server images, but it targets developer dependencies more than managed endpoints. |
| [pipeshub-ai/pipeshub-ai](https://github.com/pipeshub-ai/pipeshub-ai) | 1 | saas, helpdesk, agent | production | Self-hosted enterprise search over Slack, Drive, Microsoft 365, Jira and Confluence with permission-aware results and an MCP server. IT might run it as a knowledge platform, but it does not administer those systems. |
