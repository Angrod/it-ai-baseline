# Weekly refresh: 2026-11-24

Review the changes below. To change a score, tag or note, edit `curation/overrides.yaml` in this PR; overrides beat Claude's first pass.

| Candidates | IT-relevant | Passed gate | Scored by Claude this run | Needs review |
|---|---|---|---|---|
| 1543 | 724 | 220 | 22 | 0 |

## IT Ops lens changes

- ⬆️ **glpi-project/glpi** entered at #7
- ⬆️ **macadmins/nudge** entered at #14
- ⬇️ googleworkspace/cli left the top 15
- ⬇️ prowler-cloud/prowler left the top 15

## Scored by Claude this run

| Repo | Fit | Tags | Trust | Why for sysadmins |
|---|---|---|---|---|
| [yuezk/GlobalProtect-openconnect](https://github.com/yuezk/GlobalProtect-openconnect) | 2 | identity, endpoint, network | pilot | Open-source GlobalProtect VPN client with SAML SSO/MFA and HIP reporting, useful for supporting Linux/BSD users or headless hosts that need access to a Palo Alto VPN. |
| [BenTheCyberOne/Copperhound](https://github.com/BenTheCyberOne/Copperhound) | 2 | identity, security | pilot | Analyzes AD, ADCS and Entra ID attack paths from SharpHound/AzureHound data, ranks findings and plans remediation of privilege exposure to Tier Zero. Useful for identity hardening, though it needs collection data and AD security know-how. |
| [dromara/MaxKey](https://github.com/dromara/MaxKey) | 2 | identity | production | Self-hosted IAM/SSO platform supporting SAML, OIDC, CAS, SCIM, LDAP/AD sync, MFA and password self-service. An alternative to Keycloak or Okta for on-prem identity and lifecycle management. |
| [PlumHound/PlumHound](https://github.com/PlumHound/PlumHound) | 2 | identity, security | production | Turns BloodHound Neo4j data into HTML reports on AD privilege issues such as Kerberoastable users, delegation, DCSync rights, GPO owners and local admins, for hardening work. |
| [ASCIT31/Dark-Moon](https://github.com/ASCIT31/Dark-Moon) | 2 | security, agent | pilot | Autonomous AI pentesting tool for finding/exploiting vulnerabilities across web, AD, cloud and Kubernetes; useful for vulnerability assessment on authorized infrastructure. |
| [NH-RED-TEAM/RustHound](https://github.com/NH-RED-TEAM/RustHound) | 2 | identity, security | pilot | Collects Active Directory objects (users, groups, GPOs, ADCS) into BloodHound JSON for attack-path analysis, useful for AD security audits and hardening reviews. |
| [Mafifrizi/ARES](https://github.com/Mafifrizi/ARES) | 2 | security, agent | pilot | Red-team validation platform that proves exploitable attack paths against AD and cloud, maps MITRE ATT&CK, and produces audit-ready reports for defensive posture validation. |
| [RushB-fr/freekiosk](https://github.com/RushB-fr/freekiosk) | 2 | endpoint, automation | production | Locks Android tablets into single-app or web kiosk mode via Device Owner, with ADB provisioning and a REST/MQTT API for signage, POS and lobby devices. It's a cheaper alternative to Fully Kiosk. |
| [labnol/apps-script-starter](https://github.com/labnol/apps-script-starter) | 1 | saas, automation | pilot | Boilerplate for writing Google Apps Script projects locally with Vite, Jest and clasp. Useful if you build Workspace automations or add-ons, but it does not perform any admin tasks itself. |
| [netdata/netdata](https://github.com/netdata/netdata) | 2 | security, network, agent | production | Self-hosted per-second monitoring for servers, VMs, SNMP network gear, NetFlow and hardware (IPMI/Redfish), with anomaly detection and alerting. It is useful for infrastructure monitoring, but it is not focused on identity or endpoint management. |
| [Patrowl/PatrowlManager](https://github.com/Patrowl/PatrowlManager) | 2 | security, automation | pilot | Self-hosted platform for orchestrating vulnerability scans across assets, aggregating findings, and relaying alerts to TheHive or Splunk. Requires deploying separate scan engines alongside it. |
| [Community-VyProjects/VyManager](https://github.com/Community-VyProjects/VyManager) | 2 | network, agent | production | Web control plane for managing VyOS routers across multiple sites: firewall and routing config, live dashboards and per-site RBAC. Useful only if your network runs on VyOS. |
| [bitwire-it/ipblocklist](https://github.com/bitwire-it/ipblocklist) | 2 | security, network | pilot | Aggregated inbound/outbound IP blocklists refreshed every 2 hours, usable as external dynamic lists on pfSense, OPNsense, FortiGate, Palo Alto, or UniFi firewalls to block scanners and C2 traffic. |
| [rana-gmbh/NetFluss](https://github.com/rana-gmbh/NetFluss) | 1 | network | pilot | A personal menu bar/taskbar network monitor with per-app bandwidth, router stats (UniFi, OpenWrt, Fritzbox), DNS switching and a VPN client. It is handy for troubleshooting a single machine but is not a fleet management tool. |
| [7wdn/7shell](https://github.com/7wdn/7shell) | 2 | security, network, automation, agent | pilot | Desktop SSH/SFTP/RDP client with batch command execution, host monitoring, Docker/Kubernetes and VMware Workstation management, plus an MCP server with risk rules and an audit log. |
| [Armur-Ai/Pentest-Swarm-AI](https://github.com/Armur-Ai/Pentest-Swarm-AI) | 2 | security, automation | production | Autonomous AI pentesting swarm for web apps and APIs with verification oracles; useful for security teams running authorized vulnerability testing against their own assets. |
| [gnacho/netpulse](https://github.com/gnacho/netpulse) | 1 | network | pilot | Self-hosted dashboard for monitoring OpenWrt/GL.iNet home routers, with topology, device inventory, WireGuard peers and speed tests. It is aimed at home networks, though small offices running OpenWrt, OPNsense or UniFi may get some use from it. |
| [CISOfy/lynis](https://github.com/CISOfy/lynis) | 3 | endpoint, security | production | Agentless shell tool that audits Linux, macOS and BSD hosts for hardening gaps, vulnerable packages and misconfigurations, producing findings useful as compliance evidence (PCI DSS, HIPAA, ISO27001). |
| [appwrite/appwrite](https://github.com/appwrite/appwrite) | 1 | network | production | Backend-as-a-service platform for app developers covering auth, databases, storage and functions. Useful to IT mainly if you build or self-host internal apps, not for administering identity, endpoints or SaaS. |
| [kyverno/kyverno](https://github.com/kyverno/kyverno) | 1 | security, automation | production | Kubernetes admission policy engine for enforcing pod security standards, CIS policies and image signature checks. Relevant only to IT teams that run Kubernetes clusters; it does not cover identity, endpoint or SaaS admin. |
| [mjmirza/app-store-compliance](https://github.com/mjmirza/app-store-compliance) | 0 | security, agent | pilot | A pre-submission checker for mobile app developers publishing to the App Store or Google Play. It does not touch any IT administration task such as MDM, identity or SaaS admin. |
| [sandbox-quantum/switch](https://github.com/sandbox-quantum/switch) | 1 | automation, agent | pilot | Self-hosted chatops platform that puts AI coding agents into Slack/Teams channels with connectors like Google Workspace and GitHub. It is aimed at dev teams, not IT admin tasks, but could host helpdesk or runbook agents. |
