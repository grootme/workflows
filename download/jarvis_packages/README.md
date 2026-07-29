# JARVIS AI Automation Packages

> 25 zero-debt n8n workflows → 3 high-value products

## Packages

| Package | Price | Workflows | Services | Best For |
|---------|-------|-----------|----------|----------|
| [Starter](./jarvis-starter/) | $49 | 12 | 2 | Individuals & freelancers |
| [Professional](./jarvis-professional/) | $149 | 25 | 4 | SMBs & agencies |
| [Enterprise](./jarvis-enterprise/) | $399 | 25 | 8 | Enterprises & SaaS |

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    JARVIS AI Automation Ecosystem                │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │    Starter    │  │ Professional │  │     Enterprise        │  │
│  │  $49         │  │  $149        │  │     $399              │  │
│  │              │  │              │  │                        │  │
│  │ • Calendar   │  │ • All G1-G13 │  │ • All G1-G13         │  │
│  │ • Gmail      │  │ • 6 MCP      │  │ • 6 MCP Servers      │  │
│  │ • Contacts   │  │ • 6 Templates│  │ • 6 Templates        │  │
│  │ • Images     │  │ • RAG+Vector │  │ • Prometheus+Grafana  │  │
│  │ • Video      │  │ • WhatsApp   │  │ • Nginx+SSL          │  │
│  │ • Flowise    │  │ • E-Commerce │  │ • Zep Memory         │  │
│  │              │  │ • Marketing  │  │ • Multi-tenant       │  │
│  │ 2 services   │  │ 4 services   │  │ • CI/CD              │  │
│  │ n8n+PG       │  │ n8n+PG+Q+R  │  │ 8 services           │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                  │
│  25 Workflows • 68 AI Connections • 0 Technical Debt            │
└──────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Choose your package
cd jarvis-starter      # or jarvis-professional / jarvis-enterprise

# Configure
cp .env.example .env
nano .env

# Launch
docker compose up -d

# Access
open http://localhost:5678
```

## Pricing Page

Open [pricing.html](./pricing.html) in your browser to see the interactive pricing page.

## Zero-Debt Standards

All workflows comply with:
- ✅ Valid n8n JSON format with executionOrder v1
- ✅ Correct ai_* LangChain sub-type connections
- ✅ No orphan nodes (all nodes wired)
- ✅ Real node types (no invalid types)
- ✅ $fromAI() on all MCP/AI tool parameters
- ✅ Empty credential IDs (templates, no PLACEHOLDER)
- ✅ No hardcoded values
- ✅ No errorWorkflow references
- ✅ Clean tags array

## Repository

- **GitHub**: https://github.com/grootme/workflows
- **n8n Community**: https://community.n8n.io

---

*Built with JARVIS Package Builder v2.0*
