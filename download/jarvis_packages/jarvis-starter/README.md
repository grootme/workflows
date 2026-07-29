# JARVIS Starter

> Your Personal AI Assistant

[![Zero Debt](https://img.shields.io/badge/Zero-Debt-brightgreen)](https://github.com/grootme/workflows)
[![n8n](https://img.shields.io/badge/n8n-Compatible-orange)](https://n8n.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Overview

Complete personal AI assistant with Google Workspace MCP integration. Manage your calendar, email, and contacts through natural conversation.

**Target**: Individuals, freelancers, and small teams who want a personal AI assistant integrated with Google Workspace.

## What's Included

| Category | Count | Details |
|----------|-------|---------|
| Consolidated Workflows | 6 | Production-ready AI automation suites |
| MCP Server Templates | 4 | Reusable MCP tool servers |
| Base Templates | 2 | Starting points for custom workflows |
| **Total Workflows** | **12** | All zero-debt, production-ready |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/grootme/workflows.git
cd workflows/jarvis-starter

# 2. Configure
cp .env.example .env
# Edit .env with your API keys

# 3. Launch
docker compose up -d

# 4. Access
open http://localhost:5678
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  JARVIS Starter                    │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  MCP      │  │  Agent   │  │  Error   │          │
│  │  Servers  │  │  Suites  │  │  Handler │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       │              │              │                 │
│       └──────────────┼──────────────┘                 │
│                      │                                │
│              ┌───────▼───────┐                       │
│              │     n8n       │                       │
│              └───────┬───────┘                       │
│                      │                                │
│              ┌───────▼───────┐                       │
│              │  PostgreSQL   │                       │
│              └───────────────┘                       │
└─────────────────────────────────────────────────────┘
```

## Workflows

### Consolidated Suites

- **G1 MCP Calendar Suite** — `G1_MCP_Calendar_Suite_v2.json`
- **G2 MCP Gmail Suite** — `G2_MCP_Gmail_Suite_v2.json`
- **G3 MCP Contactos Suite** — `G3_MCP_Contactos_Suite_v2.json`
- **G7 Imagenes Citas Suite** — `G7_Imagenes_Citas_Suite_v2.json`
- **G8 Video Viral Suite** — `G8_Video_Viral_Suite_v2.json`
- **G12 Flowise RAG Suite** — `G12_Flowise_RAG_Suite_v2.json`

### MCP Server Templates

- **MCP Calendar Server** — `MCP_Calendar_Server_v2.json`
- **MCP Gmail Server** — `MCP_Gmail_Server_v2.json`
- **MCP Contacts Server** — `MCP_Contacts_Server_v2.json`
- **MCP Knowledge Base Server** — `MCP_Knowledge_Base_Server_v2.json`

### Base Templates

- **T1 Single Agent Chat** — `T1_Single_Agent_Chat_v2.json`
- **T6 MCP Server** — `T6_MCP_Server_v2.json`


## Credentials Needed

- OpenAI API Key (GPT-4o-mini)
- Google Calendar OAuth2
- Gmail OAuth2
- Google Contacts OAuth2
- Google Gemini API Key (embeddings)
- PostgreSQL connection


## LLM Strategy

GPT-4o-mini ($0.15/$0.60 per 1M tokens)

## Estimated Costs

- **One-time**: $49
- **Monthly running**: $5-15/month (depending on usage)

## Docker Services

- n8n
- postgres


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
