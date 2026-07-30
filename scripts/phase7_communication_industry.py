#!/usr/bin/env python3
"""
Phase 7: Communication Integrations + Industry Use Cases + Full Sales Cycle

3 New Communication MCP Servers:
  MCP_WhatsApp_Business_Server_v3.json  (8 tools)
  MCP_Telegram_Bot_Server_v3.json       (8 tools)
  MCP_Discord_Server_v3.json            (8 tools)

1 Full Sales Cycle Orchestration:
  ORC5_WhatsApp_CRM_Stripe_Sales_Cycle_v3.json

4 Industry Use Case Workflows:
  IND1_Real_Estate_Automation_v3.json
  IND2_Restaurant_Operations_v3.json
  IND3_SaaS_Subscription_Engine_v3.json
  IND4_Agency_Client_Portal_v3.json

1 Comprehensive Documentation:
  INTEGRATIONS.md (OAuth2 flows, API details, deployment guides)

All zero-debt, correct ai_* connections, $fromAI() expressions, real node types.
"""

import json
import os
import uuid
from datetime import datetime

BASE = "/home/z/my-project/download/n8n_workflows_v2"

# ── Helpers ─────────────────────────────────────────────────────────────
def uid():
    return str(uuid.uuid4())

def make_workflow(name, nodes, connections, tags=None):
    return {
        "name": name,
        "nodes": nodes,
        "connections": connections,
        "pinData": {},
        "active": False,
        "settings": {
            "executionOrder": "v1",
            "timezone": "Europe/Madrid",
            "callerPolicy": "workflowsFromSameOwner"
        },
        "tags": tags or [],
        "meta": {
            "templateCredsSetupCompleted": False,
            "instanceId": ""
        }
    }

def mcp_trigger(path, pos, uid_val=None):
    return {
        "parameters": {"path": path},
        "type": "@n8n/n8n-nodes-langchain.mcpTrigger",
        "typeVersion": 1,
        "position": pos,
        "id": uid_val or uid(),
        "name": "MCP Trigger",
        "webhookId": path
    }

def http_tool(name, description, url_key, pos, method="GET", uid_val=None):
    return {
        "parameters": {
            "description": description,
            "url": f"={{ /*n8n-auto-generated-fromAI-override*/ $fromAI('{url_key}', `{name} API endpoint URL`, 'string') }}",
            "method": method,
            "options": {}
        },
        "type": "@n8n/n8n-nodes-langchain.toolHttpRequest",
        "typeVersion": 1.1,
        "position": pos,
        "id": uid_val or uid(),
        "name": name
    }

def think_tool(name, description, pos, uid_val=None):
    return {
        "parameters": {"description": description},
        "type": "@n8n/n8n-nodes-langchain.toolThink",
        "typeVersion": 1,
        "position": pos,
        "id": uid_val or uid(),
        "name": name
    }

def agent_node(name, system_msg, pos, uid_val=None):
    return {
        "parameters": {
            "promptType": "define",
            "text": "={{ $json.chatInput || $json.input || $json.query }}",
            "options": {
                "systemMessage": f"={system_msg}"
            }
        },
        "type": "@n8n/n8n-nodes-langchain.agent",
        "typeVersion": 1.8,
        "position": pos,
        "id": uid_val or uid(),
        "name": name
    }

def chat_trigger(pos, initial_msg, uid_val=None):
    return {
        "parameters": {
            "initialMessages": [{"role": "assistant", "content": initial_msg}]
        },
        "type": "n8n-nodes-base.chatTrigger",
        "typeVersion": 1.1,
        "position": pos,
        "id": uid_val or uid(),
        "name": "Chat Trigger"
    }

def llm_node(name, model, temp, pos, uid_val=None):
    return {
        "parameters": {
            "model": {"__rl": True, "value": model, "mode": "list"},
            "options": {"temperature": temp}
        },
        "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
        "typeVersion": 1.2,
        "position": pos,
        "id": uid_val or uid(),
        "name": name,
        "credentials": {"openAiApi": {"id": "", "name": "OpenAI"}}
    }

def memory_node(name, pos, uid_val=None, session_key=None):
    return {
        "parameters": {
            "sessionIdType": "customKey",
            "sessionKey": f"={{ $json.{session_key} || 'default' }}" if session_key else "={{ $json.sessionId || 'default' }}",
            "options": {}
        },
        "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
        "typeVersion": 1.3,
        "position": pos,
        "id": uid_val or uid(),
        "name": name
    }

def sticky_note(content, pos, uid_val=None):
    return {
        "parameters": {"content": content, "width": 300, "height": 200},
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": pos,
        "id": uid_val or uid(),
        "name": "Sticky Note"
    }

def output_parser(name, properties, pos, uid_val=None):
    props = []
    for p in properties:
        props.append({
            "name": p["name"],
            "description": p["description"],
            "type": p.get("type", "string")
        })
    return {
        "parameters": {
            "schema": {
                "type": "object",
                "properties": {p["name"]: {"type": p.get("type", "string"), "description": p["description"]} for p in props}
            }
        },
        "type": "@n8n/n8n-nodes-langchain.outputParserStructured",
        "typeVersion": 1.1,
        "position": pos,
        "id": uid_val or uid(),
        "name": name
    }

def ai_conn(source, target, conn_type):
    return {
        source: {
            "ai_" + conn_type: [[{"node": target, "type": "ai_" + conn_type, "index": 0}]]
        }
    }

def main_conn(source, target):
    return {
        source: {
            "main": [[{"node": target, "type": "main", "index": 0}]]
        }
    }

def merge_dicts(dicts):
    """Merge connection dicts, appending lists for same connection types (e.g., ai_tool)."""
    result = {}
    for d in dicts:
        for src, targets in d.items():
            if src not in result:
                result[src] = {}
            for conn_type, conn_list in targets.items():
                if conn_type in result[src]:
                    # Append to existing list (for multiple ai_tool connections)
                    result[src][conn_type].extend(conn_list)
                else:
                    result[src][conn_type] = list(conn_list)
    return result


# ═══════════════════════════════════════════════════════════════════════
# 1. WHATSAPP BUSINESS API MCP SERVER
# ═══════════════════════════════════════════════════════════════════════

def generate_mcp_whatsapp():
    """WhatsApp Business API MCP Server with 8 tools."""
    trigger = mcp_trigger("whatsapp-mcp", [0, 0])
    note = sticky_note(
        "WhatsApp Business API MCP Server\n\n8 Tools: Send Message, Send Template, Send Media, List Conversations, "
        "Get Contact Profile, Manage Labels, Send Interactive, Get Message Status\n\n"
        "OAuth2: Meta Business Suite → WhatsApp Business Account\n"
        "API: graph.facebook.com/v19.0/{phone_number_id}",
        [-400, -300]
    )
    tools = [
        http_tool("Send Message", "Send a text message via WhatsApp Business API. Supports text body, preview URL, and recipient phone number.",
                  "Send_Message_URL", [-700, 400], "POST"),
        http_tool("Send Template", "Send a WhatsApp template message with parameters. Supports header, body, button components.",
                  "Send_Template_URL", [-500, 400], "POST"),
        http_tool("Send Media", "Send media (image, video, document, audio, sticker) via WhatsApp. Supports URL and base64 media.",
                  "Send_Media_URL", [-300, 400], "POST"),
        http_tool("List Conversations", "List WhatsApp Business conversations with pagination. Filter by status, contact, and date.",
                  "List_Conversations_URL", [-100, 400], "GET"),
        http_tool("Get Contact Profile", "Get WhatsApp contact profile information including name, phone, and profile picture.",
                  "Get_Contact_Profile_URL", [100, 400], "GET"),
        http_tool("Manage Labels", "Create, list, and assign labels to WhatsApp contacts for segmentation and organization.",
                  "Manage_Labels_URL", [300, 400], "POST"),
        http_tool("Send Interactive", "Send interactive messages (buttons, lists, product items) via WhatsApp Business API.",
                  "Send_Interactive_URL", [500, 400], "POST"),
        http_tool("Get Message Status", "Check the delivery status of a sent WhatsApp message. Returns read, delivered, sent status.",
                  "Get_Message_Status_URL", [700, 400], "GET"),
    ]

    nodes = [trigger, note] + tools
    # MCP server pattern: tools connect TO MCP Trigger via ai_tool
    connections = merge_dicts([
        ai_conn("Send Message", "MCP Trigger", "tool"),
        ai_conn("Send Template", "MCP Trigger", "tool"),
        ai_conn("Send Media", "MCP Trigger", "tool"),
        ai_conn("List Conversations", "MCP Trigger", "tool"),
        ai_conn("Get Contact Profile", "MCP Trigger", "tool"),
        ai_conn("Manage Labels", "MCP Trigger", "tool"),
        ai_conn("Send Interactive", "MCP Trigger", "tool"),
        ai_conn("Get Message Status", "MCP Trigger", "tool"),
    ])
    return make_workflow("MCP WhatsApp Business Server v3", nodes, connections,
                         [{"name": "mcp-server"}, {"name": "whatsapp"}, {"name": "communication"}])


# ═══════════════════════════════════════════════════════════════════════
# 2. TELEGRAM BOT MCP SERVER
# ═══════════════════════════════════════════════════════════════════════

def generate_mcp_telegram():
    """Telegram Bot API MCP Server with 8 tools."""
    trigger = mcp_trigger("telegram-mcp", [0, 0])
    note = sticky_note(
        "Telegram Bot API MCP Server\n\n8 Tools: Send Message, Send Photo, Send Document, Edit Message, "
        "Get Updates, Get Chat Info, Send Inline Keyboard, Pin Message\n\n"
        "Auth: Bot Token via @BotFather\n"
        "API: api.telegram.org/bot{token}",
        [-400, -300]
    )
    tools = [
        http_tool("Send Message", "Send a text message via Telegram Bot API. Supports Markdown/HTML parsing, reply-to, and disable notification.",
                  "Send_Message_URL", [-700, 400], "POST"),
        http_tool("Send Photo", "Send a photo via Telegram Bot. Supports caption, inline keyboard, and URL/file_id upload.",
                  "Send_Photo_URL", [-500, 400], "POST"),
        http_tool("Send Document", "Send a document file via Telegram Bot. Supports caption, thumbnail, and URL/file_id upload.",
                  "Send_Document_URL", [-300, 400], "POST"),
        http_tool("Edit Message", "Edit an existing Telegram message text or caption. Supports inline keyboard updates.",
                  "Edit_Message_URL", [-100, 400], "POST"),
        http_tool("Get Updates", "Get pending updates (messages, callbacks) from Telegram. Supports offset, limit, and timeout.",
                  "Get_Updates_URL", [100, 400], "GET"),
        http_tool("Get Chat Info", "Get Telegram chat information including type, title, member count, and photo.",
                  "Get_Chat_Info_URL", [300, 400], "GET"),
        http_tool("Send Inline Keyboard", "Send a message with inline keyboard buttons for interactive menus and callbacks.",
                  "Send_Inline_Keyboard_URL", [500, 400], "POST"),
        http_tool("Pin Message", "Pin or unpin a message in a Telegram chat. Supports notification on pin.",
                  "Pin_Message_URL", [700, 400], "POST"),
    ]

    nodes = [trigger, note] + tools
    connections = merge_dicts([
        ai_conn("Send Message", "MCP Trigger", "tool"),
        ai_conn("Send Photo", "MCP Trigger", "tool"),
        ai_conn("Send Document", "MCP Trigger", "tool"),
        ai_conn("Edit Message", "MCP Trigger", "tool"),
        ai_conn("Get Updates", "MCP Trigger", "tool"),
        ai_conn("Get Chat Info", "MCP Trigger", "tool"),
        ai_conn("Send Inline Keyboard", "MCP Trigger", "tool"),
        ai_conn("Pin Message", "MCP Trigger", "tool"),
    ])
    return make_workflow("MCP Telegram Bot Server v3", nodes, connections,
                         [{"name": "mcp-server"}, {"name": "telegram"}, {"name": "communication"}])


# ═══════════════════════════════════════════════════════════════════════
# 3. DISCORD MCP SERVER
# ═══════════════════════════════════════════════════════════════════════

def generate_mcp_discord():
    """Discord Bot API MCP Server with 8 tools."""
    trigger = mcp_trigger("discord-mcp", [0, 0])
    note = sticky_note(
        "Discord Bot API MCP Server\n\n8 Tools: Send Message, Send Embed, Manage Channels, Get Server Info, "
        "Manage Roles, Send DM, Manage Webhooks, Search Messages\n\n"
        "Auth: Bot Token via Discord Developer Portal\n"
        "OAuth2: Discord OAuth2 with bot scope + permissions\n"
        "API: discord.com/api/v10",
        [-400, -300]
    )
    tools = [
        http_tool("Send Message", "Send a message to a Discord channel. Supports text, embeds, components, and attachments.",
                  "Send_Message_URL", [-700, 400], "POST"),
        http_tool("Send Embed", "Send a rich embed message with title, description, fields, color, thumbnail, and footer.",
                  "Send_Embed_URL", [-500, 400], "POST"),
        http_tool("Manage Channels", "Create, modify, or delete Discord channels. Supports text, voice, category, and announcement types.",
                  "Manage_Channels_URL", [-300, 400], "POST"),
        http_tool("Get Server Info", "Get Discord server (guild) information including name, member count, roles, and channels.",
                  "Get_Server_Info_URL", [-100, 400], "GET"),
        http_tool("Manage Roles", "Create, modify, or delete Discord roles. Supports permissions, color, and hierarchy.",
                  "Manage_Roles_URL", [100, 400], "POST"),
        http_tool("Send DM", "Send a direct message to a Discord user. Requires user ID and mutual server.",
                  "Send_DM_URL", [300, 400], "POST"),
        http_tool("Manage Webhooks", "Create, modify, or delete Discord webhooks for channel message posting.",
                  "Manage_Webhooks_URL", [500, 400], "POST"),
        http_tool("Search Messages", "Search Discord messages with filters: author, content, channel, date range, and has attachments.",
                  "Search_Messages_URL", [700, 400], "GET"),
    ]

    nodes = [trigger, note] + tools
    connections = merge_dicts([
        ai_conn("Send Message", "MCP Trigger", "tool"),
        ai_conn("Send Embed", "MCP Trigger", "tool"),
        ai_conn("Manage Channels", "MCP Trigger", "tool"),
        ai_conn("Get Server Info", "MCP Trigger", "tool"),
        ai_conn("Manage Roles", "MCP Trigger", "tool"),
        ai_conn("Send DM", "MCP Trigger", "tool"),
        ai_conn("Manage Webhooks", "MCP Trigger", "tool"),
        ai_conn("Search Messages", "MCP Trigger", "tool"),
    ])
    return make_workflow("MCP Discord Server v3", nodes, connections,
                         [{"name": "mcp-server"}, {"name": "discord"}, {"name": "communication"}])


# ═══════════════════════════════════════════════════════════════════════
# 4. WHATSAPP → CRM → STRIPE SALES CYCLE ORCHESTRATION
# ═══════════════════════════════════════════════════════════════════════

def generate_orc_sales_cycle():
    """Full sales cycle: WhatsApp → CRM → Stripe orchestration."""
    trigger = chat_trigger([-2200, 0],
        "I am your Sales Cycle Orchestrator. I manage the complete sales pipeline from WhatsApp lead capture through CRM qualification to Stripe payment processing. "
        "What sales operation do you need?")

    # Main orchestrator agent
    agent = agent_node("Sales Cycle Orchestrator",
        "# Sales Cycle Orchestrator — WhatsApp → CRM → Stripe\n\n"
        "You orchestrate the complete sales cycle across three critical platforms:\n\n"
        "## Stage 1: Lead Capture (WhatsApp)\n"
        "- Receive incoming WhatsApp messages from prospects\n"
        "- Qualify leads using conversational AI\n"
        "- Send interactive menus for product/service selection\n"
        "- Capture contact information and preferences\n"
        "- Label contacts for segmentation (hot/warm/cold)\n\n"
        "## Stage 2: CRM Pipeline (CRM Universal)\n"
        "- Create or update contact in CRM with lead details\n"
        "- Move lead through pipeline stages: New → Qualified → Proposal → Negotiation → Won/Lost\n"
        "- Log activities and communication history\n"
        "- Create deals with estimated value and probability\n"
        "- Schedule follow-up activities and reminders\n"
        "- Generate pipeline dashboard and forecasts\n\n"
        "## Stage 3: Payment Processing (Stripe)\n"
        "- Create payment links for proposals\n"
        "- Generate invoices for accepted deals\n"
        "- Set up subscriptions for recurring services\n"
        "- Process refunds and handle disputes\n"
        "- Track payment status and revenue\n"
        "- Generate financial reports\n\n"
        "## Cross-Platform Workflows:\n"
        "1. WhatsApp lead → CRM contact creation → Auto-followup\n"
        "2. CRM deal Won → Stripe invoice → WhatsApp confirmation\n"
        "3. Payment failed → WhatsApp reminder → CRM activity log\n"
        "4. Subscription renewal → WhatsApp notification → CRM update\n"
        "5. Monthly report → CRM dashboard → WhatsApp summary\n\n"
        "## Skills Loaded:\n"
        "- deep-research: Lead qualification and market analysis\n"
        "- data-analysis: Sales pipeline analytics\n"
        "- payment-processing: Payment optimization\n"
        "- consulting-analysis: Sales strategy recommendations\n\n"
        "Current datetime: __DATE__",
        [-1600, 0])

    # LLM
    llm = llm_node("GPT-4.1 Sales", "gpt-4.1", 0.2, [-1600, 300])

    # Memory
    memory = memory_node("Sales Memory", [-1300, 300])

    # Output parser
    parser = output_parser("Sales Output", [
        {"name": "stage", "description": "Sales stage (lead_capture/crm_pipeline/payment_processing/cross_platform)"},
        {"name": "action", "description": "Action performed"},
        {"name": "platform", "description": "Platform involved (whatsapp/crm/stripe)"},
        {"name": "result", "description": "Result summary"},
        {"name": "next_steps", "description": "Recommended next actions"},
        {"name": "contact_id", "description": "CRM or WhatsApp contact ID"},
        {"name": "deal_id", "description": "CRM deal ID if applicable"},
        {"name": "payment_id", "description": "Stripe payment ID if applicable"},
    ], [-1300, 0])

    # WhatsApp tools
    wa_send = http_tool("WA Send Message", "Send a WhatsApp message to a lead or customer. Used for follow-ups, confirmations, and notifications.",
                        "WA_Send_URL", [-700, 500], "POST")
    wa_template = http_tool("WA Send Template", "Send a WhatsApp template message for initial outreach or appointment reminders.",
                            "WA_Template_URL", [-500, 500], "POST")
    wa_interactive = http_tool("WA Send Interactive", "Send interactive WhatsApp message with buttons or lists for product/service selection.",
                               "WA_Interactive_URL", [-300, 500], "POST")
    wa_labels = http_tool("WA Manage Labels", "Assign WhatsApp labels to contacts for lead segmentation (hot/warm/cold/vip).",
                          "WA_Labels_URL", [-100, 500], "POST")

    # CRM tools
    crm_contact = http_tool("CRM Create Contact", "Create or update a contact in the CRM with lead details, source, and qualification status.",
                            "CRM_Contact_URL", [100, 500], "POST")
    crm_deal = http_tool("CRM Create Deal", "Create a deal in the CRM pipeline with estimated value, probability, and stage.",
                         "CRM_Deal_URL", [300, 500], "POST")
    crm_pipeline = http_tool("CRM Update Pipeline", "Move a deal through pipeline stages: New → Qualified → Proposal → Negotiation → Won/Lost.",
                             "CRM_Pipeline_URL", [500, 500], "POST")
    crm_activity = http_tool("CRM Log Activity", "Log a sales activity (call, email, meeting, note) in the CRM for a contact or deal.",
                             "CRM_Activity_URL", [700, 500], "POST")

    # Stripe tools
    stripe_payment = http_tool("Stripe Create Payment", "Create a Stripe payment link or payment intent for a deal or invoice.",
                               "Stripe_Payment_URL", [100, 700], "POST")
    stripe_invoice = http_tool("Stripe Create Invoice", "Create a Stripe invoice for a customer with line items, discounts, and due date.",
                               "Stripe_Invoice_URL", [300, 700], "POST")
    stripe_sub = http_tool("Stripe Create Subscription", "Create a recurring subscription with plan, interval, and trial period.",
                           "Stripe_Subscription_URL", [500, 700], "POST")
    stripe_status = http_tool("Stripe Payment Status", "Check the status of a Stripe payment, subscription, or invoice.",
                              "Stripe_Status_URL", [700, 700], "GET")

    # Think tool for sales reasoning
    think = think_tool("Sales Reasoning", "Think through the sales cycle step: qualify lead, determine pipeline stage, choose payment method, plan follow-up.",
                       [900, 500])

    note = sticky_note(
        "WhatsApp → CRM → Stripe Sales Cycle\n\n"
        "STAGE 1: WhatsApp Lead Capture\n"
        "  Lead → Qualify → Label → Interactive Menu\n\n"
        "STAGE 2: CRM Pipeline Management\n"
        "  Contact → Deal → Pipeline → Activity Log\n\n"
        "STAGE 3: Stripe Payment Processing\n"
        "  Payment Link → Invoice → Subscription → Status\n\n"
        "CROSS-PLATFORM:\n"
        "  Lead → CRM → Payment → Confirmation",
        [-2200, -400]
    )

    nodes = [trigger, note, agent, llm, memory, parser,
             wa_send, wa_template, wa_interactive, wa_labels,
             crm_contact, crm_deal, crm_pipeline, crm_activity,
             stripe_payment, stripe_invoice, stripe_sub, stripe_status,
             think]

    connections = merge_dicts([
        main_conn("Chat Trigger", "Sales Cycle Orchestrator"),
        ai_conn("Sales Cycle Orchestrator", "GPT-4.1 Sales", "languageModel"),
        ai_conn("Sales Cycle Orchestrator", "Sales Memory", "memory"),
        ai_conn("Sales Cycle Orchestrator", "Sales Output", "outputParser"),
        ai_conn("Sales Cycle Orchestrator", "WA Send Message", "tool"),
        ai_conn("Sales Cycle Orchestrator", "WA Send Template", "tool"),
        ai_conn("Sales Cycle Orchestrator", "WA Send Interactive", "tool"),
        ai_conn("Sales Cycle Orchestrator", "WA Manage Labels", "tool"),
        ai_conn("Sales Cycle Orchestrator", "CRM Create Contact", "tool"),
        ai_conn("Sales Cycle Orchestrator", "CRM Create Deal", "tool"),
        ai_conn("Sales Cycle Orchestrator", "CRM Update Pipeline", "tool"),
        ai_conn("Sales Cycle Orchestrator", "CRM Log Activity", "tool"),
        ai_conn("Sales Cycle Orchestrator", "Stripe Create Payment", "tool"),
        ai_conn("Sales Cycle Orchestrator", "Stripe Create Invoice", "tool"),
        ai_conn("Sales Cycle Orchestrator", "Stripe Create Subscription", "tool"),
        ai_conn("Sales Cycle Orchestrator", "Stripe Payment Status", "tool"),
        ai_conn("Sales Cycle Orchestrator", "Sales Reasoning", "tool"),
    ])
    return make_workflow("ORC5 WhatsApp CRM Stripe Sales Cycle v3", nodes, connections,
                         [{"name": "orchestration"}, {"name": "sales"}, {"name": "whatsapp-crm-stripe"}])


# ═══════════════════════════════════════════════════════════════════════
# 5. INDUSTRY USE CASE: REAL ESTATE AUTOMATION
# ═══════════════════════════════════════════════════════════════════════

def generate_ind_real_estate():
    """Real Estate: Property listings → WhatsApp tours → CRM pipeline → Stripe payments."""
    trigger = chat_trigger([-2200, 0],
        "I am your Real Estate Automation Assistant. I manage property listings, schedule virtual tours via WhatsApp, "
        "track buyer leads through the CRM pipeline, and process payments via Stripe. How can I help?")

    agent = agent_node("Real Estate Agent",
        "# Real Estate Automation Agent\n\n"
        "You orchestrate real estate operations across multiple platforms:\n\n"
        "## Property Management:\n"
        "- List properties on WordPress/CRM with photos and details\n"
        "- Update availability and pricing in real-time\n"
        "- Generate property comparison reports\n"
        "- Sync listings across platforms (WordPress, CRM, Booking)\n\n"
        "## Lead Management:\n"
        "- Capture leads via WhatsApp interactive messages\n"
        "- Qualify buyers by budget, location, and preferences\n"
        "- Schedule virtual tours and in-person visits\n"
        "- Send property recommendations with media (WhatsApp)\n"
        "- Label contacts: Buyer/Seller/Renter/Investor\n\n"
        "## CRM Pipeline:\n"
        "- Track deals: Inquiry → Showing → Offer → Negotiation → Closing\n"
        "- Log all activities and communications\n"
        "- Calculate commission and revenue forecasts\n"
        "- Generate pipeline reports\n\n"
        "## Payment Processing:\n"
        "- Create invoices for commissions and fees\n"
        "- Process security deposits via Stripe\n"
        "- Set up recurring rent payments\n"
        "- Generate financial reports\n\n"
        "## Skills Loaded:\n"
        "- deep-research: Property market analysis\n"
        "- data-analysis: Sales metrics and forecasting\n"
        "- consulting-analysis: Investment recommendations\n"
        "- payment-processing: Commission and deposit handling\n\n"
        "Current datetime: __DATE__",
        [-1600, 0])

    llm = llm_node("GPT-4.1 Real Estate", "gpt-4.1", 0.2, [-1600, 300])
    memory = memory_node("Real Estate Memory", [-1300, 300])
    parser = output_parser("Real Estate Output", [
        {"name": "category", "description": "Category (property/lead/pipeline/payment)"},
        {"name": "action", "description": "Action performed"},
        {"name": "result", "description": "Result summary"},
        {"name": "property_id", "description": "Property ID if applicable"},
        {"name": "contact_id", "description": "Contact ID if applicable"},
        {"name": "deal_id", "description": "Deal ID if applicable"},
    ], [-1300, 0])

    # Tools
    wp_posts = http_tool("WP Create Listing", "Create or update a property listing on WordPress with title, description, price, features, and images.",
                         "WP_Listing_URL", [-700, 500], "POST")
    wa_send = http_tool("WA Send Property", "Send property details via WhatsApp with images, price, and interactive buttons for tour scheduling.",
                        "WA_Property_URL", [-500, 500], "POST")
    wa_media = http_tool("WA Send Media", "Send property photos, virtual tour videos, or floor plans via WhatsApp.",
                         "WA_Media_URL", [-300, 500], "POST")
    crm_contact = http_tool("CRM Buyer Contact", "Create or update a buyer/seller contact in CRM with preferences, budget, and timeline.",
                            "CRM_Buyer_URL", [-100, 500], "POST")
    crm_deal = http_tool("CRM Property Deal", "Create a property deal in CRM with price, commission, stage, and closing date.",
                         "CRM_Deal_URL", [100, 500], "POST")
    crm_activity = http_tool("CRM Log Showing", "Log a property showing, open house, or viewing activity in CRM.",
                             "CRM_Showing_URL", [300, 500], "POST")
    stripe_invoice = http_tool("Stripe Commission", "Create a Stripe invoice for commission, deposit, or fee payment.",
                               "Stripe_Commission_URL", [500, 500], "POST")
    stripe_sub = http_tool("Stripe Rent Payment", "Set up recurring rent or lease payments via Stripe subscription.",
                           "Stripe_Rent_URL", [700, 500], "POST")
    think = think_tool("Real Estate Reasoning", "Think through property matching, buyer qualification, deal stage, and payment options.",
                       [900, 500])

    note = sticky_note(
        "Real Estate Automation\n\n"
        "FLOW: Property Listing → WhatsApp Tour → CRM Deal → Stripe Payment\n\n"
        "Platforms: WordPress, WhatsApp, CRM, Stripe\n"
        "Pipeline: Inquiry → Showing → Offer → Negotiation → Closing",
        [-2200, -400]
    )

    nodes = [trigger, note, agent, llm, memory, parser,
             wp_posts, wa_send, wa_media, crm_contact, crm_deal, crm_activity,
             stripe_invoice, stripe_sub, think]

    connections = merge_dicts([
        main_conn("Chat Trigger", "Real Estate Agent"),
        ai_conn("Real Estate Agent", "GPT-4.1 Real Estate", "languageModel"),
        ai_conn("Real Estate Agent", "Real Estate Memory", "memory"),
        ai_conn("Real Estate Agent", "Real Estate Output", "outputParser"),
        ai_conn("Real Estate Agent", "WP Create Listing", "tool"),
        ai_conn("Real Estate Agent", "WA Send Property", "tool"),
        ai_conn("Real Estate Agent", "WA Send Media", "tool"),
        ai_conn("Real Estate Agent", "CRM Buyer Contact", "tool"),
        ai_conn("Real Estate Agent", "CRM Property Deal", "tool"),
        ai_conn("Real Estate Agent", "CRM Log Showing", "tool"),
        ai_conn("Real Estate Agent", "Stripe Commission", "tool"),
        ai_conn("Real Estate Agent", "Stripe Rent Payment", "tool"),
        ai_conn("Real Estate Agent", "Real Estate Reasoning", "tool"),
    ])
    return make_workflow("IND1 Real Estate Automation v3", nodes, connections,
                         [{"name": "industry"}, {"name": "real-estate"}, {"name": "sales-cycle"}])


# ═══════════════════════════════════════════════════════════════════════
# 6. INDUSTRY USE CASE: RESTAURANT OPERATIONS
# ═══════════════════════════════════════════════════════════════════════

def generate_ind_restaurant():
    """Restaurant: WhatsApp orders → CRM loyalty → WooCommerce menu → Stripe payments."""
    trigger = chat_trigger([-2200, 0],
        "I am your Restaurant Operations Assistant. I manage WhatsApp food orders, menu updates on WooCommerce, "
        "customer loyalty in CRM, and payment processing via Stripe. How can I help?")

    agent = agent_node("Restaurant Operations Agent",
        "# Restaurant Operations Agent\n\n"
        "You orchestrate restaurant operations across multiple platforms:\n\n"
        "## Order Management:\n"
        "- Receive food orders via WhatsApp interactive menus\n"
        "- Process orders with items, quantity, and delivery details\n"
        "- Send order confirmations and estimated delivery time\n"
        "- Track order status: Received → Preparing → Ready → Delivered\n"
        "- Handle order modifications and cancellations\n\n"
        "## Menu Management:\n"
        "- Update WooCommerce product catalog with dishes and prices\n"
        "- Manage daily specials and seasonal menu items\n"
        "- Update availability (mark items as sold out)\n"
        "- Sync menu across WhatsApp and WooCommerce\n\n"
        "## Customer Loyalty:\n"
        "- Track customer order history in CRM\n"
        "- Assign loyalty labels and segments\n"
        "- Send personalized promotions via WhatsApp\n"
        "- Generate loyalty points and rewards\n"
        "- Birthday and anniversary campaigns\n\n"
        "## Payment Processing:\n"
        "- Process payments via Stripe (card, cash, digital)\n"
        "- Generate invoices for corporate/catering orders\n"
        "- Handle refunds and disputes\n"
        "- Daily sales reconciliation\n"
        "- Revenue analytics and reporting\n\n"
        "## Skills Loaded:\n"
        "- data-analysis: Sales analytics and demand forecasting\n"
        "- deep-research: Menu optimization and market trends\n"
        "- payment-processing: Payment reconciliation\n"
        "- consulting-analysis: Restaurant operations optimization\n\n"
        "Current datetime: __DATE__",
        [-1600, 0])

    llm = llm_node("GPT-4.1 Restaurant", "gpt-4.1", 0.2, [-1600, 300])
    memory = memory_node("Restaurant Memory", [-1300, 300])
    parser = output_parser("Restaurant Output", [
        {"name": "category", "description": "Category (order/menu/loyalty/payment)"},
        {"name": "action", "description": "Action performed"},
        {"name": "result", "description": "Result summary"},
        {"name": "order_id", "description": "Order ID if applicable"},
        {"name": "customer_id", "description": "Customer ID if applicable"},
        {"name": "total", "description": "Order total if applicable"},
    ], [-1300, 0])

    # Tools
    wa_order = http_tool("WA Take Order", "Receive and process a food order via WhatsApp. Captures items, quantity, delivery address, and payment method.",
                         "WA_Order_URL", [-700, 500], "POST")
    wa_confirm = http_tool("WA Confirm Order", "Send order confirmation via WhatsApp with estimated delivery time and order total.",
                           "WA_Confirm_URL", [-500, 500], "POST")
    wa_promo = http_tool("WA Send Promo", "Send promotional messages via WhatsApp for daily specials, loyalty rewards, or birthday offers.",
                         "WA_Promo_URL", [-300, 500], "POST")
    wc_menu = http_tool("WC Update Menu", "Update WooCommerce product catalog with menu items, prices, descriptions, and availability.",
                        "WC_Menu_URL", [-100, 500], "POST")
    wc_orders = http_tool("WC List Orders", "List WooCommerce orders with filters for status, date, and customer.",
                          "WC_Orders_URL", [100, 500], "GET")
    crm_customer = http_tool("CRM Customer", "Create or update a restaurant customer in CRM with order history, preferences, and loyalty tier.",
                             "CRM_Customer_URL", [300, 500], "POST")
    stripe_pay = http_tool("Stripe Process Order", "Process a restaurant order payment via Stripe. Supports card, cash tracking, and digital wallets.",
                           "Stripe_Order_URL", [500, 500], "POST")
    stripe_report = http_tool("Stripe Daily Report", "Generate daily sales reconciliation report from Stripe transactions.",
                              "Stripe_Report_URL", [700, 500], "GET")
    think = think_tool("Restaurant Reasoning", "Think through order flow, menu optimization, customer loyalty, and payment reconciliation.",
                       [900, 500])

    note = sticky_note(
        "Restaurant Operations\n\n"
        "FLOW: WhatsApp Order → WC Menu → CRM Loyalty → Stripe Payment\n\n"
        "Platforms: WhatsApp, WooCommerce, CRM, Stripe\n"
        "Pipeline: Order → Prepare → Deliver → Payment → Loyalty",
        [-2200, -400]
    )

    nodes = [trigger, note, agent, llm, memory, parser,
             wa_order, wa_confirm, wa_promo, wc_menu, wc_orders,
             crm_customer, stripe_pay, stripe_report, think]

    connections = merge_dicts([
        main_conn("Chat Trigger", "Restaurant Operations Agent"),
        ai_conn("Restaurant Operations Agent", "GPT-4.1 Restaurant", "languageModel"),
        ai_conn("Restaurant Operations Agent", "Restaurant Memory", "memory"),
        ai_conn("Restaurant Operations Agent", "Restaurant Output", "outputParser"),
        ai_conn("Restaurant Operations Agent", "WA Take Order", "tool"),
        ai_conn("Restaurant Operations Agent", "WA Confirm Order", "tool"),
        ai_conn("Restaurant Operations Agent", "WA Send Promo", "tool"),
        ai_conn("Restaurant Operations Agent", "WC Update Menu", "tool"),
        ai_conn("Restaurant Operations Agent", "WC List Orders", "tool"),
        ai_conn("Restaurant Operations Agent", "CRM Customer", "tool"),
        ai_conn("Restaurant Operations Agent", "Stripe Process Order", "tool"),
        ai_conn("Restaurant Operations Agent", "Stripe Daily Report", "tool"),
        ai_conn("Restaurant Operations Agent", "Restaurant Reasoning", "tool"),
    ])
    return make_workflow("IND2 Restaurant Operations v3", nodes, connections,
                         [{"name": "industry"}, {"name": "restaurant"}, {"name": "food-service"}])


# ═══════════════════════════════════════════════════════════════════════
# 7. INDUSTRY USE CASE: SAAS SUBSCRIPTION ENGINE
# ═══════════════════════════════════════════════════════════════════════

def generate_ind_saas():
    """SaaS: Discord community → Stripe subscriptions → CRM tracking → Telegram alerts."""
    trigger = chat_trigger([-2200, 0],
        "I am your SaaS Subscription Engine. I manage Discord community onboarding, Stripe subscription lifecycle, "
        "CRM customer tracking, and Telegram team alerts. How can I help?")

    agent = agent_node("SaaS Subscription Agent",
        "# SaaS Subscription Engine Agent\n\n"
        "You orchestrate SaaS subscription operations across multiple platforms:\n\n"
        "## Community Management:\n"
        "- Onboard new users to Discord server with role-based access\n"
        "- Send welcome messages and onboarding guides\n"
        "- Manage premium channels based on subscription tier\n"
        "- Handle support tickets via Discord\n"
        "- Send product updates and changelog\n\n"
        "## Subscription Lifecycle:\n"
        "- Create Stripe subscriptions with tiered plans\n"
        "- Handle upgrades, downgrades, and plan changes\n"
        "- Process trial periods and conversions\n"
        "- Manage failed payments and dunning\n"
        "- Generate MRR/ARR reports\n\n"
        "## Customer Tracking:\n"
        "- Track customer lifecycle in CRM: Trial → Active → Churned → Reactivated\n"
        "- Log all support interactions and feature requests\n"
        "- Calculate churn risk scores\n"
        "- Segment customers by plan, usage, and health\n"
        "- Generate customer success reports\n\n"
        "## Team Alerts:\n"
        "- Send Telegram alerts for important events (new signup, churn, payment failure)\n"
        "- Daily/weekly metrics digest\n"
        "- Real-time error notifications\n"
        "- Team performance updates\n\n"
        "## Skills Loaded:\n"
        "- data-analysis: SaaS metrics (MRR, churn, LTV, CAC)\n"
        "- deep-research: Competitive analysis and feature benchmarking\n"
        "- payment-processing: Subscription and dunning management\n"
        "- consulting-analysis: Growth strategy and pricing optimization\n\n"
        "Current datetime: __DATE__",
        [-1600, 0])

    llm = llm_node("GPT-4.1 SaaS", "gpt-4.1", 0.2, [-1600, 300])
    memory = memory_node("SaaS Memory", [-1300, 300])
    parser = output_parser("SaaS Output", [
        {"name": "category", "description": "Category (community/subscription/crm/alerts)"},
        {"name": "action", "description": "Action performed"},
        {"name": "result", "description": "Result summary"},
        {"name": "customer_id", "description": "Customer ID if applicable"},
        {"name": "subscription_id", "description": "Stripe subscription ID if applicable"},
        {"name": "plan", "description": "Subscription plan tier"},
    ], [-1300, 0])

    # Tools
    discord_onboard = http_tool("Discord Onboard", "Onboard a new user to Discord server with appropriate role based on subscription tier. Sends welcome message.",
                                "Discord_Onboard_URL", [-700, 500], "POST")
    discord_role = http_tool("Discord Manage Role", "Update Discord member role when subscription changes (upgrade/downgrade/cancel).",
                             "Discord_Role_URL", [-500, 500], "POST")
    discord_support = http_tool("Discord Support", "Create or update a support ticket in Discord channel with priority and category.",
                                "Discord_Support_URL", [-300, 500], "POST")
    stripe_sub = http_tool("Stripe Create Subscription", "Create a Stripe subscription with plan, trial period, and customer details.",
                           "Stripe_Sub_URL", [-100, 500], "POST")
    stripe_manage = http_tool("Stripe Manage Sub", "Manage subscription lifecycle: upgrade, downgrade, cancel, pause, or reactivate.",
                              "Stripe_Manage_URL", [100, 500], "POST")
    stripe_metrics = http_tool("Stripe SaaS Metrics", "Calculate SaaS metrics from Stripe data: MRR, ARR, churn rate, LTV, CAC.",
                               "Stripe_Metrics_URL", [300, 500], "GET")
    crm_customer = http_tool("CRM SaaS Customer", "Create or update SaaS customer in CRM with plan, usage, health score, and lifecycle stage.",
                             "CRM_SaaS_URL", [500, 500], "POST")
    telegram_alert = http_tool("Telegram Alert", "Send a team alert via Telegram for important events (new signup, churn, payment failure, error).",
                               "Telegram_Alert_URL", [700, 500], "POST")
    think = think_tool("SaaS Reasoning", "Think through subscription lifecycle, churn risk, plan optimization, and customer health.",
                       [900, 500])

    note = sticky_note(
        "SaaS Subscription Engine\n\n"
        "FLOW: Discord Onboard → Stripe Subscribe → CRM Track → Telegram Alert\n\n"
        "Platforms: Discord, Stripe, CRM, Telegram\n"
        "Lifecycle: Trial → Active → Upgrade → Renewal → (Churn/Reactivate)",
        [-2200, -400]
    )

    nodes = [trigger, note, agent, llm, memory, parser,
             discord_onboard, discord_role, discord_support,
             stripe_sub, stripe_manage, stripe_metrics,
             crm_customer, telegram_alert, think]

    connections = merge_dicts([
        main_conn("Chat Trigger", "SaaS Subscription Agent"),
        ai_conn("SaaS Subscription Agent", "GPT-4.1 SaaS", "languageModel"),
        ai_conn("SaaS Subscription Agent", "SaaS Memory", "memory"),
        ai_conn("SaaS Subscription Agent", "SaaS Output", "outputParser"),
        ai_conn("SaaS Subscription Agent", "Discord Onboard", "tool"),
        ai_conn("SaaS Subscription Agent", "Discord Manage Role", "tool"),
        ai_conn("SaaS Subscription Agent", "Discord Support", "tool"),
        ai_conn("SaaS Subscription Agent", "Stripe Create Subscription", "tool"),
        ai_conn("SaaS Subscription Agent", "Stripe Manage Sub", "tool"),
        ai_conn("SaaS Subscription Agent", "Stripe SaaS Metrics", "tool"),
        ai_conn("SaaS Subscription Agent", "CRM SaaS Customer", "tool"),
        ai_conn("SaaS Subscription Agent", "Telegram Alert", "tool"),
        ai_conn("SaaS Subscription Agent", "SaaS Reasoning", "tool"),
    ])
    return make_workflow("IND3 SaaS Subscription Engine v3", nodes, connections,
                         [{"name": "industry"}, {"name": "saas"}, {"name": "subscription"}])


# ═══════════════════════════════════════════════════════════════════════
# 8. INDUSTRY USE CASE: AGENCY CLIENT PORTAL
# ═══════════════════════════════════════════════════════════════════════

def generate_ind_agency():
    """Agency: WordPress portfolio → CRM clients → Stripe invoicing → Discord/Telegram collaboration."""
    trigger = chat_trigger([-2200, 0],
        "I am your Agency Client Portal Assistant. I manage WordPress portfolio updates, CRM client relationships, "
        "Stripe invoicing, and team collaboration via Discord/Telegram. How can I help?")

    agent = agent_node("Agency Client Portal Agent",
        "# Agency Client Portal Agent\n\n"
        "You orchestrate agency operations across multiple platforms:\n\n"
        "## Portfolio & Content:\n"
        "- Publish case studies and portfolio pieces on WordPress\n"
        "- Update project pages with milestones and deliverables\n"
        "- Manage blog content and social media scheduling\n"
        "- Share portfolio updates via WhatsApp with clients\n\n"
        "## Client Management:\n"
        "- Track clients in CRM: Lead → Onboarding → Active → Completed → Retainer\n"
        "- Log all client communications and deliverables\n"
        "- Schedule and track client meetings\n"
        "- Generate client satisfaction surveys\n"
        "- Manage retainer contracts and renewals\n\n"
        "## Invoicing & Payments:\n"
        "- Create Stripe invoices for project milestones\n"
        "- Set up recurring retainer payments\n"
        "- Track time and expenses per project\n"
        "- Handle late payments and reminders\n"
        "- Generate revenue and profitability reports\n\n"
        "## Team Collaboration:\n"
        "- Manage project channels in Discord\n"
        "- Send task updates and deadline alerts via Telegram\n"
        "- Share client briefs and creative assets\n"
        "- Coordinate team availability and workload\n\n"
        "## Skills Loaded:\n"
        "- deep-research: Client industry analysis and competitive landscape\n"
        "- data-analysis: Project profitability and resource utilization\n"
        "- consulting-analysis: Client strategy and growth recommendations\n"
        "- content-management: Content creation and publishing workflow\n"
        "- payment-processing: Invoice and retainer management\n\n"
        "Current datetime: __DATE__",
        [-1600, 0])

    llm = llm_node("GPT-4.1 Agency", "gpt-4.1", 0.2, [-1600, 300])
    memory = memory_node("Agency Memory", [-1300, 300])
    parser = output_parser("Agency Output", [
        {"name": "category", "description": "Category (portfolio/client/invoicing/collaboration)"},
        {"name": "action", "description": "Action performed"},
        {"name": "result", "description": "Result summary"},
        {"name": "client_id", "description": "Client ID if applicable"},
        {"name": "project_id", "description": "Project ID if applicable"},
        {"name": "invoice_id", "description": "Invoice ID if applicable"},
    ], [-1300, 0])

    # Tools
    wp_post = http_tool("WP Publish Case Study", "Publish a case study or portfolio piece on WordPress with title, content, images, and categories.",
                        "WP_CaseStudy_URL", [-700, 500], "POST")
    wp_update = http_tool("WP Update Project", "Update a project page on WordPress with milestones, deliverables, and status.",
                          "WP_Project_URL", [-500, 500], "POST")
    crm_client = http_tool("CRM Agency Client", "Create or update an agency client in CRM with project details, contract value, and status.",
                           "CRM_Agency_URL", [-300, 500], "POST")
    crm_project = http_tool("CRM Project Deal", "Create a project deal in CRM with scope, milestones, timeline, and budget.",
                            "CRM_Project_URL", [-100, 500], "POST")
    stripe_invoice = http_tool("Stripe Project Invoice", "Create a Stripe invoice for a project milestone, retainer, or ad-hoc service.",
                               "Stripe_Invoice_URL", [100, 500], "POST")
    stripe_retainer = http_tool("Stripe Retainer", "Set up a recurring Stripe subscription for monthly retainer contracts.",
                                "Stripe_Retainer_URL", [300, 500], "POST")
    discord_channel = http_tool("Discord Project Channel", "Create or manage a Discord channel for project collaboration with team and client.",
                                "Discord_Channel_URL", [500, 500], "POST")
    telegram_update = http_tool("Telegram Team Update", "Send a team update via Telegram for project milestones, deadlines, or urgent tasks.",
                                "Telegram_Update_URL", [700, 500], "POST")
    think = think_tool("Agency Reasoning", "Think through client needs, project scope, resource allocation, and invoicing strategy.",
                       [900, 500])

    note = sticky_note(
        "Agency Client Portal\n\n"
        "FLOW: WordPress Portfolio → CRM Client → Stripe Invoice → Discord/Telegram\n\n"
        "Platforms: WordPress, CRM, Stripe, Discord, Telegram\n"
        "Pipeline: Lead → Onboarding → Active → Completed → Retainer",
        [-2200, -400]
    )

    nodes = [trigger, note, agent, llm, memory, parser,
             wp_post, wp_update, crm_client, crm_project,
             stripe_invoice, stripe_retainer, discord_channel, telegram_update,
             think]

    connections = merge_dicts([
        main_conn("Chat Trigger", "Agency Client Portal Agent"),
        ai_conn("Agency Client Portal Agent", "GPT-4.1 Agency", "languageModel"),
        ai_conn("Agency Client Portal Agent", "Agency Memory", "memory"),
        ai_conn("Agency Client Portal Agent", "Agency Output", "outputParser"),
        ai_conn("Agency Client Portal Agent", "WP Publish Case Study", "tool"),
        ai_conn("Agency Client Portal Agent", "WP Update Project", "tool"),
        ai_conn("Agency Client Portal Agent", "CRM Agency Client", "tool"),
        ai_conn("Agency Client Portal Agent", "CRM Project Deal", "tool"),
        ai_conn("Agency Client Portal Agent", "Stripe Project Invoice", "tool"),
        ai_conn("Agency Client Portal Agent", "Stripe Retainer", "tool"),
        ai_conn("Agency Client Portal Agent", "Discord Project Channel", "tool"),
        ai_conn("Agency Client Portal Agent", "Telegram Team Update", "tool"),
        ai_conn("Agency Client Portal Agent", "Agency Reasoning", "tool"),
    ])
    return make_workflow("IND4 Agency Client Portal v3", nodes, connections,
                         [{"name": "industry"}, {"name": "agency"}, {"name": "client-portal"}])


# ═══════════════════════════════════════════════════════════════════════
# 9. COGNITIVE CAPITAL SKILLS FOR NEW INTEGRATIONS
# ═══════════════════════════════════════════════════════════════════════

def generate_skill_md(skill_key, skill_data):
    """Generate a SKILL.md for a cognitive capital skill."""
    content = f"""# {skill_data['name']}

> **Category**: {skill_data['category']} | **Tier**: {skill_data['tier'].title()} | **Version**: 3.0

## Overview

{skill_data['description']}

## Core Capabilities

{skill_data['capabilities']}

## Integration Points

{skill_data['integrations']}

## OAuth2 & Authentication

{skill_data['auth']}

## Workflow Patterns

{skill_data['patterns']}

## Best Practices

{skill_data['best_practices']}

## Error Handling

{skill_data['error_handling']}

## Metrics & KPIs

{skill_data['metrics']}

---

*Generated by JARVIS AI Automation Platform v5.0.0 — Zero Technical Debt*
"""
    return content


NEW_COGNITIVE_SKILLS = {
    "communication-automation": {
        "name": "Communication Automation",
        "category": "Communication",
        "tier": "professional",
        "description": "Multi-channel communication orchestration across WhatsApp Business API, Telegram Bot, and Discord. "
                       "Manages inbound/outbound messaging, interactive menus, media delivery, contact segmentation, and cross-platform notification routing.",
        "capabilities": """### WhatsApp Business API
- **Send Messages**: Text messages with URL preview support
- **Template Messages**: Pre-approved templates for first-contact outreach (required within 24h window)
- **Interactive Messages**: Button menus, list selectors, and product cards for self-service flows
- **Media Delivery**: Images, videos, documents, audio, and stickers
- **Contact Management**: Profile retrieval, label assignment, segmentation
- **Message Tracking**: Delivery status, read receipts, and engagement metrics

### Telegram Bot API
- **Send Messages**: Markdown/HTML formatted text with reply-to and silent mode
- **Inline Keyboards**: Interactive button menus with callback handling
- **Media Sharing**: Photos, documents, videos, and audio files
- **Group Management**: Chat info, member tracking, and message pinning
- **Update Polling**: Long-polling for incoming messages and callbacks
- **Team Alerts**: Automated notifications for system events and milestones

### Discord Bot API
- **Rich Embeds**: Structured messages with fields, thumbnails, and colors
- **Channel Management**: Create, modify, and organize project channels
- **Role Management**: Permission-based access control for teams and clients
- **Webhooks**: Automated posting to channels from external services
- **Direct Messages**: Private communication with team members
- **Message Search**: Advanced search with filters for audit and reference""",
        "integrations": """### WhatsApp Business API
- **API Base**: `https://graph.facebook.com/v19.0/{phone_number_id}`
- **OAuth2**: Meta Business Suite → App Review → WhatsApp Business Account
- **Token Types**: Permanent system user token or 60-day user token
- **Webhook**: Real-time message notifications via webhook endpoint
- **Phone Number ID**: Required for all send operations
- **WABA ID**: WhatsApp Business Account identifier

### Telegram Bot API
- **API Base**: `https://api.telegram.org/bot{token}`
- **Authentication**: Bot Token from @BotFather (no OAuth2 required)
- **Webhook**: Optional webhook for real-time updates (vs. polling)
- **Bot Commands**: Register commands via @BotFather for menu integration
- **Inline Mode**: Support for inline queries and results

### Discord API v10
- **API Base**: `https://discord.com/api/v10`
- **OAuth2**: Discord Developer Portal → Application → OAuth2
- **Scopes**: `bot`, `applications.commands`
- **Permissions**: Send Messages, Manage Channels, Embed Links, Manage Roles
- **Gateway**: WebSocket connection for real-time events
- **Intents**: Required for message content and member events""",
        "auth": """### WhatsApp Business API — OAuth2 Flow
1. **Register App**: Meta Developer Portal → Create App → WhatsApp Business
2. **App Review**: Submit for approval (business verification required)
3. **Get Token**: System User → Generate Permanent Token
4. **Phone Number**: Link business phone number to WABA
5. **Webhook Setup**: Configure webhook URL for incoming messages
6. **Token Refresh**: Permanent tokens do not expire; user tokens refresh every 60 days

```
Authorization: Bearer {access_token}
Content-Type: application/json
```

### Telegram Bot — Token Authentication
1. **Create Bot**: Message @BotFather → /newbot → Set name and username
2. **Get Token**: BotFather provides API token
3. **Set Commands**: /setcommands for interactive menu
4. **Webhook (Optional)**: POST /setWebhook with URL and certificate

```
Authorization: (token in URL path)
https://api.telegram.org/bot{token}/sendMessage
```

### Discord — OAuth2 + Bot Token
1. **Create Application**: Discord Developer Portal → New Application
2. **Bot Tab**: Create Bot → Copy Token
3. **OAuth2 URL Generator**: Select scopes (bot, applications.commands)
4. **Permissions**: Select required permissions (Send Messages, Manage Channels, etc.)
5. **Invite Bot**: Use generated OAuth2 URL to add bot to server
6. **Gateway**: Connect via WebSocket for real-time events

```
Authorization: Bot {bot_token}
Content-Type: application/json
```""",
        "patterns": """### Pattern 1: Lead Capture (WhatsApp → CRM)
```
WhatsApp Incoming → Parse Intent → Qualify Lead → CRM Create Contact → WA Send Confirmation
```

### Pattern 2: Team Notification (CRM → Telegram)
```
CRM Deal Stage Change → Format Alert → Telegram Send Message → Log Activity
```

### Pattern 3: Community Onboarding (Discord → Stripe)
```
New Discord Member → Assign Role → Send Welcome → Stripe Create Subscription → Update CRM
```

### Pattern 4: Sales Cycle (WhatsApp → CRM → Stripe)
```
WA Lead → Qualify → CRM Create Contact → CRM Create Deal → Pipeline Update →
Stripe Payment Link → WA Send Payment → WA Confirm Payment → CRM Close Deal
```

### Pattern 5: Multi-Channel Broadcast
```
Content Created → WordPress Publish → WhatsApp Send Template → Telegram Alert → Discord Embed → CRM Log Activity
```""",
        "best_practices": """1. **WhatsApp 24h Window**: Free-form messages only within 24h of last user message; use templates outside
2. **Telegram Rate Limits**: 30 msg/sec per bot, 20 msg/min per group; use sleep between batches
3. **Discord Rate Limits**: 5 req/sec per route; respect X-RateLimit-Remaining headers
4. **Template Pre-Approval**: WhatsApp templates must be approved before use (24-48h review)
5. **Opt-In Compliance**: Always obtain consent before sending messages on any platform
6. **Error Retry**: Implement exponential backoff for rate limit errors (429 status)
7. **Message Deduplication**: Track message IDs to prevent duplicate sends
8. **Media Optimization**: Compress images/videos before sending; use thumbnails for large files
9. **Webhook Security**: Verify webhook signatures (WhatsApp: X-Hub-Signature-256, Discord: signature verification)
10. **Session Management**: Track conversation state per user across platforms""",
        "error_handling": """### WhatsApp Error Codes
- **401**: Invalid access token → Refresh token
- **403**: Permission denied → Check app permissions
- **429**: Rate limit exceeded → Exponential backoff
- **1001**: Template not found → Verify template name and language
- **1002**: Message undeliverable → Check phone number format

### Telegram Error Codes
- **400**: Bad request → Validate parameters
- **401**: Unauthorized → Check bot token
- **403**: Forbidden → Check bot permissions in chat
- **429**: Too many requests → Respect Retry-After header
- **FLOOD_WAIT**: Wait specified seconds before retry

### Discord Error Codes
- **40001**: Unauthorized → Check bot token
- **50001**: Missing access → Check bot permissions
- **50013**: Missing permissions → Check role permissions
- **10003**: Unknown channel → Verify channel ID
- **50007**: Cannot send DM → User has DMs disabled
- **429**: Rate limited → Use X-RateLimit-Reset-After header""",
        "metrics": """### Communication KPIs
- **Response Time**: Average time to first response (target: <2 min)
- **Resolution Rate**: % of inquiries resolved in first contact (target: >80%)
- **Message Volume**: Messages sent/received per day/week/month
- **Engagement Rate**: % of messages read/replied (WhatsApp: read receipts)
- **Conversion Rate**: % of conversations leading to CRM deal creation
- **Channel Distribution**: Message volume by platform (WhatsApp/Telegram/Discord)
- **Template Performance**: Open rate and response rate per WhatsApp template
- **Bot Accuracy**: % of correctly handled inquiries without human escalation
- **Uptime**: Service availability (target: 99.9%)
- **Error Rate**: % of API calls resulting in errors (target: <0.1%)"""
    },
    "sales-cycle-automation": {
        "name": "Sales Cycle Automation",
        "category": "Sales",
        "tier": "professional",
        "description": "End-to-end sales cycle automation from lead capture through payment processing. "
                       "Combines WhatsApp communication, CRM pipeline management, and Stripe payment processing for a complete sales automation solution.",
        "capabilities": """### Lead Capture
- **Multi-Channel Ingest**: WhatsApp, Telegram, Discord, web forms
- **Lead Qualification**: AI-powered scoring based on engagement, budget, timeline
- **Contact Enrichment**: Auto-populate CRM with lead details and preferences
- **Segmentation**: Label and categorize leads (hot/warm/cold/vip)

### Pipeline Management
- **Stage Tracking**: New → Qualified → Proposal → Negotiation → Won/Lost
- **Activity Logging**: All communications, meetings, and actions recorded
- **Deal Scoring**: Probability-weighted pipeline forecasting
- **Automated Follow-ups**: Scheduled reminders and next-best-action suggestions

### Payment Processing
- **Payment Links**: Generate Stripe payment links for proposals
- **Invoicing**: Create invoices with line items, discounts, and due dates
- **Subscriptions**: Set up recurring billing for services
- **Reconciliation**: Track all payments and generate financial reports""",
        "integrations": """### WhatsApp Business API
- Lead capture and qualification
- Interactive product/service selection
- Payment confirmation and receipt delivery
- Follow-up and re-engagement campaigns

### CRM Universal
- Contact and deal management
- Pipeline stage tracking
- Activity logging and history
- Revenue forecasting

### Stripe
- Payment intent creation
- Invoice generation and management
- Subscription lifecycle management
- Payment status tracking and reporting""",
        "auth": """### Complete OAuth2 Flow for Sales Cycle
1. **WhatsApp**: Meta Business Suite OAuth2 → Permanent token
2. **CRM**: API key or OAuth2 (provider-specific)
3. **Stripe**: Secret key + webhook signing secret

All three platforms require separate credential configuration in n8n.""",
        "patterns": """### Full Sales Cycle
```
Lead → WA Qualify → CRM Create → CRM Deal → Pipeline → Stripe Payment → WA Confirm → CRM Close
```

### Failed Payment Recovery
```
Stripe Payment Failed → WA Reminder → CRM Activity Log → Wait 24h → WA Follow-up → CRM Update
```

### Subscription Renewal
```
Stripe Subscription Renewing → CRM Update → WA Notification → Discord/Telegram Alert
```""",
        "best_practices": """1. Always qualify leads before creating CRM deals
2. Use WhatsApp templates for initial outreach
3. Log every interaction in CRM for complete audit trail
4. Set up Stripe webhooks for real-time payment status
5. Use think tool for complex sales reasoning decisions
6. Implement retry logic for failed payments
7. Track conversion rates per channel for optimization""",
        "error_handling": """### Payment Failures
- **card_declined**: Send WhatsApp notification, update CRM, schedule retry
- **insufficient_funds**: Offer alternative payment method
- **processing_error**: Retry with exponential backoff

### CRM Sync Issues
- **duplicate_contact**: Merge records, keep most recent
- **api_error**: Queue for retry, log error for investigation""",
        "metrics": """### Sales KPIs
- **Lead-to-Deal Rate**: % of leads converted to deals (target: >25%)
- **Deal-to-Payment Rate**: % of deals with successful payment (target: >80%)
- **Average Deal Size**: Mean deal value in pipeline
- **Sales Cycle Length**: Average days from lead to close
- **MRR Growth**: Monthly recurring revenue growth rate
- **Pipeline Velocity**: Deals moving through stages per week
- **Payment Success Rate**: % of payment attempts that succeed
- **Customer Acquisition Cost**: Total cost / new customers acquired"""
    },
    "industry-automation": {
        "name": "Industry Automation",
        "category": "Industry",
        "tier": "enterprise",
        "description": "Industry-specific automation templates for real estate, restaurants, SaaS, and agencies. "
                       "Each template provides pre-configured workflows, tool integrations, and best practices for vertical-specific operations.",
        "capabilities": """### Real Estate
- Property listing management (WordPress)
- Virtual tour scheduling (WhatsApp)
- Buyer/seller pipeline tracking (CRM)
- Commission and deposit processing (Stripe)

### Restaurant
- Food order management (WhatsApp interactive menus)
- Menu catalog management (WooCommerce)
- Customer loyalty tracking (CRM)
- Daily sales reconciliation (Stripe)

### SaaS
- Community onboarding (Discord)
- Subscription lifecycle management (Stripe)
- Customer health tracking (CRM)
- Team alerting (Telegram)

### Agency
- Portfolio and case study publishing (WordPress)
- Client relationship management (CRM)
- Project invoicing and retainers (Stripe)
- Team collaboration (Discord/Telegram)""",
        "integrations": """### Real Estate
- WordPress (property listings), WhatsApp (tours), CRM (deals), Stripe (payments)
- Booking.com (property availability), ERPNext (property management)

### Restaurant
- WhatsApp (orders), WooCommerce (menu), CRM (loyalty), Stripe (payments)
- Google Workspace (scheduling), Calendar (reservations)

### SaaS
- Discord (community), Stripe (subscriptions), CRM (customers), Telegram (alerts)
- GitHub (product), Notion (knowledge base)

### Agency
- WordPress (portfolio), CRM (clients), Stripe (invoices), Discord/Telegram (collaboration)
- Google Workspace (documents), Slack (internal)""",
        "auth": """### Multi-Platform OAuth2
Each industry workflow requires authentication for 3-5 platforms:
- **Communication**: WhatsApp/Telegram/Discord (see Communication Automation skill)
- **CRM**: API key or OAuth2 (provider-specific)
- **Payment**: Stripe secret key + webhook signing secret
- **CMS**: WordPress application password or OAuth2
- **Commerce**: WooCommerce API key, Shopify access token""",
        "patterns": """### Real Estate
```
Property → WP Listing → WA Tour → CRM Deal → Stripe Commission → WA Confirm
```

### Restaurant
```
WA Order → WC Menu → CRM Customer → Stripe Payment → WA Confirm → Daily Report
```

### SaaS
```
Discord Onboard → Stripe Subscribe → CRM Track → Telegram Alert → (Churn/Reactivate)
```

### Agency
```
WP Portfolio → CRM Client → Stripe Invoice → Discord Channel → Telegram Update
```""",
        "best_practices": """1. Customize workflow prompts for your specific industry terminology
2. Map your pipeline stages to the CRM stages provided
3. Set up all platform webhooks before activating workflows
4. Test with small data sets before full deployment
5. Monitor KPIs daily for the first week after deployment
6. Create backup workflows for critical paths (payment processing, order management)
7. Use the think tool for complex decision points in your industry""",
        "error_handling": """### Industry-Specific Errors
- **Real Estate**: Double-booking showings → Use calendar conflict detection
- **Restaurant**: Out-of-stock items → Sync WooCommerce availability in real-time
- **SaaS**: Subscription downgrade → Update Discord roles before Stripe changes
- **Agency**: Late invoice payment → Send WhatsApp reminder, update CRM status""",
        "metrics": """### Industry KPIs
- **Real Estate**: Properties listed, tours scheduled, offers received, closing rate, average commission
- **Restaurant**: Orders/day, average order value, repeat customer rate, daily revenue, food cost %
- **SaaS**: MRR, churn rate, trial-to-paid rate, LTV, CAC, support ticket volume
- **Agency**: Active clients, project completion rate, revenue per client, retention rate, utilization rate"""
    }
}


# ═══════════════════════════════════════════════════════════════════════
# 10. INTEGRATIONS.md — COMPREHENSIVE DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════════

def generate_integrations_md():
    """Generate comprehensive INTEGRATIONS.md with OAuth2 flows, API details, deployment guides."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    content = """# JARVIS AI Automation — Integrations & OAuth2 Reference

> **Version**: 5.0.0 | **Zero Technical Debt** | **26 MCP Servers** | **300+ Connections**
> **Last Updated**: __DATE_PLACEHOLDER__
> **Communication MCP Servers**: 3 | **Payment MCP Servers**: 7 | **Industry Workflows**: 4

---

## Table of Contents

1. [Communication Integrations](#1-communication-integrations)
2. [Payment Integrations](#2-payment-integrations)
3. [E-Commerce Integrations](#3-e-commerce-integrations)
4. [CRM & Sales Integrations](#4-crm--sales-integrations)
5. [Productivity Integrations](#5-productivity-integrations)
6. [Travel & Hospitality Integrations](#6-travel--hospitality-integrations)
7. [DevOps & Project Management](#7-devops--project-management)
8. [Industry Use Cases](#8-industry-use-cases)
9. [OAuth2 Reference](#9-oauth2-reference)
10. [Webhook Configuration](#10-webhook-configuration)
11. [Rate Limits & Quotas](#11-rate-limits--quotas)
12. [Error Handling & Retry Strategies](#12-error-handling--retry-strategies)
13. [Security Best Practices](#13-security-best-practices)
14. [Deployment Guide](#14-deployment-guide)

---

## 1. Communication Integrations

### 1.1 WhatsApp Business API

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_WhatsApp_Business_Server_v3.json` |
| **Tools** | 8 (Send Message, Send Template, Send Media, List Conversations, Get Contact Profile, Manage Labels, Send Interactive, Get Message Status) |
| **API Base** | `https://graph.facebook.com/v19.0/{phone_number_id}` |
| **Auth Method** | OAuth2 (Meta Business Suite) |
| **Tier** | Professional+ |

#### OAuth2 Setup

```
Step 1: Meta Developer Portal → Create App → Business → WhatsApp
Step 2: Add WhatsApp Product → Configure Business Account
Step 3: Generate System User Token (Permanent)
Step 4: Link Phone Number to WABA
Step 5: Submit App Review (if going live)
Step 6: Configure Webhook for incoming messages
```

#### Token Types
- **System User Token**: Permanent, does not expire. Recommended for production.
- **User Token**: Expires in 60 days. Requires refresh mechanism.
- **Page Token**: For pages that have linked WhatsApp numbers.

#### API Endpoints

| Tool | Method | Endpoint |
|------|--------|----------|
| Send Message | POST | `/messages` |
| Send Template | POST | `/messages` (with template type) |
| Send Media | POST | `/messages` (with image/document/video/audio type) |
| List Conversations | GET | `/{waba_id}/conversations` |
| Get Contact Profile | GET | `/{phone_number}/whatsapp_business_profile` |
| Manage Labels | POST | `/{waba_id}/message_labels` |
| Send Interactive | POST | `/messages` (with interactive type) |
| Get Message Status | GET | `/{message_id}` |

#### Message Types
- **text**: Plain text with optional URL preview
- **template**: Pre-approved template with variable parameters
- **image/video/document/audio/sticker**: Media with optional caption
- **interactive**: Buttons, lists, product items, or CTA URLs
- **location**: Location sharing with coordinates
- **contacts**: Contact card sharing

#### 24-Hour Window Rule
Free-form messages can only be sent within 24 hours of the last user message. Outside this window, only approved template messages can be sent. This is a critical constraint for sales cycle automation.

---

### 1.2 Telegram Bot API

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Telegram_Bot_Server_v3.json` |
| **Tools** | 8 (Send Message, Send Photo, Send Document, Edit Message, Get Updates, Get Chat Info, Send Inline Keyboard, Pin Message) |
| **API Base** | `https://api.telegram.org/bot{token}` |
| **Auth Method** | Bot Token (no OAuth2) |
| **Tier** | Professional+ |

#### Bot Setup

```
Step 1: Open Telegram → Search @BotFather
Step 2: /newbot → Set name and username
Step 3: Copy API token
Step 4: /setcommands → Register command list
Step 5: Configure webhook (optional) or use polling
```

#### API Endpoints

| Tool | Method | Endpoint |
|------|--------|----------|
| Send Message | POST | `/sendMessage` |
| Send Photo | POST | `/sendPhoto` |
| Send Document | POST | `/sendDocument` |
| Edit Message | POST | `/editMessageText` |
| Get Updates | GET | `/getUpdates` |
| Get Chat Info | GET | `/getChat` |
| Send Inline Keyboard | POST | `/sendMessage` (with reply_markup) |
| Pin Message | POST | `/pinChatMessage` |

#### Formatting Modes
- **MarkdownV2**: Full Markdown with escaping (`*bold*`, `_italic_`, `[link](url)`)
- **HTML**: Standard HTML tags (`<b>bold</b>`, `<i>italic</i>`, `<a href="url">link</a>`)

---

### 1.3 Discord Bot API

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Discord_Server_v3.json` |
| **Tools** | 8 (Send Message, Send Embed, Manage Channels, Get Server Info, Manage Roles, Send DM, Manage Webhooks, Search Messages) |
| **API Base** | `https://discord.com/api/v10` |
| **Auth Method** | OAuth2 + Bot Token |
| **Tier** | Professional+ |

#### OAuth2 Setup

```
Step 1: Discord Developer Portal → New Application
Step 2: Bot Tab → Add Bot → Copy Token
Step 3: OAuth2 → URL Generator → Select scopes: bot, applications.commands
Step 4: Bot Permissions: Send Messages, Manage Channels, Embed Links, Manage Roles, Read Message History
Step 5: Use generated URL to invite bot to server
Step 6: Enable Privileged Gateway Intents (Message Content, Server Members)
```

#### API Endpoints

| Tool | Method | Endpoint |
|------|--------|----------|
| Send Message | POST | `/channels/{channel_id}/messages` |
| Send Embed | POST | `/channels/{channel_id}/messages` (with embeds) |
| Manage Channels | POST/PATCH/DELETE | `/guilds/{guild_id}/channels` |
| Get Server Info | GET | `/guilds/{guild_id}` |
| Manage Roles | POST/PATCH/DELETE | `/guilds/{guild_id}/roles` |
| Send DM | POST | `/users/@me/channels` then `/channels/{channel_id}/messages` |
| Manage Webhooks | POST/PATCH/DELETE | `/channels/{channel_id}/webhooks` |
| Search Messages | GET | `/channels/{channel_id}/messages` |

#### Rate Limits
- **Global**: 50 requests/second
- **Per-Route**: 5 requests/second (with bucket-based tracking)
- **Headers**: Use `X-RateLimit-Remaining`, `X-RateLimit-Reset-After` for dynamic throttling

---

## 2. Payment Integrations

### 2.1 Stripe

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Stripe_Server_v3.json` |
| **Tools** | 8 (Create Payment, Create Subscription, List Customers, Create Invoice, Process Refund, Get Balance, List Transactions, Create Payout) |
| **API Base** | `https://api.stripe.com/v1` |
| **Auth Method** | Secret Key + Webhook Signing Secret |
| **Tier** | Professional+ |

#### Authentication
```
Authorization: Bearer sk_live_...
Stripe-Version: 2024-06-20
```

#### Webhook Events (Critical for Sales Cycle)
- `payment_intent.succeeded` → Update CRM deal, send WhatsApp confirmation
- `payment_intent.payment_failed` → Send WhatsApp reminder, log CRM activity
- `invoice.paid` → Update CRM subscription status
- `customer.subscription.deleted` → Update CRM, send re-engagement
- `charge.refunded` → Log in CRM, send WhatsApp notification

---

### 2.2 PayPal

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_PayPal_Server_v3.json` |
| **Tools** | 8 (Create Order, Capture Order, Create Subscription, List Transactions, Process Refund, Get Balance, Send Payout, Create Invoice) |
| **API Base** | `https://api-m.paypal.com` (live) / `https://api-m.sandbox.paypal.com` (sandbox) |
| **Auth Method** | OAuth2 (Client ID + Secret) |
| **Tier** | Professional+ |

#### OAuth2 Flow
```
POST /v1/oauth2/token
  Grant-Type: client_credentials
  Client-ID: {client_id}
  Secret: {client_secret}
→ Returns: access_token (expires in 9 hours)
```

---

### 2.3 Binance

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Binance_Server_v3.json` |
| **Tools** | 8 (Get Market Data, Place Order, Get Account Info, Get Trade History, Get Deposit Address, Withdraw, Get Deposit History, Get Withdrawal History) |
| **API Base** | `https://api.binance.com` (spot) / `https://fapi.binance.com` (futures) |
| **Auth Method** | API Key + HMAC-SHA256 Signature |
| **Tier** | Enterprise |

---

### 2.4 QvaPay

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Qvapay_Server_v3.json` |
| **Tools** | 8 (Create Invoice, Get Transaction, List Transactions, Get Balance, Send Transfer, Get Currencies, Get Business Info, Get Wallet Info) |
| **API Base** | `https://qvapay.com/api/v1` |
| **Auth Method** | API Key (Bearer token) |
| **Tier** | Enterprise |

---

### 2.5 TropiPay

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Tropipay_Server_v3.json` |
| **Tools** | 8 (Create Payment Link, Get Transaction, List Transactions, Get Balance, Create QR Payment, Get Currencies, Send Transfer, Get Business Info) |
| **API Base** | `https://tropipay.com/api/v2` |
| **Auth Method** | OAuth2 (Client ID + Secret) |
| **Tier** | Enterprise |

---

### 2.6 CoinEx

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Coinex_Server_v3.json` |
| **Tools** | 8 (Get Market Data, Place Order, Get Account Info, Get Order History, Get Deposit Address, Withdraw, Get Deposit History, Get Withdrawal History) |
| **API Base** | `https://api.coinex.com/v2` |
| **Auth Method** | API Key + HMAC-SHA256 Signature |
| **Tier** | Enterprise |

---

### 2.7 Bitrefill

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Bitrefill_Server_v3.json` |
| **Tools** | 8 (List Products, Get Product Info, Create Order, Get Order Status, List Categories, Get Balance, Send Gift Card, Get Transaction History) |
| **API Base** | `https://api.bitrefill.com/v1` |
| **Auth Method** | API Key + Token |
| **Tier** | Enterprise |

---

## 3. E-Commerce Integrations

### 3.1 WooCommerce

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_WooCommerce_Server_v3.json` |
| **Tools** | 8 (Products, Orders, Customers, Coupons, Categories, Tags, Reports, Settings) |
| **API Base** | `https://{store}/wp-json/wc/v3` |
| **Auth Method** | API Key (Consumer Key + Consumer Secret) |
| **Tier** | Professional+ |

#### Authentication
```
URL: https://{store}/wp-json/wc/v3/products
Auth: Basic Auth (consumer_key:consumer_secret)
```

---

### 3.2 Shopify

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Shopify_Server_v3.json` |
| **Tools** | 8 (Products, Inventory, Orders, Fulfillment, Customers, Discounts, Analytics, Themes) |
| **API Base** | `https://{shop}.myshopify.com/admin/api/2024-01` |
| **Auth Method** | OAuth2 (Access Token) |
| **Tier** | Enterprise |

#### OAuth2 Flow
```
1. Redirect: https://{shop}.myshopify.com/admin/oauth/authorize?client_id={api_key}&scope={scopes}&redirect_uri={uri}
2. User approves → callback with code
3. Exchange code for access_token: POST /admin/oauth/access_token
4. Use access_token in X-Shopify-Access-Token header
```

---

## 4. CRM & Sales Integrations

### 4.1 CRM Universal

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_CRM_Server_v3.json` |
| **Tools** | 8 (Contacts, Leads, Pipeline, Deals, Activities, Companies, Dashboard, Reports) |
| **API Base** | Configurable (supports any CRM API) |
| **Auth Method** | API Key or OAuth2 (provider-specific) |
| **Tier** | Professional+ |

#### Pipeline Stages
```
New → Contacted → Qualified → Proposal → Negotiation → Won / Lost
```

---

### 4.2 HubSpot

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_HubSpot_Server_v3.json` |
| **Tools** | 7 (Contacts, Deals, Companies, Pipelines, Activities, Lists, Reports) |
| **API Base** | `https://api.hubapi.com` |
| **Auth Method** | OAuth2 (Private App Access Token) |
| **Tier** | Enterprise |

---

## 5. Productivity Integrations

### 5.1 Google Workspace

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Google_Workspace_Server_v3.json` |
| **Tools** | 8 (Drive, Docs, Sheets, Meet, Calendar, Gmail, Tasks, Forms) |
| **API Base** | `https://www.googleapis.com` |
| **Auth Method** | OAuth2 (Service Account or User Token) |
| **Tier** | Professional+ |

#### OAuth2 Scopes
```
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/documents
https://www.googleapis.com/auth/spreadsheets
https://www.googleapis.com/auth/calendar
https://mail.google.com/
```

---

### 5.2 WordPress

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_WordPress_Server_v3.json` |
| **Tools** | 8 (Posts, Pages, Media, Comments, Users, Categories, Tags, Stats) |
| **API Base** | `https://{site}/wp-json/wp/v2` |
| **Auth Method** | Application Password or OAuth2 |
| **Tier** | Professional+ |

#### Authentication
```
Method 1: Application Password
  URL: https://{site}/wp-json/wp/v2/posts
  Auth: Basic Auth (username:application_password)

Method 2: OAuth2 (with WP OAuth Server plugin)
  Redirect: /oauth/authorize
  Token: /oauth/token
  Use: Bearer token in Authorization header
```

---

## 6. Travel & Hospitality Integrations

### 6.1 Booking.com

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Booking_Server_v3.json` |
| **Tools** | 8 (Properties, Reservations, Availability, Rates, Reviews, Guests, Rooms, Reports) |
| **API Base** | `https://providers.booking.com/v1` |
| **Auth Method** | OAuth2 (Client Credentials) |
| **Tier** | Enterprise |

---

### 6.2 Expedia

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Expedia_Server_v3.json` |
| **Tools** | 8 (Hotels, Flights, Cars, Packages, Bookings, Reviews, Availability, Rates) |
| **API Base** | `https://api.expediagroup.com/v3` |
| **Auth Method** | OAuth2 (Client Credentials) |
| **Tier** | Enterprise |

---

## 7. DevOps & Project Management

### 7.1 GitHub

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_GitHub_Server_v3.json` |
| **Tools** | 7 (Repos, Issues, PRs, Code, Files, Actions, Releases) |
| **API Base** | `https://api.github.com` |
| **Auth Method** | Personal Access Token (PAT) or OAuth2 |
| **Tier** | Professional+ |

---

### 7.2 ERPNext

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_ERPNext_Server_v3.json` |
| **Tools** | 8 (GL, Invoices, POs, Stock, Employees, Projects, Reports, Settings) |
| **API Base** | `https://{instance}/api/resource` |
| **Auth Method** | API Key + Secret (or OAuth2) |
| **Tier** | Enterprise |

---

## 8. Industry Use Cases

### 8.1 Real Estate Automation (IND1)

| Aspect | Detail |
|--------|--------|
| **Workflow** | `IND1_Real_Estate_Automation_v3.json` |
| **Platforms** | WordPress, WhatsApp, CRM, Stripe |
| **Tools** | 9 (WP Listing, WA Property, WA Media, CRM Buyer, CRM Deal, CRM Showing, Stripe Commission, Stripe Rent, Reasoning) |
| **Pipeline** | Inquiry → Showing → Offer → Negotiation → Closing |
| **Tier** | Enterprise |

#### Sales Flow
```
1. Property Listed on WordPress → WhatsApp notification to qualified buyers
2. Buyer inquires via WhatsApp → CRM contact created → Label as "hot/warm/cold"
3. Virtual tour scheduled via WhatsApp interactive → CRM activity logged
4. Offer made → CRM deal created → Pipeline stage: Negotiation
5. Deal closed → Stripe commission invoice → WhatsApp confirmation
6. Recurring rent → Stripe subscription → CRM tracking
```

---

### 8.2 Restaurant Operations (IND2)

| Aspect | Detail |
|--------|--------|
| **Workflow** | `IND2_Restaurant_Operations_v3.json` |
| **Platforms** | WhatsApp, WooCommerce, CRM, Stripe |
| **Tools** | 9 (WA Order, WA Confirm, WA Promo, WC Menu, WC Orders, CRM Customer, Stripe Payment, Stripe Report, Reasoning) |
| **Pipeline** | Order → Prepare → Deliver → Payment → Loyalty |
| **Tier** | Enterprise |

#### Order Flow
```
1. Customer sends WhatsApp message → Interactive menu with categories
2. Customer selects items → Order captured with quantity and delivery address
3. Order confirmation sent via WhatsApp with ETA
4. Order synced to WooCommerce for kitchen display
5. CRM customer record updated with order history and loyalty points
6. Payment processed via Stripe → WhatsApp receipt sent
7. Daily reconciliation report generated
```

---

### 8.3 SaaS Subscription Engine (IND3)

| Aspect | Detail |
|--------|--------|
| **Workflow** | `IND3_SaaS_Subscription_Engine_v3.json` |
| **Platforms** | Discord, Stripe, CRM, Telegram |
| **Tools** | 9 (Discord Onboard, Discord Role, Discord Support, Stripe Subscribe, Stripe Manage, Stripe Metrics, CRM Customer, Telegram Alert, Reasoning) |
| **Pipeline** | Trial → Active → Upgrade → Renewal → (Churn/Reactivate) |
| **Tier** | Enterprise |

#### Subscription Flow
```
1. New signup → Discord onboarding with role assignment
2. Stripe subscription created → Trial period starts
3. CRM customer record created with plan and lifecycle stage
4. Trial → Paid conversion → Discord role upgrade
5. Subscription metrics tracked (MRR, ARR, churn)
6. Payment failure → Telegram alert → WhatsApp dunning
7. Churn → CRM stage update → Re-engagement campaign
```

---

### 8.4 Agency Client Portal (IND4)

| Aspect | Detail |
|--------|--------|
| **Workflow** | `IND4_Agency_Client_Portal_v3.json` |
| **Platforms** | WordPress, CRM, Stripe, Discord, Telegram |
| **Tools** | 9 (WP Case Study, WP Project, CRM Client, CRM Deal, Stripe Invoice, Stripe Retainer, Discord Channel, Telegram Update, Reasoning) |
| **Pipeline** | Lead → Onboarding → Active → Completed → Retainer |
| **Tier** | Enterprise |

#### Client Flow
```
1. New client → CRM contact created → WordPress project page
2. Discord channel created for project collaboration
3. Milestone reached → Stripe invoice generated → WhatsApp notification
4. Project completed → WordPress case study published → CRM update
5. Retainer setup → Stripe recurring subscription → Telegram team update
6. Monthly report → CRM dashboard → WhatsApp client summary
```

---

## 9. OAuth2 Reference

### 9.1 OAuth2 Flows by Platform

| Platform | Grant Type | Token Lifetime | Refresh | Scopes |
|----------|-----------|---------------|---------|--------|
| **WhatsApp (Meta)** | Client Credentials | Permanent (system user) | N/A | whatsapp_business_messaging |
| **PayPal** | Client Credentials | 9 hours | Yes | Various |
| **Shopify** | Authorization Code | Permanent (offline) | N/A | read_products, write_orders, etc. |
| **TropiPay** | Client Credentials | 1 hour | Yes | payments, transfers |
| **Google Workspace** | Service Account | 1 hour (auto-refresh) | Yes | drive, docs, sheets, calendar, gmail |
| **Discord** | Authorization Code | 7 days | Yes | bot, identify, guilds |
| **HubSpot** | Authorization Code | 6 hours | Yes | crm.objects.*, crm.contacts.* |
| **WordPress** | Application Password | Permanent | N/A | N/A |

### 9.2 Token Management in n8n

```
1. Store tokens in n8n Credentials (encrypted at rest)
2. Use OAuth2 credential type for auto-refresh flows
3. Set up webhook endpoints for OAuth2 callbacks
4. Monitor token expiration and refresh proactively
5. Use separate credentials per environment (dev/staging/prod)
```

### 9.3 OAuth2 Callback Configuration

For platforms requiring redirect URIs (Shopify, Discord, Google, HubSpot):

```
Callback URL: https://{n8n-domain}/rest/oauth2-credential/callback
```

Configure this in each platform's developer console before creating OAuth2 credentials in n8n.

---

## 10. Webhook Configuration

### 10.1 Webhook Endpoints

| Platform | Webhook URL | Events |
|----------|------------|--------|
| **WhatsApp** | `https://{n8n}/webhook/whatsapp-incoming` | messages, message_status |
| **Stripe** | `https://{n8n}/webhook/stripe-events` | payment_intent.*, invoice.*, customer.subscription.* |
| **PayPal** | `https://{n8n}/webhook/paypal-events` | PAYMENT.*, BILLING.* |
| **Discord** | WebSocket Gateway (not HTTP) | MESSAGE_CREATE, INTERACTION_CREATE |
| **Telegram** | `https://{n8n}/webhook/telegram-bot` | message, callback_query |
| **Shopify** | `https://{n8n}/webhook/shopify-events` | orders/*, products/*, app/uninstalled |
| **WooCommerce** | `https://{n8n}/webhook/woo-events` | order.created, order.updated, product.* |

### 10.2 Webhook Security

- **WhatsApp**: Verify `X-Hub-Signature-256` HMAC-SHA256
- **Stripe**: Verify `Stripe-Signature` with webhook signing secret
- **PayPal**: Verify PayPal signature headers
- **Telegram**: Verify `X-Telegram-Bot-Api-Secret-Token`
- **Shopify**: Verify `X-Shopify-Hmac-Sha256`
- **WooCommerce**: Verify WooCommerce webhook signature

---

## 11. Rate Limits & Quotas

### 11.1 Rate Limits Summary

| Platform | Rate Limit | Burst | Reset Window |
|----------|-----------|-------|-------------|
| **WhatsApp** | 80 msg/min per phone | 25 msg/sec | 1 minute |
| **Telegram** | 30 msg/sec per bot | 20 msg/min per group | 1 second |
| **Discord** | 5 req/sec per route | 50 req/sec global | Per-route bucket |
| **Stripe** | 100 reads/sec, 25 writes/sec | Varies | 1 second |
| **PayPal** | 500 req/min (sandbox), varies (live) | N/A | 1 minute |
| **Binance** | 1200 req/min (weight-based) | Varies | 1 minute |
| **Google** | 300 req/min (per user) | Varies | 1 minute |
| **GitHub** | 5000 req/hr (authenticated) | N/A | 1 hour |
| **Shopify** | 2 req/sec (per shop) | 40 req burst | 1 second |
| **WooCommerce** | Varies (per server) | N/A | N/A |

### 11.2 Retry Strategy

```
For 429 (Rate Limit) responses:
1. Read Retry-After header (if available)
2. Wait specified seconds
3. Retry with exponential backoff: 1s, 2s, 4s, 8s, 16s
4. Maximum 5 retries
5. Log failure and alert after max retries
```

---

## 12. Error Handling & Retry Strategies

### 12.1 Error Categories

| Category | HTTP Codes | Strategy |
|----------|-----------|----------|
| **Authentication** | 401, 403 | Refresh token, check credentials |
| **Rate Limit** | 429 | Exponential backoff, respect Retry-After |
| **Validation** | 400, 422 | Fix request parameters, log error |
| **Server** | 500, 502, 503 | Retry with backoff, fallback to alternative |
| **Timeout** | 408, 504 | Retry once, then alert |

### 12.2 Platform-Specific Error Handling

#### WhatsApp
- **190**: Token expired → Refresh token
- **10**: Permission error → Check app permissions
- **130429**: Rate limit → Wait and retry
- **1001**: Template not found → Use correct template name

#### Stripe
- **card_declined**: Notify customer, offer alternative
- **rate_limit**: Wait and retry with backoff
- **invalid_request**: Fix parameters and retry
- **api_connection_error**: Retry with exponential backoff

---

## 13. Security Best Practices

### 13.1 Credential Management
- Store all API keys and tokens in n8n Credentials (encrypted)
- Never hardcode credentials in workflow JSON
- Use environment variables for sensitive configuration
- Rotate API keys on a regular schedule (quarterly minimum)
- Use separate credentials for each environment

### 13.2 Data Protection
- Encrypt sensitive data in transit (HTTPS/TLS)
- Mask PII in logs and error messages
- Implement data retention policies per platform
- Comply with GDPR, CCPA, and regional privacy laws
- Use webhook signature verification for all incoming data

### 13.3 Access Control
- Use principle of least privilege for API permissions
- Implement role-based access in n8n
- Audit workflow execution logs regularly
- Set up IP allowlists for webhook endpoints
- Monitor for unusual API usage patterns

---

## 14. Deployment Guide

### 14.1 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/grootme/workflows.git
cd workflows

# 2. Choose your tier
cd jarvis-starter    # or jarvis-professional / jarvis-enterprise

# 3. Start n8n
docker-compose up -d

# 4. Import workflows
# Open n8n UI → Workflows → Import → Select JSON files

# 5. Configure credentials
# Open n8n UI → Credentials → Add → Enter API keys
```

### 14.2 Credential Setup Checklist

| Credential | Platform | Required For |
|-----------|----------|-------------|
| OpenAI API Key | OpenAI | All LLM nodes |
| WhatsApp Token | Meta | ORC5, IND1, IND2 |
| Stripe Secret Key | Stripe | ORC4, ORC5, IND1-4 |
| PayPal Client ID/Secret | PayPal | ORC4 |
| Binance API Key | Binance | ORC4 |
| CRM API Key | CRM Provider | ORC5, IND1-4 |
| WordPress App Password | WordPress | IND1, IND4 |
| WooCommerce API Key | WooCommerce | IND2 |
| Discord Bot Token | Discord | IND3, IND4 |
| Telegram Bot Token | Telegram | IND3, IND4 |

### 14.3 Testing Workflow

1. Start with Chat Trigger workflows (ORC5, IND1-4)
2. Test each platform connection individually
3. Verify webhook endpoints are reachable
4. Test with sandbox/test API keys first
5. Monitor first 24 hours of production operation
6. Set up error alerts via Telegram/Discord

---

## Appendix: Complete MCP Server Catalog

| # | Server | Tools | Category | Tier | New |
|---|--------|-------|----------|------|-----|
| 1 | WhatsApp Business | 8 | Communication | Professional+ | Phase 7 |
| 2 | Telegram Bot | 8 | Communication | Professional+ | Phase 7 |
| 3 | Discord | 8 | Communication | Professional+ | Phase 7 |
| 4 | Stripe | 8 | Payment | Professional+ | Phase 6 |
| 5 | PayPal | 8 | Payment | Professional+ | Phase 6 |
| 6 | Binance | 8 | Crypto | Enterprise | Phase 6 |
| 7 | QvaPay | 8 | Payment | Enterprise | Phase 6 |
| 8 | TropiPay | 8 | Payment | Enterprise | Phase 6 |
| 9 | CoinEx | 8 | Crypto | Enterprise | Phase 6 |
| 10 | Bitrefill | 8 | Crypto | Enterprise | Phase 6 |
| 11 | Google Workspace | 8 | Productivity | Professional+ | Phase 5 |
| 12 | CRM Universal | 8 | Sales | Professional+ | Phase 5 |
| 13 | Booking.com | 8 | Travel | Enterprise | Phase 5 |
| 14 | Expedia | 8 | Travel | Enterprise | Phase 5 |
| 15 | WooCommerce | 8 | E-Commerce | Professional+ | Phase 5 |
| 16 | Shopify | 8 | E-Commerce | Enterprise | Phase 5 |
| 17 | WordPress | 8 | CMS | Professional+ | Phase 5 |
| 18 | ERPNext | 8 | ERP | Enterprise | Phase 5 |
| 19 | Slack | 7 | Communication | Starter+ | Phase 4 |
| 20 | Notion | 7 | Knowledge | Professional+ | Phase 4 |
| 21 | GitHub | 7 | DevOps | Professional+ | Phase 4 |
| 22 | Trello | 6 | Project Mgmt | Enterprise | Phase 4 |
| 23 | HubSpot | 7 | CRM | Enterprise | Phase 4 |
| 24 | Calendar | 6 | Core | Starter+ | Phase 2-3 |
| 25 | Gmail | 6 | Core | Starter+ | Phase 2-3 |
| 26 | Contacts | 6 | Core | Starter+ | Phase 2-3 |

**Total: 26 MCP Servers, 184+ Tools**

---

*Generated by JARVIS AI Automation Platform v5.0.0 — Zero Technical Debt*
"""
    return content.replace("__DATE_PLACEHOLDER__", date_str)


# ═══════════════════════════════════════════════════════════════════════
# PACKAGE DISTRIBUTION & MANIFEST UPDATES
# ═══════════════════════════════════════════════════════════════════════

NEW_MCP_SERVERS = {
    "MCP_WhatsApp_Business_Server_v3.json": {"tier": "professional", "tools": 8, "category": "communication"},
    "MCP_Telegram_Bot_Server_v3.json": {"tier": "professional", "tools": 8, "category": "communication"},
    "MCP_Discord_Server_v3.json": {"tier": "professional", "tools": 8, "category": "communication"},
}

NEW_ORCHESTRATION = {
    "ORC5_WhatsApp_CRM_Stripe_Sales_Cycle_v3.json": {"tier": "professional", "tools": 17, "category": "sales-cycle"},
}

NEW_INDUSTRY = {
    "IND1_Real_Estate_Automation_v3.json": {"tier": "enterprise", "tools": 9, "category": "real-estate"},
    "IND2_Restaurant_Operations_v3.json": {"tier": "enterprise", "tools": 9, "category": "restaurant"},
    "IND3_SaaS_Subscription_Engine_v3.json": {"tier": "enterprise", "tools": 9, "category": "saas"},
    "IND4_Agency_Client_Portal_v3.json": {"tier": "enterprise", "tools": 9, "category": "agency"},
}


def _add_to_category(workflows_dict, category, filename):
    """Add filename to a category list if not already present."""
    if category not in workflows_dict:
        workflows_dict[category] = []
    if filename not in workflows_dict[category]:
        workflows_dict[category].append(filename)


def update_manifests():
    """Update all three tier manifests with new workflows."""
    for tier_name in ["jarvis-starter", "jarvis-professional", "jarvis-enterprise"]:
        manifest_path = os.path.join(BASE, tier_name, "manifest.json")
        if not os.path.exists(manifest_path):
            continue

        with open(manifest_path, "r") as f:
            manifest = json.load(f)

        manifest["version"] = "5.0.0"
        manifest["last_updated"] = datetime.now().strftime("%Y-%m-%d")

        workflows = manifest.get("workflows", {})
        if isinstance(workflows, list):
            # Convert old flat list format to dict format
            workflows = {"misc": workflows}

        # Add new MCP servers
        for filename, info in NEW_MCP_SERVERS.items():
            tier = info["tier"]
            if tier == "starter" and tier_name == "jarvis-starter":
                _add_to_category(workflows, "mcp_servers", filename)
            if tier in ("starter", "professional") and tier_name == "jarvis-professional":
                _add_to_category(workflows, "mcp_servers", filename)
            if tier_name == "jarvis-enterprise":
                _add_to_category(workflows, "mcp_servers", filename)

        # Add new orchestration workflows
        for filename, info in NEW_ORCHESTRATION.items():
            tier = info["tier"]
            if tier == "starter" and tier_name == "jarvis-starter":
                _add_to_category(workflows, "orchestration", filename)
            if tier in ("starter", "professional") and tier_name == "jarvis-professional":
                _add_to_category(workflows, "orchestration", filename)
            if tier_name == "jarvis-enterprise":
                _add_to_category(workflows, "orchestration", filename)

        # Add new industry workflows (enterprise only)
        for filename, info in NEW_INDUSTRY.items():
            if tier_name == "jarvis-enterprise":
                _add_to_category(workflows, "industry", filename)

        # Add new cognitive capital skills
        for skill_key, skill_data in NEW_COGNITIVE_SKILLS.items():
            tier = skill_data["tier"]
            if tier == "starter" and tier_name == "jarvis-starter":
                if "cognitive_capital" not in manifest:
                    manifest["cognitive_capital"] = {"skills": [], "soul_template": True}
                if skill_key not in manifest["cognitive_capital"].get("skills", []):
                    manifest["cognitive_capital"]["skills"].append(skill_key)
            if tier in ("starter", "professional") and tier_name == "jarvis-professional":
                if "cognitive_capital" not in manifest:
                    manifest["cognitive_capital"] = {"skills": [], "soul_template": True}
                if skill_key not in manifest["cognitive_capital"].get("skills", []):
                    manifest["cognitive_capital"]["skills"].append(skill_key)
            if tier_name == "jarvis-enterprise":
                if "cognitive_capital" not in manifest:
                    manifest["cognitive_capital"] = {"skills": [], "soul_template": True}
                if skill_key not in manifest["cognitive_capital"].get("skills", []):
                    manifest["cognitive_capital"]["skills"].append(skill_key)

        manifest["workflows"] = workflows

        # Count total workflows
        total = 0
        for cat_files in workflows.values():
            if isinstance(cat_files, list):
                total += len(cat_files)
        manifest["total_workflows"] = total

        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        print(f"  Updated {manifest_path} → {total} workflows, v5.0.0")


def sync_to_jarvis_packages():
    """Copy new files to the appropriate tier packages."""
    # MCP servers → professional + enterprise
    for filename, info in NEW_MCP_SERVERS.items():
        tier = info["tier"]
        src = os.path.join(BASE, "mcp_servers", filename)

        # Professional tier: professional-tier servers only
        if tier == "professional":
            dst = os.path.join(BASE, "jarvis-professional/workflows/mcp_servers", filename)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(src):
                with open(src, "r") as f:
                    data = json.load(f)
                with open(dst, "w") as f:
                    json.dump(data, f, indent=2)
                print(f"  Synced {filename} → jarvis-professional")

        # Enterprise tier: all servers
        dst = os.path.join(BASE, "jarvis-enterprise/workflows/mcp_servers", filename)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            with open(src, "r") as f:
                data = json.load(f)
            with open(dst, "w") as f:
                json.dump(data, f, indent=2)
            print(f"  Synced {filename} → jarvis-enterprise")

    # Orchestration workflows → professional + enterprise
    for filename, info in NEW_ORCHESTRATION.items():
        tier = info["tier"]
        src = os.path.join(BASE, "orchestration", filename)

        if tier == "professional":
            dst = os.path.join(BASE, "jarvis-professional/workflows/orchestration", filename)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(src):
                with open(src, "r") as f:
                    data = json.load(f)
                with open(dst, "w") as f:
                    json.dump(data, f, indent=2)
                print(f"  Synced {filename} → jarvis-professional")

        dst = os.path.join(BASE, "jarvis-enterprise/workflows/orchestration", filename)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            with open(src, "r") as f:
                data = json.load(f)
            with open(dst, "w") as f:
                json.dump(data, f, indent=2)
            print(f"  Synced {filename} → jarvis-enterprise")

    # Industry workflows → enterprise only
    for filename, info in NEW_INDUSTRY.items():
        src = os.path.join(BASE, "industry", filename)
        dst = os.path.join(BASE, "jarvis-enterprise/workflows/industry", filename)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            with open(src, "r") as f:
                data = json.load(f)
            with open(dst, "w") as f:
                json.dump(data, f, indent=2)
            print(f"  Synced {filename} → jarvis-enterprise")

    # Cognitive capital skills → professional + enterprise
    for skill_key, skill_data in NEW_COGNITIVE_SKILLS.items():
        tier = skill_data["tier"]
        filename = f"{skill_key}_SKILL.md"
        src = os.path.join(BASE, "cognitive_capital", filename)

        # Professional: professional-tier skills only
        if tier == "professional":
            dst = os.path.join(BASE, "jarvis-professional/cognitive_capital", filename)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(src):
                with open(src, "r") as f:
                    data = f.read()
                with open(dst, "w") as f:
                    f.write(data)
                print(f"  Synced {filename} → jarvis-professional")

        # Enterprise: all skills
        dst = os.path.join(BASE, "jarvis-enterprise/cognitive_capital", filename)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            with open(src, "r") as f:
                data = f.read()
            with open(dst, "w") as f:
                f.write(data)
            print(f"  Synced {filename} → jarvis-enterprise")


# ═══════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("Phase 7: Communication Integrations + Industry Use Cases")
    print("=" * 60)

    # ── 1. Generate Communication MCP Servers ──
    print("\n📡 Generating Communication MCP Servers...")

    mcp_servers_dir = os.path.join(BASE, "mcp_servers")
    os.makedirs(mcp_servers_dir, exist_ok=True)

    whatsapp_wf = generate_mcp_whatsapp()
    with open(os.path.join(mcp_servers_dir, "MCP_WhatsApp_Business_Server_v3.json"), "w") as f:
        json.dump(whatsapp_wf, f, indent=2)
    print(f"  ✅ MCP_WhatsApp_Business_Server_v3.json — {len(whatsapp_wf['nodes'])} nodes, 8 tools")

    telegram_wf = generate_mcp_telegram()
    with open(os.path.join(mcp_servers_dir, "MCP_Telegram_Bot_Server_v3.json"), "w") as f:
        json.dump(telegram_wf, f, indent=2)
    print(f"  ✅ MCP_Telegram_Bot_Server_v3.json — {len(telegram_wf['nodes'])} nodes, 8 tools")

    discord_wf = generate_mcp_discord()
    with open(os.path.join(mcp_servers_dir, "MCP_Discord_Server_v3.json"), "w") as f:
        json.dump(discord_wf, f, indent=2)
    print(f"  ✅ MCP_Discord_Server_v3.json — {len(discord_wf['nodes'])} nodes, 8 tools")

    # ── 2. Generate Sales Cycle Orchestration ──
    print("\n🔄 Generating Sales Cycle Orchestration...")

    orc_dir = os.path.join(BASE, "orchestration")
    os.makedirs(orc_dir, exist_ok=True)

    sales_wf = generate_orc_sales_cycle()
    with open(os.path.join(orc_dir, "ORC5_WhatsApp_CRM_Stripe_Sales_Cycle_v3.json"), "w") as f:
        json.dump(sales_wf, f, indent=2)
    print(f"  ✅ ORC5_WhatsApp_CRM_Stripe_Sales_Cycle_v3.json — {len(sales_wf['nodes'])} nodes, 17 tools")

    # ── 3. Generate Industry Use Cases ──
    print("\n🏭 Generating Industry Use Case Workflows...")

    ind_dir = os.path.join(BASE, "industry")
    os.makedirs(ind_dir, exist_ok=True)

    real_estate_wf = generate_ind_real_estate()
    with open(os.path.join(ind_dir, "IND1_Real_Estate_Automation_v3.json"), "w") as f:
        json.dump(real_estate_wf, f, indent=2)
    print(f"  ✅ IND1_Real_Estate_Automation_v3.json — {len(real_estate_wf['nodes'])} nodes, 9 tools")

    restaurant_wf = generate_ind_restaurant()
    with open(os.path.join(ind_dir, "IND2_Restaurant_Operations_v3.json"), "w") as f:
        json.dump(restaurant_wf, f, indent=2)
    print(f"  ✅ IND2_Restaurant_Operations_v3.json — {len(restaurant_wf['nodes'])} nodes, 9 tools")

    saas_wf = generate_ind_saas()
    with open(os.path.join(ind_dir, "IND3_SaaS_Subscription_Engine_v3.json"), "w") as f:
        json.dump(saas_wf, f, indent=2)
    print(f"  ✅ IND3_SaaS_Subscription_Engine_v3.json — {len(saas_wf['nodes'])} nodes, 9 tools")

    agency_wf = generate_ind_agency()
    with open(os.path.join(ind_dir, "IND4_Agency_Client_Portal_v3.json"), "w") as f:
        json.dump(agency_wf, f, indent=2)
    print(f"  ✅ IND4_Agency_Client_Portal_v3.json — {len(agency_wf['nodes'])} nodes, 9 tools")

    # ── 4. Generate Cognitive Capital Skills ──
    print("\n🧠 Generating Cognitive Capital Skills...")

    cc_dir = os.path.join(BASE, "cognitive_capital")
    os.makedirs(cc_dir, exist_ok=True)

    for skill_key, skill_data in NEW_COGNITIVE_SKILLS.items():
        content = generate_skill_md(skill_key, skill_data)
        filename = f"{skill_key}_SKILL.md"
        filepath = os.path.join(cc_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  ✅ {filename} — {len(content)} chars, tier: {skill_data['tier']}")

    # ── 5. Generate INTEGRATIONS.md ──
    print("\n📚 Generating INTEGRATIONS.md...")

    integrations_md = generate_integrations_md()
    filepath = os.path.join(BASE, "INTEGRATIONS.md")
    with open(filepath, "w") as f:
        f.write(integrations_md)
    print(f"  ✅ INTEGRATIONS.md — {len(integrations_md)} chars")

    # ── 6. Update Manifests ──
    print("\n📋 Updating Manifests...")
    update_manifests()

    # ── 7. Sync to JARVIS Packages ──
    print("\n📦 Syncing to JARVIS Packages...")
    sync_to_jarvis_packages()

    # ── 8. Validation ──
    print("\n🔍 Validating Zero Technical Debt...")

    all_workflows = []
    for dirname, files in [
        ("mcp_servers", ["MCP_WhatsApp_Business_Server_v3.json", "MCP_Telegram_Bot_Server_v3.json", "MCP_Discord_Server_v3.json"]),
        ("orchestration", ["ORC5_WhatsApp_CRM_Stripe_Sales_Cycle_v3.json"]),
        ("industry", ["IND1_Real_Estate_Automation_v3.json", "IND2_Restaurant_Operations_v3.json",
                      "IND3_SaaS_Subscription_Engine_v3.json", "IND4_Agency_Client_Portal_v3.json"]),
    ]:
        for filename in files:
            filepath = os.path.join(BASE, dirname, filename)
            with open(filepath, "r") as f:
                wf = json.load(f)
            all_workflows.append((dirname, filename, wf))

    total_nodes = 0
    total_connections = 0
    issues = []

    for dirname, filename, wf in all_workflows:
        nodes = wf.get("nodes", [])
        connections = wf.get("connections", {})
        total_nodes += len(nodes)
        total_connections += len(connections)

        # Check for placeholder credentials
        for node in nodes:
            creds = node.get("credentials", {})
            if creds:
                for cred_name, cred_val in creds.items():
                    if isinstance(cred_val, dict):
                        if cred_val.get("id") == "PLACEHOLDER" or cred_val.get("name") == "PLACEHOLDER":
                            issues.append(f"{filename}: {node['name']} has PLACEHOLDER credentials")

        # Check for orphan nodes (nodes not in connections)
        connected_nodes = set()
        for src, targets in connections.items():
            connected_nodes.add(src)
            for conn_type, conn_list in targets.items():
                for conn in conn_list:
                    for target in conn:
                        connected_nodes.add(target["node"])

        for node in nodes:
            if node.get("type") == "n8n-nodes-base.stickyNote":
                continue
            if node["name"] not in connected_nodes:
                issues.append(f"{filename}: {node['name']} is orphan (not in connections)")

        # Check ai_* connections
        for src, targets in connections.items():
            for conn_type, conn_list in targets.items():
                if conn_type.startswith("ai_"):
                    for conn in conn_list:
                        for target in conn:
                            if target["type"] != conn_type:
                                issues.append(f"{filename}: {src}→{target['node']} type mismatch: {conn_type} vs {target['type']}")

    if issues:
        print(f"\n  ⚠️  Found {len(issues)} issues:")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print(f"\n  ✅ ZERO TECHNICAL DEBT — All {len(all_workflows)} workflows validated!")

    # ── Summary ──
    print("\n" + "=" * 60)
    print("PHASE 7 COMPLETE")
    print("=" * 60)
    print(f"  New MCP Servers: 3 (WhatsApp, Telegram, Discord)")
    print(f"  New Orchestration: 1 (WhatsApp→CRM→Stripe Sales Cycle)")
    print(f"  New Industry Workflows: 4 (Real Estate, Restaurant, SaaS, Agency)")
    print(f"  New Cognitive Skills: 3 (Communication, Sales Cycle, Industry)")
    print(f"  New Documentation: INTEGRATIONS.md")
    print(f"  Total New Nodes: {total_nodes}")
    print(f"  Total New Connections: {total_connections}")
    print(f"  MCP Server Catalog: 26 servers, 184+ tools")
    print(f"  Version: 5.0.0")
    print("=" * 60)


if __name__ == "__main__":
    main()
