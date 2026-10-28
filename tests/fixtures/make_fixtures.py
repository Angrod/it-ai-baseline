"""Regenerate the offline fixtures: python tests/fixtures/make_fixtures.py

All numbers are synthetic. The repos are real names so the curation files
resolve, plus a few clearly fake `acme-it/*` repos that exercise edge cases.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).parent
NOW = datetime(2026, 10, 26, 12, 0, tzinfo=timezone.utc)


def ts(days_ago: float) -> str:
    return (NOW - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")


def repo(topics, desc, stars_total, gained, lang="Python", pushed=3, release=20, license="MIT",
         owner_type="Organization", contributors=12, scorecard=None, **extra):
    rec = {
        "url": "", "description": desc, "language": lang, "topics": topics, "stars": stars_total,
        "forks": stars_total // 10, "archived": False, "fork": False, "pushed_at": ts(pushed),
        "created_at": ts(900), "license": license, "owner_type": owner_type,
        "latest_release_at": ts(release) if release is not None else None,
        "stars_30d": gained, "contributors": contributors, "scorecard": scorecard,
    }
    rec.update(extra)
    return rec


REPOS = {
    # Baseline: identity
    "okta/okta-sdk-python": repo(["okta", "sdk"], "Okta Management SDK for Python", 280, 6, scorecard=6.1),
    "okta/terraform-provider-okta": repo(["okta", "terraform-provider"], "A Terraform provider to manage Okta resources", 270, 5, lang="Go", scorecard=5.4),
    "microsoftgraph/msgraph-sdk-powershell": repo(["powershell", "microsoft-graph"], "Powershell SDK for Microsoft Graph", 820, 14, lang="PowerShell", contributors=60, scorecard=5.0),
    "okta/okta-mcp-server": repo(["okta", "mcp-server"], "The Okta MCP Server", 310, 64, release=12),
    "microsoft/EnterpriseMCP": repo(["mcp", "entra-id"], "Microsoft MCP Server for Enterprise", 190, 58, release=None, license="CC-BY-4.0", contributors=6),
    "merill/lokka": repo(["mcp", "microsoft-graph", "entra-id"], "MCP server for Microsoft Graph and Azure", 340, 41, lang="TypeScript", owner_type="User", contributors=9),
    # endpoint
    "autopkg/autopkg": repo(["macadmins", "autopkg"], "Automating packaging and software distribution on macOS", 2300, 11, release=60, license="Apache-2.0", contributors=90),
    "Installomator/Installomator": repo(["macadmins", "jamf"], "Installation script to deploy standard software on Macs", 1800, 22, lang="Shell", release=14, contributors=150),
    "osquery/osquery": repo(["osquery", "security"], "SQL powered operating system instrumentation, monitoring, and analytics", 22600, 160, lang="C++", contributors=300, scorecard=7.3),
    "deploymenttheory/terraform-provider-jamfpro": repo(["jamf", "terraform-provider"], "Terraform provider for Jamf Pro", 160, 9, lang="Go", license="MPL-2.0", contributors=14),
    "dbankscard/jamf-mcp-server": repo(["jamf", "mcp-server"], "Jamf Pro MCP server", 120, 33, lang="TypeScript", owner_type="User", contributors=2, release=None),
    # saas
    "GAM-team/GAM": repo(["google-workspace", "gam"], "command line management for Google Workspace", 4200, 38, release=9, license="Apache-2.0", contributors=70),
    "pnp/powershell": repo(["powershell", "microsoft-365"], "PnP PowerShell", 790, 12, lang="C#", contributors=200),
    "taylorwilsdon/google_workspace_mcp": repo(["google-workspace", "mcp"], "Control Gmail, Calendar, Docs, Sheets, Drive and more with MCP", 1400, 210, owner_type="User", release=6, contributors=40),
    # security
    "CrowdStrike/falconpy": repo(["crowdstrike", "sdk"], "The CrowdStrike Falcon SDK for Python", 450, 8, license="Unlicense", contributors=40, scorecard=8.2),
    "wazuh/wazuh": repo(["siem", "security"], "Wazuh - The Open Source Security Platform", 12800, 190, lang="C", license="GPL-2.0", contributors=300),
    "CrowdStrike/falcon-mcp": repo(["crowdstrike", "mcp-server"], "Connect AI agents to CrowdStrike Falcon", 240, 52, contributors=11, scorecard=7.9),
    # network
    "netbox-community/netbox": repo(["netbox", "network-automation"], "The premier source of truth powering network automation", 17800, 260, license="Apache-2.0", contributors=400, scorecard=6.6),
    "fortinetdev/terraform-provider-fortios": repo(["fortinet", "terraform-provider"], "Terraform Fortios provider", 80, 2, lang="Go", license="MPL-2.0", contributors=8),
    "netboxlabs/netbox-mcp-server": repo(["netbox", "mcp-server"], "Model Context Protocol server for read-only interaction with NetBox data", 200, 37, license="Apache-2.0", contributors=7),
    # helpdesk
    "snipe/snipe-it": repo(["asset-management", "itsm"], "A free open source IT asset/license management system", 12500, 140, lang="PHP", license="AGPL-3.0", contributors=400),
    # foundations
    "anthropics/skills": repo(["agent-skills"], "Public repository for Agent Skills", 52000, 6100, lang="Python", license="Apache-2.0", contributors=40),
    "modelcontextprotocol/servers": repo(["mcp"], "Model Context Protocol Servers", 76000, 2400, lang="TypeScript", contributors=600, scorecard=6.0),
    "ossf/scorecard": repo(["security", "supply-chain"], "OpenSSF Scorecard - Security health metrics for Open Source", 4700, 40, lang="Go", license="Apache-2.0", contributors=200, scorecard=9.6),
    # nominations
    "macadmins/nudge": repo(["macadmins", "macos"], "A tool for encouraging the installation of macOS security updates", 1300, 9, lang="Swift", contributors=40),
    "munki/munki": repo(["munki", "macadmins"], "Managed software installation for macOS", 3200, 12, license="Apache-2.0", contributors=60),
    "fleetdm/fleet": repo(["osquery", "mdm", "device-management"], "Open-source platform for IT and security teams with thousands of computers", 5200, 120, lang="Go", contributors=300, scorecard=7.1),
    "bartreardon/swiftDialog": repo(["macadmins"], "Create user notifications on macOS with swiftDialog", 1100, 15, lang="Swift", owner_type="User", contributors=25),
    "microsoft/mcp": repo(["mcp"], "Catalog of official Microsoft MCP server implementations", 2100, 300, lang="C#", contributors=120),
    # edge cases
    "acme-it/okta-offboarder": repo(["okta", "scim"], "Automated Okta offboarding with SCIM deprovisioning", 640, 95, pushed=5, owner_type="Organization", contributors=4),
    "acme-it/tiny-intune-script": repo(["intune"], "Small Intune remediation script", 40, 3, lang="PowerShell", contributors=1, release=None),
    "acme-it/old-jamf-tool": repo(["jamf"], "Legacy Jamf reporting tool", 900, 0, archived=True, pushed=700),
    "acme-it/forked-gam": repo(["google-workspace"], "Fork of GAM", 30, 0, fork=True),
    "acme-it/ai-chat-framework": repo(["llm", "chatbot"], "A framework for building chat apps", 30000, 4000, lang="TypeScript"),
    "acme-it/gam-docs-generator": repo(["gam"], "Generates documentation sites", 700, 70, contributors=5),
}

SNAPSHOT_REPOS = {
    # days_ago -> repos on daily pages that day
    1: ["acme-it/ai-chat-framework", "taylorwilsdon/google_workspace_mcp", "okta/okta-mcp-server"],
    2: ["acme-it/ai-chat-framework", "taylorwilsdon/google_workspace_mcp"],
    3: ["acme-it/ai-chat-framework", "acme-it/okta-offboarder"],
    5: ["taylorwilsdon/google_workspace_mcp", "CrowdStrike/falcon-mcp"],
    8: ["acme-it/ai-chat-framework", "wazuh/wazuh"],
    12: ["netbox-community/netbox", "taylorwilsdon/google_workspace_mcp"],
    20: ["taylorwilsdon/google_workspace_mcp", "osquery/osquery"],
    35: ["acme-it/old-jamf-tool"],  # outside the 30-day window
}


def main() -> None:
    repos = {name: {**rec, "url": f"https://github.com/{name}"} for name, rec in REPOS.items()}
    (HERE / "repos.json").write_text(json.dumps(repos, indent=2, sort_keys=True) + "\n")
    snap_dir = HERE / "snapshots"
    snap_dir.mkdir(exist_ok=True)
    for old in snap_dir.glob("*.json"):
        old.unlink()
    for days_ago, names in SNAPSHOT_REPOS.items():
        day = (NOW - timedelta(days=days_ago)).date().isoformat()
        rows = [{"repo": n, "rank": i + 1, "period_stars": 50} for i, n in enumerate(names)]
        # Same repo on the global and a language page counts once per day.
        pages = {"all/daily": rows, "powershell/daily": rows[:1], "all/weekly": rows}
        (snap_dir / f"{day}.json").write_text(json.dumps({"date": day, "pages": pages}, indent=2) + "\n")


if __name__ == "__main__":
    main()
