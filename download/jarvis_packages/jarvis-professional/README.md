# JARVIS Professional

> Business Automation Platform

[![Zero Debt](https://img.shields.io/badge/Zero-Debt-brightgreen)](https://github.com/grootme/workflows)
[![n8n](https://img.shields.io/badge/n8n-Compatible-orange)](https://n8n.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Overview

Full business automation suite with e-commerce, marketing, HR, and WhatsApp AI agents. Multi-agent orchestration with MCP client architecture.

**Target**: SMBs, agencies, and growing businesses that need automated customer service, marketing, and HR workflows.

## What's Included

| Category | Count | Details |
|----------|-------|---------|
| Consolidated Workflows | 13 | Production-ready AI automation suites |
| MCP Server Templates | 6 | Reusable MCP tool servers |
| Base Templates | 6 | Starting points for custom workflows |
| **Total Workflows** | **25** | All zero-debt, production-ready |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/grootme/workflows.git
cd workflows/jarvis-professional

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
│                  JARVIS Professional                    │
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
- **G4 Ecommerce Agent Suite** — `G4_Ecommerce_Agent_Suite_v2.json`
- **G5 Marketing MultiAgent Suite** — `G5_Marketing_MultiAgent_Suite_v2.json`
- **G6 Asistente Platform** — `G6_Asistente_Platform_v2.json`
- **G7 Imagenes Citas Suite** — `G7_Imagenes_Citas_Suite_v2.json`
- **G8 Video Viral Suite** — `G8_Video_Viral_Suite_v2.json`
- **G9 Social Scraper Suite** — `G9_Social_Scraper_Suite_v2.json`
- **G10 HR AI Agent** — `G10_HR_AI_Agent_v2.json`
- **G11 WhatsApp AI Agent** — `G11_WhatsApp_AI_Agent_v2.json`
- **G12 Flowise RAG Suite** — `G12_Flowise_RAG_Suite_v2.json`
- **G13 Global Error Handler** — `G13_Global_Error_Handler_v2.json`

### MCP Server Templates

- **MCP Calendar Server** — `MCP_Calendar_Server_v2.json`
- **MCP Gmail Server** — `MCP_Gmail_Server_v2.json`
- **MCP Contacts Server** — `MCP_Contacts_Server_v2.json`
- **MCP ECommerce Server** — `MCP_ECommerce_Server_v2.json`
- **MCP HR Server** — `MCP_HR_Server_v2.json`
- **MCP Knowledge Base Server** — `MCP_Knowledge_Base_Server_v2.json`

### Base Templates

- **T1 Single Agent Chat** — `T1_Single_Agent_Chat_v2.json`
- **T2 Agent MCP Tool** — `T2_Agent_MCP_Tool_v2.json`
- **T3 RAG Agent** — `T3_RAG_Agent_v2.json`
- **T4 Multi Agent Orchestrator** — `T4_Multi_Agent_Orchestrator_v2.json`
- **T5 Error Handler** — `T5_Error_Handler_v2.json`
- **T6 MCP Server** — `T6_MCP_Server_v2.json`


## Credentials Needed

- OpenAI API Key (GPT-4o-mini + GPT-4.1-mini)
- Google Calendar OAuth2
- Gmail OAuth2
- Google Contacts OAuth2
- Google Gemini API Key (embeddings + Flash)
- PostgreSQL connection
- Qdrant (cloud or self-hosted)
- Telegram Bot Token
- Evolution API (WhatsApp)
- Flowise URL (optional)


## LLM Strategy

GPT-4o-mini → GPT-4.1-mini → Gemini 2.5 Flash (tiered)

## Estimated Costs

- **One-time**: $149
- **Monthly running**: $25-75/month (depending on usage)

## Docker Services

- n8n
- postgres
- qdrant
- redis


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
