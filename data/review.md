# Weekly refresh: 2026-11-02

Review the changes below. To change a score, tag or note, edit `curation/overrides.yaml` in this PR; overrides beat Claude's first pass.

| Candidates | IT-relevant | Passed gate | Scored by Claude this run | Needs review |
|---|---|---|---|---|
| 1038 | 695 | 195 | 28 | 0 |

## IT Ops lens changes

- ⬆️ **CrowdStrike/falconpy** entered at #1
- ⬆️ **jmpsec/osctrl** entered at #2
- ⬆️ **netbox-community/netbox** entered at #3
- ⬆️ **Softeria/ms-365-mcp-server** entered at #4
- ⬆️ **grokability/snipe-it** entered at #5
- ⬆️ **pnp/powershell** entered at #6
- ⬆️ **taylorwilsdon/google_workspace_mcp** entered at #7
- ⬆️ **GAM-team/GAM** entered at #8
- ⬆️ **Installomator/Installomator** entered at #9
- ⬆️ **maester365/maester** entered at #10
- ⬆️ **glpi-project/glpi** entered at #11
- ⬆️ **autopkg/autopkg** entered at #12
- ⬆️ **cisagov/ScubaGear** entered at #13
- ⬆️ **googleworkspace/cli** entered at #14
- ⬆️ **prowler-cloud/prowler** entered at #15

## Scored by Claude this run

| Repo | Fit | Tags | Trust | Why for sysadmins |
|---|---|---|---|---|
| [UCS-Care-Group/mailcraft](https://github.com/UCS-Care-Group/mailcraft) | 1 | saas, agent | production | An alpha Rust mail/calendar client for Microsoft 365 and IMAP that includes an MCP server and a command channel. It is an end-user client, not an admin tool, so its IT use is limited to scripted mailbox actions. |
| [ehmo/gum](https://github.com/ehmo/gum) | 2 | identity, saas, automation, agent | pilot | CLI and MCP server for calling Google Workspace APIs (Admin, Gmail, Drive, Vault, Calendar), with read/write/destructive separation and confirmation gates. Useful for scripting or agent-assisted Workspace admin queries. |
| [useopendesk/opendesk](https://github.com/useopendesk/opendesk) | 2 | helpdesk | production | Self-hostable shared support inbox with ticketing, SLAs, a knowledge base and live chat. It could serve as an internal IT helpdesk, though it is built mainly for customer support rather than ITSM or asset management. |
| [lacs-project/sysknife](https://github.com/lacs-project/sysknife) | 2 | endpoint, security, automation, agent | production | MCP server that lets an AI assistant administer Ubuntu/Fedora Atomic hosts through typed, human-approved actions (apt, ufw, systemd) with a signed audit log. Useful for Linux server ops, not mainstream SaaS/MDM stacks. |
| [dataplat/dbatools](https://github.com/dataplat/dbatools) | 2 | network, automation | production | PowerShell module with ~700 commands for SQL Server administration: backup verification, instance migration, finding databases across servers, and health checks. Most useful where IT also looks after SQL Server. |
| [cmderdev/cmder](https://github.com/cmderdev/cmder) | 1 | automation | pilot | Portable Windows console emulator with tabbed cmd, PowerShell and Bash shells. It is a convenience for admins doing daily CLI work but does not administer any IT system itself. |
| [ansible/ansible](https://github.com/ansible/ansible) | 2 | network, automation | production | Agentless SSH/WinRM configuration management for pushing config, packages and ad-hoc commands to servers and network gear. It is a general platform rather than a turnkey fix for identity or MDM tasks. |
| [crossplane/crossplane](https://github.com/crossplane/crossplane) | 1 | network, automation | production | Kubernetes-based control plane for declaratively managing cloud infrastructure; relevant to platform/cloud engineers more than identity, endpoint or SaaS admins. |
| [fatedier/frp](https://github.com/fatedier/frp) | 2 | network | pilot | Self-hosted reverse proxy and tunnel for exposing internal services (SSH, RDP, web apps) behind NAT or firewalls. Useful for remote access to lab or branch systems, but it bypasses perimeter controls, so it needs security review. |
| [terraform-aws-modules/terraform-aws-iam](https://github.com/terraform-aws-modules/terraform-aws-iam) | 2 | identity, security, automation | production | Terraform modules for managing AWS IAM users, groups, roles, password policy, and SAML/OIDC trust roles for IdPs like Okta. Useful for IT teams that own AWS account access as code. |
| [macadmins/nudge](https://github.com/macadmins/nudge) | 3 | endpoint, patching, security | pilot | Prompts Mac users to install required macOS updates with configurable deferrals and deadlines, using the SOFA feed to track current releases. Deploy it via Jamf or Intune. |
| [munki/munki](https://github.com/munki/munki) | 3 | endpoint, patching | pilot | Munki manages software installs, removals and Apple update prompts on Mac fleets from a web-hosted package repository. It is widely paired with Jamf or Intune for app deployment. |
| [swiftDialog/swiftDialog](https://github.com/swiftDialog/swiftDialog) | None |  | production |  |
| [microsoft/mcp](https://github.com/microsoft/mcp) | 2 | network, automation, agent | production | Hosts the official Azure MCP Server and catalogs Microsoft MCP servers, letting agents query Azure resources. Useful for cloud infra admins, less so for identity, endpoint or M365 administration. |
| [okta/okta-sdk-python](https://github.com/okta/okta-sdk-python) | 2 | identity, automation | production | Official Python SDK for the Okta Management API, used to script user lifecycle, group membership, and app assignment tasks. It is a building block, so you write your own automation on top of it. |
| [microsoftgraph/msgraph-sdk-powershell](https://github.com/microsoftgraph/msgraph-sdk-powershell) | 3 | identity, endpoint, saas, security, automation | pilot | Official PowerShell modules for Microsoft Graph, used to script Entra ID users and groups, Intune devices, Exchange/Teams data and compliance tasks across Microsoft 365. |
| [Jamf-Concepts/mcp-hub](https://github.com/Jamf-Concepts/mcp-hub) | 3 | endpoint, security, automation, agent | pilot | MCP server from Jamf with 50 tools for querying and managing Jamf Pro devices, smart groups, policies and profiles, plus Jamf Protect alerts and Security Cloud risk status. |
| [CrowdStrike/falconpy](https://github.com/CrowdStrike/falconpy) | 3 | endpoint, security, automation | production | Official Python SDK for the CrowdStrike Falcon API, used to script host inventory, detections, containment, policy and sensor management without hand-rolling OAuth2 token handling. |
| [fortinetdev/terraform-provider-fortios](https://github.com/fortinetdev/terraform-provider-fortios) | 3 | security, network, automation | production | Official Fortinet Terraform provider for managing FortiGate (FortiOS 6.0–7.6) firewall policies, addresses, VPNs and interfaces as code, replacing manual GUI changes. |
| [grokability/snipe-it](https://github.com/grokability/snipe-it) | 3 | endpoint, helpdesk | production | Self-hosted IT asset and license management for tracking who has which laptop, purchase and depreciation data, and software licenses. It has a REST API and integrations such as jamf2snipe and Kandji2Snipe. |
| [bregman-arie/devops-exercises](https://github.com/bregman-arie/devops-exercises) | 1 | automation | experimental | Interview questions and exercises covering Linux, networking, DNS, Ansible, Terraform and cloud; useful for skills study or for building hiring questions, not an operational tool. |
| [MicrosoftDocs/PowerShell-Docs](https://github.com/MicrosoftDocs/PowerShell-Docs) | 1 | automation | experimental | Source for the official PowerShell cmdlet reference and conceptual docs. It is useful as a reference while writing admin scripts, but it is documentation, not a tool. |
| [MichaelCade/90DaysOfDevOps](https://github.com/MichaelCade/90DaysOfDevOps) | 1 | network, automation | experimental | A free learning curriculum covering DevOps basics like Linux, networking, Terraform, Ansible and containers. Useful for sysadmins building automation skills, but it is training material rather than an admin tool. |
| [hashicorp/terraform](https://github.com/hashicorp/terraform) | 2 | network, automation | pilot | Terraform core is the IaC engine behind providers for Okta, Entra ID, Google Workspace and cloud networks, letting admins version and review tenant and infrastructure config. It needs separate providers and workflow setup to be useful. |
| [pester/Pester](https://github.com/pester/Pester) | 2 | automation | pilot | Test and mock framework for PowerShell, used to validate admin scripts and modules before running them against production, and to write infrastructure state checks such as config or file presence tests. |
| [netbirdio/netbird](https://github.com/netbirdio/netbird) | 3 | identity, security, network | pilot | Self-hostable WireGuard mesh VPN/ZTNA with IdP SSO, group sync, posture checks and access policies. A candidate to replace a legacy VPN for remote access to internal resources. |
| [assafdori/bypass-mdm](https://github.com/assafdori/bypass-mdm) | 1 | endpoint | experimental | A script to bypass macOS MDM enrollment. Useful for sysadmins only as awareness of an evasion technique their fleet must defend against, not a management tool. |
| [awesome-foss/awesome-sysadmin](https://github.com/awesome-foss/awesome-sysadmin) | 1 | identity, network, automation, helpdesk | experimental | Curated index of open-source sysadmin software (backups, LDAP/SSO, asset management, monitoring, VPN) useful for finding self-hosted tools, but it is a list, not a tool. |
