#!/usr/bin/env python3
"""
Integrate 7 Anthropic-patterns workflows (P1-P7) into JARVIS packages:
  - Starter: P1 + P7
  - Professional: P1-P5 + P7
  - Enterprise: P1-P7

Also updates:
  - manifest.json (new category + workflow counts)
  - README.md (new section)
  - setup_guide.md (new import section)
  - pricing.html (new stats + features + comparison rows)
  - cognitive_capital/ copied into each package
"""

import json
import os
import shutil
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────
BASE = "/home/z/my-project/download"
SRC_PATTERNS = f"{BASE}/jarvis_packages/anthropic_patterns"
SRC_COGNITIVE = f"{BASE}/jarvis_packages/cognitive_capital"
REPO = f"{BASE}/n8n_workflows_v2"

PACKAGES = {
    "jarvis-starter": {
        "patterns": ["P1_Prompt_Chaining_Agent_v3.json", "P7_SOUL_Bootstrap_Agent_v3.json"],
        "label": "P1 + P7",
        "tagline": "Prompt Chaining + SOUL Bootstrap",
    },
    "jarvis-professional": {
        "patterns": [
            "P1_Prompt_Chaining_Agent_v3.json",
            "P2_Smart_Routing_Agent_v3.json",
            "P3_Orchestrator_Workers_Agent_v3.json",
            "P4_Evaluator_Optimizer_Agent_v3.json",
            "P5_Parallelization_Agent_v3.json",
            "P7_SOUL_Bootstrap_Agent_v3.json",
        ],
        "label": "P1-P5 + P7",
        "tagline": "5 Core Patterns + SOUL Bootstrap",
    },
    "jarvis-enterprise": {
        "patterns": [
            "P1_Prompt_Chaining_Agent_v3.json",
            "P2_Smart_Routing_Agent_v3.json",
            "P3_Orchestrator_Workers_Agent_v3.json",
            "P4_Evaluator_Optimizer_Agent_v3.json",
            "P5_Parallelization_Agent_v3.json",
            "P6_Cognitive_Capital_MCP_Server_v3.json",
            "P7_SOUL_Bootstrap_Agent_v3.json",
        ],
        "label": "P1-P7 (All Patterns)",
        "tagline": "All 7 Anthropic Patterns + Cognitive Capital MCP",
    },
}

PATTERN_DESCRIPTIONS = {
    "P1_Prompt_Chaining_Agent_v3.json": {
        "title": "P1 Prompt Chaining Agent",
        "desc": "Research → Gate → Draft → Gate → Polish. Multi-step content pipeline with quality gates and tiered LLMs (GPT-4o-mini → GPT-4.1-mini → GPT-4.1).",
        "skills": "deep-research, consulting-analysis, newsletter-generation",
    },
    "P2_Smart_Routing_Agent_v3.json": {
        "title": "P2 Smart Routing Agent",
        "desc": "Classifies user intent and routes to 7 specialized sub-agents (calendar, email, research, ecommerce, creative, technical, HR).",
        "skills": "deep-research, find-skills",
    },
    "P3_Orchestrator_Workers_Agent_v3.json": {
        "title": "P3 Orchestrator-Workers Agent",
        "desc": "Central orchestrator breaks complex tasks into subtasks and delegates to 4 specialized workers (Research, Creative, Technical, Data).",
        "skills": "deep-research, consulting-analysis, find-skills",
    },
    "P4_Evaluator_Optimizer_Agent_v3.json": {
        "title": "P4 Evaluator-Optimizer Agent",
        "desc": "Generator → Evaluator → Quality Gate loop. Iteratively refines content until quality threshold is met (max 3 retries).",
        "skills": "consulting-analysis, newsletter-generation, deep-research",
    },
    "P5_Parallelization_Agent_v3.json": {
        "title": "P5 Parallelization Agent",
        "desc": "3 parallel analysts (Financial, Market, Technical) → Aggregate → Synthesis Agent. Webhook-based for API integration.",
        "skills": "data-analysis, consulting-analysis, deep-research",
    },
    "P6_Cognitive_Capital_MCP_Server_v3.json": {
        "title": "P6 Cognitive Capital MCP Server",
        "desc": "6 skills as MCP tools (Deep Research, Consulting Analysis, Data Analysis, Newsletter, Code Docs, Podcast). MCP Trigger for agent consumption.",
        "skills": "All 6 cognitive capital skills",
    },
    "P7_SOUL_Bootstrap_Agent_v3.json": {
        "title": "P7 SOUL Bootstrap Agent",
        "desc": "4-phase conversational onboarding (Hello → You → Personality → Depth) that generates a personalized SOUL.md for AI assistants.",
        "skills": "bootstrap",
    },
}


# ── 1. Copy workflow files ─────────────────────────────────────────────
def copy_patterns():
    for pkg_name, cfg in PACKAGES.items():
        dest_dir = f"{REPO}/{pkg_name}/workflows/anthropic_patterns"
        os.makedirs(dest_dir, exist_ok=True)
        for fname in cfg["patterns"]:
            src = f"{SRC_PATTERNS}/{fname}"
            dst = f"{dest_dir}/{fname}"
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f"  ✓ {pkg_name}/workflows/anthropic_patterns/{fname}")
            else:
                print(f"  ✗ MISSING: {src}")


# ── 2. Copy cognitive_capital/ ─────────────────────────────────────────
def copy_cognitive_capital():
    for pkg_name in PACKAGES:
        dest = f"{REPO}/{pkg_name}/cognitive_capital"
        if os.path.exists(dest):
            shutil.rmtree(dest)
        if os.path.exists(SRC_COGNITIVE):
            shutil.copytree(SRC_COGNITIVE, dest)
            print(f"  ✓ {pkg_name}/cognitive_capital/ ({len(os.listdir(dest))} items)")


# ── 3. Update manifest.json ────────────────────────────────────────────
def update_manifests():
    for pkg_name, cfg in PACKAGES.items():
        mpath = f"{REPO}/{pkg_name}/manifest.json"
        with open(mpath) as f:
            manifest = json.load(f)

        # Add anthropic_patterns category
        manifest["workflows"]["anthropic_patterns"] = cfg["patterns"]

        # Update version
        manifest["version"] = "3.0.0"

        # Count total
        total = sum(len(v) for v in manifest["workflows"].values())
        manifest["total_workflows"] = total

        # Add cognitive_capital info
        cc_skills = ["deep-research", "consulting-analysis", "data-analysis",
                     "newsletter-generation", "code-documentation", "podcast-generation"]
        if pkg_name == "jarvis-starter":
            manifest["cognitive_capital"] = {
                "skills": ["deep-research", "consulting-analysis"],
                "soul_template": True,
            }
        elif pkg_name == "jarvis-professional":
            manifest["cognitive_capital"] = {
                "skills": cc_skills[:4],
                "soul_template": True,
            }
        else:
            manifest["cognitive_capital"] = {
                "skills": cc_skills,
                "soul_template": True,
            }

        with open(mpath, "w") as f:
            json.dump(manifest, f, indent=2)
        print(f"  ✓ {pkg_name}/manifest.json — v3.0.0, {total} workflows, {cfg['label']}")


# ── 4. Update README.md ───────────────────────────────────────────────
def generate_readme(pkg_name, cfg):
    manifest_path = f"{REPO}/{pkg_name}/manifest.json"
    with open(manifest_path) as f:
        m = json.load(f)

    total = m["total_workflows"]
    n_consolidated = len(m["workflows"].get("consolidated", []))
    n_mcp = len(m["workflows"].get("mcp_servers", []))
    n_templates = len(m["workflows"].get("templates", []))
    n_patterns = len(m["workflows"].get("anthropic_patterns", []))
    n_skills = len(m.get("cognitive_capital", {}).get("skills", []))

    price = m["price"]
    pkg_title = m["name"]
    taglines = {
        "jarvis-starter": "Your Personal AI Assistant",
        "jarvis-professional": "Business Automation Platform",
        "jarvis-enterprise": "Full AI Operations Suite",
    }
    tagline = taglines[pkg_name]

    # Build pattern list
    pattern_lines = []
    for fname in cfg["patterns"]:
        info = PATTERN_DESCRIPTIONS[fname]
        pattern_lines.append(f"- **{info['title']}** — `{fname}` — {info['desc']}")

    # Build cognitive capital section
    cc_skills = m.get("cognitive_capital", {}).get("skills", [])
    cc_lines = []
    for skill in cc_skills:
        cc_lines.append(f"- **{skill}** — `cognitive_capital/{skill}/SKILL.md`")

    # Docker services
    docker_services = m.get("docker_services", [])
    docker_yaml = "\n".join(f"  - {s}" for s in docker_services)

    # LLM tier
    llm = m.get("llm_tier", "")

    # Cost
    cost = m.get("estimated_monthly_cost", "")

    readme = f"""# {pkg_title}

> {tagline}

[![Zero Debt](https://img.shields.io/badge/Zero-Debt-brightgreen)](https://github.com/grootme/workflows)
[![n8n](https://img.shields.io/badge/n8n-Compatible-orange)](https://n8n.io)
[![Anthropic Patterns](https://img.shields.io/badge/Anthropic-Patterns-blueviolet)](https://www.anthropic.com/engineering/building-effective-agents)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)

## Overview

{tagline} with {n_patterns} Anthropic-pattern workflows, {n_skills} cognitive capital skills, and SOUL template for personalized AI personalities.

**Target**: {"Individuals, freelancers, and small teams who want a personal AI assistant with prompt chaining and personality bootstrapping." if pkg_name == "jarvis-starter" else "Businesses that need multi-pattern agent orchestration with smart routing, quality loops, and parallel analysis." if pkg_name == "jarvis-professional" else "Organizations requiring the full Anthropic agent pattern arsenal with cognitive capital MCP server, enterprise monitoring, and personalized AI personalities."}

## What's Included

| Category | Count | Details |
|----------|-------|---------|
| Consolidated Workflows | {n_consolidated} | Production-ready AI automation suites |
| MCP Server Templates | {n_mcp} | Reusable MCP tool servers |
| Base Templates | {n_templates} | Starting points for custom workflows |
| **Anthropic Patterns** | **{n_patterns}** | Agent design patterns from Anthropic research |
| Cognitive Capital Skills | {n_skills} | SKILL.md knowledge base for agents |
| **Total Workflows** | **{total}** | All zero-debt, production-ready |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/grootme/workflows.git
cd workflows/{pkg_name}

# 2. Configure
cp .env.example .env
# Edit .env with your API keys

# 3. Launch
docker compose up -d

# 4. Access
open http://localhost:5678
```

## Anthropic Pattern Workflows

Based on [Anthropic's "Building Effective Agents"](https://www.anthropic.com/engineering/building-effective-agents) research. These implement the 5 core agent design patterns plus cognitive capital and SOUL personality system.

{chr(10).join(pattern_lines)}

### Pattern Selection Guide

| Pattern | Best For | Complexity |
|---------|----------|------------|
| P1 Prompt Chaining | Multi-step content pipelines | Medium |
| P2 Smart Routing | Multi-domain intent classification | Medium-High |
| P3 Orchestrator-Workers | Complex task decomposition | High |
| P4 Evaluator-Optimizer | Quality-gated iterative refinement | Medium-High |
| P5 Parallelization | Multi-perspective analysis | Medium |
| P6 Cognitive Capital MCP | Skill-as-a-service for agents | Medium |
| P7 SOUL Bootstrap | Personalized AI personality creation | Low |

## Cognitive Capital

Skills loaded into agent memory for better results. Following [Anthropic's progressive disclosure pattern](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).

{chr(10).join(cc_lines)}

- **SOUL Template** — `cognitive_capital/SOUL.template.md` — Personalized AI personality system

## Workflows

### Consolidated Suites

{chr(10).join(f"- **{fname.replace('_', ' ').replace('.json', '').replace(' v2', '')}** — `{fname}`" for fname in m["workflows"].get("consolidated", []))}

### MCP Server Templates

{chr(10).join(f"- **{fname.replace('_', ' ').replace('.json', '').replace(' v2', '')}** — `{fname}`" for fname in m["workflows"].get("mcp_servers", []))}

### Base Templates

{chr(10).join(f"- **{fname.replace('_', ' ').replace('.json', '').replace(' v2', '')}** — `{fname}`" for fname in m["workflows"].get("templates", []))}

## Credentials Needed

- OpenAI API Key (multiple models)
- Google Workspace OAuth2 (Calendar, Gmail, Contacts)
- Google Gemini API Key (embeddings)
- PostgreSQL connection
{"- Qdrant API Key (vector store)" if "qdrant" in docker_services else ""}
{"- Redis connection (caching)" if "redis" in docker_services else ""}
{"- Zep API Key (enterprise memory)" if "zep" in docker_services else ""}

## LLM Strategy

{llm}

## Estimated Costs

- **One-time**: ${price}
- **Monthly running**: {cost}

## Docker Services

{docker_yaml}

## Documentation

- [Setup Guide](setup_guide.md) — Complete step-by-step installation
- [Docker Compose](docker-compose.yml) — Production-ready container configuration
- [Environment Template](.env.example) — All configurable variables

## Support

- **GitHub Issues**: https://github.com/grootme/workflows/issues
- **n8n Community**: https://community.n8n.io

## License

MIT License — Use, modify, and distribute freely.

---

*Part of the [JARVIS AI Automation](https://github.com/grootme/workflows) ecosystem.*
"""
    return readme


def update_readmes():
    for pkg_name, cfg in PACKAGES.items():
        rpath = f"{REPO}/{pkg_name}/README.md"
        content = generate_readme(pkg_name, cfg)
        with open(rpath, "w") as f:
            f.write(content)
        print(f"  ✓ {pkg_name}/README.md")


# ── 5. Update setup_guide.md ───────────────────────────────────────────
def update_setup_guides():
    for pkg_name, cfg in PACKAGES.items():
        sg_path = f"{REPO}/{pkg_name}/setup_guide.md"
        with open(sg_path) as f:
            content = f.read()

        # Build the Anthropic Patterns import section
        pattern_import_lines = []
        for i, fname in enumerate(cfg["patterns"], 1):
            info = PATTERN_DESCRIPTIONS[fname]
            pattern_import_lines.append(f"{i}. `{fname}` — {info['title']}")

        pattern_section = f"""
#### Anthropic Pattern Workflows

{chr(10).join(pattern_import_lines)}

#### Cognitive Capital Skills

These SKILL.md files are loaded into agent memory for better results. Copy them to your n8n data directory:

```bash
# Copy cognitive capital to n8n data volume
cp -r cognitive_capital/ /path/to/n8n/data/
```

Skills available:
"""

        cc_skills = PACKAGES[pkg_name]  # just for counting
        cc_items = []
        manifest_path = f"{REPO}/{pkg_name}/manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        for skill in m.get("cognitive_capital", {}).get("skills", []):
            cc_items.append(f"- **{skill}** — `cognitive_capital/{skill}/SKILL.md`")
        cc_items.append("- **SOUL Template** — `cognitive_capital/SOUL.template.md`")

        pattern_section += chr(10).join(cc_items)

        # Insert before "### Post-Import Configuration"
        if "#### Anthropic Pattern Workflows" not in content:
            # Find the insertion point: after the last #### section before Post-Import
            if "### Post-Import Configuration" in content:
                content = content.replace(
                    "### Post-Import Configuration",
                    pattern_section + "\n\n### Post-Import Configuration",
                )
            else:
                # Append at end
                content += "\n" + pattern_section

        # Update version
        content = content.replace("Version 2.0", "Version 3.0")

        with open(sg_path, "w") as f:
            f.write(content)
        print(f"  ✓ {pkg_name}/setup_guide.md")


# ── 6. Update pricing.html ────────────────────────────────────────────
def update_pricing_html():
    ppath = f"{REPO}/pricing.html"
    with open(ppath) as f:
        html = f.read()

    # Update stats bar
    html = html.replace(
        '<div class="number" style="color: var(--accent-starter)">25</div>\n        <div class="label">Zero-Debt Workflows</div>',
        '<div class="number" style="color: var(--accent-starter)">32</div>\n        <div class="label">Zero-Debt Workflows</div>',
    )
    html = html.replace(
        '<div class="number" style="color: var(--accent-pro)">6</div>\n        <div class="label">MCP Servers</div>',
        '<div class="number" style="color: var(--accent-pro)">7</div>\n        <div class="label">Anthropic Patterns</div>',
    )
    html = html.replace(
        '<div class="number" style="color: var(--accent-enterprise)">68</div>\n        <div class="label">AI Connections</div>',
        '<div class="number" style="color: var(--accent-enterprise)">118</div>\n        <div class="label">AI Connections</div>',
    )

    # Update subtitle
    html = html.replace(
        "Transform your workflows with 25 zero-debt n8n automations packaged into 3 tiers. From personal assistant to enterprise AI operations.",
        "Transform your workflows with 32 zero-debt n8n automations + 7 Anthropic agent patterns. From personal assistant to enterprise AI operations with cognitive capital.",
    )

    # Update header badge
    html = html.replace(
        "⚡ Zero Technical Debt • Production Ready",
        "⚡ Zero Technical Debt • Anthropic Patterns • Cognitive Capital",
    )

    # ── Starter card features ──
    starter_features = """            <li><span class="check">✓</span> 3 Google Workspace MCP Suites</li>
            <li><span class="check">✓</span> 4 MCP Server Templates</li>
            <li><span class="check">✓</span> Image & Quote generation suite</li>
            <li><span class="check">✓</span> Video content creation suite</li>
            <li><span class="check">✓</span> Flowise RAG integration</li>
            <li><span class="check">✓</span> Knowledge Base server</li>
            <li><span class="check">✓</span> 2 Base templates</li>
            <li><span class="check">✓</span> <strong>P1 Prompt Chaining Agent</strong></li>
            <li><span class="check">✓</span> <strong>P7 SOUL Bootstrap Agent</strong></li>
            <li><span class="check">✓</span> 2 Cognitive Capital Skills</li>
            <li><span class="check">✓</span> SOUL Template for AI personality</li>
            <li><span class="check">✓</span> Docker Compose (n8n + PostgreSQL)</li>
            <li><span class="check">✓</span> Step-by-step setup guide</li>"""

    html = html.replace(
        """            <li><span class="check">✓</span> 3 Google Workspace MCP Suites</li>
            <li><span class="check">✓</span> 4 MCP Server Templates</li>
            <li><span class="check">✓</span> Image & Quote generation suite</li>
            <li><span class="check">✓</span> Video content creation suite</li>
            <li><span class="check">✓</span> Flowise RAG integration</li>
            <li><span class="check">✓</span> Knowledge Base server</li>
            <li><span class="check">✓</span> 2 Base templates</li>
            <li><span class="check">✓</span> Docker Compose (n8n + PostgreSQL)</li>
            <li><span class="check">✓</span> Step-by-step setup guide</li>""",
        starter_features,
    )

    # ── Professional card features ──
    pro_features = """            <li><span class="check">✓</span> <strong>Everything in Starter, plus:</strong></li>
            <li><span class="check">✓</span> 13 consolidated workflows (G1-G13)</li>
            <li><span class="check">✓</span> 6 MCP Server templates</li>
            <li><span class="check">✓</span> 6 Base templates</li>
            <li><span class="check">✓</span> E-Commerce Agent + WhatsApp AI</li>
            <li><span class="check">✓</span> Marketing Multi-Agent orchestrator</li>
            <li><span class="check">✓</span> HR AI Agent + Social Scraper</li>
            <li><span class="check">✓</span> Global Error Handler</li>
            <li><span class="check">✓</span> <strong>P1 Prompt Chaining Agent</strong></li>
            <li><span class="check">✓</span> <strong>P2 Smart Routing Agent</strong></li>
            <li><span class="check">✓</span> <strong>P3 Orchestrator-Workers</strong></li>
            <li><span class="check">✓</span> <strong>P4 Evaluator-Optimizer</strong></li>
            <li><span class="check">✓</span> <strong>P5 Parallelization Agent</strong></li>
            <li><span class="check">✓</span> <strong>P7 SOUL Bootstrap Agent</strong></li>
            <li><span class="check">✓</span> 4 Cognitive Capital Skills</li>
            <li><span class="check">✓</span> Docker Compose (n8n + PG + Qdrant + Redis)</li>
            <li><span class="check">✓</span> Complete setup guide</li>"""

    html = html.replace(
        """            <li><span class="check">✓</span> <strong>Everything in Starter, plus:</strong></li>
            <li><span class="check">✓</span> 13 consolidated workflows (G1-G13)</li>
            <li><span class="check">✓</span> 6 MCP Server templates</li>
            <li><span class="check">✓</span> 6 Base templates</li>
            <li><span class="check">✓</span> E-Commerce Agent + WhatsApp AI</li>
            <li><span class="check">✓</span> Marketing Multi-Agent orchestrator</li>
            <li><span class="check">✓</span> HR AI Agent + Social Scraper</li>
            <li><span class="check">✓</span> Global Error Handler</li>
            <li><span class="check">✓</span> Docker Compose (n8n + PG + Qdrant + Redis)</li>
            <li><span class="check">✓</span> Complete setup guide</li>""",
        pro_features,
    )

    # ── Enterprise card features ──
    ent_features = """            <li><span class="check">✓</span> <strong>Everything in Professional, plus:</strong></li>
            <li><span class="check">✓</span> <strong>P6 Cognitive Capital MCP Server</strong></li>
            <li><span class="check">✓</span> 6 Cognitive Capital Skills (all)</li>
            <li><span class="check">✓</span> Prometheus + Grafana monitoring</li>
            <li><span class="check">✓</span> Nginx reverse proxy + SSL</li>
            <li><span class="check">✓</span> Zep enterprise memory</li>
            <li><span class="check">✓</span> Multi-tenant architecture</li>
            <li><span class="check">✓</span> CI/CD pipeline config</li>
            <li><span class="check">✓</span> Security hardening guide</li>
            <li><span class="check">✓</span> White-label customization</li>
            <li><span class="check">✓</span> Full 8-service Docker Compose</li>
            <li><span class="check">✓</span> 1 hour consultation call</li>"""

    html = html.replace(
        """            <li><span class="check">✓</span> <strong>Everything in Professional, plus:</strong></li>
            <li><span class="check">✓</span> Prometheus + Grafana monitoring</li>
            <li><span class="check">✓</span> Nginx reverse proxy + SSL</li>
            <li><span class="check">✓</span> Zep enterprise memory</li>
            <li><span class="check">✓</span> Multi-tenant architecture</li>
            <li><span class="check">✓</span> CI/CD pipeline config</li>
            <li><span class="check">✓</span> Security hardening guide</li>
            <li><span class="check">✓</span> White-label customization</li>
            <li><span class="check">✓</span> Full 8-service Docker Compose</li>
            <li><span class="check">✓</span> 1 hour consultation call</li>""",
        ent_features,
    )

    # ── Update comparison table ──
    # Add new rows to the comparison table
    new_rows = """            <tr><td>Anthropic Pattern Workflows</td><td>2 (P1+P7)</td><td>6 (P1-P5+P7)</td><td>7 (P1-P7)</td></tr>
            <tr><td>Cognitive Capital Skills</td><td>2</td><td>4</td><td>6</td></tr>
            <tr><td>P1 Prompt Chaining</td><td class="yes">✓</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>P2 Smart Routing</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>P3 Orchestrator-Workers</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>P4 Evaluator-Optimizer</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>P5 Parallelization</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>P6 Cognitive Capital MCP</td><td class="no">—</td><td class="no">—</td><td class="yes">✓</td></tr>
            <tr><td>P7 SOUL Bootstrap</td><td class="yes">✓</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>SOUL Template</td><td class="yes">✓</td><td class="yes">✓</td><td class="yes">✓</td></tr>"""

    # Insert before the Docker Compose row
    html = html.replace(
        '            <tr><td>Docker Compose</td>',
        new_rows + '\n            <tr><td>Docker Compose</td>',
    )

    # Update existing rows
    html = html.replace(
        "<tr><td>Consolidated Workflows</td><td>6</td><td>13</td><td>13</td></tr>",
        "<tr><td>Consolidated Workflows</td><td>6</td><td>13</td><td>13</td></tr>",
    )
    html = html.replace(
        "<tr><td>Base Templates</td><td>2</td><td>6</td><td>6</td></tr>",
        "<tr><td>Base Templates</td><td>2</td><td>6</td><td>6</td></tr>",
    )

    # Update footer
    html = html.replace(
        "Built with zero technical debt • 25 workflows • 68 AI connections",
        "Built with zero technical debt • 32 workflows • 7 Anthropic patterns • 6 cognitive capital skills",
    )
    html = html.replace(
        "© 2026 JARVIS Automation • All workflows validated and production-ready",
        "© 2026 JARVIS Automation • Anthropic Patterns • Cognitive Capital • Production-ready",
    )

    with open(ppath, "w") as f:
        f.write(html)
    print(f"  ✓ pricing.html updated")


# ── 7. Update root README.md ───────────────────────────────────────────
def update_root_readme():
    rpath = f"{REPO}/README.md"
    with open(rpath) as f:
        content = f.read()

    # Update version references
    content = content.replace("v2.0", "v3.0")

    # Update workflow count
    content = content.replace("25 zero-debt", "32 zero-debt")

    # Add Anthropic patterns section if not present
    if "anthropic_patterns" not in content:
        patterns_section = """
## Anthropic Agent Patterns (Phase 3)

Based on [Anthropic's "Building Effective Agents"](https://www.anthropic.com/engineering/building-effective-agents) research, implementing the 5 core agent design patterns:

| Pattern | Workflow | Description |
|---------|----------|-------------|
| Prompt Chaining | P1 | Research → Gate → Draft → Gate → Polish |
| Routing | P2 | Smart intent classification → 7 specialized sub-agents |
| Orchestrator-Workers | P3 | Central orchestrator → 4 specialized workers |
| Evaluator-Optimizer | P4 | Generator → Evaluator → Quality Gate loop |
| Parallelization | P5 | 3 parallel analysts → Aggregate → Synthesis |

Plus 2 cognitive capital patterns:
- **P6 Cognitive Capital MCP Server** — 6 skills as MCP tools for agent consumption
- **P7 SOUL Bootstrap Agent** — 4-phase conversational onboarding for personalized AI personalities

### Package Distribution

| Package | Anthropic Patterns | Cognitive Capital Skills |
|---------|-------------------|-------------------------|
| Starter ($49) | P1 + P7 | 2 |
| Professional ($149) | P1-P5 + P7 | 4 |
| Enterprise ($399) | P1-P7 (All) | 6 |

### Cognitive Capital Skills

Following [Anthropic's progressive disclosure pattern](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills):

1. **deep-research** — Systematic multi-angle research methodology
2. **consulting-analysis** — Professional analysis framework
3. **data-analysis** — Data extraction and visualization
4. **newsletter-generation** — Content structure and formatting
5. **code-documentation** — Precision and clarity standards
6. **podcast-generation** — Audio content production

Each skill is a SKILL.md file with 3 levels of progressive disclosure, loaded into agent memory for better results.
"""
        # Insert before the last section
        content += patterns_section

    with open(rpath, "w") as f:
        f.write(content)
    print(f"  ✓ README.md updated")


# ── 8. Update jarvis_packages/ too (source of truth) ──────────────────
def sync_to_jarvis_packages():
    """Copy the same changes to the jarvis_packages/ directory."""
    for pkg_name, cfg in PACKAGES.items():
        # Copy anthropic_patterns
        src_dir = f"{REPO}/{pkg_name}/workflows/anthropic_patterns"
        dst_dir = f"{BASE}/jarvis_packages/{pkg_name}/workflows/anthropic_patterns"
        if os.path.exists(dst_dir):
            shutil.rmtree(dst_dir)
        if os.path.exists(src_dir):
            shutil.copytree(src_dir, dst_dir)
            print(f"  ✓ sync {pkg_name}/workflows/anthropic_patterns/")

        # Copy cognitive_capital
        src_cc = f"{REPO}/{pkg_name}/cognitive_capital"
        dst_cc = f"{BASE}/jarvis_packages/{pkg_name}/cognitive_capital"
        if os.path.exists(dst_cc):
            shutil.rmtree(dst_cc)
        if os.path.exists(src_cc):
            shutil.copytree(src_cc, dst_cc)
            print(f"  ✓ sync {pkg_name}/cognitive_capital/")

        # Copy manifest
        shutil.copy2(f"{REPO}/{pkg_name}/manifest.json", f"{BASE}/jarvis_packages/{pkg_name}/manifest.json")
        # Copy README
        shutil.copy2(f"{REPO}/{pkg_name}/README.md", f"{BASE}/jarvis_packages/{pkg_name}/README.md")
        # Copy setup guide
        shutil.copy2(f"{REPO}/{pkg_name}/setup_guide.md", f"{BASE}/jarvis_packages/{pkg_name}/setup_guide.md")

    # Copy pricing.html
    shutil.copy2(f"{REPO}/pricing.html", f"{BASE}/jarvis_packages/pricing.html")
    print(f"  ✓ sync pricing.html")

    # Copy root README
    shutil.copy2(f"{REPO}/README.md", f"{BASE}/jarvis_packages/README.md")
    print(f"  ✓ sync README.md")


# ── Main ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  Integrating Anthropic Patterns into JARVIS Packages v3.0")
    print("=" * 60)

    print("\n1. Copying workflow files...")
    copy_patterns()

    print("\n2. Copying cognitive_capital/...")
    copy_cognitive_capital()

    print("\n3. Updating manifest.json files...")
    update_manifests()

    print("\n4. Updating README.md files...")
    update_readmes()

    print("\n5. Updating setup_guide.md files...")
    update_setup_guides()

    print("\n6. Updating pricing.html...")
    update_pricing_html()

    print("\n7. Updating root README.md...")
    update_root_readme()

    print("\n8. Syncing to jarvis_packages/...")
    sync_to_jarvis_packages()

    print("\n" + "=" * 60)
    print("  ✅ Integration complete!")
    print("=" * 60)

    # Summary
    for pkg_name, cfg in PACKAGES.items():
        mpath = f"{REPO}/{pkg_name}/manifest.json"
        with open(mpath) as f:
            m = json.load(f)
        total = m["total_workflows"]
        n_patterns = len(m["workflows"]["anthropic_patterns"])
        n_skills = len(m.get("cognitive_capital", {}).get("skills", []))
        print(f"  {pkg_name}: {total} workflows, {n_patterns} Anthropic patterns, {n_skills} cognitive capital skills")
