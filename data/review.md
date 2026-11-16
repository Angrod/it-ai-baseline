# Weekly refresh: 2026-11-16

Review the changes below. To change a score, tag or note, edit `curation/overrides.yaml` in this PR; overrides beat Claude's first pass.

| Candidates | IT-relevant | Passed gate | Scored by Claude this run | Needs review |
|---|---|---|---|---|
| 1470 | 712 | 209 | 13 | 0 |

## IT Ops lens changes

- ⬆️ **crowdsecurity/crowdsec** entered at #10
- ⬇️ glpi-project/glpi left the top 15

## Scored by Claude this run

| Repo | Fit | Tags | Trust | Why for sysadmins |
|---|---|---|---|---|
| [jm33-m0/emp3r0r](https://github.com/jm33-m0/emp3r0r) | 0 | identity, security, agent | pilot | This is an offensive C2/post-exploitation framework for red teaming and malware operations, not a tool for administering IT systems. |
| [fleetdm/fleet](https://github.com/fleetdm/fleet) | 3 | endpoint, patching, security, automation | pilot | Open-source MDM and osquery-based device management for macOS, Windows, Linux, iOS and Android. It covers inventory, software deployment, patching, CIS benchmark checks and GitOps-managed configuration. |
| [zinggAI/zingg](https://github.com/zinggAI/zingg) | 1 | endpoint | production | Spark-based ML entity resolution for deduplicating customer/master data. 'Identity resolution' here means customer records, not IAM; marginal use for deduping exported user or asset lists. |
| [Bytedesk/bytedesk](https://github.com/Bytedesk/bytedesk) | 1 | helpdesk | pilot | Self-hosted omnichannel customer-service platform with ticketing, SLA tracking and a knowledge base; built for external customer support rather than internal IT, though it could serve as a basic ticket desk. |
| [GroundedCoreAI/nexusdesk](https://github.com/GroundedCoreAI/nexusdesk) | 1 | helpdesk, agent | pilot | Self-hosted AI agent platform aimed at external customer support with RAG knowledge bases and ticketing; could be adapted into an internal IT helpdesk bot but has no built-in IT system integrations. |
| [pipeshub-ai/pipeshub-ai](https://github.com/pipeshub-ai/pipeshub-ai) | 1 | saas, helpdesk, agent | production | Self-hosted enterprise search and RAG platform that indexes Slack, Google Drive, Microsoft 365, Jira and Confluence with permission sync. IT may deploy or run it as an internal knowledge or helpdesk answer layer, but it is not an admin tool. |
| [community-scripts/ProxmoxVE](https://github.com/community-scripts/ProxmoxVE) | 2 | network, automation | production | One-command shell scripts that deploy 700+ services as LXC containers or VMs on Proxmox VE, plus host post-install and maintenance tooling. Most relevant to admins running Proxmox infrastructure. |
| [projectdiscovery/nuclei](https://github.com/projectdiscovery/nuclei) | 2 | security, network | production | Template-based vulnerability scanner for checking internal and external hosts, web apps, DNS and TLS for known CVEs and misconfigurations. It is useful for periodic exposure checks, but it is security-team oriented. |
| [kubescape/kubescape](https://github.com/kubescape/kubescape) | 1 | security, network, agent | production | Scans Kubernetes clusters, manifests and images against CIS, NSA-CISA and MITRE baselines for misconfigurations and CVEs. This is useful only where IT runs Kubernetes, which is mostly platform/DevOps territory. |
| [crowdsecurity/crowdsec](https://github.com/crowdsecurity/crowdsec) | 3 | security, network | production | Log-based IDS/IPS and WAF that detects brute force, port scans and web scans on Linux/Windows servers and blocks malicious IPs at firewalls or reverse proxies. A fail2ban replacement with a shared community blocklist. |
| [gravitational/teleport](https://github.com/gravitational/teleport) | 2 | identity, security, network | production | Self-hosted access proxy that puts SSH, RDP, Kubernetes and database access behind SSO with Okta or Entra ID, short-lived certificates, JIT access requests and session recording for audit. |
| [meshery/meshery](https://github.com/meshery/meshery) | 1 | network, automation | production | Kubernetes multi-cluster management platform with visual GitOps design and dry-run deployments. Useful only to IT teams that run Kubernetes infrastructure; it does not touch identity, endpoint or SaaS administration. |
| [SigmaHQ/sigma](https://github.com/SigmaHQ/sigma) | 2 | security | pilot | Library of 3000+ vendor-agnostic SIEM detection rules (Windows, Sysmon, cloud, compliance) that convert to Splunk, Elastic, Sentinel and other query languages for building detections. |
