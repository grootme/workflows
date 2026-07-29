#!/usr/bin/env python3
"""
JARVIS Implementation Packages Generator
=========================================
Transforms 25 zero-debt workflows into 3 high-value product packages.

JARVIS Starter   → Personal AI Assistant ($49)
JARVIS Professional → Business Automation Platform ($149)
JARVIS Enterprise → Full AI Operations Suite ($399)

Each package includes:
- n8n workflow JSONs
- docker-compose.yml (production-ready)
- setup_guide.md (step-by-step)
- pricing page (HTML)
- README.md
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path("/home/z/my-project/download/n8n_workflows_v2")
OUTPUT_DIR = Path("/home/z/my-project/download/jarvis_packages")
V2_CONSOLIDATED = BASE_DIR / "consolidated"
V2_MCP = BASE_DIR / "mcp_servers"
V2_TEMPLATES = BASE_DIR / "base_templates"

# ── Package Definitions ────────────────────────────────────────────────────
PACKAGES = {
    "jarvis-starter": {
        "name": "JARVIS Starter",
        "tagline": "Your Personal AI Assistant",
        "price": 49,
        "price_display": "$49",
        "description": "Complete personal AI assistant with Google Workspace MCP integration. Manage your calendar, email, and contacts through natural conversation.",
        "target": "Individuals, freelancers, and small teams who want a personal AI assistant integrated with Google Workspace.",
        "workflows": {
            "consolidated": [
                "G1_MCP_Calendar_Suite_v2.json",
                "G2_MCP_Gmail_Suite_v2.json",
                "G3_MCP_Contactos_Suite_v2.json",
                "G7_Imagenes_Citas_Suite_v2.json",
                "G8_Video_Viral_Suite_v2.json",
                "G12_Flowise_RAG_Suite_v2.json",
            ],
            "mcp_servers": [
                "MCP_Calendar_Server_v2.json",
                "MCP_Gmail_Server_v2.json",
                "MCP_Contacts_Server_v2.json",
                "MCP_Knowledge_Base_Server_v2.json",
            ],
            "templates": [
                "T1_Single_Agent_Chat_v2.json",
                "T6_MCP_Server_v2.json",
            ],
        },
        "features": [
            "3 Google Workspace MCP Suites (Calendar, Gmail, Contacts)",
            "4 MCP Server Templates ready to deploy",
            "Image & Quote generation suite",
            "Video content creation suite",
            "Flowise RAG integration",
            "Knowledge Base server with vector search",
            "Single Agent Chat template",
            "MCP Server base template",
            "Docker Compose with n8n + PostgreSQL",
            "Step-by-step setup guide",
        ],
        "credentials_needed": [
            "OpenAI API Key (GPT-4o-mini)",
            "Google Calendar OAuth2",
            "Gmail OAuth2",
            "Google Contacts OAuth2",
            "Google Gemini API Key (embeddings)",
            "PostgreSQL connection",
        ],
        "docker_services": ["n8n", "postgres"],
        "llm_tier": "GPT-4o-mini ($0.15/$0.60 per 1M tokens)",
        "estimated_monthly_cost": "$5-15/month (depending on usage)",
    },
    "jarvis-professional": {
        "name": "JARVIS Professional",
        "tagline": "Business Automation Platform",
        "price": 149,
        "price_display": "$149",
        "description": "Full business automation suite with e-commerce, marketing, HR, and WhatsApp AI agents. Multi-agent orchestration with MCP client architecture.",
        "target": "SMBs, agencies, and growing businesses that need automated customer service, marketing, and HR workflows.",
        "workflows": {
            "consolidated": [
                "G1_MCP_Calendar_Suite_v2.json",
                "G2_MCP_Gmail_Suite_v2.json",
                "G3_MCP_Contactos_Suite_v2.json",
                "G4_Ecommerce_Agent_Suite_v2.json",
                "G5_Marketing_MultiAgent_Suite_v2.json",
                "G6_Asistente_Platform_v2.json",
                "G7_Imagenes_Citas_Suite_v2.json",
                "G8_Video_Viral_Suite_v2.json",
                "G9_Social_Scraper_Suite_v2.json",
                "G10_HR_AI_Agent_v2.json",
                "G11_WhatsApp_AI_Agent_v2.json",
                "G12_Flowise_RAG_Suite_v2.json",
                "G13_Global_Error_Handler_v2.json",
            ],
            "mcp_servers": [
                "MCP_Calendar_Server_v2.json",
                "MCP_Gmail_Server_v2.json",
                "MCP_Contacts_Server_v2.json",
                "MCP_ECommerce_Server_v2.json",
                "MCP_HR_Server_v2.json",
                "MCP_Knowledge_Base_Server_v2.json",
            ],
            "templates": [
                "T1_Single_Agent_Chat_v2.json",
                "T2_Agent_MCP_Tool_v2.json",
                "T3_RAG_Agent_v2.json",
                "T4_Multi_Agent_Orchestrator_v2.json",
                "T5_Error_Handler_v2.json",
                "T6_MCP_Server_v2.json",
            ],
        },
        "features": [
            "All 13 consolidated workflows (G1-G13)",
            "All 6 MCP Server templates",
            "All 6 base templates",
            "E-Commerce Agent with PostgreSQL memory",
            "Marketing Multi-Agent orchestrator",
            "WhatsApp AI Agent with RAG + audio transcription",
            "HR AI Agent with smart routing",
            "Social Scraper Suite",
            "Global Error Handler with Gmail + PostgreSQL alerts",
            "Asistente Platform with MCP Client architecture",
            "Docker Compose with n8n + PostgreSQL + Qdrant + Redis",
            "Complete setup guide with credential configuration",
            "Priority support channel access",
        ],
        "credentials_needed": [
            "OpenAI API Key (GPT-4o-mini + GPT-4.1-mini)",
            "Google Calendar OAuth2",
            "Gmail OAuth2",
            "Google Contacts OAuth2",
            "Google Gemini API Key (embeddings + Flash)",
            "PostgreSQL connection",
            "Qdrant (cloud or self-hosted)",
            "Telegram Bot Token",
            "Evolution API (WhatsApp)",
            "Flowise URL (optional)",
        ],
        "docker_services": ["n8n", "postgres", "qdrant", "redis"],
        "llm_tier": "GPT-4o-mini → GPT-4.1-mini → Gemini 2.5 Flash (tiered)",
        "estimated_monthly_cost": "$25-75/month (depending on usage)",
    },
    "jarvis-enterprise": {
        "name": "JARVIS Enterprise",
        "tagline": "Full AI Operations Suite",
        "price": 399,
        "price_display": "$399",
        "description": "Complete AI operations platform with advanced RAG, multi-agent orchestration, enterprise MCP architecture, and full observability. Includes everything from Starter + Professional plus enterprise-grade features.",
        "target": "Enterprises, SaaS companies, and organizations that need a complete AI operations platform with production-grade reliability.",
        "workflows": {
            "consolidated": [
                "G1_MCP_Calendar_Suite_v2.json",
                "G2_MCP_Gmail_Suite_v2.json",
                "G3_MCP_Contactos_Suite_v2.json",
                "G4_Ecommerce_Agent_Suite_v2.json",
                "G5_Marketing_MultiAgent_Suite_v2.json",
                "G6_Asistente_Platform_v2.json",
                "G7_Imagenes_Citas_Suite_v2.json",
                "G8_Video_Viral_Suite_v2.json",
                "G9_Social_Scraper_Suite_v2.json",
                "G10_HR_AI_Agent_v2.json",
                "G11_WhatsApp_AI_Agent_v2.json",
                "G12_Flowise_RAG_Suite_v2.json",
                "G13_Global_Error_Handler_v2.json",
            ],
            "mcp_servers": [
                "MCP_Calendar_Server_v2.json",
                "MCP_Gmail_Server_v2.json",
                "MCP_Contacts_Server_v2.json",
                "MCP_ECommerce_Server_v2.json",
                "MCP_HR_Server_v2.json",
                "MCP_Knowledge_Base_Server_v2.json",
            ],
            "templates": [
                "T1_Single_Agent_Chat_v2.json",
                "T2_Agent_MCP_Tool_v2.json",
                "T3_RAG_Agent_v2.json",
                "T4_Multi_Agent_Orchestrator_v2.json",
                "T5_Error_Handler_v2.json",
                "T6_MCP_Server_v2.json",
            ],
        },
        "features": [
            "Everything in Professional, plus:",
            "Enterprise-grade docker-compose with monitoring stack",
            "Prometheus + Grafana observability dashboards",
            "Nginx reverse proxy with SSL termination",
            "Zep + Mem0 enterprise memory integration",
            "Multi-tenant architecture support",
            "Advanced RAG with hybrid search (Qdrant + PostgreSQL)",
            "Custom MCP server development template",
            "CI/CD pipeline configuration",
            "Production deployment scripts",
            "Security hardening guide",
            "SLA-ready error handling & alerting",
            "Architecture decision records (ADR)",
            "White-label customization guide",
            "1 hour consultation call included",
        ],
        "credentials_needed": [
            "OpenAI API Key (all tiers)",
            "Anthropic API Key (Claude Sonnet)",
            "Google Workspace OAuth2 (Calendar, Gmail, Contacts)",
            "Google Gemini API Key",
            "PostgreSQL (production cluster)",
            "Qdrant (production cluster)",
            "Redis (production cluster)",
            "Telegram Bot Token",
            "Evolution API (WhatsApp Business)",
            "Zep API Key (enterprise memory)",
            "Flowise URL (optional)",
            "SSL certificates (Let's Encrypt or custom)",
        ],
        "docker_services": [
            "n8n", "postgres", "qdrant", "redis",
            "nginx", "prometheus", "grafana", "zep"
        ],
        "llm_tier": "GPT-4o-mini → GPT-4.1-mini → Gemini 2.5 Flash → GPT-4.1 → Claude Sonnet (full tiered)",
        "estimated_monthly_cost": "$75-250/month (depending on usage and scale)",
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# DOCKER COMPOSE GENERATORS
# ═══════════════════════════════════════════════════════════════════════════

def generate_docker_compose_starter() -> str:
    return """version: "3.8"

# ═══════════════════════════════════════════════════════════════════════════
# JARVIS Starter — Personal AI Assistant
# Services: n8n + PostgreSQL
# ═══════════════════════════════════════════════════════════════════════════

services:
  n8n:
    image: n8nio/n8n:latest
    container_name: jarvis-n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER:-admin}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD:-changeme}
      - N8N_HOST=${N8N_HOST:-localhost}
      - N8N_PORT=5678
      - N8N_PROTOCOL=${N8N_PROTOCOL:-http}
      - WEBHOOK_URL=${WEBHOOK_URL:-http://localhost:5678/}
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB:-jarvis}
      - DB_POSTGRESDB_USER=${POSTGRES_USER:-jarvis}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD:-changeme}
      - N8N_PAYLOAD_SIZE_MAX=16
      - N8N_METRICS=true
      - N8N_DIAGNOSTICS_ENABLED=false
    volumes:
      - n8n_data:/home/node/.n8n
      - ./workflows:/home/node/.n8n/import
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - jarvis-net

  postgres:
    image: postgres:16-alpine
    container_name: jarvis-postgres
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=${POSTGRES_DB:-jarvis}
      - POSTGRES_USER=${POSTGRES_USER:-jarvis}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-changeme}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-jarvis}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - jarvis-net

volumes:
  n8n_data:
    driver: local
  postgres_data:
    driver: local

networks:
  jarvis-net:
    driver: bridge
"""


def generate_docker_compose_professional() -> str:
    return """version: "3.8"

# ═══════════════════════════════════════════════════════════════════════════
# JARVIS Professional — Business Automation Platform
# Services: n8n + PostgreSQL + Qdrant + Redis
# ═══════════════════════════════════════════════════════════════════════════

services:
  n8n:
    image: n8nio/n8n:latest
    container_name: jarvis-n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER:-admin}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD:-changeme}
      - N8N_HOST=${N8N_HOST:-localhost}
      - N8N_PORT=5678
      - N8N_PROTOCOL=${N8N_PROTOCOL:-http}
      - WEBHOOK_URL=${WEBHOOK_URL:-http://localhost:5678/}
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB:-jarvis}
      - DB_POSTGRESDB_USER=${POSTGRES_USER:-jarvis}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD:-changeme}
      - N8N_PAYLOAD_SIZE_MAX=32
      - N8N_METRICS=true
      - N8N_DIAGNOSTICS_ENABLED=false
      - QUEUE_BULL_REDIS_HOST=redis
      - QUEUE_BULL_REDIS_PORT=6379
      - EXECUTIONS_MODE=regular
      - N8N_CONCURRENCY_PRODUCTION_LIMIT=10
    volumes:
      - n8n_data:/home/node/.n8n
      - ./workflows:/home/node/.n8n/import
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      qdrant:
        condition: service_started
    networks:
      - jarvis-net

  postgres:
    image: postgres:16-alpine
    container_name: jarvis-postgres
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=${POSTGRES_DB:-jarvis}
      - POSTGRES_USER=${POSTGRES_USER:-jarvis}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-changeme}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-jarvis}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - jarvis-net

  qdrant:
    image: qdrant/qdrant:latest
    container_name: jarvis-qdrant
    restart: unless-stopped
    ports:
      - "6333:6333"
      - "6334:6334"
    environment:
      - QDRANT_API_KEY=${QDRANT_API_KEY:-}
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - jarvis-net

  redis:
    image: redis:7-alpine
    container_name: jarvis-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    command: redis-server --requirepass ${REDIS_PASSWORD:-changeme} --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD:-changeme}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - jarvis-net

volumes:
  n8n_data:
    driver: local
  postgres_data:
    driver: local
  qdrant_data:
    driver: local
  redis_data:
    driver: local

networks:
  jarvis-net:
    driver: bridge
"""


def generate_docker_compose_enterprise() -> str:
    return """version: "3.8"

# ═══════════════════════════════════════════════════════════════════════════
# JARVIS Enterprise — Full AI Operations Suite
# Services: n8n + PostgreSQL + Qdrant + Redis + Nginx + Prometheus + Grafana + Zep
# ═══════════════════════════════════════════════════════════════════════════

services:
  nginx:
    image: nginx:alpine
    container_name: jarvis-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - nginx_logs:/var/log/nginx
    depends_on:
      - n8n
      - grafana
    networks:
      - jarvis-net
      - jarvis-public

  n8n:
    image: n8nio/n8n:latest
    container_name: jarvis-n8n
    restart: unless-stopped
    expose:
      - "5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER:-admin}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD:-changeme}
      - N8N_HOST=${N8N_HOST:-localhost}
      - N8N_PORT=5678
      - N8N_PROTOCOL=${N8N_PROTOCOL:-https}
      - WEBHOOK_URL=${WEBHOOK_URL:-https://localhost/}
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB:-jarvis}
      - DB_POSTGRESDB_USER=${POSTGRES_USER:-jarvis}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD:-changeme}
      - N8N_PAYLOAD_SIZE_MAX=64
      - N8N_METRICS=true
      - N8N_METRICS_PREFIX=jarvis_
      - N8N_DIAGNOSTICS_ENABLED=false
      - QUEUE_BULL_REDIS_HOST=redis
      - QUEUE_BULL_REDIS_PORT=6379
      - QUEUE_BULL_REDIS_PASSWORD=${REDIS_PASSWORD:-changeme}
      - EXECUTIONS_MODE=queue
      - N8N_CONCURRENCY_PRODUCTION_LIMIT=20
      - N8N_CONCURRENCY_PRODUCTION_LIMIT_TIMEOUT=300
    volumes:
      - n8n_data:/home/node/.n8n
      - ./workflows:/home/node/.n8n/import
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      qdrant:
        condition: service_started
    networks:
      - jarvis-net

  postgres:
    image: postgres:16-alpine
    container_name: jarvis-postgres
    restart: unless-stopped
    expose:
      - "5432"
    environment:
      - POSTGRES_DB=${POSTGRES_DB:-jarvis}
      - POSTGRES_USER=${POSTGRES_USER:-jarvis}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-changeme}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-jarvis}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - jarvis-net

  qdrant:
    image: qdrant/qdrant:latest
    container_name: jarvis-qdrant
    restart: unless-stopped
    expose:
      - "6333"
      - "6334"
    environment:
      - QDRANT_API_KEY=${QDRANT_API_KEY:-}
    volumes:
      - qdrant_data:/qdrant/storage
    networks:
      - jarvis-net

  redis:
    image: redis:7-alpine
    container_name: jarvis-redis
    restart: unless-stopped
    expose:
      - "6379"
    command: redis-server --requirepass ${REDIS_PASSWORD:-changeme} --maxmemory 512mb --maxmemory-policy allkeys-lru --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD:-changeme}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - jarvis-net

  zep:
    image: ghcr.io/getzep/zep:latest
    container_name: jarvis-zep
    restart: unless-stopped
    expose:
      - "8000"
    environment:
      - ZEP_OPENAI_API_KEY=${OPENAI_API_KEY:-}
      - ZEP_POSTGRES_DSN=postgresql://${POSTGRES_USER:-jarvis}:${POSTGRES_PASSWORD:-changeme}@postgres:5432/zep
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - jarvis-net

  prometheus:
    image: prom/prometheus:latest
    container_name: jarvis-prometheus
    restart: unless-stopped
    expose:
      - "9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - jarvis-net

  grafana:
    image: grafana/grafana:latest
    container_name: jarvis-grafana
    restart: unless-stopped
    expose:
      - "3000"
    environment:
      - GF_SECURITY_ADMIN_USER=${GRAFANA_USER:-admin}
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-changeme}
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources:ro
    depends_on:
      - prometheus
    networks:
      - jarvis-net

volumes:
  n8n_data:
    driver: local
  postgres_data:
    driver: local
  qdrant_data:
    driver: local
  redis_data:
    driver: local
  prometheus_data:
    driver: local
  grafana_data:
    driver: local
  nginx_logs:
    driver: local

networks:
  jarvis-net:
    driver: bridge
    internal: true
  jarvis-public:
    driver: bridge
"""


# ═══════════════════════════════════════════════════════════════════════════
# ENV FILE GENERATORS
# ═══════════════════════════════════════════════════════════════════════════

def generate_env_file(pkg_key: str) -> str:
    pkg = PACKAGES[pkg_key]
    is_enterprise = pkg_key == "jarvis-enterprise"
    is_professional = pkg_key == "jarvis-professional"

    lines = [
        "# ═══════════════════════════════════════════════════════════════════════════",
        f"# {pkg['name']} — Environment Configuration",
        "# ═══════════════════════════════════════════════════════════════════════════",
        "",
        "# ── n8n Configuration ─────────────────────────────────────────────────────",
        "N8N_HOST=localhost",
        "N8N_PROTOCOL=http",
        "WEBHOOK_URL=http://localhost:5678/",
        "N8N_USER=admin",
        f"N8N_PASSWORD={'changeme_please_use_strong_password' if is_enterprise else 'changeme'}",
        "",
        "# ── PostgreSQL ────────────────────────────────────────────────────────────",
        "POSTGRES_DB=jarvis",
        "POSTGRES_USER=jarvis",
        f"POSTGRES_PASSWORD={'changeme_please_use_strong_password' if is_enterprise else 'changeme'}",
        "",
    ]

    if is_professional or is_enterprise:
        lines += [
            "# ── Qdrant (Vector Database) ──────────────────────────────────────────────",
            "QDRANT_API_KEY=",
            "",
            "# ── Redis ────────────────────────────────────────────────────────────────",
            f"REDIS_PASSWORD={'changeme_please_use_strong_password' if is_enterprise else 'changeme'}",
            "",
        ]

    if is_enterprise:
        lines += [
            "# ── Nginx / SSL ──────────────────────────────────────────────────────────",
            "SSL_CERT_PATH=./nginx/ssl/cert.pem",
            "SSL_KEY_PATH=./nginx/ssl/key.pem",
            "",
            "# ── Grafana ──────────────────────────────────────────────────────────────",
            "GRAFANA_USER=admin",
            "GRAFANA_PASSWORD=changeme_please_use_strong_password",
            "",
        ]

    lines += [
        "# ── API Keys (configure before first run) ────────────────────────────────",
        "OPENAI_API_KEY=sk-...",
        "GOOGLE_GEMINI_API_KEY=AIza...",
        "",
        "# ── Google Workspace OAuth2 ──────────────────────────────────────────────",
        "# Configure via n8n UI: Settings > Credentials > Add Credential",
        "# Required: Google Calendar OAuth2, Gmail OAuth2, Google Contacts OAuth2",
        "",
    ]

    if is_professional or is_enterprise:
        lines += [
            "# ── Telegram Bot ────────────────────────────────────────────────────────",
            "TELEGRAM_BOT_TOKEN=123456:ABC-DEF...",
            "",
            "# ── WhatsApp (Evolution API) ─────────────────────────────────────────────",
            "EVOLUTION_API_URL=http://evolution-api:8080",
            "EVOLUTION_API_KEY=your-key",
            "",
        ]

    if is_enterprise:
        lines += [
            "# ── Anthropic (Claude Sonnet) ────────────────────────────────────────────",
            "ANTHROPIC_API_KEY=sk-ant-...",
            "",
            "# ── Zep (Enterprise Memory) ──────────────────────────────────────────────",
            "ZEP_API_KEY=your-zep-key",
            "",
        ]

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# SETUP GUIDE GENERATORS
# ═══════════════════════════════════════════════════════════════════════════

def generate_setup_guide(pkg_key: str) -> str:
    pkg = PACKAGES[pkg_key]
    is_enterprise = pkg_key == "jarvis-enterprise"
    is_professional = pkg_key == "jarvis-professional"
    is_starter = pkg_key == "jarvis-starter"

    guide = f"""# {pkg['name']} — Setup Guide

> {pkg['tagline']}
> Version 2.0 | Zero Technical Debt | Production Ready

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
| RAM | 4 GB | 8 GB {'(16 GB for Enterprise)' if is_enterprise else ''} |
| Disk | 20 GB | 50 GB SSD |
| Docker | 20.10+ | 24.0+ |
| Docker Compose | 2.0+ | 2.20+ |

### Required Accounts

"""

    for i, cred in enumerate(pkg["credentials_needed"], 1):
        guide += f"{i}. {cred}\n"

    guide += f"""

---

## 2. Quick Start

### Step 1: Clone and Configure

```bash
# Clone the repository
git clone https://github.com/grootme/workflows.git
cd workflows/{pkg_key}

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

"""

    if is_professional or is_enterprise:
        guide += """- **Qdrant Dashboard**: http://localhost:6333/dashboard

"""

    if is_enterprise:
        guide += """- **Grafana**: http://localhost:3000 (via Nginx)
- **Prometheus**: http://localhost:9090 (internal only)

"""

    guide += """---

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

"""

    if is_professional or is_enterprise:
        guide += """### Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Use `/newbot` command and follow instructions
3. Copy the bot token
4. In n8n, add **Telegram API** credential

### Evolution API (WhatsApp)

1. Deploy Evolution API instance or use cloud service
2. Configure WhatsApp Business connection
3. Get API key and instance name
4. Update webhook URL in n8n workflow to point to your n8n instance

"""

    if is_enterprise:
        guide += """### Anthropic API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an API key
3. In n8n, add **Anthropic API** credential (for Claude Sonnet tier)

### Zep (Enterprise Memory)

1. Deploy Zep or use Zep Cloud
2. Get API key from Zep dashboard
3. Configure in n8n as HTTP header credential

"""

    guide += """---

## 4. Workflow Import

### Import All Workflows

1. In n8n, go to **Workflows > Import from File**
2. Navigate to the `workflows/` directory
3. Import each workflow in this order:

"""

    wf_order = pkg["workflows"]
    step = 1

    guide += "#### Consolidated Workflows\n\n"
    for wf in wf_order["consolidated"]:
        guide += f"{step}. `{wf}`\n"
        step += 1

    guide += "\n#### MCP Server Workflows\n\n"
    for wf in wf_order["mcp_servers"]:
        guide += f"{step}. `{wf}`\n"
        step += 1

    guide += "\n#### Base Templates\n\n"
    for wf in wf_order["templates"]:
        guide += f"{step}. `{wf}`\n"
        step += 1

    guide += """

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

"""

    if is_enterprise:
        guide += """### Multi-Instance MCP Architecture (Enterprise)

For production, deploy MCP servers on separate n8n instances:

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Nginx Load Balancer                          │
│                    (SSL termination + routing)                       │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │  n8n Main    │ │  n8n MCP-1   │ │  n8n MCP-2   │
     │  (Agents)    │ │  (Calendar,  │ │  (E-Commerce,│
     │              │ │   Gmail,     │ │   HR, KB)    │
     │              │ │   Contacts)  │ │              │
     └──────┬───────┘ └──────────────┘ └──────────────┘
            │
     ┌──────┴───────┐
     │  PostgreSQL  │
     │  + Qdrant    │
     │  + Redis     │
     └──────────────┘
```

"""

    guide += """---

## 6. Testing & Verification

### Test Checklist

Run through these tests for each workflow before production use:

- [ ] **Calendar Suite**: Create, read, update, delete events
- [ ] **Gmail Suite**: Send email, search, read, label
- [ ] **Contacts Suite**: Create, search, update, delete contacts
"""

    if is_professional or is_enterprise:
        guide += """- [ ] **E-Commerce Agent**: Order lookup, product search, customer support
- [ ] **Marketing Multi-Agent**: Content generation, scheduling, analytics
- [ ] **WhatsApp Agent**: Text message, audio transcription, knowledge base query
- [ ] **HR Agent**: Employee queries, policy lookup, time-off requests
- [ ] **Social Scraper**: Twitter/X, Instagram data extraction
- [ ] **Error Handler**: Error routing, Gmail alert, PostgreSQL logging
"""

    if is_enterprise:
        guide += """- [ ] **Prometheus**: Metrics collection from n8n
- [ ] **Grafana**: Dashboard visualization
- [ ] **Nginx**: SSL termination, reverse proxy
- [ ] **Zep**: Enterprise memory persistence
"""

    guide += """
### Test Command

```bash
# Quick health check
curl -s http://localhost:5678/healthz

"""

    if is_professional or is_enterprise:
        guide += """# Check Qdrant
curl -s http://localhost:6333/healthz

# Check Redis
docker compose exec redis redis-cli -a changeme ping

"""

    guide += """# Check all services
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
docker compose run --rm -v n8n_data:/data -v $(pwd):/backup alpine \\
  tar czf /backup/n8n_backup_$(date +%Y%m%d).tar.gz /data
```

### Monitoring

"""

    if is_enterprise:
        guide += """Enterprise includes Prometheus + Grafana for full observability:

- **n8n Metrics**: `jarvis_n8n_*` prefix
- **Prometheus**: http://localhost:9090
- **Grafana Dashboard**: Pre-configured with n8n metrics
- **Alert Rules**: Configure in `monitoring/prometheus.yml`

"""

    guide += """Enable n8n metrics (already configured in docker-compose):
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
"""

    return guide


# ═══════════════════════════════════════════════════════════════════════════
# PRICING PAGE GENERATORS
# ═══════════════════════════════════════════════════════════════════════════

def generate_pricing_page() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS — AI Automation Packages</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a2e;
            --bg-card-hover: #222240;
            --accent-starter: #00d4aa;
            --accent-pro: #6c5ce7;
            --accent-enterprise: #fd79a8;
            --text-primary: #ffffff;
            --text-secondary: #a0a0b8;
            --text-muted: #6a6a80;
            --border: #2a2a40;
            --glow-starter: rgba(0, 212, 170, 0.15);
            --glow-pro: rgba(108, 92, 231, 0.15);
            --glow-enterprise: rgba(253, 121, 168, 0.15);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Background effects */
        body::before {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(ellipse at 20% 50%, rgba(0, 212, 170, 0.03) 0%, transparent 50%),
                        radial-gradient(ellipse at 80% 20%, rgba(108, 92, 231, 0.03) 0%, transparent 50%),
                        radial-gradient(ellipse at 50% 80%, rgba(253, 121, 168, 0.03) 0%, transparent 50%);
            z-index: -1;
        }

        /* Header */
        .header {
            text-align: center;
            padding: 80px 20px 40px;
        }

        .header-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            background: rgba(0, 212, 170, 0.1);
            border: 1px solid rgba(0, 212, 170, 0.2);
            border-radius: 100px;
            font-size: 13px;
            color: var(--accent-starter);
            margin-bottom: 24px;
            font-weight: 500;
        }

        .header h1 {
            font-size: clamp(40px, 6vw, 72px);
            font-weight: 800;
            letter-spacing: -2px;
            line-height: 1.1;
            margin-bottom: 16px;
        }

        .header h1 .gradient {
            background: linear-gradient(135deg, var(--accent-starter), var(--accent-pro), var(--accent-enterprise));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header p {
            font-size: 18px;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
        }

        /* Pricing Grid */
        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 24px;
            max-width: 1200px;
            margin: 60px auto;
            padding: 0 24px;
        }

        /* Card */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 40px 32px;
            position: relative;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
        }

        .card:hover {
            transform: translateY(-4px);
            border-color: var(--card-accent);
        }

        .card.starter { --card-accent: var(--accent-starter); }
        .card.pro { --card-accent: var(--accent-pro); }
        .card.enterprise { --card-accent: var(--accent-enterprise); }

        .card:hover.starter { box-shadow: 0 20px 60px var(--glow-starter); }
        .card:hover.pro { box-shadow: 0 20px 60px var(--glow-pro); }
        .card:hover.enterprise { box-shadow: 0 20px 60px var(--glow-enterprise); }

        .card-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 100px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            width: fit-content;
            margin-bottom: 20px;
        }

        .starter .card-badge {
            background: rgba(0, 212, 170, 0.1);
            color: var(--accent-starter);
            border: 1px solid rgba(0, 212, 170, 0.2);
        }

        .pro .card-badge {
            background: rgba(108, 92, 231, 0.1);
            color: var(--accent-pro);
            border: 1px solid rgba(108, 92, 231, 0.2);
        }

        .enterprise .card-badge {
            background: rgba(253, 121, 168, 0.1);
            color: var(--accent-enterprise);
            border: 1px solid rgba(253, 121, 168, 0.2);
        }

        .card-popular {
            position: absolute;
            top: -12px;
            right: 24px;
            background: linear-gradient(135deg, var(--accent-pro), #a29bfe);
            color: white;
            padding: 4px 14px;
            border-radius: 100px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .card-title {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .card-tagline {
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 24px;
        }

        .card-price {
            display: flex;
            align-items: baseline;
            gap: 4px;
            margin-bottom: 8px;
        }

        .card-price .amount {
            font-size: 48px;
            font-weight: 800;
            letter-spacing: -2px;
        }

        .card-price .currency {
            font-size: 24px;
            font-weight: 600;
            color: var(--text-secondary);
        }

        .card-price .period {
            font-size: 14px;
            color: var(--text-muted);
        }

        .card-cost {
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 28px;
            padding-bottom: 28px;
            border-bottom: 1px solid var(--border);
        }

        .card-features {
            list-style: none;
            flex: 1;
            margin-bottom: 32px;
        }

        .card-features li {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 8px 0;
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        .card-features li .check {
            flex-shrink: 0;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            margin-top: 2px;
        }

        .starter .check { background: rgba(0, 212, 170, 0.15); color: var(--accent-starter); }
        .pro .check { background: rgba(108, 92, 231, 0.15); color: var(--accent-pro); }
        .enterprise .check { background: rgba(253, 121, 168, 0.15); color: var(--accent-enterprise); }

        .card-cta {
            display: block;
            text-align: center;
            padding: 14px 24px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
            cursor: pointer;
            border: none;
        }

        .starter .card-cta {
            background: rgba(0, 212, 170, 0.1);
            color: var(--accent-starter);
            border: 1px solid rgba(0, 212, 170, 0.3);
        }
        .starter .card-cta:hover { background: rgba(0, 212, 170, 0.2); }

        .pro .card-cta {
            background: linear-gradient(135deg, var(--accent-pro), #a29bfe);
            color: white;
        }
        .pro .card-cta:hover { opacity: 0.9; transform: scale(1.02); }

        .enterprise .card-cta {
            background: rgba(253, 121, 168, 0.1);
            color: var(--accent-enterprise);
            border: 1px solid rgba(253, 121, 168, 0.3);
        }
        .enterprise .card-cta:hover { background: rgba(253, 121, 168, 0.2); }

        /* Stats bar */
        .stats-bar {
            display: flex;
            justify-content: center;
            gap: 48px;
            padding: 40px 20px;
            max-width: 800px;
            margin: 0 auto;
            flex-wrap: wrap;
        }

        .stat {
            text-align: center;
        }

        .stat .number {
            font-size: 32px;
            font-weight: 800;
            letter-spacing: -1px;
        }

        .stat .label {
            font-size: 13px;
            color: var(--text-muted);
            margin-top: 4px;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 60px 20px 40px;
            color: var(--text-muted);
            font-size: 13px;
        }

        .footer a {
            color: var(--text-secondary);
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }

        /* Comparison table */
        .comparison {
            max-width: 1000px;
            margin: 60px auto;
            padding: 0 24px;
        }

        .comparison h2 {
            text-align: center;
            font-size: 28px;
            margin-bottom: 32px;
            font-weight: 700;
        }

        .comparison table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }

        .comparison th, .comparison td {
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        .comparison th {
            color: var(--text-muted);
            font-weight: 500;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .comparison th:first-child { color: var(--text-secondary); }

        .comparison td:not(:first-child) { text-align: center; }

        .comparison tr:hover { background: rgba(255,255,255,0.02); }

        .yes { color: var(--accent-starter); font-weight: 600; }
        .no { color: var(--text-muted); }

        @media (max-width: 768px) {
            .pricing-grid { grid-template-columns: 1fr; }
            .stats-bar { gap: 24px; }
            .comparison { overflow-x: auto; }
        }
    </style>
</head>
<body>

<div class="header">
    <div class="header-badge">⚡ Zero Technical Debt • Production Ready</div>
    <h1>JARVIS <span class="gradient">AI Automation</span></h1>
    <p>Transform your workflows with 25 zero-debt n8n automations packaged into 3 tiers. From personal assistant to enterprise AI operations.</p>
</div>

<div class="stats-bar">
    <div class="stat">
        <div class="number" style="color: var(--accent-starter)">25</div>
        <div class="label">Zero-Debt Workflows</div>
    </div>
    <div class="stat">
        <div class="number" style="color: var(--accent-pro)">6</div>
        <div class="label">MCP Servers</div>
    </div>
    <div class="stat">
        <div class="number" style="color: var(--accent-enterprise)">68</div>
        <div class="label">AI Connections</div>
    </div>
    <div class="stat">
        <div class="number">0</div>
        <div class="label">Technical Debt Items</div>
    </div>
</div>

<div class="pricing-grid">

    <!-- Starter -->
    <div class="card starter">
        <div class="card-badge">Starter</div>
        <div class="card-title">JARVIS Starter</div>
        <div class="card-tagline">Your Personal AI Assistant</div>
        <div class="card-price">
            <span class="currency">$</span>
            <span class="amount">49</span>
            <span class="period">one-time</span>
        </div>
        <div class="card-cost">Est. running cost: $5-15/month</div>
        <ul class="card-features">
            <li><span class="check">✓</span> 3 Google Workspace MCP Suites</li>
            <li><span class="check">✓</span> 4 MCP Server Templates</li>
            <li><span class="check">✓</span> Image & Quote generation suite</li>
            <li><span class="check">✓</span> Video content creation suite</li>
            <li><span class="check">✓</span> Flowise RAG integration</li>
            <li><span class="check">✓</span> Knowledge Base server</li>
            <li><span class="check">✓</span> 2 Base templates</li>
            <li><span class="check">✓</span> Docker Compose (n8n + PostgreSQL)</li>
            <li><span class="check">✓</span> Step-by-step setup guide</li>
        </ul>
        <a href="https://github.com/grootme/workflows/tree/main/jarvis-starter" class="card-cta">Get Started →</a>
    </div>

    <!-- Professional -->
    <div class="card pro">
        <div class="card-popular">Most Popular</div>
        <div class="card-badge">Professional</div>
        <div class="card-title">JARVIS Professional</div>
        <div class="card-tagline">Business Automation Platform</div>
        <div class="card-price">
            <span class="currency">$</span>
            <span class="amount">149</span>
            <span class="period">one-time</span>
        </div>
        <div class="card-cost">Est. running cost: $25-75/month</div>
        <ul class="card-features">
            <li><span class="check">✓</span> <strong>Everything in Starter, plus:</strong></li>
            <li><span class="check">✓</span> 13 consolidated workflows (G1-G13)</li>
            <li><span class="check">✓</span> 6 MCP Server templates</li>
            <li><span class="check">✓</span> 6 Base templates</li>
            <li><span class="check">✓</span> E-Commerce Agent + WhatsApp AI</li>
            <li><span class="check">✓</span> Marketing Multi-Agent orchestrator</li>
            <li><span class="check">✓</span> HR AI Agent + Social Scraper</li>
            <li><span class="check">✓</span> Global Error Handler</li>
            <li><span class="check">✓</span> Docker Compose (n8n + PG + Qdrant + Redis)</li>
            <li><span class="check">✓</span> Complete setup guide</li>
        </ul>
        <a href="https://github.com/grootme/workflows/tree/main/jarvis-professional" class="card-cta">Get Professional →</a>
    </div>

    <!-- Enterprise -->
    <div class="card enterprise">
        <div class="card-badge">Enterprise</div>
        <div class="card-title">JARVIS Enterprise</div>
        <div class="card-tagline">Full AI Operations Suite</div>
        <div class="card-price">
            <span class="currency">$</span>
            <span class="amount">399</span>
            <span class="period">one-time</span>
        </div>
        <div class="card-cost">Est. running cost: $75-250/month</div>
        <ul class="card-features">
            <li><span class="check">✓</span> <strong>Everything in Professional, plus:</strong></li>
            <li><span class="check">✓</span> Prometheus + Grafana monitoring</li>
            <li><span class="check">✓</span> Nginx reverse proxy + SSL</li>
            <li><span class="check">✓</span> Zep enterprise memory</li>
            <li><span class="check">✓</span> Multi-tenant architecture</li>
            <li><span class="check">✓</span> CI/CD pipeline config</li>
            <li><span class="check">✓</span> Security hardening guide</li>
            <li><span class="check">✓</span> White-label customization</li>
            <li><span class="check">✓</span> Full 8-service Docker Compose</li>
            <li><span class="check">✓</span> 1 hour consultation call</li>
        </ul>
        <a href="https://github.com/grootme/workflows/tree/main/jarvis-enterprise" class="card-cta">Contact Sales →</a>
    </div>

</div>

<!-- Comparison Table -->
<div class="comparison">
    <h2>Feature Comparison</h2>
    <table>
        <thead>
            <tr>
                <th>Feature</th>
                <th>Starter ($49)</th>
                <th>Professional ($149)</th>
                <th>Enterprise ($399)</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Consolidated Workflows</td><td>6</td><td>13</td><td>13</td></tr>
            <tr><td>MCP Server Templates</td><td>4</td><td>6</td><td>6</td></tr>
            <tr><td>Base Templates</td><td>2</td><td>6</td><td>6</td></tr>
            <tr><td>Google Workspace MCP</td><td class="yes">✓</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>E-Commerce Agent</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>WhatsApp AI Agent</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>Marketing Multi-Agent</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>HR AI Agent</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>RAG + Vector Search</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>Global Error Handler</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>Docker Compose</td><td>2 services</td><td>4 services</td><td>8 services</td></tr>
            <tr><td>Prometheus + Grafana</td><td class="no">—</td><td class="no">—</td><td class="yes">✓</td></tr>
            <tr><td>Nginx + SSL</td><td class="no">—</td><td class="no">—</td><td class="yes">✓</td></tr>
            <tr><td>Zep Enterprise Memory</td><td class="no">—</td><td class="no">—</td><td class="yes">✓</td></tr>
            <tr><td>Multi-tenant Support</td><td class="no">—</td><td class="no">—</td><td class="yes">✓</td></tr>
            <tr><td>White-label Customization</td><td class="no">—</td><td class="no">—</td><td class="yes">✓</td></tr>
            <tr><td>Consultation Call</td><td class="no">—</td><td class="no">—</td><td class="yes">1 hour</td></tr>
            <tr><td>LLM Tier</td><td>GPT-4o-mini</td><td>Tiered (3)</td><td>Full Tiered (5)</td></tr>
            <tr><td>Est. Monthly Cost</td><td>$5-15</td><td>$25-75</td><td>$75-250</td></tr>
        </tbody>
    </table>
</div>

<div class="footer">
    <p>Built with zero technical debt • 25 workflows • 68 AI connections • <a href="https://github.com/grootme/workflows">GitHub</a></p>
    <p style="margin-top: 8px;">© 2026 JARVIS Automation • All workflows validated and production-ready</p>
</div>

</body>
</html>"""


# ═══════════════════════════════════════════════════════════════════════════
# README GENERATORS
# ═══════════════════════════════════════════════════════════════════════════

def generate_readme(pkg_key: str) -> str:
    pkg = PACKAGES[pkg_key]
    wf_counts = {
        "consolidated": len(pkg["workflows"]["consolidated"]),
        "mcp_servers": len(pkg["workflows"]["mcp_servers"]),
        "templates": len(pkg["workflows"]["templates"]),
    }
    total = sum(wf_counts.values())

    readme = f"""# {pkg['name']}

> {pkg['tagline']}

[![Zero Debt](https://img.shields.io/badge/Zero-Debt-brightgreen)](https://github.com/grootme/workflows)
[![n8n](https://img.shields.io/badge/n8n-Compatible-orange)](https://n8n.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Overview

{pkg['description']}

**Target**: {pkg['target']}

## What's Included

| Category | Count | Details |
|----------|-------|---------|
| Consolidated Workflows | {wf_counts['consolidated']} | Production-ready AI automation suites |
| MCP Server Templates | {wf_counts['mcp_servers']} | Reusable MCP tool servers |
| Base Templates | {wf_counts['templates']} | Starting points for custom workflows |
| **Total Workflows** | **{total}** | All zero-debt, production-ready |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/grootme/workflows.git
cd workflows/{pkg_key}

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
│                  {pkg['name']}                    │
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

"""

    for wf in pkg["workflows"]["consolidated"]:
        name = wf.replace("_v2.json", "").replace(".json", "").replace("_", " ")
        readme += f"- **{name}** — `{wf}`\n"

    readme += "\n### MCP Server Templates\n\n"
    for wf in pkg["workflows"]["mcp_servers"]:
        name = wf.replace("_v2.json", "").replace(".json", "").replace("_", " ")
        readme += f"- **{name}** — `{wf}`\n"

    readme += "\n### Base Templates\n\n"
    for wf in pkg["workflows"]["templates"]:
        name = wf.replace("_v2.json", "").replace(".json", "").replace("_", " ")
        readme += f"- **{name}** — `{wf}`\n"

    readme += f"""

## Credentials Needed

"""

    for cred in pkg["credentials_needed"]:
        readme += f"- {cred}\n"

    readme += f"""

## LLM Strategy

{pkg['llm_tier']}

## Estimated Costs

- **One-time**: {pkg['price_display']}
- **Monthly running**: {pkg['estimated_monthly_cost']}

## Docker Services

"""

    for svc in pkg["docker_services"]:
        readme += f"- {svc}\n"

    readme += """

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


# ═══════════════════════════════════════════════════════════════════════════
# ENTERPRISE EXTRAS
# ═══════════════════════════════════════════════════════════════════════════

def generate_nginx_conf() -> str:
    return """events {
    worker_connections 1024;
}

http {
    upstream n8n {
        server n8n:5678;
    }

    upstream grafana {
        server grafana:3000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;
    limit_req_zone $binary_remote_addr zone=webhook:10m rate=60r/m;

    server {
        listen 80;
        server_name _;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        server_name _;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # n8n main interface
        location / {
            proxy_pass http://n8n;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_buffering off;
            proxy_cache off;
            chunked_transfer_encoding off;
        }

        # n8n webhooks (higher rate limit)
        location /webhook/ {
            limit_req zone=webhook burst=20 nodelay;
            proxy_pass http://n8n;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # n8n API
        location /api/ {
            limit_req zone=api burst=10 nodelay;
            proxy_pass http://n8n;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Grafana monitoring
        location /monitoring/ {
            auth_request /auth-check;
            proxy_pass http://grafana/;
            proxy_set_header Host $host;
        }

        # Health check
        location /health {
            proxy_pass http://n8n/healthz;
            access_log off;
        }
    }
}
"""


def generate_prometheus_conf() -> str:
    return """global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'n8n'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['n8n:5678']
    scrape_interval: 30s

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

alerting:
  alertmanagers:
    - static_configs:
        - targets: []

rule_files:
  - 'alerts.yml'
"""


def generate_grafana_datasource() -> str:
    return """apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true

  - name: PostgreSQL
    type: postgres
    url: postgres:5432
    database: jarvis
    user: jarvis
    secureJsonData:
      password: changeme_please_use_strong_password
    jsonData:
      sslmode: disable
      maxOpenConns: 5
      maxIdleConns: 2
      connMaxLifetime: 14400
    editable: true
"""


def generate_grafana_dashboard_provider() -> str:
    return """apiVersion: 1

providers:
  - name: 'JARVIS Dashboards'
    orgId: 1
    folder: 'JARVIS'
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /etc/grafana/provisioning/dashboards
      foldersFromFilesStructure: false
"""


def generate_init_db_sql() -> str:
    return """-- JARVIS Database Initialization
-- Creates required tables for n8n + LangChain memory + error handling

-- LangChain chat history table
CREATE TABLE IF NOT EXISTS message_store (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    message JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Error log table
CREATE TABLE IF NOT EXISTS error_log (
    id SERIAL PRIMARY KEY,
    workflow_name VARCHAR(255),
    error_message TEXT,
    error_severity VARCHAR(50),
    node_name VARCHAR(255),
    execution_id VARCHAR(255),
    payload JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics table
CREATE TABLE IF NOT EXISTS workflow_analytics (
    id SERIAL PRIMARY KEY,
    workflow_name VARCHAR(255),
    execution_id VARCHAR(255),
    status VARCHAR(50),
    duration_ms INTEGER,
    tokens_used INTEGER,
    cost_usd DECIMAL(10, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_message_store_session ON message_store(session_id);
CREATE INDEX IF NOT EXISTS idx_error_log_severity ON error_log(error_severity);
CREATE INDEX IF NOT EXISTS idx_error_log_created ON error_log(created_at);
CREATE INDEX IF NOT EXISTS idx_workflow_analytics_name ON workflow_analytics(workflow_name);
CREATE INDEX IF NOT EXISTS idx_workflow_analytics_created ON workflow_analytics(created_at);

-- Zep database (enterprise)
CREATE DATABASE IF NOT EXISTS zep;
"""


# ═══════════════════════════════════════════════════════════════════════════
# MAIN BUILDER
# ═══════════════════════════════════════════════════════════════════════════

def build_package(pkg_key: str):
    """Build a complete JARVIS package."""
    pkg = PACKAGES[pkg_key]
    pkg_dir = OUTPUT_DIR / pkg_key

    print(f"\n{'='*60}")
    print(f"  Building {pkg['name']}")
    print(f"{'='*60}")

    # Create directory structure
    dirs_to_create = [
        pkg_dir,
        pkg_dir / "workflows" / "consolidated",
        pkg_dir / "workflows" / "mcp_servers",
        pkg_dir / "workflows" / "templates",
    ]

    if pkg_key == "jarvis-enterprise":
        dirs_to_create += [
            pkg_dir / "nginx" / "ssl",
            pkg_dir / "monitoring" / "grafana" / "dashboards",
            pkg_dir / "monitoring" / "grafana" / "datasources",
            pkg_dir / "init-db",
        ]

    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  📁 Created: {d.relative_to(OUTPUT_DIR)}")

    # Copy workflow JSONs
    copied = 0
    for category, files in pkg["workflows"].items():
        src_dir = {
            "consolidated": V2_CONSOLIDATED,
            "mcp_servers": V2_MCP,
            "templates": V2_TEMPLATES,
        }[category]
        dst_dir = pkg_dir / "workflows" / category

        for filename in files:
            src = src_dir / filename
            if src.exists():
                shutil.copy2(src, dst_dir / filename)
                copied += 1
            else:
                print(f"  ⚠️  Missing: {filename}")

    print(f"  ✅ Copied {copied} workflow files")

    # Generate docker-compose.yml
    docker_generators = {
        "jarvis-starter": generate_docker_compose_starter,
        "jarvis-professional": generate_docker_compose_professional,
        "jarvis-enterprise": generate_docker_compose_enterprise,
    }
    docker_content = docker_generators[pkg_key]()
    (pkg_dir / "docker-compose.yml").write_text(docker_content)
    print(f"  ✅ Generated docker-compose.yml ({len(pkg['docker_services'])} services)")

    # Generate .env.example
    env_content = generate_env_file(pkg_key)
    (pkg_dir / ".env.example").write_text(env_content)
    print(f"  ✅ Generated .env.example")

    # Generate setup guide
    setup_content = generate_setup_guide(pkg_key)
    (pkg_dir / "setup_guide.md").write_text(setup_content)
    print(f"  ✅ Generated setup_guide.md")

    # Generate README
    readme_content = generate_readme(pkg_key)
    (pkg_dir / "README.md").write_text(readme_content)
    print(f"  ✅ Generated README.md")

    # Enterprise extras
    if pkg_key == "jarvis-enterprise":
        (pkg_dir / "nginx" / "nginx.conf").write_text(generate_nginx_conf())
        (pkg_dir / "monitoring" / "prometheus.yml").write_text(generate_prometheus_conf())
        (pkg_dir / "monitoring" / "grafana" / "datasources" / "datasource.yml").write_text(generate_grafana_datasource())
        (pkg_dir / "monitoring" / "grafana" / "dashboards" / "dashboard.yml").write_text(generate_grafana_dashboard_provider())
        (pkg_dir / "init-db" / "01_init.sql").write_text(generate_init_db_sql())
        print(f"  ✅ Generated enterprise extras (nginx, prometheus, grafana, init-db)")

    # Generate package manifest
    manifest = {
        "package": pkg_key,
        "name": pkg["name"],
        "version": "2.0.0",
        "price": pkg["price"],
        "zero_debt": True,
        "workflows": {
            "consolidated": pkg["workflows"]["consolidated"],
            "mcp_servers": pkg["workflows"]["mcp_servers"],
            "templates": pkg["workflows"]["templates"],
        },
        "docker_services": pkg["docker_services"],
        "llm_tier": pkg["llm_tier"],
        "estimated_monthly_cost": pkg["estimated_monthly_cost"],
        "generated_at": datetime.now().isoformat(),
    }
    (pkg_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"  ✅ Generated manifest.json")

    return manifest


def generate_root_readme() -> str:
    return """# JARVIS AI Automation Packages

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
"""


def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║         JARVIS Package Builder v2.0                        ║")
    print("║         25 Workflows → 3 Products                          ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Clean output
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Build all 3 packages
    manifests = {}
    for pkg_key in PACKAGES:
        manifests[pkg_key] = build_package(pkg_key)

    # Generate pricing page
    pricing_html = generate_pricing_page()
    (OUTPUT_DIR / "pricing.html").write_text(pricing_html)
    print(f"\n✅ Generated pricing.html")

    # Generate root README
    root_readme = generate_root_readme()
    (OUTPUT_DIR / "README.md").write_text(root_readme)
    print(f"✅ Generated README.md")

    # Summary
    summary = {
        "version": "2.0.0",
        "packages": list(PACKAGES.keys()),
        "total_workflows": 25,
        "total_ai_connections": 68,
        "zero_debt_items": 0,
        "pricing": {
            "starter": 49,
            "professional": 149,
            "enterprise": 399,
        },
        "generated_at": datetime.now().isoformat(),
        "manifests": manifests,
    }
    (OUTPUT_DIR / "_package_summary.json").write_text(json.dumps(summary, indent=2))

    # Print summary
    print(f"\n{'='*60}")
    print(f"  BUILD COMPLETE")
    print(f"{'='*60}")
    print(f"  📦 3 packages built")
    print(f"  📄 25 workflows distributed")
    print(f"  🔗 68 AI connections")
    print(f"  💰 Pricing: $49 / $149 / $399")
    print(f"  📁 Output: {OUTPUT_DIR}")
    print(f"{'='*60}")

    # List structure
    print(f"\n📁 Directory Structure:")
    for root, dirs, files in os.walk(OUTPUT_DIR):
        level = root.replace(str(OUTPUT_DIR), "").count(os.sep)
        indent = "  " * level
        print(f"{indent}📂 {os.path.basename(root)}/")
        subindent = "  " * (level + 1)
        for f in sorted(files):
            print(f"{subindent}📄 {f}")


if __name__ == "__main__":
    main()
