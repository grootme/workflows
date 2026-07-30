# JARVIS Enterprise

> Full AI Operations Suite

[![Zero Debt](https://img.shields.io/badge/Zero-Debt-brightgreen)](https://github.com/grootme/workflows)
[![n8n](https://img.shields.io/badge/n8n-Compatible-orange)](https://n8n.io)
[![Anthropic Patterns](https://img.shields.io/badge/Anthropic-Patterns-blueviolet)](https://www.anthropic.com/engineering/building-effective-agents)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)

## Overview

Full AI Operations Suite with 7 Anthropic-pattern workflows, 6 cognitive capital skills, and SOUL template for personalized AI personalities.

**Target**: Organizations requiring the full Anthropic agent pattern arsenal with cognitive capital MCP server, enterprise monitoring, and personalized AI personalities.

## What's Included

| Category | Count | Details |
|----------|-------|---------|
| Consolidated Workflows | 13 | Production-ready AI automation suites |
| MCP Server Templates | 6 | Reusable MCP tool servers |
| Base Templates | 6 | Starting points for custom workflows |
| **Anthropic Patterns** | **7** | Agent design patterns from Anthropic research |
| Cognitive Capital Skills | 6 | SKILL.md knowledge base for agents |
| **Total Workflows** | **32** | All zero-debt, production-ready |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/grootme/workflows.git
cd workflows/jarvis-enterprise

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

- **P1 Prompt Chaining Agent** — `P1_Prompt_Chaining_Agent_v3.json` — Research → Gate → Draft → Gate → Polish. Multi-step content pipeline with quality gates and tiered LLMs (GPT-4o-mini → GPT-4.1-mini → GPT-4.1).
- **P2 Smart Routing Agent** — `P2_Smart_Routing_Agent_v3.json` — Classifies user intent and routes to 7 specialized sub-agents (calendar, email, research, ecommerce, creative, technical, HR).
- **P3 Orchestrator-Workers Agent** — `P3_Orchestrator_Workers_Agent_v3.json` — Central orchestrator breaks complex tasks into subtasks and delegates to 4 specialized workers (Research, Creative, Technical, Data).
- **P4 Evaluator-Optimizer Agent** — `P4_Evaluator_Optimizer_Agent_v3.json` — Generator → Evaluator → Quality Gate loop. Iteratively refines content until quality threshold is met (max 3 retries).
- **P5 Parallelization Agent** — `P5_Parallelization_Agent_v3.json` — 3 parallel analysts (Financial, Market, Technical) → Aggregate → Synthesis Agent. Webhook-based for API integration.
- **P6 Cognitive Capital MCP Server** — `P6_Cognitive_Capital_MCP_Server_v3.json` — 6 skills as MCP tools (Deep Research, Consulting Analysis, Data Analysis, Newsletter, Code Docs, Podcast). MCP Trigger for agent consumption.
- **P7 SOUL Bootstrap Agent** — `P7_SOUL_Bootstrap_Agent_v3.json` — 4-phase conversational onboarding (Hello → You → Personality → Depth) that generates a personalized SOUL.md for AI assistants.

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

- **deep-research** — `cognitive_capital/deep-research/SKILL.md`
- **consulting-analysis** — `cognitive_capital/consulting-analysis/SKILL.md`
- **data-analysis** — `cognitive_capital/data-analysis/SKILL.md`
- **newsletter-generation** — `cognitive_capital/newsletter-generation/SKILL.md`
- **code-documentation** — `cognitive_capital/code-documentation/SKILL.md`
- **podcast-generation** — `cognitive_capital/podcast-generation/SKILL.md`

- **SOUL Template** — `cognitive_capital/SOUL.template.md` — Personalized AI personality system

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

- OpenAI API Key (multiple models)
- Google Workspace OAuth2 (Calendar, Gmail, Contacts)
- Google Gemini API Key (embeddings)
- PostgreSQL connection
- Qdrant API Key (vector store)
- Redis connection (caching)
- Zep API Key (enterprise memory)

## LLM Strategy

GPT-4o-mini → GPT-4.1-mini → Gemini 2.5 Flash → GPT-4.1 → Claude Sonnet (full tiered)

## Estimated Costs

- **One-time**: $399
- **Monthly running**: $75-250/month (depending on usage and scale)

## Docker Services

  - n8n
  - postgres
  - qdrant
  - redis
  - nginx
  - prometheus
  - grafana
  - zep

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
