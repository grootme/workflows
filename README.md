# JARVIS AI Automation — n8n Workflows

> 25 zero-debt n8n workflows → 3 high-value product packages

[![Zero Debt](https://img.shields.io/badge/Zero-Debt-brightgreen)]()
[![n8n](https://img.shields.io/badge/n8n-Compatible-orange)](https://n8n.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)

## 🚀 JARVIS Packages

| Package | Price | Workflows | Docker Services | Best For |
|---------|-------|-----------|-----------------|----------|
| [**Starter**](./jarvis-starter/) | **$49** | 12 | 2 (n8n + PostgreSQL) | Individuals & freelancers |
| [**Professional**](./jarvis-professional/) | **$149** | 25 | 4 (n8n + PG + Qdrant + Redis) | SMBs & agencies |
| [**Enterprise**](./jarvis-enterprise/) | **$399** | 25 | 8 (Full stack + monitoring) | Enterprises & SaaS |

👉 **[Interactive Pricing Page](./pricing.html)** — Open in browser for the full experience

## 📊 Overview

| Category | Count | Zero-Debt | AI Connections |
|----------|-------|-----------|----------------|
| Consolidated Workflows | 13 | ✅ | 47 |
| MCP Server Workflows | 6 | ✅ | 24 |
| Base Templates | 6 | ✅ | 16 |
| **Total** | **25** | **✅** | **68** |

## 🏗️ Architecture

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

### Tiered LLM Strategy

| Role | Model | Price/1M tokens | Best For |
|------|-------|-----------------|----------|
| Classification | GPT-4o-mini | $0.15/$0.60 | Routing, simple tasks |
| Cost-Effective | Gemini 2.5 Flash | $0.15/$0.60 | Best price/quality |
| Primary Agent | GPT-4.1-mini | $0.40/$1.60 | Agent tasks |
| Orchestrator | GPT-4.1 | $2/$8 | Complex reasoning |
| Specialized | Claude Sonnet | $3/$15 | Highest quality |

## 📁 Repository Structure

```
workflows/
├── jarvis-starter/              # 💚 $49 — Personal AI Assistant
│   ├── workflows/               # 12 zero-debt workflows
│   │   ├── consolidated/        # 6 suites (Calendar, Gmail, Contacts, Images, Video, Flowise)
│   │   ├── mcp_servers/         # 4 MCP servers (Calendar, Gmail, Contacts, KB)
│   │   └── templates/           # 2 templates (Single Agent, MCP Server)
│   ├── docker-compose.yml       # n8n + PostgreSQL
│   ├── .env.example             # Environment configuration
│   ├── setup_guide.md           # Step-by-step setup
│   └── README.md
│
├── jarvis-professional/         # 💜 $149 — Business Automation Platform
│   ├── workflows/               # 25 zero-debt workflows
│   │   ├── consolidated/        # 13 suites (G1-G13, all)
│   │   ├── mcp_servers/         # 6 MCP servers
│   │   └── templates/           # 6 templates
│   ├── docker-compose.yml       # n8n + PostgreSQL + Qdrant + Redis
│   ├── .env.example             # Environment configuration
│   ├── setup_guide.md           # Step-by-step setup
│   └── README.md
│
├── jarvis-enterprise/           # 💗 $399 — Full AI Operations Suite
│   ├── workflows/               # 25 zero-debt workflows
│   ├── docker-compose.yml       # 8 services (full stack)
│   ├── nginx/                   # Reverse proxy + SSL
│   ├── monitoring/              # Prometheus + Grafana
│   ├── init-db/                 # Database initialization
│   ├── .env.example             # Environment configuration
│   ├── setup_guide.md           # Step-by-step setup
│   └── README.md
│
├── consolidated/                # Individual workflow files (G1-G13)
├── mcp_servers/                 # Individual MCP server files
├── base_templates/              # Individual template files
├── marketplace_listings/        # n8nmarkets.com listings
├── pricing.html                 # Interactive pricing page
└── README.md
```

## 🔧 Zero-Debt Standards

All 25 workflows comply with:
- ✅ Valid n8n JSON format with `executionOrder: "v1"`
- ✅ Correct `ai_*` LangChain sub-type connections (ai_languageModel, ai_memory, ai_tool, ai_outputParser, ai_embedding)
- ✅ No orphan nodes — every node is wired
- ✅ Real node types only (googleCalendarTool, gmailTool, etc.)
- ✅ `$fromAI()` expressions on all MCP/AI tool parameters
- ✅ Empty credential IDs (templates, no PLACEHOLDER strings)
- ✅ Dynamic expressions instead of hardcoded values
- ✅ No `errorWorkflow` references (for distribution)
- ✅ Clean tags array

## 🚀 Quick Start

```bash
# 1. Choose your package
git clone https://github.com/grootme/workflows.git
cd workflows/jarvis-starter     # or jarvis-professional / jarvis-enterprise

# 2. Configure
cp .env.example .env
nano .env                        # Add your API keys

# 3. Launch
docker compose up -d

# 4. Access
open http://localhost:5678
```

## 💰 Pricing

| Package | One-Time | Monthly Running Cost | Included |
|---------|----------|---------------------|----------|
| Starter | $49 | $5-15 | 12 workflows, 2 Docker services |
| Professional | $149 | $25-75 | 25 workflows, 4 Docker services |
| Enterprise | $399 | $75-250 | 25 workflows, 8 Docker services + monitoring |

## 🔧 Requirements

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **n8n**: Self-hosted via Docker (included in docker-compose)
- **API Credentials**: OpenAI, Google Workspace, Gemini (as needed per package)
- **PostgreSQL**: Included in docker-compose
- **Qdrant**: For RAG vector store (Professional+)
- **Redis**: For queue management (Professional+)

## 📜 License

MIT License — Use, modify, and distribute freely.

---

*Built with JARVIS Package Builder v2.0 — 25 workflows • 68 AI connections • 0 technical debt*
