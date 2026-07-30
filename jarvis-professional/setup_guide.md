# JARVIS Professional — Setup Guide

> Business Automation Platform
> Version 3.0 | Zero Technical Debt | Production Ready

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Quick Start](#2-quick-start)
3. [Credential Configuration](#3-credential-configuration)
4. [Workflow Import](#4-workflow-import)
5. [MCP Server Deployment](#5-mcp-server-deployment)
6. [Testing & Verification](#6-testing--verification)
7. [Production Deployment](#7-production-deployment)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4 cores |
| RAM | 4 GB | 8 GB  |
| Disk | 20 GB | 50 GB SSD |
| Docker | 20.10+ | 24.0+ |
| Docker Compose | 2.0+ | 2.20+ |

### Required Accounts

1. OpenAI API Key (GPT-4o-mini + GPT-4.1-mini)
2. Google Calendar OAuth2
3. Gmail OAuth2
4. Google Contacts OAuth2
5. Google Gemini API Key (embeddings + Flash)
6. PostgreSQL connection
7. Qdrant (cloud or self-hosted)
8. Telegram Bot Token
9. Evolution API (WhatsApp)
10. Flowise URL (optional)


---

## 2. Quick Start

### Step 1: Clone and Configure

```bash
# Clone the repository
git clone https://github.com/grootme/workflows.git
cd workflows/jarvis-professional

# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### Step 2: Configure Required Variables

At minimum, update these in your `.env` file:

```bash
# Required for all workflows
OPENAI_API_KEY=sk-your-actual-key-here
GOOGLE_GEMINI_API_KEY=AIza-your-actual-key-here

# Strong passwords for production
N8N_PASSWORD=your-strong-password
POSTGRES_PASSWORD=your-strong-password
```

### Step 3: Launch Services

```bash
# Start all services
docker compose up -d

# Verify services are running
docker compose ps

# Check n8n logs
docker compose logs n8n -f
```

### Step 4: Access n8n

Open your browser and navigate to:

- **n8n UI**: http://localhost:5678
- **Login**: Use the credentials from your `.env` file

- **Qdrant Dashboard**: http://localhost:6333/dashboard

---

## 3. Credential Configuration

### Google Workspace OAuth2

For Calendar, Gmail, and Contacts MCP suites:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable APIs:
   - Google Calendar API
   - Gmail API
   - Google Contacts API (People API)
4. Create OAuth 2.0 credentials
5. Configure OAuth consent screen
6. Add redirect URL: `http://localhost:5678/rest/oauth2-credential/callback`
7. In n8n, go to **Settings > Credentials > Add Credential**
8. Select **Google Calendar OAuth2 API** and authenticate

### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to **API Keys**
3. Create a new key with appropriate permissions
4. Set spending limits (recommended: $10/month for Starter)
5. In n8n, add **OpenAI API** credential

### Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create an API key
3. In n8n, add **Google Gemini API** credential

### Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Use `/newbot` command and follow instructions
3. Copy the bot token
4. In n8n, add **Telegram API** credential

### Evolution API (WhatsApp)

1. Deploy Evolution API instance or use cloud service
2. Configure WhatsApp Business connection
3. Get API key and instance name
4. Update webhook URL in n8n workflow to point to your n8n instance

---

## 4. Workflow Import

### Import All Workflows

1. In n8n, go to **Workflows > Import from File**
2. Navigate to the `workflows/` directory
3. Import each workflow in this order:

#### Consolidated Workflows

1. `G1_MCP_Calendar_Suite_v2.json`
2. `G2_MCP_Gmail_Suite_v2.json`
3. `G3_MCP_Contactos_Suite_v2.json`
4. `G4_Ecommerce_Agent_Suite_v2.json`
5. `G5_Marketing_MultiAgent_Suite_v2.json`
6. `G6_Asistente_Platform_v2.json`
7. `G7_Imagenes_Citas_Suite_v2.json`
8. `G8_Video_Viral_Suite_v2.json`
9. `G9_Social_Scraper_Suite_v2.json`
10. `G10_HR_AI_Agent_v2.json`
11. `G11_WhatsApp_AI_Agent_v2.json`
12. `G12_Flowise_RAG_Suite_v2.json`
13. `G13_Global_Error_Handler_v2.json`

#### MCP Server Workflows

14. `MCP_Calendar_Server_v2.json`
15. `MCP_Gmail_Server_v2.json`
16. `MCP_Contacts_Server_v2.json`
17. `MCP_ECommerce_Server_v2.json`
18. `MCP_HR_Server_v2.json`
19. `MCP_Knowledge_Base_Server_v2.json`

#### Base Templates

20. `T1_Single_Agent_Chat_v2.json`
21. `T2_Agent_MCP_Tool_v2.json`
22. `T3_RAG_Agent_v2.json`
23. `T4_Multi_Agent_Orchestrator_v2.json`
24. `T5_Error_Handler_v2.json`
25. `T6_MCP_Server_v2.json`



#### Anthropic Pattern Workflows

1. `P1_Prompt_Chaining_Agent_v3.json` — P1 Prompt Chaining Agent
2. `P2_Smart_Routing_Agent_v3.json` — P2 Smart Routing Agent
3. `P3_Orchestrator_Workers_Agent_v3.json` — P3 Orchestrator-Workers Agent
4. `P4_Evaluator_Optimizer_Agent_v3.json` — P4 Evaluator-Optimizer Agent
5. `P5_Parallelization_Agent_v3.json` — P5 Parallelization Agent
6. `P7_SOUL_Bootstrap_Agent_v3.json` — P7 SOUL Bootstrap Agent

#### Cognitive Capital Skills

These SKILL.md files are loaded into agent memory for better results. Copy them to your n8n data directory:

```bash
# Copy cognitive capital to n8n data volume
cp -r cognitive_capital/ /path/to/n8n/data/
```

Skills available:
- **deep-research** — `cognitive_capital/deep-research/SKILL.md`
- **consulting-analysis** — `cognitive_capital/consulting-analysis/SKILL.md`
- **data-analysis** — `cognitive_capital/data-analysis/SKILL.md`
- **newsletter-generation** — `cognitive_capital/newsletter-generation/SKILL.md`
- **SOUL Template** — `cognitive_capital/SOUL.template.md`

### Post-Import Configuration

After importing each workflow:

1. **Open the workflow** in n8n
2. **Configure credentials** for each node that shows a credential warning
3. **Review the sticky notes** — each workflow has setup documentation
4. **Test the workflow** in manual mode before activating
5. **Activate** when ready

---

## 5. MCP Server Deployment

MCP (Model Context Protocol) servers are standalone workflows that expose tools via the MCP trigger. They can be consumed by any n8n Agent node through the MCP Client Tool.

### Deploying MCP Servers

1. Import the MCP server workflow
2. Configure all tool credentials
3. **Activate** the MCP server workflow
4. Copy the webhook URL from the MCP trigger node
5. In the consuming Agent workflow, add an **MCP Client Tool** node
6. Set the `sseEndpoint` to the MCP server webhook URL

### MCP Server Architecture

```
┌─────────────────┐     ai_tool      ┌──────────────────┐
│   Agent Node     │ ◄─────────────── │  MCP Client Tool  │
│   (Consumer)     │                  │  (SSE Endpoint)   │
└─────────────────┘                  └────────┬──────────┘
                                              │
                                              │ HTTP/SSE
                                              ▼
                                     ┌──────────────────┐
                                     │   MCP Trigger     │
                                     │   (Server)        │
                                     └────────┬──────────┘
                                              │
                                     ┌────────┴──────────┐
                                     │                   │
                              ┌──────▼──────┐  ┌───────▼──────┐
                              │  Tool Node 1 │  │  Tool Node 2  │
                              │  (Calendar)  │  │   (Gmail)     │
                              └─────────────┘  └──────────────┘
```

---

## 6. Testing & Verification

### Test Checklist

Run through these tests for each workflow before production use:

- [ ] **Calendar Suite**: Create, read, update, delete events
- [ ] **Gmail Suite**: Send email, search, read, label
- [ ] **Contacts Suite**: Create, search, update, delete contacts
- [ ] **E-Commerce Agent**: Order lookup, product search, customer support
- [ ] **Marketing Multi-Agent**: Content generation, scheduling, analytics
- [ ] **WhatsApp Agent**: Text message, audio transcription, knowledge base query
- [ ] **HR Agent**: Employee queries, policy lookup, time-off requests
- [ ] **Social Scraper**: Twitter/X, Instagram data extraction
- [ ] **Error Handler**: Error routing, Gmail alert, PostgreSQL logging

### Test Command

```bash
# Quick health check
curl -s http://localhost:5678/healthz

# Check Qdrant
curl -s http://localhost:6333/healthz

# Check Redis
docker compose exec redis redis-cli -a changeme ping

# Check all services
docker compose ps
```

---

## 7. Production Deployment

### Security Checklist

- [ ] Change all default passwords in `.env`
- [ ] Enable HTTPS (use Let's Encrypt for automatic certificates)
- [ ] Restrict n8n port access (do not expose 5678 directly)
- [ ] Set up firewall rules
- [ ] Enable PostgreSQL SSL connections
- [ ] Configure Qdrant API key
- [ ] Review n8n webhook URL (must use HTTPS in production)
- [ ] Set up regular database backups

### Backup Strategy

```bash
# PostgreSQL backup
docker compose exec postgres pg_dump -U jarvis jarvis > backup_$(date +%Y%m%d).sql

# Qdrant snapshot
curl -X POST http://localhost:6333/snapshots

# n8n data backup
docker compose run --rm -v n8n_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/n8n_backup_$(date +%Y%m%d).tar.gz /data
```

### Monitoring

Enable n8n metrics (already configured in docker-compose):
- n8n exposes metrics at `http://localhost:5678/metrics`
- Key metrics: `n8n_workflow_success`, `n8n_workflow_error`, `n8n_workflow_duration`

---

## 8. Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Credential not found" | OAuth not configured | Complete Google OAuth flow in n8n UI |
| "Connection refused" | Service not ready | Wait 30s, check `docker compose ps` |
| "MCP tool not found" | MCP server inactive | Activate MCP server workflow first |
| "$fromAI() not resolved" | Old n8n version | Update to n8n 1.40+ |
| "Memory error" | PostgreSQL not connected | Check postgres health, verify credentials |
| "Qdrant timeout" | Vector DB not ready | Check qdrant container logs |

### Useful Commands

```bash
# View n8n logs
docker compose logs n8n -f --tail=100

# Restart a service
docker compose restart n8n

# Full rebuild
docker compose down && docker compose up -d --build

# Check resource usage
docker stats
```

### Getting Help

- **GitHub Issues**: https://github.com/grootme/workflows/issues
- **n8n Community**: https://community.n8n.io
- **Documentation**: https://docs.n8n.io

---

*Generated by JARVIS Package Builder v2.0 | {datetime.now().strftime('%Y-%m-%d')}*
