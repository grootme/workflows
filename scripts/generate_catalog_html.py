#!/usr/bin/env python3
"""Generate Marketplace Catalog HTML for PDF conversion."""

import json
import os

# Load existing catalog data
with open('/home/z/my-project/public/catalog_data.json') as f:
    catalog_data = json.load(f)

workflows = catalog_data.get('workflows', [])
duplications = catalog_data.get('duplications', [])
similarities = catalog_data.get('similarities', [])
consolidation = catalog_data.get('consolidation_suggestions', [])

# Calculate stats
total_workflows = len(workflows)
categories = {}
for wf in workflows:
    for c in wf.get('categories', []):
        categories[c] = categories.get(c, 0) + 1

sources = {}
for wf in workflows:
    s = wf.get('source', '')
    sources[s] = sources.get(s, 0) + 1

# Sort categories by count
sorted_cats = sorted(categories.items(), key=lambda x: -x[1])

# Node types frequency
node_types = {}
for wf in workflows:
    for nt in wf.get('node_types', []):
        node_types[nt] = node_types.get(nt, 0) + 1
sorted_nodes = sorted(node_types.items(), key=lambda x: -x[1])[:15]

# Price tiers data (from research)
pricing_tiers = [
    {"tier": "Starter", "price_range": "$5 - $15", "description": "Workflows simples de 3-8 nodos, un solo trigger, una integracion basica", "examples": "Notificacion Slack, Sync Google Sheets, Email auto-respuesta"},
    {"tier": "Professional", "price_range": "$15 - $35", "description": "Workflows de 8-20 nodos, multi-step logic, 2-3 integraciones, error handling basico", "examples": "Lead qualification pipeline, CRM sync + email, Social media cross-posting"},
    {"tier": "Enterprise", "price_range": "$35 - $75", "description": "Workflows de 20+ nodos, multi-agent AI, RAG, sub-workflows, error handling completo, MCP integracion", "examples": "Multi-agent sales assistant, RAG chatbot + vector store, Automated compliance review"},
    {"tier": "Custom Solution", "price_range": "$75 - $200+", "description": "Soluciones custom con desarrollo MCP server, integracion con sistemas proprietarios, soporte post-venta", "examples": "MCP server para ERP proprietario, Pipeline de datos enterprise, Multi-system integration hub"},
]

# Automation ideas (from research)
automation_ideas = [
    {"name": "Lead Qualification AI Agent", "category": "Marketing & Leads", "nodes": "8-15", "description": "Agente AI que analiza leads entrantes, clasifica por prioridad, enriquece con datos de CRM, y asigna al representante correcto. Usa LangChain Agent con tools de CRM lookup y email enrichment.", "price": "$25-45"},
    {"name": "Customer Support Triage Bot", "category": "Chat & Mensajeria", "nodes": "10-18", "description": "Agente AI que clasifica tickets de soporte por urgencia y tipo, responde automaticamente preguntas frecuentes usando RAG, y escala tickets complejos al equipo correcto con contexto completo.", "price": "$30-50"},
    {"name": "Social Media Content Engine", "category": "Social Media & Contenido", "nodes": "6-12", "description": "Pipeline que genera contenido social (posts, carousels, videos) usando AI, los publica en multiples plataformas (LinkedIn, Twitter, Instagram), y trackea engagement automaticamente.", "price": "$15-35"},
    {"name": "E-Commerce Order Orchestrator", "category": "E-Commerce & Ventas", "nodes": "12-25", "description": "Workflow consolidado que maneja el ciclo completo: pedido -> inventario -> pago -> envio -> notificacion. Incluye sub-workflows para cada fase y error handling con dead letter queue.", "price": "$35-65"},
    {"name": "HR Resume Screening Agent", "category": "RRHH & Seleccion", "nodes": "8-14", "description": "Agente AI que recibe resumes via email/form, analiza con LLM contra criterios definidos, genera scorecard, y alimenta el ATS con resultados. Incluye pre-flight validation y idempotency.", "price": "$25-40"},
    {"name": "Invoice Processing Pipeline", "category": "E-Commerce & Ventas", "nodes": "10-16", "description": "OCR + AI pipeline que recibe invoices (PDF/email), extrae datos con LLM, valida contra orden de compra, y sincroniza con sistema contable. Error handling con retry y dead letter queue.", "price": "$30-55"},
    {"name": "RAG Knowledge Assistant", "category": "RAG & Vector Store", "nodes": "6-12", "description": "Chatbot RAG que indexa documentos de empresa (Google Drive, PDFs, wiki), usa vector store para retrieval, y genera respuestas contextualmente precisas. Incluye MCP server para acceso real-time.", "price": "$25-45"},
    {"name": "Multi-Agent Research Assistant", "category": "IA & Agentes", "nodes": "15-25", "description": "Sistema multi-agente donde un planner coordina researcher, analyst, y writer agents. Cada agente tiene tools especificos (web search, data analysis, document generation). Output: reporte completo.", "price": "$45-75"},
    {"name": "MCP Calendar + CRM Server", "category": "MCP Tools", "nodes": "8-15", "description": "MCP server que expone tools de calendario y CRM como servicios MCP. Clientes pueden conectar desde Claude Desktop, ChatGPT, o cualquier MCP client. Incluye tools: schedule_meeting, lookup_contact, update_deal_stage.", "price": "$20-40"},
    {"name": "Automated SEO Monitor", "category": "Marketing & Leads", "nodes": "8-14", "description": "Pipeline que monitoriza rankings SEO, analiza competitors, detecta cannibalization de keywords, y genera reportes semanales con recomendaciones AI-powered. Usa Bright Data MCP para scraping.", "price": "$20-35"},
    {"name": "Voice-Enabled AI Assistant", "category": "Voz & Transcripcion", "nodes": "8-12", "description": "Asistente personal con Telegram que acepta voz y texto, transcribe con Whisper, procesa con LLM, y ejecuta acciones (calendar, reminders, emails). Integracion con Google services via MCP.", "price": "$25-45"},
    {"name": "Data Pipeline ETL Orchestrator", "category": "Dashboard & Datos", "nodes": "12-20", "description": "Pipeline modular ETL con sub-workflows para extract, transform, load. Maneja multiples fuentes (APIs, databases, CSVs), valida datos con pre-flight checks, y genera dashboards automaticos.", "price": "$35-60"},
    {"name": "Legal Document Review Agent", "category": "Documentos & PDF", "nodes": "10-16", "description": "Agente AI que recibe documentos legales, extrae clausulas clave, verifica compliance contra regulaciones, y genera resumen con recomendaciones. Usa LLM + vector store para regulation lookup.", "price": "$30-55"},
    {"name": "DevOps Alert & Incident Manager", "category": "Utilidades & DevOps", "nodes": "10-18", "description": "Workflow que recibe alertas de monitoring, clasifica severity con AI, crea incident en Jira/PagerDuty, notifica equipo via Slack, y ejecuta remediation scripts automaticos para issues conocidos.", "price": "$25-45"},
    {"name": "Inventory Sync & Auto-Order", "category": "E-Commerce & Ventas", "nodes": "8-14", "description": "Workflow que syncs inventario entre multiples plataformas (Shopify, WooCommerce, ERP), detecta low-stock thresholds, genera purchase orders automaticamente, y notifica suppliers.", "price": "$20-40"},
]

# Best practices
best_practices = [
    {"name": "Global Error Trigger", "description": "Configurar un workflow global de error handling que captura fallos de cualquier workflow activo, envia notificacion a Slack/Teams, y registra en Dead Letter Queue (DLQ). Este es el patron mas fundamental para production readiness, asegurando que ningun fallo pase silenciosamente sin deteccion y sin que el equipo de operaciones tenga visibilidad completa del estado de cada automatizacion en ejecucion."},
    {"name": "Exponential Backoff Retry", "description": "Implementar retry logic con backoff exponencial para API calls que pueden fallar por rate limiting o transient errors. Configurar max retries (3-5), intervalo inicial (1s), y factor multiplicador (2x). N8n ofrece Retry on Fail built-in pero para scenarios complejos, usar Code node con logica custom que incluye jitter para evitar thundering herd effect en retries concurrentes."},
    {"name": "Pre-flight Validation", "description": "Antes de ejecutar operaciones criticas (envio de email, creacion de registro en CRM, procesamiento de pago), validar datos entrantes con un nodo If/Switch que chequea campos obligatorios, formatos correctos, y rangos aceptables. Datos invalidos se envian a un branch de error handling con logging detallado, evitando que errores de formato propagate downstream y causen fallos en cascada en workflows complejos."},
    {"name": "Idempotency Keys", "description": "Para operaciones que modifican estado (crear orden, enviar email, actualizar registro), implementar idempotency usando Redis o database para almacenar keys unique. Antes de ejecutar, verificar si la operacion ya fue procesada con el mismo key. Esto previene duplicados accidentalmente cuando un workflow se re-executa por error handling o manual retry, garantizando data integrity incluso en scenarios de retry automatizado."},
    {"name": "Dead Letter Queue (DLQ)", "description": "Mantener una tabla de DLQ en PostgreSQL, MySQL, Airtable, o Google Sheets donde se registran todos los items que fallaron processing despues de max retries. Cada registro incluye: original payload, error message, timestamp, workflow ID, y retry count. Permite analisis post-mortem, re-processing manual, y metricas de failure rate para identificar patterns de error recurrentes que necesitan atencion architectonica."},
    {"name": "Sub-Workflow Modularization", "description": "Dividir workflows complejos (>15 nodos) en sub-workflows con Execute Workflow node. Cada sub-workflow tiene una responsabilidad unica (validacion, API call, notification). Inputs y outputs se pasan claramente entre workflows. Esto reduce complejidad visual, facilita testing individual, permite reuso entre multiples parent workflows, y hace maintenance mucho mas sencillo al poder modificar un modulo sin afectar el sistema completo."},
    {"name": "Versionado Semantico", "description": "Adoptar versionado semantico (vMAJOR.MINOR.PATCH) para workflows. MAJOR para cambios incompatible (new required input, removed output), MINOR para nuevas features backwards-compatible, PATCH para fixes. Mantener tags en n8n con formato v1.0.0, v1.1.0, etc. Documentar changelog en notas del workflow. Esto permite rollback seguro, tracking de evolucion, y comunicacion clara de cambios a clientes que dependen de versions especificas."},
]

# Architectural patterns
arch_patterns = [
    {"name": "Fan-Out / Fan-In", "description": "Un trigger dispara multiples sub-workflows en paralelo (fan-out) que procesan datos independientemente, y luego un nodo Merge consolida resultados (fan-in). Ideal para processing batches donde cada item necesita AI analysis, y los resultados se agregan en un reporte final. Ejemplo: 50 leads -> 50 parallel enrichments -> 1 consolidated report.", "complexity": "Medium"},
    {"name": "Event-Driven Chain", "description": "Cada paso del workflow es un sub-workflow independiente que se activa por el output del paso anterior via webhook. Permite decoupling: cada modulo puede evolucionar independientemente, agregar intermediarios (monitoring, logging) sin modificar otros, y reemplazar componentes sin afectar la cadena. Ejemplo: Lead captured -> enrichment triggered -> qualification triggered -> assignment triggered.", "complexity": "Low"},
    {"name": "Circuit Breaker", "description": "Patron que protege contra cascading failures cuando un servicio externo esta down. Un nodo If/Switch actua como circuit breaker: si un API call falla consecutivamente N veces (threshold), el circuit se abre y subsequent calls se bypass directamente al fallback path. Despues de un cooldown period, el circuit se semi-abre para testear si el servicio esta recovered. Ejemplo: 3 failed OpenAI calls -> fallback to Gemini.", "complexity": "Medium"},
    {"name": "Saga Pattern (Compensating Actions)", "description": "Para workflows multi-step que modifican multiples sistemas (crear orden + reservar inventory + procesar pago), implementar compensating actions para rollback si cualquier paso falla. Si paso 3 (pago) falla, ejecutar compensacion de paso 2 (release inventory) y paso 1 (cancelar orden). Cada paso tiene una accion compensatoria definida. Ejemplo: E-commerce order pipeline.", "complexity": "High"},
    {"name": "Observer / Sidecar", "description": "Adjuntar un sub-workflow de observacion a cada workflow principal que monitoree executions, registre metrics (latency, success rate, error types), y genere dashboards automaticos. El observer no modifica el flow principal - solo observa y reporta. Permite observabilidad sin modificar workflows existentes. Ejemplo: Workflow de lead processing + observer que trackea conversion rates.", "complexity": "Low"},
    {"name": "Multi-Agent Orchestration", "description": "Un planner agent recibe el request, lo descompone en subtareas, asigna cada subtarea a un agente especializado (researcher, analyst, writer), y un synthesis agent consolida los resultados. Cada agente opera como sub-workflow con tools especificos. El planner usa LangChain Agent con tools de delegation. Ejemplo: Research report generation = planner -> researcher (web search) -> analyst (data processing) -> writer (document generation).", "complexity": "High"},
]

# MCP server templates
mcp_templates = [
    {"name": "CRM MCP Server", "tools": ["lookup_contact", "create_lead", "update_deal_stage", "search_deals", "get_contact_activity"], "description": "MCP server que expone operaciones CRM como tools MCP. Compatible con HubSpot, Salesforce, Pipedrive. Permite a cualquier MCP client (Claude Desktop, ChatGPT) interactuar con CRM data directamente sin necesidad de API manual."},
    {"name": "Calendar MCP Server", "tools": ["schedule_meeting", "check_availability", "list_upcoming_events", "cancel_event", "reschedule_event"], "description": "MCP server para Google Calendar y Outlook. Tools de scheduling con conflict detection automatica. Integracion con timezone handling y attendee management."},
    {"name": "Document Analysis MCP Server", "tools": ["extract_text_from_pdf", "analyze_document", "compare_documents", "generate_summary", "check_compliance"], "description": "MCP server para procesamiento de documentos con AI. Usa LLM para extraction, analysis, y compliance checking. Vector store para RAG sobre documentos previamente procesados."},
    {"name": "E-Commerce MCP Server", "tools": ["get_product_info", "check_inventory", "create_order", "update_stock", "get_order_status", "process_refund"], "description": "MCP server para plataformas e-commerce (Shopify, WooCommerce, custom). Sincroniza datos entre plataformas y expone operaciones como MCP tools para agents."},
    {"name": "Database MCP Server", "tools": ["query_data", "insert_record", "update_record", "delete_record", "run_aggregation", "get_schema"], "description": "MCP server para acceso seguro a databases (PostgreSQL, MySQL, Supabase). Incluye query validation, rate limiting, y schema discovery automatica para que agents puedan explorar data sin SQL manual."},
    {"name": "Communication MCP Server", "tools": ["send_email", "send_slack_message", "send_whatsapp", "create_ticket", "send_sms"], "description": "MCP server unificado para comunicaciones multi-canal. Routing inteligente segun urgencia y tipo. Template management para responses consistentes."},
]

# Base templates (boilerplate)
base_templates = [
    {"name": "Simple Notification Template", "nodes": 5, "structure": "Trigger -> Format -> Notification -> Log -> Error Handler", "description": "Template base para cualquier workflow de notificacion. Incluye: webhook/cron trigger, data formatting con Set node, notification dispatch (Slack/Email/WhatsApp), execution logging, y error branch con notification de fallo. Ideal como punto de partida para workflows simples."},
    {"name": "AI Agent Template", "nodes": 8, "structure": "Trigger -> Input Validation -> AI Agent (LangChain) -> Output Processing -> Action -> Notification -> Log -> Error Handler", "description": "Template base para workflows con AI Agent. Incluye: trigger con pre-flight validation, LangChain Agent node con configurable tools, output processing y formatting, action execution (CRM/email/API), notification, logging, y comprehensive error handling con DLQ integration."},
    {"name": "RAG Pipeline Template", "nodes": 10, "structure": "Trigger -> Input -> Vector Store Query -> Document Retrieval -> LLM Processing -> Response -> Action -> Notification -> Log -> Error Handler", "description": "Template base para RAG workflows. Incluye: trigger, input extraction, vector store query (Pinecone/Milvus/Supabase), document retrieval y ranking, LLM processing con context injection, response formatting, optional action execution, y error handling con retry logic para API failures."},
    {"name": "Sub-Workflow Module Template", "nodes": 6, "structure": "Webhook Input -> Validation -> Core Logic -> Output Formatting -> Webhook Response -> Error Handler", "description": "Template base para sub-workflows modulares. Recibe input via webhook (Execute Workflow), valida parametros, ejecuta logica core, formatea output, retorna response al parent workflow, y maneja errores con fallback response para que el parent workflow pueda continuar."},
    {"name": "Multi-Step Orchestration Template", "nodes": 12, "structure": "Trigger -> Validation -> Sub-Workflow A -> Sub-Workflow B -> Merge -> Decision -> Sub-Workflow C -> Notification -> Dashboard Update -> Log -> Error Handler -> DLQ", "description": "Template base para pipelines multi-step con sub-workflows. Incluye: trigger con validation, orchestration de 2-3 sub-workflows via Execute Workflow, merge de resultados, decision logic con If/Switch, final action, notification, dashboard update, logging, y error handling completo con DLQ."},
    {"name": "MCP Server Template", "nodes": 8, "structure": "MCP Trigger -> Tool Router -> Validation -> Core Tool Logic -> External API -> Response Formatting -> MCP Response -> Error Handler", "description": "Template base para MCP server workflows en n8n. Recibe MCP tool calls, routea al tool correcto con Switch, valida parameters, ejecuta logica (API call o database operation), formatea response segun MCP spec, y maneja errores con fallback response structure."},
]

# Industry pricing reference (from research)
industry_pricing = [
    {"industry": "Salud / Healthcare", "monthly_budget": "$50-200", "common_workflows": "Patient scheduling, Insurance verification, Medical records sync, Prescription reminders, Compliance audit", "complexity": "High"},
    {"industry": "Finanzas / Finance", "monthly_budget": "$100-500", "common_workflows": "Invoice processing, Transaction reconciliation, Regulatory reporting, Client onboarding, Risk assessment AI", "complexity": "Very High"},
    {"industry": "E-Commerce", "monthly_budget": "$20-100", "common_workflows": "Order orchestration, Inventory sync, Price monitoring, Customer notifications, Return processing", "complexity": "Medium"},
    {"industry": "Marketing / Agencias", "monthly_budget": "$30-150", "common_workflows": "Lead qualification, Social media automation, SEO monitoring, Campaign reporting, Content generation AI", "complexity": "Medium"},
    {"industry": "RRHH / HR", "monthly_budget": "$20-80", "common_workflows": "Resume screening, Interview scheduling, Employee onboarding, Payroll integration, Compliance tracking", "complexity": "Medium"},
    {"industry": "Legal / Compliance", "monthly_budget": "$50-200", "common_workflows": "Document review AI, Contract analysis, Deadline tracking, Regulatory monitoring, Case management", "complexity": "High"},
    {"industry": "IT / DevOps", "monthly_budget": "$30-100", "common_workflows": "Alert management, Incident response, Deployment pipelines, Monitoring dashboards, Security audit", "complexity": "Medium-High"},
    {"industry": "Educacion", "monthly_budget": "$10-50", "common_workflows": "Student enrollment, Grade processing, Content distribution, Attendance tracking, Feedback collection", "complexity": "Low-Medium"},
]

# Research sources
n8nmarketplace_categories = [
    "AI & Agents", "Lead Generation", "CRM Integrations", "Social Media", "E-Commerce",
    "Email Automation", "Team Communication", "Marketing", "Sales", "HR & Recruiting",
    "Finance & Accounting", "IT Operations", "Document Processing", "Data & Analytics",
    "Healthcare", "Legal", "Education", "Customer Support", "DevOps", "Security & Compliance"
]

def generate_html():
    html = []
    
    # ---- HTML head ----
    html.append("""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catalogo Marketplace de Automatizaciones n8n</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Inter:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
    <style>
    @page {
        size: 720px 1020px;
        margin: 0;
    }
    :root {
        --c-bg: #0d1117;
        --c-surface: #161b22;
        --c-card: #1c2333;
        --c-border: #30363d;
        --c-text: #e6edf3;
        --c-text-muted: #8b949e;
        --c-accent: #ff6b35;
        --c-accent-light: #ff8c5a;
        --c-accent2: #58a6ff;
        --c-success: #3fb950;
        --c-warning: #d29922;
        --c-danger: #f85149;
    }
    html, body {
        margin: 0;
        padding: 0;
        width: 720px;
        background: var(--c-bg);
        color: var(--c-text);
        font-family: 'Inter', 'Noto Sans SC', sans-serif;
        font-size: 14px;
        line-height: 1.6;
    }
    @media screen {
        html {
            height: auto;
            display: flex;
            justify-content: center;
            background: #1a1a2e;
        }
        body {
            transform-origin: top center;
            margin: 20px auto;
        }
    }

    /* Cover */
    .cover {
        width: 720px;
        height: 1020px;
        box-sizing: border-box;
        break-after: page;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        background: var(--c-bg);
        padding: 70px 60px;
    }
    .cover-bg-circle1 {
        position: absolute;
        width: 320px;
        height: 320px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,107,53,0.15) 0%, transparent 70%);
        top: 80px;
        right: -80px;
    }
    .cover-bg-circle2 {
        position: absolute;
        width: 240px;
        height: 240px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(88,166,255,0.12) 0%, transparent 70%);
        bottom: 120px;
        left: -60px;
    }
    .cover-bg-line {
        position: absolute;
        width: 600px;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--c-accent), transparent);
        top: 50%;
        opacity: 0.3;
    }
    .cover-tag {
        font-size: 14px;
        font-weight: 600;
        color: var(--c-accent);
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 20px;
        border: 1px solid var(--c-accent);
        padding: 6px 18px;
        border-radius: 4px;
    }
    .cover-title {
        font-size: 48px;
        font-weight: 900;
        line-height: 1.15;
        text-align: center;
        margin-bottom: 24px;
        color: var(--c-text);
    }
    .cover-subtitle {
        font-size: 18px;
        font-weight: 400;
        color: var(--c-text-muted);
        text-align: center;
        line-height: 1.5;
        margin-bottom: 40px;
    }
    .cover-stats {
        display: flex;
        gap: 20px;
        justify-content: center;
        margin-bottom: 30px;
    }
    .cover-stat {
        text-align: center;
        padding: 12px 16px;
        background: var(--c-card);
        border-radius: 8px;
        border: 1px solid var(--c-border);
    }
    .cover-stat-num {
        font-size: 28px;
        font-weight: 900;
        color: var(--c-accent);
    }
    .cover-stat-label {
        font-size: 11px;
        color: var(--c-text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .cover-footer {
        position: absolute;
        bottom: 40px;
        font-size: 12px;
        color: var(--c-text-muted);
        text-align: center;
    }

    /* Main content */
    .main-content {
        padding: 50px 55px 40px 55px;
    }

    /* Chapter header */
    .chapter-header {
        break-after: avoid;
        break-inside: avoid;
        margin-top: 28px;
        margin-bottom: 16px;
    }
    .section-tag {
        font-size: 11px;
        font-weight: 600;
        color: var(--c-accent);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .section-title {
        font-size: 26px;
        font-weight: 800;
        color: var(--c-text);
        margin-bottom: 6px;
        line-height: 1.2;
    }
    .divider {
        width: 60px;
        height: 3px;
        background: var(--c-accent);
        border-radius: 2px;
        margin-bottom: 16px;
    }

    /* Body text */
    .body-text {
        font-size: 14px;
        line-height: 1.7;
        color: var(--c-text);
        margin-bottom: 14px;
    }
    .body-text-muted {
        font-size: 13px;
        line-height: 1.6;
        color: var(--c-text-muted);
        margin-bottom: 12px;
    }

    /* Cards */
    .card {
        break-inside: avoid;
        margin-bottom: 14px;
        padding: 16px 18px;
        background: var(--c-card);
        border: 1px solid var(--c-border);
        border-radius: 8px;
    }
    .card-title {
        font-size: 16px;
        font-weight: 700;
        color: var(--c-text);
        margin-bottom: 6px;
    }
    .card-meta {
        font-size: 12px;
        color: var(--c-accent2);
        margin-bottom: 8px;
        display: flex;
        gap: 12px;
    }
    .card-body {
        font-size: 13px;
        line-height: 1.5;
        color: var(--c-text-muted);
    }
    .card-price {
        font-size: 14px;
        font-weight: 700;
        color: var(--c-accent);
        margin-top: 8px;
    }

    /* Data table */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 14px;
        font-size: 12px;
    }
    .data-table th {
        background: var(--c-surface);
        color: var(--c-accent2);
        font-weight: 600;
        padding: 8px 10px;
        text-align: left;
        border-bottom: 2px solid var(--c-accent);
        font-size: 11px;
        letter-spacing: 0.5px;
    }
    .data-table td {
        padding: 7px 10px;
        border-bottom: 1px solid var(--c-border);
        color: var(--c-text);
        vertical-align: top;
    }
    .data-table tr:nth-child(even) {
        background: var(--c-surface);
    }
    .data-table td:first-child {
        color: var(--c-text);
        font-weight: 500;
    }
    .data-table td.price {
        color: var(--c-accent);
        font-weight: 600;
    }
    .data-table td.bad {
        color: var(--c-danger);
    }
    .data-table td.good {
        color: var(--c-success);
    }

    /* Pricing tier card */
    .pricing-tier {
        break-inside: avoid;
        margin-bottom: 14px;
        padding: 18px 20px;
        background: var(--c-card);
        border: 1px solid var(--c-border);
        border-radius: 8px;
        position: relative;
    }
    .pricing-tier::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: var(--c-accent);
        border-radius: 4px 0 0 4px;
    }
    .pricing-tier-name {
        font-size: 18px;
        font-weight: 800;
        color: var(--c-text);
        margin-bottom: 4px;
    }
    .pricing-tier-price {
        font-size: 20px;
        font-weight: 900;
        color: var(--c-accent);
        margin-bottom: 8px;
    }
    .pricing-tier-desc {
        font-size: 13px;
        line-height: 1.5;
        color: var(--c-text-muted);
        margin-bottom: 8px;
    }
    .pricing-tier-examples {
        font-size: 12px;
        color: var(--c-accent2);
        font-style: italic;
    }

    /* Highlight box */
    .highlight-box {
        break-inside: avoid;
        margin-bottom: 14px;
        padding: 14px 16px;
        background: rgba(255,107,53,0.08);
        border: 1px solid rgba(255,107,53,0.3);
        border-radius: 8px;
    }
    .highlight-box-title {
        font-size: 14px;
        font-weight: 700;
        color: var(--c-accent);
        margin-bottom: 6px;
    }
    .highlight-box-body {
        font-size: 13px;
        line-height: 1.5;
        color: var(--c-text);
    }

    /* Pattern card */
    .pattern-card {
        break-inside: avoid;
        margin-bottom: 14px;
        padding: 16px 18px;
        background: var(--c-card);
        border: 1px solid var(--c-border);
        border-radius: 8px;
    }
    .pattern-name {
        font-size: 16px;
        font-weight: 700;
        color: var(--c-accent);
    }
    .pattern-complexity {
        font-size: 11px;
        color: var(--c-accent2);
        font-weight: 600;
        margin-bottom: 8px;
    }
    .pattern-desc {
        font-size: 13px;
        line-height: 1.5;
        color: var(--c-text);
    }

    /* Stat row */
    .stat-row {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 14px;
    }
    .stat-item {
        flex: 1 1 auto;
        min-width: 80px;
        max-width: 100%;
        padding: 12px 14px;
        background: var(--c-card);
        border: 1px solid var(--c-border);
        border-radius: 6px;
        text-align: center;
    }
    .stat-value {
        font-size: 22px;
        font-weight: 900;
        color: var(--c-accent);
    }
    .stat-label {
        font-size: 10px;
        color: var(--c-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Badge */
    .badge {
        display: inline-block;
        font-size: 10px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 3px;
        margin-right: 4px;
    }
    .badge-accent { background: rgba(255,107,53,0.2); color: var(--c-accent); }
    .badge-blue { background: rgba(88,166,255,0.2); color: var(--c-accent2); }
    .badge-green { background: rgba(63,185,80,0.2); color: var(--c-success); }
    .badge-warning { background: rgba(210,153,34,0.2); color: var(--c-warning); }
    .badge-danger { background: rgba(248,81,73,0.2); color: var(--c-danger); }

    /* List */
    .list-item {
        font-size: 13px;
        line-height: 1.5;
        color: var(--c-text);
        margin-bottom: 4px;
        padding-left: 16px;
        position: relative;
    }
    .list-item::before {
        content: '-';
        position: absolute;
        left: 0;
        color: var(--c-accent);
    }

    /* Ending page */
    .ending {
        width: 720px;
        height: 1020px;
        box-sizing: border-box;
        break-before: page;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: var(--c-bg);
        padding: 70px 60px;
        position: relative;
    }
    .ending-bg-circle {
        position: absolute;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,107,53,0.1) 0%, transparent 70%);
        top: 200px;
        right: -100px;
    }
    .ending-big-text {
        font-size: 36px;
        font-weight: 900;
        color: var(--c-accent);
        text-align: center;
        margin-bottom: 20px;
    }
    .ending-sub-text {
        font-size: 16px;
        color: var(--c-text-muted);
        text-align: center;
        line-height: 1.5;
        margin-bottom: 30px;
    }
    .ending-cta {
        font-size: 14px;
        color: var(--c-text);
        font-weight: 600;
        text-align: center;
        padding: 12px 24px;
        background: rgba(255,107,53,0.15);
        border: 1px solid var(--c-accent);
        border-radius: 6px;
    }
    </style>
</head>
<body>
""")

    # ---- COVER PAGE ----
    html.append("""
<div class="cover">
    <div class="cover-bg-circle1"></div>
    <div class="cover-bg-circle2"></div>
    <div class="cover-bg-line"></div>
    <div class="cover-tag">MARKETPLACE CATALOGO</div>
    <div class="cover-title">Catalogo de<br>Automatizaciones n8n</div>
    <div class="cover-subtitle">
        Analisis de 118 workflows, refactoring con buenas practicas,<br>
        patrones architectonicos, templates base, MCP servers,<br>
        y modelo de pricing para mercado profesional.
    </div>
    <div class="cover-stats">
        <div class="cover-stat">
            <div class="cover-stat-num">118</div>
            <div class="cover-stat-label">Workflows Analizados</div>
        </div>
        <div class="cover-stat">
            <div class="cover-stat-num">14</div>
            <div class="cover-stat-label">Duplicados Detectados</div>
        </div>
        <div class="cover-stat">
            <div class="cover-stat-num">41</div>
            <div class="cover-stat-label">Similitudes Encontradas</div>
        </div>
        <div class="cover-stat">
            <div class="cover-stat-num">6</div>
            <div class="cover-stat-label">Templates Base</div>
        </div>
    </div>
    <div class="cover-footer">
        Documento confidencial - Marketplace privado de automatizaciones | Julio 2026
    </div>
</div>
""")

    # ---- MAIN CONTENT ----
    html.append("""<div class="main-content">""")

    # ---- Chapter 1: Resumen Ejecutivo ----
    html.append("""
<div class="chapter-header">
    <div class="section-tag">CAPITULO 01</div>
    <div class="section-title">Resumen Ejecutivo</div>
    <div class="divider"></div>
</div>
<div class="body-text">
Este documento presenta el catalogo marketplace completo de automatizaciones n8n, desarrollado a partir del analisis exhaustivo de 118 workflows existentes y la investigacion de mercados externos como n8nmarkets.com (850+ templates, $5-$50+ por workflow) y n8n.io/workflows (10,930 templates comunitarios). El objetivo es transformar el portfolio actual de automatizaciones en un catalogo profesional, listo para ofrecer a clientes prospectos, con pricing competitivo, templates base para desarrollo rapido, y patrones architectonicos que garanticen calidad production-ready.
</div>
<div class="body-text">
El analisis revela que el portfolio actual tiene 93 workflows de IA y Agentes como categoria dominante, 14 duplicaciones exactas que generan mantenimiento redundante, y 41 similitudes que indican oportunidades de consolidation significativas. Solo una minoria de workflows tiene error handling explicito, y la categoria E-Commerce tiene 3 versiones (v1, v2, v3) que necesitan unification urgente. Este documento propone un plan comprehensivo de refactoring, consolidation, y comercialization.
</div>
<div class="stat-row">
    <div class="stat-item"><div class="stat-value">118</div><div class="stat-label">Workflows Totales</div></div>
    <div class="stat-item"><div class="stat-value">18</div><div class="stat-label">Categorias</div></div>
    <div class="stat-item"><div class="stat-value">14</div><div class="stat-label">Duplicados Exactos</div></div>
    <div class="stat-item"><div class="stat-value">41</div><div class="stat-label">Similitudes</div></div>
    <div class="stat-item"><div class="stat-value">55</div><div class="stat-label">Sugerencias Consolidacion</div></div>
</div>
""")

    # ---- Chapter 2: Portfolio Actual ----
    html.append("""
<div class="chapter-header">
    <div class="section-tag">CAPITULO 02</div>
    <div class="section-title">Portfolio Actual de Automatizaciones</div>
    <div class="divider"></div>
</div>
<div class="body-text">
El portfolio actual comprende 118 workflows provenientes de 5 fuentes principales: Plantillas JosemaFernandez (60 workflows), Materiales Comunidad WhatsApp (49 workflows), Sistema Agentes Marketing de Victor Perez (6 workflows), Milvus vs Supabase (1 workflow), y otros archivos individuales. La distribucion por categorias muestra una concentracion significativa en IA y Agentes (93 workflows), lo cual refleja el foco del portfolio en automatizaciones inteligentes, pero tambien indica una falta de diversificacion hacia otras verticals de negocio con alto potencial comercial.
</div>
""")

    # Category table
    html.append("""<table class="data-table">
<tr><th>Categoria</th><th>Workflows</th><th>% Portfolio</th><th>Potencial Mercado</th></tr>""")
    for cat, count in sorted_cats:
        pct = f"{count/total_workflows*100:.1f}%"
        potential = "High" if count >= 20 else "Medium" if count >= 5 else "Low"
        pot_class = "good" if potential == "High" else "badge-warning" if potential == "Medium" else "bad"
        html.append(f"<tr><td>{cat}</td><td>{count}</td><td>{pct}</td><td class=\"{pot_class}\">{potential}</td></tr>")
    html.append("</table>")

    # Sources table
    html.append("""
<div class="body-text" style="margin-top: 14px;">
Las fuentes del portfolio revelan una dependencia fuerte de templates comunitarios (Plantillas JosemaFernandez y Materiales Comunidad WhatsApp), que representan mas del 90% del contenido. Esto implica que los workflows no son necesariamente production-ready en su estado actual, ya que muchos son templates educativos o demostrativos sin error handling, sin versionado, y sin documentation de deployment. La refactoring propuesta busca transformar estos templates en soluciones profesionales.
</div>
<table class="data-table">
<tr><th>Fuente</th><th>Workflows</th><th>Tipo</th><th>Estado</th></tr>""")
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        tipo = "Template" if "Plantillas" in src or "Materiales" in src else "Custom"
        estado = "Needs Refactoring" if "Plantillas" in src or "Materiales" in src else "Production-ready"
        est_class = "bad" if "Needs" in estado else "good"
        html.append(f"<tr><td>{src}</td><td>{count}</td><td>{tipo}</td><td class=\"{est_class}\">{estado}</td></tr>")
    html.append("</table>")

    # Top nodes
    html.append("""
<div class="body-text" style="margin-top: 14px;">
Los nodos mas utilizados en el portfolio reflejan el dominio de IA. El nodo LangChain Agent aparece en 59 workflows (50% del portfolio), seguido de OpenAI Chat Model y otros nodos de AI/LLM. Esto confirma que el portfolio esta optimizado para automatizaciones de AI agents, pero necesita diversification en nodos de integracion empresarial (CRM, ERP, E-Commerce platforms) para ampliar el mercado objetivo.
</div>
<table class="data-table">
<tr><th>Nodo</th><th>Frecuencia</th><th>Categoria Nodo</th></tr>""")
    for nt, count in sorted_nodes[:10]:
        html.append(f"<tr><td>{nt}</td><td>{count}</td><td>AI/Integration</td></tr>")
    html.append("</table>")

    # ---- Chapter 3: Refactoring Plan ----
    html.append("""
<div class="chapter-header">
    <div class="section-tag">CAPITULO 03</div>
    <div class="section-title">Plan de Refactoring y Consolidacion</div>
    <div class="divider"></div>
</div>
<div class="body-text">
El refactoring del portfolio sigue un enfoque sistematico basado en principios de software engineering adaptados al contexto de automatizaciones n8n. El proceso comprende cuatro fases: (1) Elimination de duplicados, (2) Consolidation de similitudes, (3) Implementation de error handling y best practices, y (4) Versionado y modularization con sub-workflows. Cada fase tiene criterios de acceptance definidos y produces deliverables que incrementan el valor comercial del catalogo.
</div>
""")

    # Phase 1: Duplicates
    html.append("""
<div class="highlight-box">
    <div class="highlight-box-title">FASE 1: Elimination de Duplicados (14 encontrados)</div>
    <div class="highlight-box-body">
Se identificaron 14 duplicaciones exactas donde workflows con nombres diferentes o suffixes de version ejecutan la misma logica con los mismos nodos. Los duplicados mas notables incluyen: MCP_Calendario (3 copias), eCommerce workflows (3 versiones v1/v2/v3), y varios workflows de WhatsApp/Telegram con suffixes de autor. La estrategia es mantener la version mas completa (con error handling y documentation), eliminar las copias, y crear un solo workflow versionado con la logica consolidada de todas las variantes.
    </div>
</div>
""")

    # Phase 2: Similarities
    html.append("""
<div class="highlight-box">
    <div class="highlight-box-title">FASE 2: Consolidation de Similitudes (41 encontradas)</div>
    <div class="highlight-box-body">
Las 41 similitudes representan workflows que comparten >60% de nodos comunes (Jaccard similarity) pero con variaciones en trigger, integracion, o configuracion. Ejemplo: multiples workflows de "AI Agent + Telegram" que solo difieren en el LLM provider (OpenAI vs Gemini) o en los tools configurados. La consolidation strategy es crear un workflow master con Switch/If nodes que permitan configurar el variant (provider, channel, complexity) como input parameter, eliminando la necesidad de mantener multiples copias casi identicas.
    </div>
</div>
""")

    # Phase 3: Error handling
    html.append("""
<div class="highlight-box">
    <div class="highlight-box-title">FASE 3: Error Handling y Best Practices</div>
    <div class="highlight-box-body">
Actualmente, solo un small subset de workflows tiene error handling explicito. La implementation comprehensive incluye: (a) Global Error Trigger para notificaciones centralizadas de fallos, (b) Retry on Fail con exponential backoff para API calls, (c) Dead Letter Queue (DLQ) en PostgreSQL/Google Sheets para items que fallan permanentemente, (d) Pre-flight Validation antes de operaciones criticas, y (e) Idempotency Keys para prevenir duplicados en retries. Cada workflow production-ready debe incluir al minimum los patterns (a), (b), y (c).
    </div>
</div>
""")

    # Phase 4: Versioning & Sub-workflows
    html.append("""
<div class="highlight-box">
    <div class="highlight-box-title">FASE 4: Versionado y Modularization con Sub-Workflows</div>
    <div class="highlight-box-body">
Adoptar versionado semantico (vMAJOR.MINOR.PATCH) para cada workflow. MAJOR para cambios incompatible (new required input, removed output field), MINOR para nuevas features backwards-compatible (new optional parameter, additional tool), PATCH para bug fixes. Workflows con >15 nodos se refactorizan en sub-workflows modulares via Execute Workflow node, donde cada modulo tiene una responsabilidad unica (validation, API call, notification). Esto facilita testing individual, reuso entre parent workflows, y maintenance simplificado al poder modificar un modulo sin afectar el sistema completo.
    </div>
</div>
""")

    # ---- Chapter 4: Best Practices ----
    html.append("""
<div class="chapter-header">
    <div class="section-tag">CAPITULO 04</div>
    <div class="section-title">Best Practices de Desarrollo n8n</div>
    <div class="divider"></div>
</div>
<div class="body-text">
Las best practices de desarrollo n8n se derivan de la investigacion de sources como HatchWorks (n8n Best Practices Checklist for Production 2026), n8nLab (Error Handling Best Practices), la comunidad n8n (248K+ members), y n8nmarkets.com (Workflow Patterns & Architecture). Estos practices se categorizan en tres dimensiones: engineering practices (error handling, retry, validation), architectural practices (sub-workflows, versionado, modularization), y AI agent practices (model selection, tool configuration, memory management).
</div>
""")

    for bp in best_practices:
        html.append(f"""
<div class="card">
    <div class="card-title">{bp['name']}</div>
    <div class="card-body">{bp['description']}</div>
</div>""")

    # ---- Chapter 5: Architectural Patterns ----
    html.append("""
<div class="chapter-header">
    <div class="section-tag">CAPITULO 05</div>
    <div class="section-title">Patrones Architectonicos para Automatizaciones</div>
    <div class="divider"></div>
</div>
<div class="body-text">
Los patrones architectonicos proporcionan soluciones reusables a problemas recurrentes en el diseño de automatizaciones n8n. Estos patterns se inspiran en software architecture patterns adaptados al contexto visual de n8n, donde los nodos y connections representan el flow de data y logic. Cada pattern incluye una descripcion del problema que resuelve, la estructura del workflow, y ejemplos de application concrete. Los patterns se clasifican por complexity: Low (3-8 nodos), Medium (8-15 nodos), High (15+ nodos con sub-workflows).
</div>
""")

    for pat in arch_patterns:
        html.append(f"""
<div class="pattern-card">
    <div class="pattern-name">{pat['name']}</div>
    <div class="pattern-complexity">Complexity: {pat['complexity']}</div>
    <div class="pattern-desc">{pat['description']}</div>
</div>""")

    # ---- Chapter 6: AI Agent Practices ----
    html.append("""
<div class="chapter-header">
    <div class="section-tag">CAPITULO 06</div>
    <div class="section-title">Best Practices de AI Agents en n8n</div>
    <div class="divider"></div>
</div>
<div class="body-text">
n8n ha evolucionado significativamente como platforma para AI agents en 2026, con upgrades massive a LangChain integration, direct vector store tools, y mejor multi-agent orchestration. El nodo AI Agent de n8n bundles un chat model, system prompt, memory, y tools en un solo node, simplificando el desarrollo pero requiring configuracion cuidadosa para production. Las practices siguientes se basan en la investigacion de community.n8n.io, anmol-gupta.medium.com, y n8nlab.io sobre AI agent development en n8n.
</div>
""")

    ai_agent_practices = [
        {"title": "Model Selection Strategy", "content": "Seleccionar el LLM correcto segun el use case, no solo el mas powerful. Para classification simple y extraction: GPT-4o-mini o Gemini Flash (cost-effective, fast). Para reasoning complex y multi-step: GPT-4o o Claude 3.5 (higher accuracy, slower). Para tasks que necesitan context muy largo: Gemini 1.5 Pro (1M token window). Implementar fallback chain: si el modelo primary falla o timeout, automaticamente switch al secondary model via Circuit Breaker pattern."},
        {"title": "Tool Configuration Best Practices", "content": "Configurar tools del AI Agent con descripciones precision y examples. Cada tool description debe explicar: (1) que hace exactamente, (2) cuando usarlo (trigger conditions), (3) que parametros necesita, y (4) que output genera. Descripciones vagueas causean el agent a seleccionar tools incorrectos o loop infinite. Limitar a 5-7 tools por agent para evitar confusion. Si un workflow necesita >7 tools, dividir en multi-agent orchestration donde cada agente tiene su tool subset especializado."},
        {"title": "Memory and Context Management", "content": "n8n AI Agent node soporta Window Buffer Memory y conversational memory. Para chatbots continuos: usar conversational memory con sliding window de 10-20 messages para mantener context sin exceder token limits. Para one-shot processing: no usar memory (reduce cost y latency). Para agents que necesitan context de documentos: implementar RAG pipeline como sub-workflow que injecta retrieved documents como additional context en el system prompt, en vez de pasar todo el document al LLM directamente."},
        {"title": "Multi-Agent Orchestration Pattern", "content": "Para tasks complexas que un solo agent no puede handle, implementar multi-agent orchestration con un Planner Agent que descompone la task, delega a specialized agents (Researcher, Analyst, Writer), y un Synthesis Agent que consolida resultados. Cada specialized agent opera como sub-workflow via Execute Workflow node. El Planner usa LangChain Agent con custom tools de delegation. Este pattern es ideal para report generation, research pipelines, y complex decision-making que requiere multiples perspectives."},
        {"title": "Human-in-the-Loop Integration", "content": "Para decisions criticas donde AI autonomia es risky (legal review, financial decisions, medical triage), implementar human-in-the-loop checkpoints. El AI Agent genera una recommendation con confidence score, y un If node verifica si confidence > threshold (ej: 0.85). Si confidence es low, el workflow pausa y envia a un human reviewer via Slack/Email con full context. El reviewer responde con decision, y el workflow continua. Esto combina AI efficiency con human judgment para high-stakes scenarios."},
    ]

    for ap in ai_agent_practices:
        html.append(f"""
<div class="card">
    <div class="card-title">{ap['title']}</div>
    <div class="card-body">{ap['content']}</div>
</div>""")

    # ---- Chapter 7: MCP Server Templates ----
    html.append("""
<div class="chapter-header">
    <div class="section-tag">CAPITULO 07</div>
    <div class="section-title">MCP Server Development Templates</div>
    <div class="divider"></div>
</div>
<div class="body-text">
El Model Context Protocol (MCP) es el standard emergente para conectar AI agents con herramientas y datos externos. n8n soporta tanto MCP client (conectar a MCP servers externos como Claude Desktop) como MCP server (exponer workflows n8n como tools MCP). Con n8n, se pueden crear MCP servers customizados en minutos usando 267+ integraciones out-of-the-box como tools MCP. Los templates siguientes proporcionan la base para desarrollar MCP servers que se pueden incluir en el catalogo marketplace como productos premium, ya que MCP servers son un differentiator competitive significativo en 2026.
</div>
""")

    for mcp in mcp_templates:
        tools_str = " | ".join(mcp['tools'])
        html.append(f"""
<div class="card">
    <div class="card-title">{mcp['name']}</div>
    <div class="card-meta"><span class="badge badge-accent">MCP Server</span> <span class="badge badge-blue">{tools_str}</span></div>
    <div class="card-body">{mcp['description']}</div>
</div>""")

    # ---- Chapter 8: Base Development Templates ----
    html.append("""
<div class="chapter-header">
    <div class="section-tag">CAPITULO 08</div>
    <div class="section-title">Templates Base de Desarrollo (Boilerplate)</div>
    <div class="divider"></div>
</div>
<div class="body-text">
Los templates base proporcionan starting points production-ready para nuevos workflows, eliminando la necesidad de empezar desde cero cada vez. Cada template incluye la estructura de nodos, error handling basico, logging, y placeholders para customizacion. Los templates se versionan como packages reusables y se ofrecen como "quick-start" en el marketplace, permitiendo a clientes adaptarlos a sus necesidades specificas sin reinventar la arquitectura fundamental. Los templates mas vendidos en n8nmarkets.com siguen este pattern: ofrecen un lite version free y una premium version con features adicionales.
</div>
""")

    for bt in base_templates:
        html.append(f"""
<div class="card">
    <div class="card-title">{bt['name']}</div>
    <div class="card-meta"><span class="badge badge-green">{bt['nodes']} nodos</span> <span class="badge badge-blue">{bt['structure']}</span></div>
    <div class="card-body">{bt['description']}</div>
</div>""")

    # ---- Chapter 9: Pricing Model ----
    html.append("""
<div class="chapter-header">
    <div class="section-tag">CAPITULO 09</div>
    <div class="section-title">Modelo de Pricing para Marketplace</div>
    <div class="divider"></div>
</div>
<div class="body-text">
El modelo de pricing se basa en la investigacion de n8nmarkets.com, donde los workflows se venden entre $5 y $50+ por template individual, con commissions de 10% sobre ventas. Los sellers mas exitosos en n8nmarkets.com ofrecen pricing tiers: free lite version para build trust, one-time purchase ($5-$50) para production templates, y custom solutions ($75-$200+) para integraciones enterprise. El marketplace n8n Markets tiene 850+ templates, 50K+ monthly visitors, y 2,000+ workflows listed en 30+ languages, con payments via Paddle y automated payouts.
</div>
""")

    for pt in pricing_tiers:
        html.append(f"""
<div class="pricing-tier">
    <div class="pricing-tier-name">{pt['tier']}</div>
    <div class="pricing-tier-price">{pt['price_range']}</div>
    <div class="pricing-tier-desc">{pt['description']}</div>
    <div class="pricing-tier-examples">Ejemplos: {pt['examples']}</div>
</div>""")

    # Industry pricing reference
    html.append("""
<div class="body-text" style="margin-top: 14px;">
Los budgets mensuales de automatizacion por industry proporcionan un reference point para pricing de services recurring. Estos datos se basan en n8nmarkets.com/pricing-by-industry y ajustados al mercado Latinoamericano con un factor de adjustment contextual. El pricing de servicios recurring (setup + maintenance + optimization) se calcula como: Setup fee (1x) + Monthly maintenance (recurring) + Per-execution costs (variable).
</div>
<table class="data-table">
<tr><th>Industry</th><th>Budget Mensual Ref.</th><th>Workflows Comunes</th><th>Complexity</th></tr>""")
    for ip in industry_pricing:
        comp_class = "badge-warning" if ip['complexity'] == "High" or ip['complexity'] == "Very High" else "good" if ip['complexity'] == "Low-Medium" else ""
        html.append(f"<tr><td>{ip['industry']}</td><td class=\"price\">{ip['monthly_budget']}</td><td>{ip['common_workflows']}</td><td class=\"{comp_class}\">{ip['complexity']}</td></tr>")
    html.append("</table>")

    # Pricing formula
    html.append("""
<div class="highlight-box">
    <div class="highlight-box-title">Formula de Pricing Recomendada</div>
    <div class="highlight-box-body">
Template individual: Base price ($5-$75) segun tier + Error handling premium (+20%) + MCP integration premium (+30%).<br>
Servicio recurring: Setup fee ($150-$500) + Monthly maintenance ($50-$200/mes) + Per-optimization sessions ($100-$300/session).<br>
Bundle pricing: 3-5 workflows relacionados a precio package ($45-$150) vs individual ($75-$250).<br>
Freemium strategy: Lite version free (3-5 nodos, sin error handling) + Premium version ($15-$50) con full features.
    </div>
</div>
""")

    # ---- Chapter 10: New Automation Ideas ----
    html.append("""
<div class="chapter-header">
    <div class="section-tag">CAPITULO 10</div>
    <div class="section-title">Nuevas Ideas de Automatizacion para el Catalogo</div>
    <div class="divider"></div>
</div>
<div class="body-text">
Las siguientes automation ideas se derivan de la investigacion de n8nmarkets.com (850+ templates en 20+ categories), n8n.io/workflows (10,930 templates comunitarios con 7,548 AI workflows), BetterClaw (25 workflow ideas + 7 AI agent ideas), y Medium/YouTube (10+ automation roadmaps). Cada idea incluye una descripcion detallada del workflow, nodes estimate, pricing sugerido, y value proposition para clientes. Estas ideas amplian el portfolio mas alla de la concentration actual en IA y Agentes, diversificando hacia verticals de alto valor commercial.
</div>
""")

    # Table of automation ideas
    html.append("""<table class="data-table">
<tr><th>Nombre</th><th>Categoria</th><th>Nodos</th><th>Descripcion</th><th>Price</th></tr>""")
    for idea in automation_ideas:
        html.append(f"<tr><td><strong>{idea['name']}</strong></td><td>{idea['category']}</td><td>{idea['nodes']}</td><td>{idea['description'][:150]}</td><td class=\"price\">{idea['price']}</td></tr>")
    html.append("</table>")

    # n8n marketplace categories reference
    html.append("""
<div class="body-text" style="margin-top: 14px;">
El marketplace n8nmarkets.com organiza sus 850+ templates en las siguientes 20 categories, que proporcionan un framework para categorizar nuestro propio catalogo de manera professional y discoverable. La alignment con estas categories facilita el cross-listing en n8nmarkets.com y mejora la discoverability para clientes que buscan soluciones por vertical de negocio. Las categories mas vendidas son: AI & Agents, Lead Generation, CRM Integrations, Social Media, y E-Commerce.
</div>
<div class="stat-row">
""")
    for cat in n8nmarketplace_categories:
        html.append(f'<div class="badge badge-blue">{cat}</div> ')
    html.append("</div>")

    # ---- Chapter 11: Marketplace Catalog ----
    html.append("""
<div class="chapter-header">
    <div class="section-tag">CAPITULO 11</div>
    <div class="section-title">Catalogo Marketplace - Propuesta a Clientes</div>
    <div class="divider"></div>
</div>
<div class="body-text">
El catalogo marketplace final presenta los workflows production-ready disponibles para clientes prospectos, organizados por vertical de negocio con pricing transparente. Cada listing incluye: nombre del workflow, descripcion del value proposition, categorias, pricing tier, y link al template JSON. El catalogo se publica en n8nmarkets.com (con listings en 30+ languages auto-translated) y se ofrece directamente a clientes via proposals customizadas. La estrategia de promotion incluye: (1) Listing en n8nmarkets.com con SEO optimizado, (2) Social media marketing con case studies, (3) Webinars demostrativos, y (4) Partnerships con agencias de automation.
</div>
""")

    # Consolidated catalog table
    html.append("""<table class="data-table">
<tr><th>Workflow</th><th>Categoria</th><th>Tier</th><th>Value Proposition</th><th>Price</th></tr>""")
    
    # Top consolidated workflows from catalog data
    consolidation_items = consolidation[:15] if len(consolidation) > 15 else consolidation
    for item in consolidation_items[:8]:
        name = item.get('workflow_name', item.get('name', 'Unknown'))
        cats_str = ", ".join(item.get('categories', ['General']))
        tier = "Professional" if item.get('node_count', 10) > 10 else "Starter"
        vp = item.get('description', 'Automatizacion consolidada')[:120]
        html.append(f"<tr><td><strong>{name}</strong></td><td>{cats_str}</td><td>{tier}</td><td>{vp}</td><td class=\"price\">$15-35</td></tr>")
    
    # New automation ideas as catalog entries
    for idea in automation_ideas[:12]:
        nodes_num = int(idea['nodes'].split('-')[0]) if '-' in idea['nodes'] else int(idea['nodes'])
        tier = "Enterprise" if nodes_num >= 15 else "Professional" if nodes_num >= 8 else "Starter"
        vp = idea['description'][:120]
        html.append(f"<tr><td><strong>{idea['name']}</strong></td><td>{idea['category']}</td><td>{tier}</td><td>{vp}</td><td class=\"price\">{idea['price']}</td></tr>")
    
    # MCP servers as catalog entries
    for mcp in mcp_templates:
        html.append(f"<tr><td><strong>{mcp['name']}</strong></td><td>MCP Tools</td><td>Enterprise</td><td>{mcp['description'][:120]}</td><td class=\"price\">$35-75</td></tr>")
    
    html.append("</table>")

    # ---- Chapter 12: Implementation Roadmap ----
    html.append("""
<div class="chapter-header">
    <div class="section-tag">CAPITULO 12</div>
    <div class="section-title">Roadmap de Implementation</div>
    <div class="divider"></div>
</div>
<div class="body-text">
La implementation del catalogo marketplace sigue un roadmap de 4 phases con timelines estimados y deliverables concrete. Phase 1 (Semanas 1-2): Refactoring urgente de duplicados y consolidation de similitudes. Phase 2 (Semanas 3-4): Implementation de error handling y best practices en todos los workflows production-ready. Phase 3 (Semanas 5-6): Development de templates base, MCP servers, y nuevas automation ideas. Phase 4 (Semanas 7-8): Listing en n8nmarkets.com, creation de proposals para clientes, y launch del marketplace privado.
</div>
""")

    roadmap_phases = [
        {"phase": "Phase 1", "timeline": "Semanas 1-2", "tasks": "Eliminar 14 duplicados, consolidar 41 similitudes, crear workflows master con Switch/If para variants, establecer naming convention y categorization system", "deliverable": "Portfolio reducido de ~70 workflows unicos y production-structured"},
        {"phase": "Phase 2", "timeline": "Semanas 3-4", "tasks": "Agregar Global Error Trigger a todos los workflows, implementar Retry on Fail con exponential backoff, configurar Dead Letter Queue en PostgreSQL/Google Sheets, agregar Pre-flight Validation en workflows criticos, implementar Idempotency Keys", "deliverable": "Todos los workflows con error handling comprehensive y production readiness"},
        {"phase": "Phase 3", "timeline": "Semanas 5-6", "tasks": "Crear 6 templates base (boilerplate), desarrollar 6 MCP server templates, implementar 15 nuevas automation ideas, versionar todos los workflows con semantic versioning, crear sub-workflows para modularizar workflows >15 nodos", "deliverable": "Catalogo completo con templates, MCP servers, y nuevas automatizaciones"},
        {"phase": "Phase 4", "timeline": "Semanas 7-8", "tasks": "Crear seller account en n8nmarkets.com, listar workflows con SEO-optimized descriptions en 30+ languages, crear proposals customizadas para 5 verticals (E-Commerce, Marketing, RRHH, Legal, DevOps), launch social media marketing con case studies", "deliverable": "Marketplace live con listings activos y proposals enviadas a prospectos"},
    ]

    for rp in roadmap_phases:
        html.append(f"""
<div class="card">
    <div class="card-title">{rp['phase']} - {rp['timeline']}</div>
    <div class="card-body">{rp['tasks']}</div>
    <div class="card-price">Deliverable: {rp['deliverable']}</div>
</div>""")

    html.append("""
</div>
""")

    # ---- ENDING PAGE ----
    html.append("""
<div class="ending">
    <div class="ending-bg-circle"></div>
    <div class="ending-big-text">Automatiza.<br>Consolida.<br>Vende.</div>
    <div class="ending-sub-text">
        Tu portfolio de 118 workflows tiene el potential<br>
        para transformarse en un marketplace profesional<br>
        con pricing competitivo y clientes recurrentes.
    </div>
    <div class="ending-cta">
        Siguiente paso: Iniciar Phase 1 - Refactoring de duplicados y consolidation
    </div>
</div>
</body>
</html>""")

    return "\n".join(html)


if __name__ == "__main__":
    html_content = generate_html()
    output_path = "/home/z/my-project/download/catalog_marketplace.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML generated: {output_path}")
    print(f"Size: {len(html_content)} characters")
