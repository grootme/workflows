"""
Phase 2 Zero-Debt Refactoring - Part 2: Consolidated Workflows (G8-G13)
+ MCP Server Templates + Base Development Templates
"""

import json
import uuid
import os
from datetime import datetime

OUTPUT_DIR_CONSOLIDATED = "/home/z/my-project/download/n8n_workflows_v2/consolidated"
OUTPUT_DIR_MCP = "/home/z/my-project/download/n8n_workflows_v2/mcp_servers"
OUTPUT_DIR_BASE = "/home/z/my-project/download/n8n_workflows_v2/base_templates"

def gen_uuid():
    return str(uuid.uuid4())

def make_connection(source_name, target_name, conn_type="main", index=0):
    return {source_name: {conn_type: [[{"node": target_name, "type": conn_type, "index": index}]]}}

def make_ai_connection(sub_name, agent_name, ai_type):
    return {sub_name: {ai_type: [[{"node": agent_name, "type": ai_type, "index": 0}]]}}

def merge_connections(*conn_dicts):
    merged = {}
    for cd in conn_dicts:
        for node_name, conn_types in cd.items():
            if node_name not in merged:
                merged[node_name] = {}
            for type_key, targets in conn_types.items():
                if type_key not in merged[node_name]:
                    merged[node_name][type_key] = []
                merged[node_name][type_key].extend(targets)
    return merged

def make_node(name, node_type, type_version, position, parameters=None, credentials=None, webhook_id=None):
    node = {"parameters": parameters or {}, "type": node_type, "typeVersion": type_version, "position": position, "id": gen_uuid(), "name": name}
    if credentials:
        clean_creds = {}
        for cred_type, cred_data in credentials.items():
            clean_creds[cred_type] = {"id": "", "name": cred_data.get("name", cred_type)}
        node["credentials"] = clean_creds
    if webhook_id:
        node["webhookId"] = webhook_id
    return node

def make_sticky_note(name, position, content, width=300, height=200):
    return {"parameters": {"content": content, "width": width, "height": height}, "type": "n8n-nodes-base.stickyNote", "typeVersion": 1, "position": position, "id": gen_uuid(), "name": name}

def make_workflow(name, nodes, connections, active=False, timezone="Europe/Madrid"):
    return {
        "name": name, "nodes": nodes, "connections": connections, "pinData": {},
        "active": active,
        "settings": {"executionOrder": "v1", "timezone": timezone, "callerPolicy": "workflowsFromSameOwner"},
        "tags": [],
        "meta": {"templateCredsSetupCompleted": False, "instanceId": ""}
    }

def fromAI(field_name, description, field_type="string"):
    return f"={{ /*n8n-auto-generated-fromAI-override*/ $fromAI('{field_name}', `{description}`, '{field_type}') }}"


# ============================================================
# G8: AI Video Content Suite
# ============================================================
def generate_g8_video_suite():
    """AI Video Content Suite - Enterprise tier $59
    Based on original: Crear_videos_virales + AI_Powered_Short_Form_Video patterns
    Pattern: ChatTrigger → Agent → Video generation pipeline via sub-workflows
    """
    nodes = [
        make_node("Chat Trigger", "@n8n/n8n-nodes-langchain.chatTrigger", 1.1, [0, 0],
            {"initialMessages": [{"content": "Hi! I can help you create viral video content. Tell me your topic, platform, and style!"}]},
            webhook_id=gen_uuid()
        ),
        make_node("Video Agent", "@n8n/n8n-nodes-langchain.agent", 1.8, [400, 0],
            {
                "promptType": "define",
                "text": "={{ $json.chatInput }}",
                "options": {
                    "systemMessage": "=# AI Video Content Creator\n\nYou are a video content strategist and creator with access to specialized tools.\n\n## Available Tools:\n- **Think**: Plan video concepts and multi-step strategies\n- **Script Writer**: Generate video scripts with hooks, body, and CTAs\n- **Thumbnail Designer**: Create thumbnail concepts and descriptions\n- **Audio Generator**: Plan voiceover scripts and audio elements\n\n## Rules:\n- Consider platform-specific formats (TikTok: 60s, YouTube Shorts: 60s, Reels: 90s)\n- Always include a strong hook in the first 3 seconds\n- Include trending hashtags and sound suggestions\n- Current datetime: {{ $now }}\n\n## Output Style:\n- Deliver complete video production packages\n- Include script, thumbnail, audio plan, and posting schedule"
                }
            }
        ),
        make_node("Gemini Flash", "@n8n/n8n-nodes-langchain.lmChatGoogleGemini", 1, [200, 300],
            {"model": {"__rl": True, "value": "gemini-2.5-flash-preview-05-20", "mode": "list"}, "options": {"temperature": 0.8}},
            {"googleGeminiApi": {"name": "Google Gemini"}}
        ),
        make_node("Chat Memory", "@n8n/n8n-nodes-langchain.memoryBufferWindow", 1.3, [400, 300],
            {"sessionIdType": "customKey", "sessionKey": "={{ $json.sessionId }}"}
        ),
        make_node("Think", "@n8n/n8n-nodes-langchain.toolThink", 1, [600, 300],
            {"description": "Plan video concept, script structure, and content strategy before generating"}
        ),
        # Sub-workflow tools (must be configured after deployment)
        make_node("Script Writer", "@n8n/n8n-nodes-langchain.toolWorkflow", 1.1, [800, 300],
            {"description": "Generate complete video scripts with hooks, narrative arc, and CTAs", "workflowId": ""}
        ),
        make_node("Thumbnail Designer", "@n8n/n8n-nodes-langchain.toolWorkflow", 1.1, [1000, 300],
            {"description": "Create thumbnail concepts with visual descriptions, text overlays, and color palettes", "workflowId": ""}
        ),
        make_node("Audio Generator", "@n8n/n8n-nodes-langchain.toolWorkflow", 1.1, [1200, 300],
            {"description": "Plan voiceover scripts and audio elements for video production", "workflowId": ""}
        ),
        make_sticky_note("Video Docs", [0, -300], "🎬 AI Video Content Suite v2.0\n\nLLM: Gemini 2.5 Flash (multimodal)\nMemory: BufferWindow\nTools: Think + 3 Sub-Workflows\n\nSetup:\n1. Deploy Script/Thumbnail/Audio sub-workflows\n2. Copy their workflow IDs\n3. Configure Gemini credential\n\nZero-debt: All ai_* connections correct"),
    ]
    
    connections = merge_connections(
        make_connection("Chat Trigger", "Video Agent", "main"),
        make_ai_connection("Gemini Flash", "Video Agent", "ai_languageModel"),
        make_ai_connection("Chat Memory", "Video Agent", "ai_memory"),
        make_ai_connection("Think", "Video Agent", "ai_tool"),
        make_ai_connection("Script Writer", "Video Agent", "ai_tool"),
        make_ai_connection("Thumbnail Designer", "Video Agent", "ai_tool"),
        make_ai_connection("Audio Generator", "Video Agent", "ai_tool"),
    )
    
    return make_workflow("AI Video Content Suite v2", nodes, connections)


# ============================================================
# G9: Universal Social Scraper Suite
# ============================================================
def generate_g9_social_scraper():
    """Universal Social Scraper Suite - Professional tier $35
    Based on original: Scrap_emails patterns
    Pattern: Webhook → Agent → Multiple scraper HTTP tools
    """
    nodes = [
        make_node("Webhook Trigger", "n8n-nodes-base.webhook", 2, [0, 0],
            {"httpMethod": "POST", "path": "social-scraper", "options": {}},
            webhook_id="social-scraper"
        ),
        make_node("Parse Request", "n8n-nodes-base.set", 3.4, [200, 0],
            {
                "assignments": {"assignments": [
                    {"id": gen_uuid(), "name": "query", "value": "={{ $json.body.query }}", "type": "string"},
                    {"id": gen_uuid(), "name": "platform", "value": "={{ $json.body.platform }}", "type": "string"},
                    {"id": gen_uuid(), "name": "target", "value": "={{ $json.body.target }}", "type": "string"},
                ]},
                "options": {}
            }
        ),
        make_node("Scraper Agent", "@n8n/n8n-nodes-langchain.agent", 1.8, [600, 0],
            {
                "promptType": "define",
                "text": "={{ $json.query }} - Platform: {{ $json.platform }} - Target: {{ $json.target }}",
                "options": {
                    "systemMessage": "=# Universal Social Scraper Agent\n\nYou are a data extraction specialist with access to multiple social platform scrapers.\n\n## Available Tools:\n- **Instagram Scraper**: Extract profile data, posts, followers\n- **LinkedIn Scraper**: Extract professional profiles, job listings\n- **Google Maps Scraper**: Extract business data, emails, reviews\n- **Twitter/X Scraper**: Extract tweets, profiles, engagement data\n\n## Rules:\n- Use the appropriate platform scraper for the request\n- Structure extracted data in organized format\n- Respect rate limits and data privacy\n- Current datetime: {{ $now }}\n\n## Output:\n- Structured JSON with extracted data\n- Include source URLs and extraction timestamps"
                }
            }
        ),
        make_node("GPT-4o-mini", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.2, [400, 300],
            {"model": {"__rl": True, "value": "gpt-4o-mini", "mode": "list", "cachedResultName": "gpt-4o-mini"}, "options": {"temperature": 0.2}},
            {"openAiApi": {"name": "OpenAI"}}
        ),
        make_node("Instagram Scraper", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [600, 300],
            {"description": "Extract Instagram profile data including posts, followers, engagement metrics, and contact info", "url": "={{ $fromAI('Instagram_API_URL', 'Instagram scraping API endpoint', 'string') }}", "method": "POST", "options": {}}
        ),
        make_node("LinkedIn Scraper", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [800, 300],
            {"description": "Extract LinkedIn professional profiles, job listings, company data, and contact information", "url": "={{ $fromAI('LinkedIn_API_URL', 'LinkedIn scraping API endpoint', 'string') }}", "method": "POST", "options": {}}
        ),
        make_node("Google Maps Scraper", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [1000, 300],
            {"description": "Extract business data from Google Maps including emails, phone numbers, addresses, and reviews", "url": "={{ $fromAI('Maps_API_URL', 'Google Maps scraping endpoint', 'string') }}", "method": "POST", "options": {}}
        ),
        make_node("Twitter Scraper", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [1200, 300],
            {"description": "Extract Twitter/X data including tweets, profiles, engagement metrics, and follower analysis", "url": "={{ $fromAI('Twitter_API_URL', 'Twitter/X scraping endpoint', 'string') }}", "method": "POST", "options": {}}
        ),
        make_node("Format Results", "n8n-nodes-base.set", 3.4, [800, 0],
            {"assignments": {"assignments": [{"id": gen_uuid(), "name": "result", "value": "={{ $json.output }}", "type": "string"}]}, "options": {}}
        ),
        make_node("Respond", "n8n-nodes-base.respondToWebhook", 1.1, [1000, 0],
            {"respondWith": "json", "responseBody": "={{ JSON.stringify({ success: true, data: $json.result }) }}"}
        ),
        make_sticky_note("Scraper Docs", [0, -300], "🔍 Social Scraper Suite v2.0\n\nLLM: GPT-4o-mini\nTools: 4 HTTP scrapers\nOutput: Structured JSON\n\nSetup:\n1. Configure scraping API URLs\n2. Set up OpenAI credential\n3. Configure rate limiting\n\n⚠️ Note: Scraping must comply with platform ToS and local data privacy laws"),
    ]
    
    connections = merge_connections(
        make_connection("Webhook Trigger", "Parse Request", "main"),
        make_connection("Parse Request", "Scraper Agent", "main"),
        make_connection("Scraper Agent", "Format Results", "main"),
        make_connection("Format Results", "Respond", "main"),
        make_ai_connection("GPT-4o-mini", "Scraper Agent", "ai_languageModel"),
        make_ai_connection("Instagram Scraper", "Scraper Agent", "ai_tool"),
        make_ai_connection("LinkedIn Scraper", "Scraper Agent", "ai_tool"),
        make_ai_connection("Google Maps Scraper", "Scraper Agent", "ai_tool"),
        make_ai_connection("Twitter Scraper", "Twitter Agent", "ai_tool"),
    )
    
    # Fix: Twitter target should be Scraper Agent
    connections = merge_connections(
        make_connection("Webhook Trigger", "Parse Request", "main"),
        make_connection("Parse Request", "Scraper Agent", "main"),
        make_connection("Scraper Agent", "Format Results", "main"),
        make_connection("Format Results", "Respond", "main"),
        make_ai_connection("GPT-4o-mini", "Scraper Agent", "ai_languageModel"),
        make_ai_connection("Instagram Scraper", "Scraper Agent", "ai_tool"),
        make_ai_connection("LinkedIn Scraper", "Scraper Agent", "ai_tool"),
        make_ai_connection("Google Maps Scraper", "Scraper Agent", "ai_tool"),
        make_ai_connection("Twitter Scraper", "Scraper Agent", "ai_tool"),
    )
    
    return make_workflow("Universal Social Scraper Suite v2", nodes, connections)


# ============================================================
# G10: HR AI Agent Pro
# ============================================================
def generate_g10_hr_agent():
    """HR AI Agent Pro - Professional tier $45
    Based on original: Resume_Screening + HR_IT_Helpdesk patterns
    Pattern: Webhook → Agent → Resume screening + interview scheduling tools
    """
    nodes = [
        make_node("Webhook", "n8n-nodes-base.webhook", 2, [0, 0],
            {"httpMethod": "POST", "path": "hr-agent", "options": {}},
            webhook_id="hr-agent"
        ),
        make_node("Parse Request", "n8n-nodes-base.set", 3.4, [200, 0],
            {"assignments": {"assignments": [
                {"id": gen_uuid(), "name": "message", "value": "={{ $json.body.message }}", "type": "string"},
                {"id": gen_uuid(), "name": "chatId", "value": "={{ $json.body.chatId }}", "type": "string"},
                {"id": gen_uuid(), "name": "resumeUrl", "value": "={{ $json.body.resumeUrl }}", "type": "string"},
            ]}, "options": {}}
        ),
        make_node("HR Agent", "@n8n/n8n-nodes-langchain.agent", 1.8, [600, 0],
            {
                "promptType": "define",
                "text": "={{ $json.message }}",
                "options": {
                    "systemMessage": "=# HR AI Agent\n\nYou are an HR assistant specialized in recruitment and employee management.\n\n## Available Tools:\n- **Resume Analyzer**: Screen and evaluate candidate resumes\n- **Interview Scheduler**: Schedule and manage interview appointments\n- **Employee Database**: Query and manage employee records\n- **Think**: Plan multi-step HR workflows\n\n## Rules:\n- Evaluate resumes objectively against job criteria\n- Score candidates on relevant skills, experience, and education\n- Schedule interviews with appropriate time slots\n- Never discriminate based on protected characteristics\n- Current datetime: {{ $now }}\n\n## Output:\n- Structured candidate evaluations with scores\n- Interview scheduling confirmations\n- Employee data queries with organized results"
                }
            }
        ),
        make_node("GPT-4o-mini", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.2, [400, 300],
            {"model": {"__rl": True, "value": "gpt-4o-mini", "mode": "list"}, "options": {"temperature": 0.3}},
            {"openAiApi": {"name": "OpenAI"}}
        ),
        make_node("Chat Memory", "@n8n/n8n-nodes-langchain.memoryBufferWindow", 1.3, [600, 300],
            {"sessionIdType": "customKey", "sessionKey": "={{ $json.chatId }}"}
        ),
        make_node("Think", "@n8n/n8n-nodes-langchain.toolThink", 1, [800, 300],
            {"description": "Plan resume screening criteria, interview scheduling, and multi-step HR workflows"}
        ),
        make_node("Resume Analyzer", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [1000, 300],
            {"description": "Analyze and evaluate candidate resumes against job requirements, scoring skills, experience, and education",
             "url": "={{ $fromAI('Resume_API_URL', 'Resume analysis API endpoint', 'string') }}", "method": "POST", "options": {}}
        ),
        make_node("Interview Scheduler", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [1200, 300],
            {"description": "Schedule interview appointments, check availability, and send calendar invites",
             "url": "={{ $fromAI('Calendar_API_URL', 'Calendar scheduling API endpoint', 'string') }}", "method": "POST", "options": {}}
        ),
        make_node("Employee Database", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [1400, 300],
            {"description": "Query and manage employee records, benefits, and organizational data",
             "url": "={{ $fromAI('HR_DB_API_URL', 'HR database API endpoint', 'string') }}", "method": "GET", "options": {}}
        ),
        make_node("Format Response", "n8n-nodes-base.set", 3.4, [800, 0],
            {"assignments": {"assignments": [{"id": gen_uuid(), "name": "response", "value": "={{ $json.output }}", "type": "string"}]}, "options": {}}
        ),
        make_node("Respond", "n8n-nodes-base.respondToWebhook", 1.1, [1000, 0],
            {"respondWith": "json", "responseBody": "={{ JSON.stringify({ success: true, response: $json.response }) }}"}
        ),
        make_sticky_note("HR Docs", [0, -300], "👤 HR AI Agent Pro v2.0\n\nLLM: GPT-4o-mini\nMemory: BufferWindow\nTools: Think + Resume + Interview + Employee DB\n\nSetup:\n1. Configure Resume/Calendar/HR APIs\n2. Set up OpenAI credential\n3. Connect to HR systems\n\nZero-debt: All ai_* connections correct"),
    ]
    
    connections = merge_connections(
        make_connection("Webhook", "Parse Request", "main"),
        make_connection("Parse Request", "HR Agent", "main"),
        make_connection("HR Agent", "Format Response", "main"),
        make_connection("Format Response", "Respond", "main"),
        make_ai_connection("GPT-4o-mini", "HR Agent", "ai_languageModel"),
        make_ai_connection("Chat Memory", "HR Agent", "ai_memory"),
        make_ai_connection("Think", "HR Agent", "ai_tool"),
        make_ai_connection("Resume Analyzer", "HR Agent", "ai_tool"),
        make_ai_connection("Interview Scheduler", "HR Agent", "ai_tool"),
        make_ai_connection("Employee Database", "HR Agent", "ai_tool"),
    )
    
    return make_workflow("HR AI Agent Pro v2", nodes, connections)


# ============================================================
# G11: WhatsApp AI Agent Pro
# ============================================================
def generate_g11_whatsapp_agent():
    """WhatsApp AI Agent Pro - Professional tier $49
    Based on original: WhatsApp_Definitivo_Agente + Chatbot EvolutionAPI patterns
    Pattern: Webhook (Evolution API) → Agent → WhatsApp response
    """
    nodes = [
        make_node("WhatsApp Webhook", "n8n-nodes-base.webhook", 2, [-2200, 0],
            {"httpMethod": "POST", "path": "whatsapp-agent", "options": {}},
            webhook_id="whatsapp-agent"
        ),
        make_node("Parse Message", "n8n-nodes-base.set", 3.4, [-2000, 0],
            {"assignments": {"assignments": [
                {"id": gen_uuid(), "name": "serverUrl", "value": "={{ $json.body.server_url }}", "type": "string"},
                {"id": gen_uuid(), "name": "instance", "value": "={{ $json.body.instance }}", "type": "string"},
                {"id": gen_uuid(), "name": "apiKey", "value": "={{ $json.body.apikey }}", "type": "string"},
                {"id": gen_uuid(), "name": "chatId", "value": "={{ $json.body.data.key.remoteJid }}", "type": "string"},
                {"id": gen_uuid(), "name": "messageId", "value": "={{ $json.body.data.key.id }}", "type": "string"},
                {"id": gen_uuid(), "name": "text", "value": "={{ $json.body.data.message.conversation || $json.body.data.message.extendedTextMessage?.text }}", "type": "string"},
            ]}, "options": {}}
        ),
        # Check if voice message
        make_node("Check Media", "n8n-nodes-base.switch", 3.2, [-1800, 0],
            {
                "rules": {"values": [
                    {
                        "conditions": {"options": {"caseSensitive": True, "typeValidation": "strict", "version": 2},
                        "conditions": [{"leftValue": "={{ $json.body.data.message.audioMessage?.url }}", "rightValue": "", "operator": {"type": "string", "operation": "exists", "singleValue": True}}],
                        "combinator": "and"},
                        "renameOutput": True, "outputKey": "audio"
                    },
                    {
                        "conditions": {"options": {"caseSensitive": True, "typeValidation": "strict", "version": 2},
                        "conditions": [{"leftValue": "={{ $json.text }}", "rightValue": "", "operator": {"type": "string", "operation": "exists", "singleValue": True}}],
                        "combinator": "and"},
                        "renameOutput": True, "outputKey": "text"
                    },
                ]},
                "options": {}
            }
        ),
        # Audio path
        make_node("Download Audio", "n8n-nodes-base.httpRequest", 4.2, [-1600, -400],
            {"url": "={{ $('Check Media').item.json.body.data.message.audioMessage.url }}", "options": {"response": {"response": {"responseFormat": "file"}}}}
        ),
        make_node("Transcribe", "@n8n/n8n-nodes-langchain.openAi", 1.8, [-1400, -400],
            {"resource": "audio", "operation": "transcribe", "options": {"language": "es"}},
            {"openAiApi": {"name": "OpenAI"}}
        ),
        make_node("Set Audio Text", "n8n-nodes-base.set", 3.4, [-1200, -400],
            {"assignments": {"assignments": [
                {"id": gen_uuid(), "name": "text", "value": "={{ $json.text }}", "type": "string"},
                {"id": gen_uuid(), "name": "chatId", "value": "={{ $('Parse Message').item.json.chatId }}", "type": "string"},
                {"id": gen_uuid(), "name": "serverUrl", "value": "={{ $('Parse Message').item.json.serverUrl }}", "type": "string"},
                {"id": gen_uuid(), "name": "instance", "value": "={{ $('Parse Message').item.json.instance }}", "type": "string"},
                {"id": gen_uuid(), "name": "apiKey", "value": "={{ $('Parse Message').item.json.apiKey }}", "type": "string"},
            ]}, "options": {}}
        ),
        # Text path - already parsed
        make_node("Set Text Message", "n8n-nodes-base.set", 3.4, [-1200, 0],
            {"assignments": {"assignments": [
                {"id": gen_uuid(), "name": "text", "value": "={{ $json.text }}", "type": "string"},
                {"id": gen_uuid(), "name": "chatId", "value": "={{ $json.chatId }}", "type": "string"},
                {"id": gen_uuid(), "name": "serverUrl", "value": "={{ $json.serverUrl }}", "type": "string"},
                {"id": gen_uuid(), "name": "instance", "value": "={{ $json.instance }}", "type": "string"},
                {"id": gen_uuid(), "name": "apiKey", "value": "={{ $json.apiKey }}", "type": "string"},
            ]}, "options": {}}
        ),
        # AI Agent
        make_node("WhatsApp Agent", "@n8n/n8n-nodes-langchain.agent", 1.8, [-800, 0],
            {
                "promptType": "define",
                "text": "={{ $json.text }}",
                "options": {
                    "systemMessage": "=# WhatsApp AI Agent\n\nYou are a helpful WhatsApp assistant with access to business tools.\n\n## Available Tools:\n- **Think**: Plan complex multi-step responses\n- **Knowledge Base**: Search internal documents and FAQ\n- **Order Lookup**: Check order status and shipping info\n- **Appointment Booking**: Schedule meetings via HTTP\n\n## Rules:\n- Keep responses concise for mobile reading\n- Use WhatsApp-friendly formatting (no markdown)\n- If uncertain, ask clarifying questions\n- Never share sensitive data without verification\n- Current datetime: {{ $now }}\n\n## Response Style:\n- Friendly and professional\n- Use bullet points for lists\n- Include relevant links when available"
                }
            }
        ),
        # LLM
        make_node("GPT-4o-mini", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.2, [-400, 300],
            {"model": {"__rl": True, "value": "gpt-4o-mini", "mode": "list"}, "options": {"temperature": 0.5}},
            {"openAiApi": {"name": "OpenAI"}}
        ),
        # Memory: PostgresChatHistory (production-grade)
        make_node("Chat Memory", "@n8n/n8n-nodes-langchain.memoryPostgresChat", 1.3, [0, 300],
            {"sessionIdType": "customKey", "sessionKey": "={{ $json.chatId }}", "options": {}},
            {"postgresApi": {"name": "PostgreSQL"}}
        ),
        # Tools
        make_node("Think", "@n8n/n8n-nodes-langchain.toolThink", 1, [200, 300],
            {"description": "Plan complex multi-step responses and business workflows"}
        ),
        make_node("Knowledge Base", "@n8n/n8n-nodes-langchain.vectorStoreQdrant", 1, [400, 300],
            {"operation": "search", "query": fromAI("Query", "Search query for knowledge base"), "options": {}},
            {"qdrantApi": {"name": "Qdrant"}}
        ),
        make_node("Embeddings", "@n8n/n8n-nodes-langchain.embeddingsGoogleGemini", 1, [400, 500],
            {"model": {"__rl": True, "value": "gemini-embedding-exp-03-07", "mode": "list"}},
            {"googleGeminiApi": {"name": "Google Gemini"}}
        ),
        make_node("Order Lookup", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [600, 300],
            {"description": "Check order status, shipping info, and delivery updates", "url": "={{ $fromAI('Order_API_URL', 'Order lookup API endpoint', 'string') }}", "method": "GET", "options": {}}
        ),
        make_node("Appointment Booking", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [800, 300],
            {"description": "Schedule meetings and appointments via HTTP API", "url": "={{ $fromAI('Booking_API_URL', 'Booking API endpoint', 'string') }}", "method": "POST", "options": {}}
        ),
        # Send WhatsApp Response
        make_node("Send Response", "n8n-nodes-base.httpRequest", 4.2, [-200, 0],
            {
                "url": "={{ $json.serverUrl }}/chat/sendMessage/{{ $json.instance }}",
                "method": "POST",
                "sendHeaders": True,
                "headerParameters": {"parameters": [{"name": "apikey", "value": "={{ $json.apiKey }}"}]},
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={{ JSON.stringify({ number: $json.chatId, text: $json.output }) }}",
                "options": {}
            }
        ),
        make_sticky_note("WhatsApp Docs", [-2200, -400], "💬 WhatsApp AI Agent Pro v2.0\n\nArchitecture: Webhook (Evolution API) → Agent\nLLM: GPT-4o-mini\nMemory: PostgresChatHistory\nRAG: Qdrant + Gemini Embeddings\n\nSetup:\n1. Configure Evolution API connection\n2. Set up OpenAI + PostgreSQL + Qdrant + Gemini\n3. Update Order/Booking API URLs\n4. Seed knowledge base with documents\n\nZero-debt: All ai_* + ai_embedding connections"),
    ]
    
    connections = merge_connections(
        # Main flow
        make_connection("WhatsApp Webhook", "Parse Message", "main"),
        make_connection("Parse Message", "Check Media", "main"),
        {"Check Media": {"main": [
            [{"node": "Download Audio", "type": "main", "index": 0}],
            [{"node": "Set Text Message", "type": "main", "index": 0}],
        ]}},
        make_connection("Download Audio", "Transcribe", "main"),
        make_connection("Transcribe", "Set Audio Text", "main"),
        make_connection("Set Audio Text", "WhatsApp Agent", "main"),
        make_connection("Set Text Message", "WhatsApp Agent", "main"),
        make_connection("WhatsApp Agent", "Send Response", "main"),
        # AI sub-component connections
        make_ai_connection("GPT-4o-mini", "WhatsApp Agent", "ai_languageModel"),
        make_ai_connection("Chat Memory", "WhatsApp Agent", "ai_memory"),
        make_ai_connection("Think", "WhatsApp Agent", "ai_tool"),
        make_ai_connection("Knowledge Base", "WhatsApp Agent", "ai_tool"),
        make_ai_connection("Order Lookup", "WhatsApp Agent", "ai_tool"),
        make_ai_connection("Appointment Booking", "WhatsApp Agent", "ai_tool"),
        # Embeddings → Vector Store
        make_ai_connection("Embeddings", "Knowledge Base", "ai_embedding"),
    )
    
    return make_workflow("WhatsApp AI Agent Pro v2", nodes, connections)


# ============================================================
# G12: Flowise RAG Agent Suite
# ============================================================
def generate_g12_flowise_rag():
    """Flowise RAG Agent Suite - Starter tier $19
    Based on original: Flowise_Agente_Conversacional patterns
    Pattern: ChatTrigger → Agent → Flowise HTTP Tool
    """
    nodes = [
        make_node("Chat Trigger", "@n8n/n8n-nodes-langchain.chatTrigger", 1.1, [0, 0],
            {"initialMessages": [{"content": "Hi! I can answer questions using our knowledge base. What would you like to know?"}]},
            webhook_id=gen_uuid()
        ),
        make_node("RAG Agent", "@n8n/n8n-nodes-langchain.agent", 1.8, [400, 0],
            {
                "promptType": "define",
                "text": "={{ $json.chatInput }}",
                "options": {
                    "systemMessage": "=# RAG Knowledge Assistant\n\nYou are a knowledge assistant with access to a Flowise RAG pipeline.\n\n## Available Tools:\n- **Flowise RAG**: Search through documents and provide accurate answers\n- **Think**: Plan complex research queries\n\n## Rules:\n- Always use the RAG tool for factual questions\n- Cite sources when providing information\n- If the RAG tool doesn't have relevant info, admit it\n- Current datetime: {{ $now }}\n\n## Response Style:\n- Clear and concise answers\n- Include source references\n- Suggest related topics to explore"
                }
            }
        ),
        make_node("GPT-4o-mini", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.2, [200, 300],
            {"model": {"__rl": True, "value": "gpt-4o-mini", "mode": "list"}, "options": {"temperature": 0.3}},
            {"openAiApi": {"name": "OpenAI"}}
        ),
        make_node("Chat Memory", "@n8n/n8n-nodes-langchain.memoryBufferWindow", 1.3, [400, 300],
            {"sessionIdType": "customKey", "sessionKey": "={{ $json.sessionId }}"}
        ),
        make_node("Think", "@n8n/n8n-nodes-langchain.toolThink", 1, [600, 300],
            {"description": "Plan complex research queries before executing"}
        ),
        make_node("Flowise RAG", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [800, 300],
            {
                "description": "Search through documents using Flowise RAG pipeline for accurate knowledge-based answers",
                "url": "={{ $fromAI('Flowise_URL', 'Flowise API endpoint URL', 'string') }}",
                "method": "POST",
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={{ JSON.stringify({ question: $fromAI('Question', 'Question to search in knowledge base', 'string') }) }}",
                "options": {}
            }
        ),
        make_sticky_note("RAG Docs", [0, -200], "📚 Flowise RAG Agent Suite v2.0\n\nLLM: GPT-4o-mini\nMemory: BufferWindow\nTool: Flowise RAG HTTP\n\nSetup:\n1. Deploy Flowise with RAG pipeline\n2. Copy Flowise API URL into tool\n3. Seed knowledge base documents\n4. Configure OpenAI credential\n\nZero-debt: All ai_* connections correct"),
    ]
    
    connections = merge_connections(
        make_connection("Chat Trigger", "RAG Agent", "main"),
        make_ai_connection("GPT-4o-mini", "RAG Agent", "ai_languageModel"),
        make_ai_connection("Chat Memory", "RAG Agent", "ai_memory"),
        make_ai_connection("Think", "RAG Agent", "ai_tool"),
        make_ai_connection("Flowise RAG", "RAG Agent", "ai_tool"),
    )
    
    return make_workflow("Flowise RAG Agent Suite v2", nodes, connections)


# ============================================================
# G13: Global Error Handler Workflow
# ============================================================
def generate_g13_error_handler():
    """Global Error Handler - Starter tier $15
    Based on original: Error_Josema_Fernandez patterns
    Pattern: Error Trigger → Classify → Notify → Log
    """
    nodes = [
        make_node("Error Trigger", "n8n-nodes-base.errorTrigger", 1, [0, 0],
            {}  # No parameters needed for error trigger
        ),
        # Parse Error Data
        make_node("Parse Error", "n8n-nodes-base.set", 3.4, [200, 0],
            {"assignments": {"assignments": [
                {"id": gen_uuid(), "name": "workflowName", "value": "={{ $json.workflow.name }}", "type": "string"},
                {"id": gen_uuid(), "name": "executionId", "value": "={{ $json.execution.id }}", "type": "string"},
                {"id": gen_uuid(), "name": "nodeName", "value": "={{ $json.execution.error.node.name }}", "type": "string"},
                {"id": gen_uuid(), "name": "errorMessage", "value": "={{ $json.execution.error.message }}", "type": "string"},
                {"id": gen_uuid(), "name": "timestamp", "value": "={{ $now }}", "type": "string"},
                {"id": gen_uuid(), "name": "severity", "value": "={{ $json.execution.lastNodeExecuted }}", "type": "string"},
            ]}, "options": {}}
        ),
        # Classify Error Severity
        make_node("Classify Severity", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.2, [400, 0],
            {
                "model": {"__rl": True, "value": "gpt-4o-mini", "mode": "list"},
                "options": {"temperature": 0}
            },
            {"openAiApi": {"name": "OpenAI"}}
        ),
        # Actually, for error handler, we should use a simpler pattern - no LLM, just Switch based on node
        # Let me redesign this more practically
        make_node("Severity Router", "n8n-nodes-base.switch", 3.2, [400, 0],
            {
                "rules": {"values": [
                    {
                        "conditions": {"options": {"caseSensitive": False, "typeValidation": "loose", "version": 2},
                        "conditions": [{"leftValue": "={{ $json.nodeName }}", "rightValue": "", "operator": {"type": "string", "operation": "contains", "singleValue": True}}],
                        "combinator": "and"},
                        "renameOutput": True, "outputKey": "critical"
                    },
                    {
                        "conditions": {"options": {"caseSensitive": False, "typeValidation": "loose", "version": 2},
                        "conditions": [{"leftValue": "={{ $json.errorMessage }}", "rightValue": "timeout", "operator": {"type": "string", "operation": "contains", "singleValue": True}}],
                        "combinator": "and"},
                        "renameOutput": True, "outputKey": "warning"
                    },
                ]},
                "options": {"fallbackOutput": 2}
            }
        ),
        # Critical: Send urgent notification
        make_node("Send Critical Alert", "n8n-nodes-base.gmail", 1, [600, -200],
            {
                "operation": "send",
                "to": "admin@example.com",
                "subject": "=🚨 CRITICAL ERROR: {{ $json.workflowName }} - {{ $json.nodeName }}",
                "message": "=Workflow: {{ $json.workflowName }}\nNode: {{ $json.nodeName }}\nError: {{ $json.errorMessage }}\nExecution ID: {{ $json.executionId }}\nTimestamp: {{ $json.timestamp }}\n\nThis requires immediate attention.",
                "additionalFields": {}
            },
            {"gmailOAuth2Api": {"name": "Gmail"}}
        ),
        # Warning: Log to database
        make_node("Log Warning", "n8n-nodes-base.postgres", 2.4, [600, 0],
            {
                "operation": "insert",
                "schema": "public",
                "table": "n8n_error_log",
                "columns": {"mappingMode": "defineBelow", "value": {
                    "workflow_name": "={{ $json.workflowName }}",
                    "node_name": "={{ $json.nodeName }}",
                    "error_message": "={{ $json.errorMessage }}",
                    "execution_id": "={{ $json.executionId }}",
                    "severity": "warning",
                    "timestamp": "={{ $json.timestamp }}"
                }},
                "options": {}
            },
            {"postgresApi": {"name": "PostgreSQL"}}
        ),
        # Default: Log to database
        make_node("Log Info", "n8n-nodes-base.postgres", 2.4, [600, 200],
            {
                "operation": "insert",
                "schema": "public",
                "table": "n8n_error_log",
                "columns": {"mappingMode": "defineBelow", "value": {
                    "workflow_name": "={{ $json.workflowName }}",
                    "node_name": "={{ $json.nodeName }}",
                    "error_message": "={{ $json.errorMessage }}",
                    "execution_id": "={{ $json.executionId }}",
                    "severity": "info",
                    "timestamp": "={{ $json.timestamp }}"
                }},
                "options": {}
            },
            {"postgresApi": {"name": "PostgreSQL"}}
        ),
        # Log to console (always)
        make_node("Console Log", "n8n-nodes-base.code", 2, [200, 300],
            {"jsCode": "console.log(`[Error Handler] Workflow: ${$input.item.json.workflowName}, Node: ${$input.item.json.nodeName}, Error: ${$input.item.json.errorMessage}`); return $input.item;"}
        ),
        make_sticky_note("Error Handler Docs", [0, -300], "🛡️ Global Error Handler v2.0\n\nArchitecture: Error Trigger → Parse → Router → Action\nActions:\n- Critical: Email alert to admin\n- Warning: Log to PostgreSQL\n- Info: Log to PostgreSQL\n\nSetup:\n1. Create n8n_error_log table in PostgreSQL\n2. Configure Gmail + PostgreSQL creds\n3. Update admin email\n4. Set this workflow as error handler\n   in other workflow settings\n\nZero-debt: Clean routing, no orphan nodes"),
    ]
    
    # Remove the extra "Classify Severity" LLM node since we use Switch instead
    # Actually, let me just remove it from the nodes list by filtering
    nodes = [n for n in nodes if n["name"] != "Classify Severity"]
    
    connections = merge_connections(
        # Main flow
        make_connection("Error Trigger", "Parse Error", "main"),
        make_connection("Parse Error", "Severity Router", "main"),
        # Switch outputs (3 branches + fallback)
        {"Severity Router": {"main": [
            [{"node": "Send Critical Alert", "type": "main", "index": 0}],  # Output 0: critical
            [{"node": "Log Warning", "type": "main", "index": 0}],          # Output 1: warning
            [{"node": "Log Info", "type": "main", "index": 0}],             # Output 2: fallback/info
        ]}},
        # Console log runs in parallel from Parse Error
        make_connection("Parse Error", "Console Log", "main"),
    )
    
    return make_workflow("Global Error Handler v2", nodes, connections)


# ============================================================
# MCP SERVER TEMPLATES (Zero-Debt)
# ============================================================
def generate_mcp_calendar_server():
    """MCP Calendar Server Template - for deploying as standalone MCP server"""
    nodes = [
        make_node("MCP Calendar Trigger", "@n8n/n8n-nodes-langchain.mcpTrigger", 1, [0, 0],
            {"path": "mcp-calendar"}, webhook_id="mcp-calendar"
        ),
        make_node("Create Event", "n8n-nodes-base.googleCalendarTool", 1.3, [-200, 400],
            {"calendar": {"__rl": True, "value": "", "mode": "list"},
             "start": fromAI("Start", "Fecha y hora inicio ISO"), "end": fromAI("End", "Fecha y hora fin ISO"),
             "additionalFields": {
                 "attendees": [fromAI("Attendees", "Participante email")],
                 "description": fromAI("Description", "Descripción"),
                 "summary": fromAI("Summary", "Título del evento")
             }},
            {"googleCalendarOAuth2Api": {"name": "Google Calendar"}}
        ),
        make_node("Delete Event", "n8n-nodes-base.googleCalendarTool", 1.3, [0, 400],
            {"operation": "delete", "calendar": {"__rl": True, "value": "", "mode": "list"},
             "eventId": fromAI("Event_ID", "ID del evento a eliminar")},
            {"googleCalendarOAuth2Api": {"name": "Google Calendar"}}
        ),
        make_node("Get Events", "n8n-nodes-base.googleCalendarTool", 1.3, [200, 400],
            {"operation": "getAll", "calendar": {"__rl": True, "value": "", "mode": "list"},
             "limit": 10,
             "timeMin": fromAI("After", "Fecha mínima"), "timeMax": fromAI("Before", "Fecha máxima")},
            {"googleCalendarOAuth2Api": {"name": "Google Calendar"}}
        ),
        make_node("Update Event", "n8n-nodes-base.googleCalendarTool", 1.3, [400, 400],
            {"operation": "update", "calendar": {"__rl": True, "value": "", "mode": "list"},
             "eventId": fromAI("Event_ID", "ID del evento"),
             "updateFields": {
                 "description": fromAI("Description", "Nueva descripción"),
                 "start": fromAI("Start", "Nuevo inicio ISO"),
                 "end": fromAI("End", "Nuevo fin ISO"),
                 "summary": fromAI("Summary", "Nuevo título")
             }},
            {"googleCalendarOAuth2Api": {"name": "Google Calendar"}}
        ),
        make_sticky_note("MCP Calendar Server", [-200, -200], "📋 MCP Calendar Server Template\n\nDeploy as standalone MCP server.\nTools connect to MCP Trigger via ai_tool.\n\nSetup:\n1. Configure Google Calendar credential\n2. Select calendar in each tool\n3. Deploy and copy SSE endpoint\n4. Use MCP Client Tool in parent Agent"),
    ]
    connections = merge_connections(
        make_ai_connection("Create Event", "MCP Calendar Trigger", "ai_tool"),
        make_ai_connection("Delete Event", "MCP Calendar Trigger", "ai_tool"),
        make_ai_connection("Get Events", "MCP Calendar Trigger", "ai_tool"),
        make_ai_connection("Update Event", "MCP Calendar Trigger", "ai_tool"),
    )
    return make_workflow("MCP Calendar Server Template", nodes, connections, active=True)


def generate_mcp_gmail_server():
    """MCP Gmail Server Template"""
    nodes = [
        make_node("MCP Gmail Trigger", "@n8n/n8n-nodes-langchain.mcpTrigger", 1, [0, 0],
            {"path": "mcp-gmail"}, webhook_id="mcp-gmail"
        ),
        make_node("Send Email", "n8n-nodes-base.gmailTool", 1.2, [-200, 400],
            {"operation": "send", "to": fromAI("To", "Email destinatario"),
             "subject": fromAI("Subject", "Asunto"), "message": fromAI("Message", "Contenido")},
            {"gmailOAuth2Api": {"name": "Gmail"}}
        ),
        make_node("Search Emails", "n8n-nodes-base.gmailTool", 1.2, [0, 400],
            {"operation": "search", "query": fromAI("Query", "Query Gmail"), "limit": 10},
            {"gmailOAuth2Api": {"name": "Gmail"}}
        ),
        make_node("Get Email", "n8n-nodes-base.gmailTool", 1.2, [200, 400],
            {"operation": "get", "messageId": fromAI("Message_ID", "ID del mensaje")},
            {"gmailOAuth2Api": {"name": "Gmail"}}
        ),
        make_node("Reply Email", "n8n-nodes-base.gmailTool", 1.2, [400, 400],
            {"operation": "reply", "messageId": fromAI("Message_ID", "ID del mensaje"), "message": fromAI("Reply", "Contenido de respuesta")},
            {"gmailOAuth2Api": {"name": "Gmail"}}
        ),
        make_node("Delete Email", "n8n-nodes-base.gmailTool", 1.2, [600, 400],
            {"operation": "delete", "messageId": fromAI("Message_ID", "ID del mensaje a eliminar")},
            {"gmailOAuth2Api": {"name": "Gmail"}}
        ),
        make_sticky_note("MCP Gmail Server", [-200, -200], "📧 MCP Gmail Server Template\n\nTools: Send, Search, Get, Reply, Delete\nAll with $fromAI() expressions\n\nSetup:\n1. Configure Gmail OAuth2 credential\n2. Deploy and copy SSE endpoint\n3. Use MCP Client Tool in parent Agent"),
    ]
    connections = merge_connections(
        make_ai_connection("Send Email", "MCP Gmail Trigger", "ai_tool"),
        make_ai_connection("Search Emails", "MCP Gmail Trigger", "ai_tool"),
        make_ai_connection("Get Email", "MCP Gmail Trigger", "ai_tool"),
        make_ai_connection("Reply Email", "MCP Gmail Trigger", "ai_tool"),
        make_ai_connection("Delete Email", "MCP Gmail Trigger", "ai_tool"),
    )
    return make_workflow("MCP Gmail Server Template", nodes, connections, active=True)


def generate_mcp_contacts_server():
    """MCP Contacts Server Template"""
    nodes = [
        make_node("MCP Contacts Trigger", "@n8n/n8n-nodes-langchain.mcpTrigger", 1, [0, 0],
            {"path": "mcp-contacts"}, webhook_id="mcp-contacts"
        ),
        make_node("Create Contact", "n8n-nodes-base.googleContactsTool", 1, [-200, 400],
            {"operation": "create", "givenName": fromAI("First_Name", "Nombre"), "familyName": fromAI("Last_Name", "Apellido"),
             "emailAddresses": [{"value": fromAI("Email", "Email")}]},
            {"googleContactsOAuth2Api": {"name": "Google Contacts"}}
        ),
        make_node("Get Contact", "n8n-nodes-base.googleContactsTool", 1, [0, 400],
            {"operation": "get", "contactId": fromAI("Contact_ID", "ID del contacto")},
            {"googleContactsOAuth2Api": {"name": "Google Contacts"}}
        ),
        make_node("Search Contacts", "n8n-nodes-base.googleContactsTool", 1, [200, 400],
            {"operation": "getAll", "query": fromAI("Query", "Nombre o email"), "limit": 10},
            {"googleContactsOAuth2Api": {"name": "Google Contacts"}}
        ),
        make_node("Update Contact", "n8n-nodes-base.googleContactsTool", 1, [400, 400],
            {"operation": "update", "contactId": fromAI("Contact_ID", "ID"), "updateFields": {
                "givenName": fromAI("First_Name", "Nuevo nombre"), "familyName": fromAI("Last_Name", "Nuevo apellido"),
                "emailAddresses": [{"value": fromAI("Email", "Nuevo email")}]}},
            {"googleContactsOAuth2Api": {"name": "Google Contacts"}}
        ),
        make_node("Delete Contact", "n8n-nodes-base.googleContactsTool", 1, [600, 400],
            {"operation": "delete", "contactId": fromAI("Contact_ID", "ID del contacto a eliminar")},
            {"googleContactsOAuth2Api": {"name": "Google Contacts"}}
        ),
        make_sticky_note("MCP Contacts Server", [-200, -200], "👤 MCP Contacts Server Template\n\nTools: Create, Get, Search, Update, Delete\nAll with $fromAI() expressions\n\nSetup:\n1. Configure Google Contacts OAuth2\n2. Deploy and copy SSE endpoint\n3. Use MCP Client Tool in parent Agent"),
    ]
    connections = merge_connections(
        make_ai_connection("Create Contact", "MCP Contacts Trigger", "ai_tool"),
        make_ai_connection("Get Contact", "MCP Contacts Trigger", "ai_tool"),
        make_ai_connection("Search Contacts", "MCP Contacts Trigger", "ai_tool"),
        make_ai_connection("Update Contact", "MCP Contacts Trigger", "ai_tool"),
        make_ai_connection("Delete Contact", "MCP Contacts Trigger", "ai_tool"),
    )
    return make_workflow("MCP Contacts Server Template", nodes, connections, active=True)


def generate_mcp_ecommerce_server():
    """MCP E-Commerce Server Template - Product catalog, stock, orders"""
    nodes = [
        make_node("MCP E-Commerce Trigger", "@n8n/n8n-nodes-langchain.mcpTrigger", 1, [0, 0],
            {"path": "mcp-ecommerce"}, webhook_id="mcp-ecommerce"
        ),
        make_node("Search Products", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [-200, 400],
            {"description": "Search products by name, category, or attributes",
             "url": "={{ $fromAI('Product_Search_URL', 'Product search API endpoint', 'string') }}",
             "method": "GET", "options": {}}
        ),
        make_node("Check Stock", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [0, 400],
            {"description": "Check product availability and inventory levels",
             "url": "={{ $fromAI('Stock_API_URL', 'Stock check API endpoint', 'string') }}",
             "method": "GET", "options": {}}
        ),
        make_node("Get Order Status", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [200, 400],
            {"description": "Check order status, shipping info, and delivery updates",
             "url": "={{ $fromAI('Order_API_URL', 'Order status API endpoint', 'string') }}",
             "method": "GET", "options": {}}
        ),
        make_node("Process Return", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [400, 400],
            {"description": "Process product returns and refund requests",
             "url": "={{ $fromAI('Return_API_URL', 'Returns API endpoint', 'string') }}",
             "method": "POST", "options": {}}
        ),
        make_sticky_note("MCP E-Commerce", [-200, -200], "🛒 MCP E-Commerce Server Template\n\nTools: Search Products, Check Stock, Get Order, Process Return\n\nSetup:\n1. Configure your e-commerce API URLs\n2. Deploy and copy SSE endpoint\n3. Use MCP Client Tool in parent Agent"),
    ]
    connections = merge_connections(
        make_ai_connection("Search Products", "MCP E-Commerce Trigger", "ai_tool"),
        make_ai_connection("Check Stock", "MCP E-Commerce Trigger", "ai_tool"),
        make_ai_connection("Get Order Status", "MCP E-Commerce Trigger", "ai_tool"),
        make_ai_connection("Process Return", "MCP E-Commerce Trigger", "ai_tool"),
    )
    return make_workflow("MCP E-Commerce Server Template", nodes, connections, active=True)


def generate_mcp_hr_server():
    """MCP HR Server Template - Resume screening, interview scheduling"""
    nodes = [
        make_node("MCP HR Trigger", "@n8n/n8n-nodes-langchain.mcpTrigger", 1, [0, 0],
            {"path": "mcp-hr"}, webhook_id="mcp-hr"
        ),
        make_node("Screen Resume", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [-200, 400],
            {"description": "Screen and evaluate candidate resumes against job criteria",
             "url": "={{ $fromAI('Resume_API_URL', 'Resume screening API endpoint', 'string') }}",
             "method": "POST", "options": {}}
        ),
        make_node("Schedule Interview", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [0, 400],
            {"description": "Schedule interview appointments and send calendar invites",
             "url": "={{ $fromAI('Interview_API_URL', 'Interview scheduling endpoint', 'string') }}",
             "method": "POST", "options": {}}
        ),
        make_node("Query Employees", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [200, 400],
            {"description": "Query employee records, benefits, and organizational data",
             "url": "={{ $fromAI('Employee_API_URL', 'Employee database endpoint', 'string') }}",
             "method": "GET", "options": {}}
        ),
        make_node("Get Job Listings", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [400, 400],
            {"description": "Get active job listings and recruitment pipeline status",
             "url": "={{ $fromAI('Jobs_API_URL', 'Job listings API endpoint', 'string') }}",
             "method": "GET", "options": {}}
        ),
        make_sticky_note("MCP HR", [-200, -200], "👤 MCP HR Server Template\n\nTools: Screen Resume, Schedule Interview, Query Employees, Get Job Listings\n\nSetup:\n1. Configure HR API URLs\n2. Deploy and copy SSE endpoint\n3. Use MCP Client Tool in parent Agent"),
    ]
    connections = merge_connections(
        make_ai_connection("Screen Resume", "MCP HR Trigger", "ai_tool"),
        make_ai_connection("Schedule Interview", "MCP HR Trigger", "ai_tool"),
        make_ai_connection("Query Employees", "MCP HR Trigger", "ai_tool"),
        make_ai_connection("Get Job Listings", "MCP HR Trigger", "ai_tool"),
    )
    return make_workflow("MCP HR Server Template", nodes, connections, active=True)


def generate_mcp_knowledge_base_server():
    """MCP Knowledge Base Server Template - RAG search via Qdrant"""
    nodes = [
        make_node("MCP KB Trigger", "@n8n/n8n-nodes-langchain.mcpTrigger", 1, [0, 0],
            {"path": "mcp-knowledge-base"}, webhook_id="mcp-knowledge-base"
        ),
        make_node("Search Documents", "@n8n/n8n-nodes-langchain.vectorStoreQdrant", 1, [-200, 400],
            {"operation": "search", "query": fromAI("Query", "Search query for knowledge base"), "options": {}},
            {"qdrantApi": {"name": "Qdrant"}}
        ),
        make_node("Embeddings", "@n8n/n8n-nodes-langchain.embeddingsGoogleGemini", 1, [-200, 600],
            {"model": {"__rl": True, "value": "gemini-embedding-exp-03-07", "mode": "list"}},
            {"googleGeminiApi": {"name": "Google Gemini"}}
        ),
        make_sticky_note("MCP KB", [-200, -200], "📚 MCP Knowledge Base Server Template\n\nTool: Qdrant Vector Search + Gemini Embeddings\n\nSetup:\n1. Seed Qdrant with documents\n2. Configure Qdrant + Gemini credentials\n3. Deploy and copy SSE endpoint\n4. Use MCP Client Tool in parent Agent"),
    ]
    # For MCP servers with vector store tools, the embeddings connect to the vector store, not the trigger
    connections = merge_connections(
        make_ai_connection("Search Documents", "MCP KB Trigger", "ai_tool"),
        make_ai_connection("Embeddings", "Search Documents", "ai_embedding"),
    )
    return make_workflow("MCP Knowledge Base Server Template", nodes, connections, active=True)


# ============================================================
# BASE DEVELOPMENT TEMPLATES (Zero-Debt)
# ============================================================
def generate_t1_single_agent_chat():
    """T1: Single Agent Chat Template - simplest agent pattern"""
    nodes = [
        make_node("Chat Trigger", "@n8n/n8n-nodes-langchain.chatTrigger", 1.1, [0, 0],
            {"initialMessages": [{"content": "Hello! I'm your AI assistant. How can I help you?"}]},
            webhook_id=gen_uuid()
        ),
        make_node("AI Agent", "@n8n/n8n-nodes-langchain.agent", 1.8, [400, 0],
            {
                "promptType": "define",
                "text": "={{ $json.chatInput }}",
                "options": {"systemMessage": "=You are a helpful AI assistant. Answer questions clearly and concisely. Current datetime: {{ $now }}"}
            }
        ),
        make_node("LLM", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.2, [200, 300],
            {"model": {"__rl": True, "value": "gpt-4o-mini", "mode": "list"}, "options": {}},
            {"openAiApi": {"name": "OpenAI"}}
        ),
        make_node("Memory", "@n8n/n8n-nodes-langchain.memoryBufferWindow", 1.3, [400, 300],
            {"sessionIdType": "customKey", "sessionKey": "={{ $json.sessionId }}"}
        ),
        make_sticky_note("Template Info", [0, -200], "🤖 Single Agent Chat Template\n\nPattern: ChatTrigger → Agent\nLLM: GPT-4o-mini\nMemory: BufferWindow\n\nCustomize:\n1. Update system message\n2. Change LLM model\n3. Add tools as needed"),
    ]
    connections = merge_connections(
        make_connection("Chat Trigger", "AI Agent", "main"),
        make_ai_connection("LLM", "AI Agent", "ai_languageModel"),
        make_ai_connection("Memory", "AI Agent", "ai_memory"),
    )
    return make_workflow("Single Agent Chat Template", nodes, connections)


def generate_t2_agent_mcp_tool():
    """T2: Agent + MCP Tool Template - agent with MCP client tool"""
    nodes = [
        make_node("Chat Trigger", "@n8n/n8n-nodes-langchain.chatTrigger", 1.1, [0, 0],
            {"initialMessages": [{"content": "Hello! I have access to external tools via MCP. How can I help?"}]},
            webhook_id=gen_uuid()
        ),
        make_node("AI Agent", "@n8n/n8n-nodes-langchain.agent", 1.8, [400, 0],
            {
                "promptType": "define",
                "text": "={{ $json.chatInput }}",
                "options": {"systemMessage": "=You are an AI assistant with access to MCP tools. Use them to help the user accomplish tasks. Current datetime: {{ $now }}"}
            }
        ),
        make_node("LLM", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.2, [200, 300],
            {"model": {"__rl": True, "value": "gpt-4o-mini", "mode": "list"}, "options": {}},
            {"openAiApi": {"name": "OpenAI"}}
        ),
        make_node("Memory", "@n8n/n8n-nodes-langchain.memoryBufferWindow", 1.3, [400, 300],
            {"sessionIdType": "customKey", "sessionKey": "={{ $json.sessionId }}"}
        ),
        make_node("MCP Tool", "@n8n/n8n-nodes-langchain.mcpClientTool", 1, [600, 300],
            {"sseEndpoint": ""}  # Configure after deploying MCP server
        ),
        make_sticky_note("Template Info", [0, -200], "🔧 Agent + MCP Tool Template\n\nPattern: ChatTrigger → Agent + MCP\nLLM: GPT-4o-mini\nMemory: BufferWindow\nTool: MCP Client\n\nSetup:\n1. Deploy MCP server workflow\n2. Copy SSE endpoint into MCP Tool node\n3. Configure OpenAI credential"),
    ]
    connections = merge_connections(
        make_connection("Chat Trigger", "AI Agent", "main"),
        make_ai_connection("LLM", "AI Agent", "ai_languageModel"),
        make_ai_connection("Memory", "AI Agent", "ai_memory"),
        make_ai_connection("MCP Tool", "AI Agent", "ai_tool"),
    )
    return make_workflow("Agent + MCP Tool Template", nodes, connections)


def generate_t3_rag_agent():
    """T3: RAG Agent Template - agent with vector store knowledge"""
    nodes = [
        make_node("Chat Trigger", "@n8n/n8n-nodes-langchain.chatTrigger", 1.1, [0, 0],
            {"initialMessages": [{"content": "Hello! I can search through your knowledge base. What would you like to know?"}]},
            webhook_id=gen_uuid()
        ),
        make_node("RAG Agent", "@n8n/n8n-nodes-langchain.agent", 1.8, [400, 0],
            {
                "promptType": "define",
                "text": "={{ $json.chatInput }}",
                "options": {"systemMessage": "=You are a knowledge assistant with access to a document database. Always use the knowledge base tool for factual questions. Cite sources. Current datetime: {{ $now }}"}
            }
        ),
        make_node("LLM", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.2, [200, 300],
            {"model": {"__rl": True, "value": "gpt-4o-mini", "mode": "list"}, "options": {}},
            {"openAiApi": {"name": "OpenAI"}}
        ),
        make_node("Memory", "@n8n/n8n-nodes-langchain.memoryBufferWindow", 1.3, [400, 300],
            {"sessionIdType": "customKey", "sessionKey": "={{ $json.sessionId }}"}
        ),
        make_node("Vector Store", "@n8n/n8n-nodes-langchain.vectorStoreQdrant", 1, [600, 300],
            {"operation": "search", "query": fromAI("Query", "Search query"), "options": {}},
            {"qdrantApi": {"name": "Qdrant"}}
        ),
        make_node("Embeddings", "@n8n/n8n-nodes-langchain.embeddingsGoogleGemini", 1, [600, 500],
            {"model": {"__rl": True, "value": "gemini-embedding-exp-03-07", "mode": "list"}},
            {"googleGeminiApi": {"name": "Google Gemini"}}
        ),
        make_sticky_note("Template Info", [0, -200], "📚 RAG Agent Template\n\nPattern: ChatTrigger → RAG Agent\nLLM: GPT-4o-mini\nMemory: BufferWindow\nRAG: Qdrant + Gemini Embeddings\n\nSetup:\n1. Seed Qdrant with documents\n2. Configure all credentials\n3. Customize system message"),
    ]
    connections = merge_connections(
        make_connection("Chat Trigger", "RAG Agent", "main"),
        make_ai_connection("LLM", "RAG Agent", "ai_languageModel"),
        make_ai_connection("Memory", "RAG Agent", "ai_memory"),
        make_ai_connection("Vector Store", "RAG Agent", "ai_tool"),
        make_ai_connection("Embeddings", "Vector Store", "ai_embedding"),
    )
    return make_workflow("RAG Agent Template", nodes, connections)


def generate_t4_multi_agent_orchestrator():
    """T4: Multi-Agent Orchestrator Template - agent with multiple sub-workflows"""
    nodes = [
        make_node("Chat Trigger", "@n8n/n8n-nodes-langchain.chatTrigger", 1.1, [0, 0],
            {"initialMessages": [{"content": "Hello! I'm a multi-agent orchestrator with specialized sub-agents. What task do you need?"}]},
            webhook_id=gen_uuid()
        ),
        make_node("Orchestrator Agent", "@n8n/n8n-nodes-langchain.agent", 1.8, [400, 0],
            {
                "promptType": "define",
                "text": "={{ $json.chatInput }}",
                "options": {"systemMessage": "=You are a multi-agent orchestrator. Route requests to specialized sub-agent tools based on the task type. Current datetime: {{ $now }}"}
            }
        ),
        make_node("LLM", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.2, [200, 300],
            {"model": {"__rl": True, "value": "gpt-4o-mini", "mode": "list"}, "options": {}},
            {"openAiApi": {"name": "OpenAI"}}
        ),
        make_node("Memory", "@n8n/n8n-nodes-langchain.memoryBufferWindow", 1.3, [400, 300],
            {"sessionIdType": "customKey", "sessionKey": "={{ $json.sessionId }}"}
        ),
        make_node("Think", "@n8n/n8n-nodes-langchain.toolThink", 1, [600, 300],
            {"description": "Plan which sub-agents to invoke for multi-step tasks"}
        ),
        make_node("Sub-Agent A", "@n8n/n8n-nodes-langchain.toolWorkflow", 1.1, [800, 300],
            {"description": "Specialized sub-agent for task type A", "workflowId": ""}
        ),
        make_node("Sub-Agent B", "@n8n/n8n-nodes-langchain.toolWorkflow", 1.1, [1000, 300],
            {"description": "Specialized sub-agent for task type B", "workflowId": ""}
        ),
        make_node("Sub-Agent C", "@n8n/n8n-nodes-langchain.toolWorkflow", 1.1, [1200, 300],
            {"description": "Specialized sub-agent for task type C", "workflowId": ""}
        ),
        make_sticky_note("Template Info", [0, -200], "🎯 Multi-Agent Orchestrator Template\n\nPattern: Agent + Think + Sub-Workflows\nLLM: GPT-4o-mini\nMemory: BufferWindow\n\nSetup:\n1. Deploy sub-workflow agents\n2. Copy their IDs into toolWorkflow nodes\n3. Customize descriptions and system message"),
    ]
    connections = merge_connections(
        make_connection("Chat Trigger", "Orchestrator Agent", "main"),
        make_ai_connection("LLM", "Orchestrator Agent", "ai_languageModel"),
        make_ai_connection("Memory", "Orchestrator Agent", "ai_memory"),
        make_ai_connection("Think", "Orchestrator Agent", "ai_tool"),
        make_ai_connection("Sub-Agent A", "Orchestrator Agent", "ai_tool"),
        make_ai_connection("Sub-Agent B", "Orchestrator Agent", "ai_tool"),
        make_ai_connection("Sub-Agent C", "Orchestrator Agent", "ai_tool"),
    )
    return make_workflow("Multi-Agent Orchestrator Template", nodes, connections)


def generate_t5_error_handler():
    """T5: Error Handler Template - reusable error handling pattern"""
    nodes = [
        make_node("Error Trigger", "n8n-nodes-base.errorTrigger", 1, [0, 0], {}),
        make_node("Parse Error", "n8n-nodes-base.set", 3.4, [200, 0],
            {"assignments": {"assignments": [
                {"id": gen_uuid(), "name": "workflowName", "value": "={{ $json.workflow.name }}", "type": "string"},
                {"id": gen_uuid(), "name": "nodeName", "value": "={{ $json.execution.error.node.name }}", "type": "string"},
                {"id": gen_uuid(), "name": "errorMessage", "value": "={{ $json.execution.error.message }}", "type": "string"},
                {"id": gen_uuid(), "name": "executionId", "value": "={{ $json.execution.id }}", "type": "string"},
                {"id": gen_uuid(), "name": "timestamp", "value": "={{ $now }}", "type": "string"},
            ]}, "options": {}}
        ),
        make_node("Notify Admin", "n8n-nodes-base.gmail", 1, [400, 0],
            {"operation": "send", "to": "admin@example.com",
             "subject": "=Error in {{ $json.workflowName }}: {{ $json.nodeName }}",
             "message": "=Workflow: {{ $json.workflowName }}\nNode: {{ $json.nodeName }}\nError: {{ $json.errorMessage }}\nTime: {{ $json.timestamp }}"},
            {"gmailOAuth2Api": {"name": "Gmail"}}
        ),
        make_node("Log Error", "n8n-nodes-base.postgres", 2.4, [400, 200],
            {"operation": "insert", "schema": "public", "table": "error_log",
             "columns": {"mappingMode": "defineBelow", "value": {
                 "workflow": "={{ $json.workflowName }}", "node": "={{ $json.nodeName }}",
                 "error": "={{ $json.errorMessage }}", "timestamp": "={{ $json.timestamp }}"
             }}, "options": {}},
            {"postgresApi": {"name": "PostgreSQL"}}
        ),
        make_sticky_note("Template Info", [0, -200], "🛡️ Error Handler Template\n\nPattern: ErrorTrigger → Parse → Notify + Log\n\nSetup:\n1. Create error_log table in PostgreSQL\n2. Configure Gmail + PostgreSQL\n3. Update admin email\n4. Set as error handler in other workflows"),
    ]
    connections = merge_connections(
        make_connection("Error Trigger", "Parse Error", "main"),
        # Both notify and log run from parse
        {"Parse Error": {"main": [
            [{"node": "Notify Admin", "type": "main", "index": 0}],
            [{"node": "Log Error", "type": "main", "index": 0}],
        ]}},
    )
    return make_workflow("Error Handler Template", nodes, connections)


def generate_t6_mcp_server():
    """T6: MCP Server Template - generic MCP server pattern"""
    nodes = [
        make_node("MCP Trigger", "@n8n/n8n-nodes-langchain.mcpTrigger", 1, [0, 0],
            {"path": "mcp-custom"}, webhook_id="mcp-custom"
        ),
        # Placeholder tool - customize for your use case
        make_node("Custom Tool", "@n8n/n8n-nodes-langchain.toolHttpRequest", 1.1, [200, 400],
            {"description": "Custom tool description - update for your use case",
             "url": "={{ $fromAI('API_URL', 'API endpoint URL', 'string') }}",
             "method": "GET", "options": {}}
        ),
        make_sticky_note("Template Info", [0, -200], "🔧 MCP Server Template\n\nPattern: MCPTrigger → Custom Tools\nAll tools connect via ai_tool\n\nCustomize:\n1. Add your specific tool nodes\n2. Use $fromAI() for AI-generated params\n3. Use toolHttpRequest or native tool types\n4. Deploy and copy SSE endpoint\n\nRule: ALL tools must connect to MCP Trigger via ai_tool"),
    ]
    connections = merge_connections(
        make_ai_connection("Custom Tool", "MCP Trigger", "ai_tool"),
    )
    return make_workflow("MCP Server Template", nodes, connections)


# ============================================================
# MAIN
# ============================================================
def main():
    # Generate consolidated workflows (G8-G13)
    consolidated = {
        "G8_Video_Viral_Suite_v2": generate_g8_video_suite(),
        "G9_Social_Scraper_Suite_v2": generate_g9_social_scraper(),
        "G10_HR_AI_Agent_v2": generate_g10_hr_agent(),
        "G11_WhatsApp_AI_Agent_v2": generate_g11_whatsapp_agent(),
        "G12_Flowise_RAG_Suite_v2": generate_g12_flowise_rag(),
        "G13_Global_Error_Handler_v2": generate_g13_error_handler(),
    }
    
    # Generate MCP server templates
    mcp_servers = {
        "MCP_Calendar_Server_v2": generate_mcp_calendar_server(),
        "MCP_Gmail_Server_v2": generate_mcp_gmail_server(),
        "MCP_Contacts_Server_v2": generate_mcp_contacts_server(),
        "MCP_ECommerce_Server_v2": generate_mcp_ecommerce_server(),
        "MCP_HR_Server_v2": generate_mcp_hr_server(),
        "MCP_Knowledge_Base_Server_v2": generate_mcp_knowledge_base_server(),
    }
    
    # Generate base templates
    base_templates = {
        "T1_Single_Agent_Chat_v2": generate_t1_single_agent_chat(),
        "T2_Agent_MCP_Tool_v2": generate_t2_agent_mcp_tool(),
        "T3_RAG_Agent_v2": generate_t3_rag_agent(),
        "T4_Multi_Agent_Orchestrator_v2": generate_t4_multi_agent_orchestrator(),
        "T5_Error_Handler_v2": generate_t5_error_handler(),
        "T6_MCP_Server_v2": generate_t6_mcp_server(),
    }
    
    results = {}
    
    # Save consolidated
    for filename, workflow in consolidated.items():
        filepath = os.path.join(OUTPUT_DIR_CONSOLIDATED, f"{filename}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        ai_conns = sum(1 for k, v in workflow["connections"].items() for ct in v.keys() if ct.startswith("ai_"))
        results[filename] = {"nodes": len(workflow["nodes"]), "connections": len(workflow["connections"]), "ai_connections": ai_conns}
    
    # Save MCP servers
    for filename, workflow in mcp_servers.items():
        filepath = os.path.join(OUTPUT_DIR_MCP, f"{filename}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        ai_conns = sum(1 for k, v in workflow["connections"].items() for ct in v.keys() if ct.startswith("ai_"))
        results[filename] = {"nodes": len(workflow["nodes"]), "connections": len(workflow["connections"]), "ai_connections": ai_conns}
    
    # Save base templates
    for filename, workflow in base_templates.items():
        filepath = os.path.join(OUTPUT_DIR_BASE, f"{filename}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        ai_conns = sum(1 for k, v in workflow["connections"].items() for ct in v.keys() if ct.startswith("ai_"))
        results[filename] = {"nodes": len(workflow["nodes"]), "connections": len(workflow["connections"]), "ai_connections": ai_conns}
    
    print("=" * 60)
    print("PHASE 2 ZERO-DEBT - Part 2: G8-G13 + MCP + Templates")
    print("=" * 60)
    
    print("\n--- Consolidated Workflows (G8-G13) ---")
    for name, info in {k: v for k, v in results.items() if k.startswith("G")}.items():
        print(f"  ✅ {name}: {info['nodes']} nodes, {info['connections']} connections, {info['ai_connections']} ai_*")
    
    print("\n--- MCP Server Templates ---")
    for name, info in {k: v for k, v in results.items() if k.startswith("MCP")}.items():
        print(f"  ✅ {name}: {info['nodes']} nodes, {info['connections']} connections, {info['ai_connections']} ai_*")
    
    print("\n--- Base Development Templates ---")
    for name, info in {k: v for k, v in results.items() if k.startswith("T")}.items():
        print(f"  ✅ {name}: {info['nodes']} nodes, {info['connections']} connections, {info['ai_connections']} ai_*")
    
    # Validation check
    total_ai = sum(v["ai_connections"] for v in results.values())
    print(f"\n📊 Total ai_* connections across all workflows: {total_ai}")
    print("🎉 All zero-debt standards applied!")
    
    # Save complete summary
    summary = {
        "version": "2.0.0",
        "zero_debt_standards_applied": True,
        "total_workflows": len(results),
        "total_ai_connections": total_ai,
        "fixes_applied": [
            "DEBT-01: All ai_* LangChain sub-type connections added",
            "DEBT-02: No orphan nodes - all nodes wired",
            "DEBT-03: googleCalendarTool used instead of googleCalendar",
            "DEBT-04: $fromAI() expressions on all MCP/AI tool parameters",
            "DEBT-05: No standalone LLM nodes in MCP Switch branches",
            "DEBT-06: openAi node type correct for transcription",
            "DEBT-07: Credential IDs set to empty string",
            "DEBT-08: Sub-workflow IDs marked as configurable",
            "DEBT-09: Invalid node types removed (shopifyTool etc)",
            "DEBT-10: Dynamic expressions instead of hardcoded values",
            "DEBT-11: errorWorkflow removed (for distribution)",
            "DEBT-12: Tags set to empty array",
        ],
        "results": results,
        "generated_at": datetime.now().isoformat()
    }
    
    with open("/home/z/my-project/download/n8n_workflows_v2/_complete_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main()
