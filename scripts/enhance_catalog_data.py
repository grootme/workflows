#!/usr/bin/env python3
"""Generate enhanced marketplace catalog data for the Next.js app."""
import json
import os

# Load existing catalog data
with open('/home/z/my-project/public/catalog_data.json') as f:
    catalog_data = json.load(f)

# Add marketplace research data
catalog_data['marketplace_research'] = {
    'n8nmarkets': {
        'url': 'https://n8nmarkets.com/en/',
        'total_templates': 850,
        'monthly_visitors': '50K+',
        'languages': '30+',
        'commission': '10%',
        'pricing_range': '$5-$50+ per template',
        'categories': [
            "AI & Agents", "Lead Generation", "CRM Integrations", "Social Media",
            "E-Commerce", "Email Automation", "Team Communication", "Marketing",
            "Sales", "HR & Recruiting", "Finance & Accounting", "IT Operations",
            "Document Processing", "Data & Analytics", "Healthcare", "Legal",
            "Education", "Customer Support", "DevOps", "Security & Compliance"
        ],
        'pricing_structure': {
            'free': 'Lite version for trust building',
            'one_time': '$5-$50 per production template',
            'custom': '$75-$200+ for enterprise solutions',
            'name_your_price': 'Flexible pricing option'
        },
        'seller_tips': [
            'Include 2-3 high-quality screenshots',
            'Write detailed description covering use cases',
            'Add error handling and retry logic (premium feature)',
            'Tag with relevant categories for discoverability',
            'Offer free lite version alongside premium',
            'Respond promptly to buyer questions'
        ],
        'market_size': '$26 billion by 2028 (projected)'
    },
    'n8n_workflows': {
        'url': 'https://n8n.io/workflows/',
        'total_templates': 10930,
        'ai_workflows': 7548,
        'lead_generation': 758,
        'social_media': 612,
        'secops': 195,
        'top_categories': ['AI', 'Marketing', 'Sales', 'IT Ops', 'Document Ops', 'Support']
    }
}

# Add pricing tiers
catalog_data['pricing_tiers'] = [
    {"tier": "Starter", "price_range": "$5 - $15", "description": "Workflows simples de 3-8 nodos, un solo trigger, una integracion basica", "examples": ["Notificacion Slack", "Sync Google Sheets", "Email auto-respuesta"], "node_range": "3-8", "color": "#3fb950"},
    {"tier": "Professional", "price_range": "$15 - $35", "description": "Workflows de 8-20 nodos, multi-step logic, 2-3 integraciones, error handling basico", "examples": ["Lead qualification pipeline", "CRM sync + email", "Social media cross-posting"], "node_range": "8-20", "color": "#58a6ff"},
    {"tier": "Enterprise", "price_range": "$35 - $75", "description": "Workflows de 20+ nodos, multi-agent AI, RAG, sub-workflows, error handling completo, MCP integracion", "examples": ["Multi-agent sales assistant", "RAG chatbot + vector store", "Automated compliance review"], "node_range": "20+", "color": "#ff6b35"},
    {"tier": "Custom Solution", "price_range": "$75 - $200+", "description": "Soluciones custom con desarrollo MCP server, integracion con sistemas proprietarios, soporte post-venta", "examples": ["MCP server para ERP proprietario", "Pipeline de datos enterprise", "Multi-system integration hub"], "node_range": "Custom", "color": "#d29922"}
]

# Add automation ideas
catalog_data['automation_ideas'] = [
    {"name": "Lead Qualification AI Agent", "category": "Marketing & Leads", "nodes": "8-15", "description": "Agente AI que analiza leads entrantes, clasifica por prioridad, enriquece con datos de CRM, y asigna al representante correcto. Usa LangChain Agent con tools de CRM lookup y email enrichment.", "price": "$25-45", "tier": "Professional"},
    {"name": "Customer Support Triage Bot", "category": "Chat & Mensajería", "nodes": "10-18", "description": "Agente AI que clasifica tickets de soporte por urgencia y tipo, responde automaticamente preguntas frecuentes usando RAG, y escala tickets complejos al equipo correcto.", "price": "$30-50", "tier": "Professional"},
    {"name": "Social Media Content Engine", "category": "Social Media & Contenido", "nodes": "6-12", "description": "Pipeline que genera contenido social usando AI, publica en multiples plataformas, y trackea engagement automaticamente.", "price": "$15-35", "tier": "Professional"},
    {"name": "E-Commerce Order Orchestrator", "category": "E-Commerce & Ventas", "nodes": "12-25", "description": "Workflow consolidado que maneja el ciclo completo: pedido -> inventario -> pago -> envio -> notificacion. Incluye sub-workflows y error handling con DLQ.", "price": "$35-65", "tier": "Enterprise"},
    {"name": "HR Resume Screening Agent", "category": "RRHH & Selección", "nodes": "8-14", "description": "Agente AI que recibe resumes, analiza con LLM contra criterios, genera scorecard, y alimenta el ATS.", "price": "$25-40", "tier": "Professional"},
    {"name": "Invoice Processing Pipeline", "category": "E-Commerce & Ventas", "nodes": "10-16", "description": "OCR + AI pipeline que recibe invoices, extrae datos, valida contra PO, y sincroniza con sistema contable.", "price": "$30-55", "tier": "Enterprise"},
    {"name": "RAG Knowledge Assistant", "category": "RAG & Vector Store", "nodes": "6-12", "description": "Chatbot RAG que indexa documentos de empresa, usa vector store para retrieval, y genera respuestas contextualmente precisas.", "price": "$25-45", "tier": "Professional"},
    {"name": "Multi-Agent Research Assistant", "category": "IA & Agentes", "nodes": "15-25", "description": "Sistema multi-agente donde planner coordina researcher, analyst, y writer agents.", "price": "$45-75", "tier": "Enterprise"},
    {"name": "MCP Calendar + CRM Server", "category": "MCP Tools", "nodes": "8-15", "description": "MCP server que expone tools de calendario y CRM como servicios MCP.", "price": "$20-40", "tier": "Enterprise"},
    {"name": "Automated SEO Monitor", "category": "Marketing & Leads", "nodes": "8-14", "description": "Pipeline que monitoriza rankings SEO, analiza competitors, detecta cannibalization.", "price": "$20-35", "tier": "Professional"},
    {"name": "Voice-Enabled AI Assistant", "category": "Voz & Transcripción", "nodes": "8-12", "description": "Asistente personal con Telegram que acepta voz y texto, transcribe con Whisper, procesa con LLM.", "price": "$25-45", "tier": "Professional"},
    {"name": "Data Pipeline ETL Orchestrator", "category": "Dashboard & Datos", "nodes": "12-20", "description": "Pipeline modular ETL con sub-workflows para extract, transform, load.", "price": "$35-60", "tier": "Enterprise"},
    {"name": "Legal Document Review Agent", "category": "Documentos & PDF", "nodes": "10-16", "description": "Agente AI que recibe documentos legales, extrae clausulas, verifica compliance.", "price": "$30-55", "tier": "Enterprise"},
    {"name": "DevOps Alert & Incident Manager", "category": "Utilidades & DevOps", "nodes": "10-18", "description": "Workflow que recibe alertas, clasifica severity con AI, crea incident, notifica equipo.", "price": "$25-45", "tier": "Professional"},
    {"name": "Inventory Sync & Auto-Order", "category": "E-Commerce & Ventas", "nodes": "8-14", "description": "Workflow que syncs inventario entre multiples plataformas, detecta low-stock, genera PO.", "price": "$20-40", "tier": "Professional"}
]

# Add best practices
catalog_data['best_practices'] = [
    {"name": "Global Error Trigger", "description": "Configurar un workflow global de error handling que captura fallos de cualquier workflow activo.", "priority": "Critical"},
    {"name": "Exponential Backoff Retry", "description": "Implementar retry logic con backoff exponencial para API calls que pueden fallar.", "priority": "Critical"},
    {"name": "Pre-flight Validation", "description": "Antes de ejecutar operaciones criticas, validar datos entrantes con un nodo If/Switch.", "priority": "High"},
    {"name": "Idempotency Keys", "description": "Para operaciones que modifican estado, implementar idempotency usando Redis o database.", "priority": "High"},
    {"name": "Dead Letter Queue (DLQ)", "description": "Mantener una tabla de DLQ donde se registran todos los items que fallaron processing.", "priority": "Critical"},
    {"name": "Sub-Workflow Modularization", "description": "Dividir workflows complejos (>15 nodos) en sub-workflows con Execute Workflow node.", "priority": "High"},
    {"name": "Versionado Semantico", "description": "Adoptar versionado semantico (vMAJOR.MINOR.PATCH) para workflows.", "priority": "Medium"}
]

# Add architectural patterns
catalog_data['architectural_patterns'] = [
    {"name": "Fan-Out / Fan-In", "description": "Un trigger dispara multiples sub-workflows en paralelo y luego un nodo Merge consolida resultados.", "complexity": "Medium", "nodes": "10-20"},
    {"name": "Event-Driven Chain", "description": "Cada paso es un sub-workflow independiente que se activa por el output del paso anterior via webhook.", "complexity": "Low", "nodes": "6-12"},
    {"name": "Circuit Breaker", "description": "Patron que protege contra cascading failures cuando un servicio externo esta down.", "complexity": "Medium", "nodes": "8-15"},
    {"name": "Saga Pattern (Compensating Actions)", "description": "Para workflows multi-step que modifican multiples sistemas, implementar compensating actions para rollback.", "complexity": "High", "nodes": "15-25"},
    {"name": "Observer / Sidecar", "description": "Adjuntar un sub-workflow de observacion a cada workflow principal que monitoree executions.", "complexity": "Low", "nodes": "6-10"},
    {"name": "Multi-Agent Orchestration", "description": "Un planner agent descompone subtareas, asigna a agentes especializados, y consolida resultados.", "complexity": "High", "nodes": "15-30"}
]

# Add MCP server templates
catalog_data['mcp_server_templates'] = [
    {"name": "CRM MCP Server", "tools": ["lookup_contact", "create_lead", "update_deal_stage", "search_deals", "get_contact_activity"], "description": "MCP server que expone operaciones CRM como tools MCP. Compatible con HubSpot, Salesforce, Pipedrive.", "price": "$35-55"},
    {"name": "Calendar MCP Server", "tools": ["schedule_meeting", "check_availability", "list_upcoming_events", "cancel_event", "reschedule_event"], "description": "MCP server para Google Calendar y Outlook con conflict detection.", "price": "$20-40"},
    {"name": "Document Analysis MCP Server", "tools": ["extract_text_from_pdf", "analyze_document", "compare_documents", "generate_summary", "check_compliance"], "description": "MCP server para procesamiento de documentos con AI y vector store para RAG.", "price": "$35-60"},
    {"name": "E-Commerce MCP Server", "tools": ["get_product_info", "check_inventory", "create_order", "update_stock", "get_order_status", "process_refund"], "description": "MCP server para plataformas e-commerce (Shopify, WooCommerce).", "price": "$30-50"},
    {"name": "Database MCP Server", "tools": ["query_data", "insert_record", "update_record", "delete_record", "run_aggregation", "get_schema"], "description": "MCP server para acceso seguro a databases con query validation y rate limiting.", "price": "$25-45"},
    {"name": "Communication MCP Server", "tools": ["send_email", "send_slack_message", "send_whatsapp", "create_ticket", "send_sms"], "description": "MCP server unificado para comunicaciones multi-canal con routing inteligente.", "price": "$20-35"}
]

# Add base templates (boilerplate)
catalog_data['base_templates'] = [
    {"name": "Simple Notification Template", "nodes": 5, "structure": "Trigger -> Format -> Notification -> Log -> Error Handler", "description": "Template base para workflows de notificacion con webhook/cron trigger y error handling.", "tier": "Starter"},
    {"name": "AI Agent Template", "nodes": 8, "structure": "Trigger -> Validation -> AI Agent -> Processing -> Action -> Notification -> Log -> Error Handler", "description": "Template base para workflows con AI Agent y pre-flight validation.", "tier": "Professional"},
    {"name": "RAG Pipeline Template", "nodes": 10, "structure": "Trigger -> Input -> Vector Store -> Retrieval -> LLM -> Response -> Action -> Notification -> Log -> Error Handler", "description": "Template base para RAG workflows con vector store y context injection.", "tier": "Enterprise"},
    {"name": "Sub-Workflow Module Template", "nodes": 6, "structure": "Webhook Input -> Validation -> Core Logic -> Output Formatting -> Response -> Error Handler", "description": "Template base para sub-workflows modulares.", "tier": "Professional"},
    {"name": "Multi-Step Orchestration Template", "nodes": 12, "structure": "Trigger -> Validation -> Sub-A -> Sub-B -> Merge -> Decision -> Sub-C -> Notification -> Dashboard -> Log -> Error -> DLQ", "description": "Template base para pipelines multi-step con sub-workflows.", "tier": "Enterprise"},
    {"name": "MCP Server Template", "nodes": 8, "structure": "MCP Trigger -> Tool Router -> Validation -> Core Logic -> External API -> Response -> MCP Response -> Error Handler", "description": "Template base para MCP server workflows en n8n.", "tier": "Enterprise"}
]

# Add industry pricing reference
catalog_data['industry_pricing'] = [
    {"industry": "Salud / Healthcare", "monthly_budget": "$50-200", "complexity": "High"},
    {"industry": "Finanzas / Finance", "monthly_budget": "$100-500", "complexity": "Very High"},
    {"industry": "E-Commerce", "monthly_budget": "$20-100", "complexity": "Medium"},
    {"industry": "Marketing / Agencias", "monthly_budget": "$30-150", "complexity": "Medium"},
    {"industry": "RRHH / HR", "monthly_budget": "$20-80", "complexity": "Medium"},
    {"industry": "Legal / Compliance", "monthly_budget": "$50-200", "complexity": "High"},
    {"industry": "IT / DevOps", "monthly_budget": "$30-100", "complexity": "Medium-High"},
    {"industry": "Educacion", "monthly_budget": "$10-50", "complexity": "Low-Medium"}
]

# Add implementation roadmap
catalog_data['roadmap'] = [
    {"phase": "Phase 1", "timeline": "Semanas 1-2", "tasks": "Eliminar 14 duplicados, consolidar 41 similitudes, crear workflows master", "deliverable": "Portfolio reducido de ~70 workflows unicos"},
    {"phase": "Phase 2", "timeline": "Semanas 3-4", "tasks": "Agregar error handling, retry logic, DLQ, pre-flight validation, idempotency", "deliverable": "Todos los workflows production-ready"},
    {"phase": "Phase 3", "timeline": "Semanas 5-6", "tasks": "Crear templates base, MCP servers, nuevas automation ideas, versionado", "deliverable": "Catalogo completo"},
    {"phase": "Phase 4", "timeline": "Semanas 7-8", "tasks": "Listar en n8nmarkets.com, proposals para verticals, marketing launch", "deliverable": "Marketplace live"}
]

# Write enhanced data
output_path = '/home/z/my-project/public/catalog_data_enhanced.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(catalog_data, f, indent=2, ensure_ascii=False)
    
print(f"Enhanced catalog data written: {output_path}")
print(f"Total size: {os.path.getsize(output_path)} bytes")
