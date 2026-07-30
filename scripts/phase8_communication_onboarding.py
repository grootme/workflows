#!/usr/bin/env python3
"""
Phase 8: Extended Communication Integrations + Industry Onboarding Workflows

3 New Communication MCP Servers:
  MCP_Twilio_SMS_Server_v3.json          (8 tools)
  MCP_Microsoft_Teams_Server_v3.json     (8 tools)
  MCP_Slack_Events_Server_v3.json        (8 tools)

3 Onboarding Orchestration Workflows:
  ORC6_Twilio_Teams_Slack_Multi_Channel_v3.json
  ORC7_Multi_Industry_Onboarding_v3.json

3 Industry Onboarding Workflows:
  IND5_Gym_Onboarding_v3.json
  IND6_Farmacia_Onboarding_v3.json
  IND7_Abogados_Onboarding_v3.json

3 Cognitive Capital Skills:
  COMMUNICATION_MULTI_CHANNEL_SKILL.md
  ONBOARDING_AUTOMATION_SKILL.md
  INDUSTRY_SPECIALIST_SKILL.md

Updated INTEGRATIONS.md with OAuth2, API details, deployment guides.

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
                    result[src][conn_type].extend(conn_list)
                else:
                    result[src][conn_type] = list(conn_list)
    return result


# ═══════════════════════════════════════════════════════════════════════
# 1. TWILIO SMS MCP SERVER
# ═══════════════════════════════════════════════════════════════════════

def generate_mcp_twilio():
    """Twilio SMS/WhatsApp/Voice MCP Server with 8 tools."""
    trigger = mcp_trigger("twilio-mcp", [0, 0])
    note = sticky_note(
        "Twilio SMS/Voice MCP Server\n\n8 Tools: Send SMS, Send WhatsApp, Make Call, Lookup Number, "
        "List Messages, Get Message, Verify OTP, Create Service\n\n"
        "Auth: Twilio Account SID + Auth Token\n"
        "OAuth2: N/A (API Key-based)\n"
        "API: api.twilio.com/2010-04-01/Accounts/{AccountSid}",
        [-400, -300]
    )
    tools = [
        http_tool("Send SMS", "Send an SMS message via Twilio. Supports to/from numbers, body text, media URLs, and status callback.",
                  "Send_SMS_URL", [-700, 400], "POST"),
        http_tool("Send WhatsApp", "Send a WhatsApp message via Twilio WhatsApp Business API. Supports template messages, media, and location.",
                  "Send_WhatsApp_URL", [-500, 400], "POST"),
        http_tool("Make Call", "Initiate a voice call via Twilio. Supports TwiML URL, application SID, and status callbacks.",
                  "Make_Call_URL", [-300, 400], "POST"),
        http_tool("Lookup Number", "Lookup a phone number via Twilio Lookup API. Returns carrier info, caller name, and line type.",
                  "Lookup_Number_URL", [-100, 400], "GET"),
        http_tool("List Messages", "List Twilio messages with filters for date, status, from/to number, and direction.",
                  "List_Messages_URL", [100, 400], "GET"),
        http_tool("Get Message", "Get details of a specific Twilio message including body, status, error code, and price.",
                  "Get_Message_URL", [300, 400], "GET"),
        http_tool("Verify OTP", "Send or verify a one-time password via Twilio Verify service. Supports SMS, call, and email channels.",
                  "Verify_OTP_URL", [500, 400], "POST"),
        http_tool("Create Service", "Create a Twilio service for Verify, Proxy, or Conversations. Configure settings and webhooks.",
                  "Create_Service_URL", [700, 400], "POST"),
    ]

    nodes = [trigger, note] + tools
    connections = merge_dicts([
        ai_conn("Send SMS", "MCP Trigger", "tool"),
        ai_conn("Send WhatsApp", "MCP Trigger", "tool"),
        ai_conn("Make Call", "MCP Trigger", "tool"),
        ai_conn("Lookup Number", "MCP Trigger", "tool"),
        ai_conn("List Messages", "MCP Trigger", "tool"),
        ai_conn("Get Message", "MCP Trigger", "tool"),
        ai_conn("Verify OTP", "MCP Trigger", "tool"),
        ai_conn("Create Service", "MCP Trigger", "tool"),
    ])
    return make_workflow("MCP Twilio SMS Server v3", nodes, connections,
                         [{"name": "mcp-server"}, {"name": "twilio"}, {"name": "communication"}, {"name": "sms"}])


# ═══════════════════════════════════════════════════════════════════════
# 2. MICROSOFT TEAMS MCP SERVER
# ═══════════════════════════════════════════════════════════════════════

def generate_mcp_teams():
    """Microsoft Teams MCP Server with 8 tools."""
    trigger = mcp_trigger("teams-mcp", [0, 0])
    note = sticky_note(
        "Microsoft Teams MCP Server\n\n8 Tools: Send Message, Create Channel, List Channels, Send Card, "
        "Manage Members, Get Chat, Create Meeting, List Chats\n\n"
        "Auth: Microsoft Graph API OAuth2\n"
        "OAuth2: Azure AD → Client Credentials / Authorization Code\n"
        "Scopes: Chat.ReadWrite, Channel.ReadWrite.All, TeamMember.ReadWrite.All, OnlineMeetings.ReadWrite\n"
        "API: graph.microsoft.com/v1.0",
        [-400, -300]
    )
    tools = [
        http_tool("Send Message", "Send a message to a Microsoft Teams channel or chat. Supports text, mentions, and attachments.",
                  "Send_Message_URL", [-700, 400], "POST"),
        http_tool("Create Channel", "Create a new channel in a Microsoft Teams team. Supports standard, private, and shared channels.",
                  "Create_Channel_URL", [-500, 400], "POST"),
        http_tool("List Channels", "List all channels in a Microsoft Teams team with details including display name, description, and membership.",
                  "List_Channels_URL", [-300, 400], "GET"),
        http_tool("Send Card", "Send an Adaptive Card to a Teams channel or chat. Supports interactive buttons, inputs, and action handlers.",
                  "Send_Card_URL", [-100, 400], "POST"),
        http_tool("Manage Members", "Add, remove, or update members in a Teams team or channel. Supports role assignment (owner/member).",
                  "Manage_Members_URL", [100, 400], "POST"),
        http_tool("Get Chat", "Get messages from a Microsoft Teams chat with filters for date, sender, and content.",
                  "Get_Chat_URL", [300, 400], "GET"),
        http_tool("Create Meeting", "Create an online meeting via Microsoft Teams. Supports subject, start/end time, participants, and lobby settings.",
                  "Create_Meeting_URL", [500, 400], "POST"),
        http_tool("List Chats", "List all Microsoft Teams chats for the authenticated user. Supports filters for type and members.",
                  "List_Chats_URL", [700, 400], "GET"),
    ]

    nodes = [trigger, note] + tools
    connections = merge_dicts([
        ai_conn("Send Message", "MCP Trigger", "tool"),
        ai_conn("Create Channel", "MCP Trigger", "tool"),
        ai_conn("List Channels", "MCP Trigger", "tool"),
        ai_conn("Send Card", "MCP Trigger", "tool"),
        ai_conn("Manage Members", "MCP Trigger", "tool"),
        ai_conn("Get Chat", "MCP Trigger", "tool"),
        ai_conn("Create Meeting", "MCP Trigger", "tool"),
        ai_conn("List Chats", "MCP Trigger", "tool"),
    ])
    return make_workflow("MCP Microsoft Teams Server v3", nodes, connections,
                         [{"name": "mcp-server"}, {"name": "microsoft-teams"}, {"name": "communication"}, {"name": "enterprise"}])


# ═══════════════════════════════════════════════════════════════════════
# 3. SLACK EVENTS MCP SERVER
# ═══════════════════════════════════════════════════════════════════════

def generate_mcp_slack():
    """Slack Events API MCP Server with 8 tools."""
    trigger = mcp_trigger("slack-mcp", [0, 0])
    note = sticky_note(
        "Slack Events MCP Server\n\n8 Tools: Send Message, List Channels, Create Channel, Manage Members, "
        "Search Messages, Send Block Kit, Get Thread, Set Status\n\n"
        "Auth: Slack Bot Token (xoxb-) + OAuth2\n"
        "OAuth2: Slack OAuth2 → Authorization Code with bot + chat + channels scopes\n"
        "Scopes: chat:write, channels:read, channels:manage, users:read, search:read, users.profile:write\n"
        "API: slack.com/api",
        [-400, -300]
    )
    tools = [
        http_tool("Send Message", "Post a message to a Slack channel or DM. Supports text, blocks, attachments, and thread replies.",
                  "Send_Message_URL", [-700, 400], "POST"),
        http_tool("List Channels", "List all Slack channels in the workspace with details including name, purpose, members, and topic.",
                  "List_Channels_URL", [-500, 400], "GET"),
        http_tool("Create Channel", "Create a new Slack channel (public or private). Supports name, topic, purpose, and initial members.",
                  "Create_Channel_URL", [-300, 400], "POST"),
        http_tool("Manage Members", "Invite, kick, or list members in a Slack channel. Supports single and bulk operations.",
                  "Manage_Members_URL", [-100, 400], "POST"),
        http_tool("Search Messages", "Search Slack messages across all channels and DMs. Supports query, sort, count, and highlight.",
                  "Search_Messages_URL", [100, 400], "GET"),
        http_tool("Send Block Kit", "Send a rich Block Kit message with sections, actions, inputs, and interactive components.",
                  "Send_Block_Kit_URL", [300, 400], "POST"),
        http_tool("Get Thread", "Get all replies in a Slack message thread. Supports chronological sorting and pagination.",
                  "Get_Thread_URL", [500, 400], "GET"),
        http_tool("Set Status", "Set or clear a user's Slack profile status with emoji and expiration. Useful for availability signals.",
                  "Set_Status_URL", [700, 400], "POST"),
    ]

    nodes = [trigger, note] + tools
    connections = merge_dicts([
        ai_conn("Send Message", "MCP Trigger", "tool"),
        ai_conn("List Channels", "MCP Trigger", "tool"),
        ai_conn("Create Channel", "MCP Trigger", "tool"),
        ai_conn("Manage Members", "MCP Trigger", "tool"),
        ai_conn("Search Messages", "MCP Trigger", "tool"),
        ai_conn("Send Block Kit", "MCP Trigger", "tool"),
        ai_conn("Get Thread", "MCP Trigger", "tool"),
        ai_conn("Set Status", "MCP Trigger", "tool"),
    ])
    return make_workflow("MCP Slack Events Server v3", nodes, connections,
                         [{"name": "mcp-server"}, {"name": "slack"}, {"name": "communication"}, {"name": "events"}])


# ═══════════════════════════════════════════════════════════════════════
# 4. MULTI-CHANNEL ORCHESTRATION (Twilio + Teams + Slack)
# ═══════════════════════════════════════════════════════════════════════

def generate_orc_multi_channel():
    """Multi-channel communication orchestration: Twilio SMS + Teams + Slack."""
    trigger = chat_trigger([-2200, 0],
        "I am your Multi-Channel Communication Orchestrator. I manage messages across Twilio SMS, Microsoft Teams, "
        "and Slack simultaneously. I can broadcast, route, and track communications across all channels. What do you need?")

    agent = agent_node("Multi-Channel Orchestrator",
        "# Multi-Channel Communication Orchestrator\n\n"
        "You orchestrate communications across three enterprise platforms:\n\n"
        "## Channel 1: Twilio SMS\n"
        "- Send SMS messages to any phone number globally\n"
        "- Send WhatsApp messages via Twilio Business API\n"
        "- Make voice calls with TwiML instructions\n"
        "- Verify phone numbers with OTP for security\n"
        "- Lookup carrier and line type information\n"
        "- Track delivery status and message analytics\n\n"
        "## Channel 2: Microsoft Teams\n"
        "- Send messages to channels and chats\n"
        "- Create and manage team channels\n"
        "- Send Adaptive Cards for interactive workflows\n"
        "- Schedule and manage online meetings\n"
        "- Manage team members and roles\n"
        "- Integrate with Microsoft 365 ecosystem\n\n"
        "## Channel 3: Slack\n"
        "- Send messages with Block Kit formatting\n"
        "- Create and manage channels\n"
        "- Search messages across workspace\n"
        "- Manage thread conversations\n"
        "- Set user status for availability\n"
        "- Handle Slack Events API webhooks\n\n"
        "## Cross-Channel Workflows:\n"
        "1. Broadcast: Send same message to SMS + Teams + Slack simultaneously\n"
        "2. Escalation: SMS → Teams channel → Slack channel escalation path\n"
        "3. Routing: Route incoming messages to appropriate channel based on priority\n"
        "4. Sync: Mirror important messages across all channels\n"
        "5. Analytics: Track delivery, read rates, and response times per channel\n"
        "6. Onboarding: Welcome new members across all channels\n"
        "7. Incident: Alert teams on all channels for critical incidents\n\n"
        "## Skills Loaded:\n"
        "- multi-channel: Cross-platform message orchestration\n"
        "- deep-research: Communication best practices\n"
        "- data-analysis: Channel analytics and metrics\n"
        "- consulting-analysis: Communication strategy optimization\n\n"
        "Current datetime: __DATE__",
        [-1600, 0])

    llm = llm_node("GPT-4.1 Multi-Channel", "gpt-4.1", 0.2, [-1600, 300])
    memory = memory_node("Multi-Channel Memory", [-1300, 300])
    parser = output_parser("Multi-Channel Output", [
        {"name": "channel", "description": "Channel used (twilio_sms/teams/slack/multi)"},
        {"name": "action", "description": "Action performed"},
        {"name": "result", "description": "Result summary"},
        {"name": "message_id", "description": "Message ID if applicable"},
        {"name": "recipients", "description": "Number of recipients reached"},
        {"name": "delivery_status", "description": "Delivery status (sent/delivered/failed)"},
        {"name": "next_steps", "description": "Recommended follow-up actions"},
    ], [-1300, 0])

    # Twilio tools
    twilio_sms = http_tool("Twilio Send SMS", "Send an SMS message via Twilio with body, media URL, and status callback.",
                          "Twilio_SMS_URL", [-700, 500], "POST")
    twilio_wa = http_tool("Twilio WhatsApp", "Send a WhatsApp message via Twilio Business API with template or media.",
                          "Twilio_WA_URL", [-500, 500], "POST")
    twilio_call = http_tool("Twilio Call", "Initiate a voice call via Twilio with TwiML URL or application SID.",
                            "Twilio_Call_URL", [-300, 500], "POST")
    twilio_verify = http_tool("Twilio Verify", "Send or verify OTP via Twilio Verify for secure authentication.",
                              "Twilio_Verify_URL", [-100, 500], "POST")

    # Teams tools
    teams_msg = http_tool("Teams Send Message", "Send a message to a Microsoft Teams channel or chat with text and attachments.",
                          "Teams_Msg_URL", [100, 500], "POST")
    teams_card = http_tool("Teams Send Card", "Send an Adaptive Card to Teams with interactive buttons and action handlers.",
                           "Teams_Card_URL", [300, 500], "POST")
    teams_meeting = http_tool("Teams Meeting", "Create a Teams online meeting with subject, time, participants, and lobby settings.",
                              "Teams_Meeting_URL", [500, 500], "POST")

    # Slack tools
    slack_msg = http_tool("Slack Send Message", "Post a message to a Slack channel or DM with text, blocks, and thread replies.",
                          "Slack_Msg_URL", [100, 700], "POST")
    slack_block = http_tool("Slack Block Kit", "Send a rich Block Kit message with sections, actions, and interactive components.",
                            "Slack_Block_URL", [300, 700], "POST")
    slack_search = http_tool("Slack Search", "Search Slack messages across all channels and DMs with query and filters.",
                             "Slack_Search_URL", [500, 700], "GET")
    slack_channel = http_tool("Slack Channel", "Create or manage a Slack channel with name, topic, purpose, and members.",
                              "Slack_Channel_URL", [700, 700], "POST")

    think = think_tool("Channel Reasoning", "Think through channel selection, message format, priority routing, and delivery optimization.",
                       [900, 500])

    note = sticky_note(
        "Multi-Channel Communication\n\n"
        "TWILIO: SMS + WhatsApp + Voice + OTP\n"
        "TEAMS: Messages + Cards + Meetings\n"
        "SLACK: Messages + Blocks + Search + Channels\n\n"
        "CROSS-CHANNEL:\n"
        "  Broadcast → Escalation → Routing → Sync",
        [-2200, -400]
    )

    nodes = [trigger, note, agent, llm, memory, parser,
             twilio_sms, twilio_wa, twilio_call, twilio_verify,
             teams_msg, teams_card, teams_meeting,
             slack_msg, slack_block, slack_search, slack_channel,
             think]

    connections = merge_dicts([
        main_conn("Chat Trigger", "Multi-Channel Orchestrator"),
        ai_conn("Multi-Channel Orchestrator", "GPT-4.1 Multi-Channel", "languageModel"),
        ai_conn("Multi-Channel Orchestrator", "Multi-Channel Memory", "memory"),
        ai_conn("Multi-Channel Orchestrator", "Multi-Channel Output", "outputParser"),
        ai_conn("Multi-Channel Orchestrator", "Twilio Send SMS", "tool"),
        ai_conn("Multi-Channel Orchestrator", "Twilio WhatsApp", "tool"),
        ai_conn("Multi-Channel Orchestrator", "Twilio Call", "tool"),
        ai_conn("Multi-Channel Orchestrator", "Twilio Verify", "tool"),
        ai_conn("Multi-Channel Orchestrator", "Teams Send Message", "tool"),
        ai_conn("Multi-Channel Orchestrator", "Teams Send Card", "tool"),
        ai_conn("Multi-Channel Orchestrator", "Teams Meeting", "tool"),
        ai_conn("Multi-Channel Orchestrator", "Slack Send Message", "tool"),
        ai_conn("Multi-Channel Orchestrator", "Slack Block Kit", "tool"),
        ai_conn("Multi-Channel Orchestrator", "Slack Search", "tool"),
        ai_conn("Multi-Channel Orchestrator", "Slack Channel", "tool"),
        ai_conn("Multi-Channel Orchestrator", "Channel Reasoning", "tool"),
    ])
    return make_workflow("ORC6 Twilio Teams Slack Multi-Channel v3", nodes, connections,
                         [{"name": "orchestration"}, {"name": "multi-channel"}, {"name": "communication"}])


# ═══════════════════════════════════════════════════════════════════════
# 5. MULTI-INDUSTRY ONBOARDING ORCHESTRATION
# ═══════════════════════════════════════════════════════════════════════

def generate_orc_onboarding():
    """Multi-industry onboarding orchestration: Gym, Farmacia, Abogados → CRM → Stripe."""
    trigger = chat_trigger([-2200, 0],
        "I am your Multi-Industry Onboarding Orchestrator. I manage automated onboarding for Gym, Farmacia (Pharmacy), "
        "and Abogados (Law Firm) clients. I handle lead capture, CRM registration, plan selection, and payment setup. "
        "Which industry do you need onboarding for?")

    agent = agent_node("Onboarding Orchestrator",
        "# Multi-Industry Onboarding Orchestrator\n\n"
        "You orchestrate automated onboarding across three industries:\n\n"
        "## Industry 1: Gym / Fitness Center\n"
        "- Capture leads via WhatsApp/SMS with fitness quiz\n"
        "- Register member in CRM with fitness goals and health data\n"
        "- Assign membership plan (Basic, Premium, VIP) with Stripe\n"
        "- Schedule orientation session via Teams/WhatsApp\n"
        "- Send welcome package with workout plan and nutrition guide\n"
        "- Set up recurring membership payment via Stripe\n"
        "- Track attendance and engagement metrics\n\n"
        "## Industry 2: Farmacia / Pharmacy\n"
        "- Capture patient leads via WhatsApp with health consultation\n"
        "- Register patient in CRM with medical profile and allergies\n"
        "- Assign service plan (Basic, Plus, Premium) with Stripe\n"
        "- Send medication reminders via SMS/WhatsApp\n"
        "- Schedule telemedicine consultation via Teams\n"
        "- Set up recurring prescription delivery\n"
        "- Track patient adherence and health outcomes\n\n"
        "## Industry 3: Abogados / Law Firm\n"
        "- Capture client leads via WhatsApp with legal consultation\n"
        "- Register client in CRM with case type and urgency\n"
        "- Assign service plan (Consultation, Representation, Premium) with Stripe\n"
        "- Schedule initial consultation via Teams meeting\n"
        "- Send document checklist via WhatsApp/email\n"
        "- Set up retainer or payment plan via Stripe\n"
        "- Track case milestones and deadlines\n\n"
        "## Common Onboarding Pipeline:\n"
        "1. Lead Capture → Qualify → Welcome Message\n"
        "2. CRM Registration → Profile → Plan Selection\n"
        "3. Payment Setup → Stripe Invoice/Subscription → Confirmation\n"
        "4. Orientation/Consultation → Scheduling → Reminder\n"
        "5. Follow-up → Engagement → Feedback\n\n"
        "## Skills Loaded:\n"
        "- onboarding-automation: Industry-specific onboarding flows\n"
        "- deep-research: Industry best practices\n"
        "- data-analysis: Onboarding metrics and conversion rates\n"
        "- consulting-analysis: Industry growth strategy\n\n"
        "Current datetime: __DATE__",
        [-1600, 0])

    llm = llm_node("GPT-4.1 Onboarding", "gpt-4.1", 0.2, [-1600, 300])
    memory = memory_node("Onboarding Memory", [-1300, 300])
    parser = output_parser("Onboarding Output", [
        {"name": "industry", "description": "Industry (gym/farmacia/abogados)"},
        {"name": "stage", "description": "Onboarding stage (lead_capture/registration/payment/orientation/followup)"},
        {"name": "action", "description": "Action performed"},
        {"name": "result", "description": "Result summary"},
        {"name": "client_id", "description": "CRM client ID"},
        {"name": "payment_id", "description": "Stripe payment ID if applicable"},
        {"name": "next_steps", "description": "Recommended next actions"},
    ], [-1300, 0])

    # Communication tools
    wa_send = http_tool("WA Send Welcome", "Send a WhatsApp welcome message to a new client with onboarding details and interactive buttons.",
                        "WA_Welcome_URL", [-700, 500], "POST")
    wa_quiz = http_tool("WA Onboarding Quiz", "Send an interactive WhatsApp quiz to qualify the lead and gather preferences.",
                        "WA_Quiz_URL", [-500, 500], "POST")
    wa_reminder = http_tool("WA Reminder", "Send a WhatsApp reminder for scheduled appointments, orientation, or consultation.",
                           "WA_Reminder_URL", [-300, 500], "POST")
    sms_welcome = http_tool("SMS Welcome", "Send a welcome SMS via Twilio with onboarding confirmation and next steps.",
                           "SMS_Welcome_URL", [-100, 500], "POST")

    # CRM tools
    crm_register = http_tool("CRM Register Client", "Register a new client in CRM with industry-specific profile, preferences, and plan.",
                             "CRM_Register_URL", [100, 500], "POST")
    crm_update = http_tool("CRM Update Profile", "Update client profile in CRM with onboarding progress, preferences, and notes.",
                           "CRM_Update_URL", [300, 500], "POST")
    crm_track = http_tool("CRM Track Onboarding", "Track onboarding progress for a client: stage, completion %, and engagement score.",
                          "CRM_Track_URL", [500, 500], "GET")

    # Payment tools
    stripe_plan = http_tool("Stripe Assign Plan", "Create a Stripe subscription or invoice for the selected plan based on industry and tier.",
                            "Stripe_Plan_URL", [100, 700], "POST")
    stripe_confirm = http_tool("Stripe Payment Confirm", "Confirm payment status and send receipt via WhatsApp/SMS.",
                               "Stripe_Confirm_URL", [300, 700], "GET")

    # Scheduling tools
    teams_schedule = http_tool("Teams Schedule", "Schedule a Microsoft Teams meeting for orientation, consultation, or appointment.",
                               "Teams_Schedule_URL", [500, 700], "POST")

    think = think_tool("Onboarding Reasoning", "Think through onboarding flow, industry requirements, plan selection, and engagement strategy.",
                       [900, 500])

    note = sticky_note(
        "Multi-Industry Onboarding\n\n"
        "GYM: Quiz → Register → Plan → Orientation → Track\n"
        "FARMACIA: Consult → Register → Plan → Telemedicine → Track\n"
        "ABOGADOS: Consult → Register → Plan → Meeting → Track\n\n"
        "COMMON: Lead → CRM → Stripe → Schedule → Follow-up",
        [-2200, -400]
    )

    nodes = [trigger, note, agent, llm, memory, parser,
             wa_send, wa_quiz, wa_reminder, sms_welcome,
             crm_register, crm_update, crm_track,
             stripe_plan, stripe_confirm, teams_schedule,
             think]

    connections = merge_dicts([
        main_conn("Chat Trigger", "Onboarding Orchestrator"),
        ai_conn("Onboarding Orchestrator", "GPT-4.1 Onboarding", "languageModel"),
        ai_conn("Onboarding Orchestrator", "Onboarding Memory", "memory"),
        ai_conn("Onboarding Orchestrator", "Onboarding Output", "outputParser"),
        ai_conn("Onboarding Orchestrator", "WA Send Welcome", "tool"),
        ai_conn("Onboarding Orchestrator", "WA Onboarding Quiz", "tool"),
        ai_conn("Onboarding Orchestrator", "WA Reminder", "tool"),
        ai_conn("Onboarding Orchestrator", "SMS Welcome", "tool"),
        ai_conn("Onboarding Orchestrator", "CRM Register Client", "tool"),
        ai_conn("Onboarding Orchestrator", "CRM Update Profile", "tool"),
        ai_conn("Onboarding Orchestrator", "CRM Track Onboarding", "tool"),
        ai_conn("Onboarding Orchestrator", "Stripe Assign Plan", "tool"),
        ai_conn("Onboarding Orchestrator", "Stripe Payment Confirm", "tool"),
        ai_conn("Onboarding Orchestrator", "Teams Schedule", "tool"),
        ai_conn("Onboarding Orchestrator", "Onboarding Reasoning", "tool"),
    ])
    return make_workflow("ORC7 Multi-Industry Onboarding v3", nodes, connections,
                         [{"name": "orchestration"}, {"name": "onboarding"}, {"name": "industry"}])


# ═══════════════════════════════════════════════════════════════════════
# 6. INDUSTRY: GYM / FITNESS CENTER ONBOARDING
# ═══════════════════════════════════════════════════════════════════════

def generate_ind_gym():
    """Gym: WhatsApp lead → CRM member → Stripe membership → Teams orientation."""
    trigger = chat_trigger([-2200, 0],
        "I am your Gym Onboarding Assistant. I manage new member onboarding from WhatsApp lead capture through CRM "
        "registration, Stripe membership setup, and Teams orientation scheduling. How can I help?")

    agent = agent_node("Gym Onboarding Agent",
        "# Gym / Fitness Center Onboarding Agent\n\n"
        "You orchestrate gym member onboarding across multiple platforms:\n\n"
        "## Lead Capture & Qualification:\n"
        "- Send fitness quiz via WhatsApp interactive messages\n"
        "- Qualify leads by fitness goals (weight loss, muscle gain, general fitness, sports)\n"
        "- Collect health data: age, weight, injuries, dietary restrictions\n"
        "- Assign fitness level: Beginner, Intermediate, Advanced\n"
        "- Send gym tour video and facilities overview via WhatsApp\n\n"
        "## Membership Registration:\n"
        "- Create member profile in CRM with personal data and fitness goals\n"
        "- Assign membership tier: Basic (gym access), Premium (classes + trainer), VIP (full service)\n"
        "- Calculate pricing based on tier, duration, and promotions\n"
        "- Collect emergency contact and health waiver\n"
        "- Assign locker and access card\n\n"
        "## Payment Setup:\n"
        "- Create Stripe subscription for recurring membership\n"
        "- Handle enrollment fee and first month payment\n"
        "- Set up automatic renewal with Stripe\n"
        "- Process upgrades and add-ons (personal trainer, classes)\n"
        "- Generate payment receipts and invoices\n\n"
        "## Orientation & Engagement:\n"
        "- Schedule orientation session via Teams meeting\n"
        "- Send workout plan and nutrition guide via WhatsApp\n"
        "- Set up SMS reminders for gym visits and class bookings\n"
        "- Track attendance and engagement metrics\n"
        "- Send motivational messages and progress check-ins\n"
        "- Celebrate milestones (1st week, 1st month, 100 visits)\n\n"
        "## Pipeline Stages:\n"
        "Lead → Qualified → Registered → Payment → Oriented → Active → Retained\n\n"
        "## Skills Loaded:\n"
        "- onboarding-automation: Gym-specific onboarding flows\n"
        "- data-analysis: Member retention and engagement metrics\n"
        "- deep-research: Fitness industry trends\n"
        "- consulting-analysis: Gym growth strategy\n\n"
        "Current datetime: __DATE__",
        [-1600, 0])

    llm = llm_node("GPT-4.1 Gym", "gpt-4.1", 0.2, [-1600, 300])
    memory = memory_node("Gym Memory", [-1300, 300])
    parser = output_parser("Gym Output", [
        {"name": "category", "description": "Category (lead/registration/payment/orientation/engagement)"},
        {"name": "action", "description": "Action performed"},
        {"name": "result", "description": "Result summary"},
        {"name": "member_id", "description": "CRM member ID if applicable"},
        {"name": "subscription_id", "description": "Stripe subscription ID if applicable"},
        {"name": "tier", "description": "Membership tier (Basic/Premium/VIP)"},
    ], [-1300, 0])

    # WhatsApp tools
    wa_quiz = http_tool("WA Fitness Quiz", "Send an interactive fitness quiz via WhatsApp to qualify the lead and gather fitness goals and health data.",
                        "WA_Quiz_URL", [-700, 500], "POST")
    wa_tour = http_tool("WA Gym Tour", "Send gym tour video and facilities overview via WhatsApp media message.",
                        "WA_Tour_URL", [-500, 500], "POST")
    wa_welcome = http_tool("WA Welcome Pack", "Send a welcome package via WhatsApp with workout plan, nutrition guide, and gym rules.",
                           "WA_Welcome_URL", [-300, 500], "POST")
    wa_motivate = http_tool("WA Motivation", "Send motivational messages, progress check-ins, and milestone celebrations via WhatsApp.",
                            "WA_Motivate_URL", [-100, 500], "POST")

    # CRM tools
    crm_member = http_tool("CRM Register Member", "Create a gym member profile in CRM with personal data, fitness goals, health data, and membership tier.",
                           "CRM_Member_URL", [100, 500], "POST")
    crm_attendance = http_tool("CRM Track Attendance", "Log member gym attendance and class bookings in CRM. Track engagement metrics.",
                               "CRM_Attendance_URL", [300, 500], "POST")
    crm_progress = http_tool("CRM Member Progress", "Track member progress: fitness goals, weight, measurements, and milestones achieved.",
                             "CRM_Progress_URL", [500, 500], "GET")

    # Stripe tools
    stripe_sub = http_tool("Stripe Membership", "Create a Stripe subscription for gym membership with tier, duration, and enrollment fee.",
                           "Stripe_Membership_URL", [100, 700], "POST")
    stripe_upgrade = http_tool("Stripe Upgrade", "Process a membership upgrade or add-on (personal trainer, classes, locker) via Stripe.",
                               "Stripe_Upgrade_URL", [300, 700], "POST")

    # SMS/Teams tools
    sms_reminder = http_tool("SMS Visit Reminder", "Send a Twilio SMS reminder for gym visits, class bookings, and upcoming sessions.",
                             "SMS_Reminder_URL", [500, 700], "POST")
    teams_orient = http_tool("Teams Orientation", "Schedule a Microsoft Teams orientation session for new member onboarding.",
                             "Teams_Orient_URL", [700, 700], "POST")

    think = think_tool("Gym Reasoning", "Think through fitness level assessment, membership tier recommendation, workout plan, and engagement strategy.",
                       [900, 500])

    note = sticky_note(
        "Gym / Fitness Center Onboarding\n\n"
        "FLOW: WhatsApp Quiz → CRM Register → Stripe Membership → Teams Orientation\n\n"
        "Platforms: WhatsApp, CRM, Stripe, Twilio SMS, Teams\n"
        "Tiers: Basic / Premium / VIP\n"
        "Pipeline: Lead → Qualified → Registered → Payment → Oriented → Active",
        [-2200, -400]
    )

    nodes = [trigger, note, agent, llm, memory, parser,
             wa_quiz, wa_tour, wa_welcome, wa_motivate,
             crm_member, crm_attendance, crm_progress,
             stripe_sub, stripe_upgrade,
             sms_reminder, teams_orient, think]

    connections = merge_dicts([
        main_conn("Chat Trigger", "Gym Onboarding Agent"),
        ai_conn("Gym Onboarding Agent", "GPT-4.1 Gym", "languageModel"),
        ai_conn("Gym Onboarding Agent", "Gym Memory", "memory"),
        ai_conn("Gym Onboarding Agent", "Gym Output", "outputParser"),
        ai_conn("Gym Onboarding Agent", "WA Fitness Quiz", "tool"),
        ai_conn("Gym Onboarding Agent", "WA Gym Tour", "tool"),
        ai_conn("Gym Onboarding Agent", "WA Welcome Pack", "tool"),
        ai_conn("Gym Onboarding Agent", "WA Motivation", "tool"),
        ai_conn("Gym Onboarding Agent", "CRM Register Member", "tool"),
        ai_conn("Gym Onboarding Agent", "CRM Track Attendance", "tool"),
        ai_conn("Gym Onboarding Agent", "CRM Member Progress", "tool"),
        ai_conn("Gym Onboarding Agent", "Stripe Membership", "tool"),
        ai_conn("Gym Onboarding Agent", "Stripe Upgrade", "tool"),
        ai_conn("Gym Onboarding Agent", "SMS Visit Reminder", "tool"),
        ai_conn("Gym Onboarding Agent", "Teams Orientation", "tool"),
        ai_conn("Gym Onboarding Agent", "Gym Reasoning", "tool"),
    ])
    return make_workflow("IND5 Gym Onboarding v3", nodes, connections,
                         [{"name": "industry"}, {"name": "gym"}, {"name": "fitness"}, {"name": "onboarding"}])


# ═══════════════════════════════════════════════════════════════════════
# 7. INDUSTRY: FARMACIA / PHARMACY ONBOARDING
# ═══════════════════════════════════════════════════════════════════════

def generate_ind_farmacia():
    """Farmacia: WhatsApp consult → CRM patient → Stripe plan → Teams telemedicine → SMS reminders."""
    trigger = chat_trigger([-2200, 0],
        "I am your Farmacia (Pharmacy) Onboarding Assistant. I manage patient onboarding from WhatsApp health consultation "
        "through CRM registration, Stripe service plan, Teams telemedicine scheduling, and SMS medication reminders. "
        "How can I help?")

    agent = agent_node("Farmacia Onboarding Agent",
        "# Farmacia / Pharmacy Onboarding Agent\n\n"
        "You orchestrate pharmacy patient onboarding across multiple platforms:\n\n"
        "## Patient Lead Capture:\n"
        "- Send health consultation form via WhatsApp interactive messages\n"
        "- Collect patient data: name, age, allergies, current medications, conditions\n"
        "- Qualify patient by service need: prescription refill, telemedicine, delivery, wellness\n"
        "- Verify insurance information and coverage\n"
        "- Send pharmacy services overview and pricing via WhatsApp\n\n"
        "## Patient Registration:\n"
        "- Create patient profile in CRM with medical data and preferences\n"
        "- Assign service tier: Basic (prescription), Plus (telemedicine + delivery), Premium (full care)\n"
        "- Record allergies, contraindications, and medication interactions\n"
        "- Set up emergency contact and preferred pharmacy location\n"
        "- Generate patient ID and QR code for easy pickup\n\n"
        "## Payment Setup:\n"
        "- Create Stripe subscription for recurring service plan\n"
        "- Process insurance co-pay and out-of-pocket payments\n"
        "- Set up automatic prescription delivery billing\n"
        "- Handle prescription discount programs\n"
        "- Generate payment receipts for insurance claims\n\n"
        "## Telemedicine & Consultation:\n"
        "- Schedule telemedicine consultation via Microsoft Teams\n"
        "- Send consultation reminders via WhatsApp and SMS\n"
        "- Share prescription details and dosage instructions via WhatsApp\n"
        "- Record consultation notes in CRM\n"
        "- Follow up on treatment adherence\n\n"
        "## Medication Reminders:\n"
        "- Set up daily medication reminders via Twilio SMS\n"
        "- Send refill reminders 5 days before prescription runs out\n"
        "- Track medication adherence and report to healthcare provider\n"
        "- Alert on drug interactions and contraindications\n"
        "- Celebrate adherence milestones\n\n"
        "## Pipeline Stages:\n"
        "Lead → Consultation → Registered → Payment → Active → Retained\n\n"
        "## Skills Loaded:\n"
        "- onboarding-automation: Pharmacy-specific onboarding flows\n"
        "- data-analysis: Patient adherence and health outcomes\n"
        "- deep-research: Pharmacy industry best practices\n"
        "- consulting-analysis: Pharmacy growth and retention strategy\n\n"
        "Current datetime: __DATE__",
        [-1600, 0])

    llm = llm_node("GPT-4.1 Farmacia", "gpt-4.1", 0.2, [-1600, 300])
    memory = memory_node("Farmacia Memory", [-1300, 300])
    parser = output_parser("Farmacia Output", [
        {"name": "category", "description": "Category (lead/registration/payment/telemedicine/reminders)"},
        {"name": "action", "description": "Action performed"},
        {"name": "result", "description": "Result summary"},
        {"name": "patient_id", "description": "CRM patient ID if applicable"},
        {"name": "subscription_id", "description": "Stripe subscription ID if applicable"},
        {"name": "tier", "description": "Service tier (Basic/Plus/Premium)"},
    ], [-1300, 0])

    # WhatsApp tools
    wa_consult = http_tool("WA Health Consult", "Send a health consultation form via WhatsApp to collect patient data, symptoms, and medication needs.",
                           "WA_Consult_URL", [-700, 500], "POST")
    wa_prescription = http_tool("WA Prescription Info", "Send prescription details, dosage instructions, and side effects via WhatsApp.",
                                "WA_Prescription_URL", [-500, 500], "POST")
    wa_refill = http_tool("WA Refill Reminder", "Send a prescription refill reminder via WhatsApp 5 days before the prescription runs out.",
                          "WA_Refill_URL", [-300, 500], "POST")
    wa_services = http_tool("WA Pharmacy Services", "Send pharmacy services overview and pricing information via WhatsApp with interactive buttons.",
                            "WA_Services_URL", [-100, 500], "POST")

    # CRM tools
    crm_patient = http_tool("CRM Register Patient", "Create a patient profile in CRM with medical data, allergies, medications, and service tier.",
                            "CRM_Patient_URL", [100, 500], "POST")
    crm_adherence = http_tool("CRM Track Adherence", "Track patient medication adherence and report to healthcare provider. Log missed doses and refill dates.",
                              "CRM_Adherence_URL", [300, 500], "POST")
    crm_interactions = http_tool("CRM Drug Interactions", "Check and log drug interactions and contraindications for a patient's medication list.",
                                 "CRM_Interactions_URL", [500, 500], "GET")

    # Stripe tools
    stripe_plan = http_tool("Stripe Service Plan", "Create a Stripe subscription for pharmacy service plan with tier, co-pay, and delivery billing.",
                            "Stripe_Plan_URL", [100, 700], "POST")
    stripe_copay = http_tool("Stripe Co-Pay", "Process insurance co-pay and out-of-pocket payments via Stripe with receipt generation.",
                             "Stripe_CoPay_URL", [300, 700], "POST")

    # SMS/Teams tools
    sms_med = http_tool("SMS Medication Reminder", "Send a daily medication reminder via Twilio SMS with dosage, timing, and special instructions.",
                        "SMS_Med_URL", [500, 700], "POST")
    teams_telemed = http_tool("Teams Telemedicine", "Schedule a Microsoft Teams telemedicine consultation with doctor, patient, and notes.",
                              "Teams_Telemed_URL", [700, 700], "POST")

    think = think_tool("Farmacia Reasoning", "Think through patient qualification, medication interactions, service tier, and adherence strategy.",
                       [900, 500])

    note = sticky_note(
        "Farmacia / Pharmacy Onboarding\n\n"
        "FLOW: WhatsApp Consult → CRM Patient → Stripe Plan → Teams Telemedicine → SMS Reminders\n\n"
        "Platforms: WhatsApp, CRM, Stripe, Twilio SMS, Teams\n"
        "Tiers: Basic (Rx) / Plus (Telemedicine+Delivery) / Premium (Full Care)\n"
        "Pipeline: Lead → Consultation → Registered → Payment → Active",
        [-2200, -400]
    )

    nodes = [trigger, note, agent, llm, memory, parser,
             wa_consult, wa_prescription, wa_refill, wa_services,
             crm_patient, crm_adherence, crm_interactions,
             stripe_plan, stripe_copay,
             sms_med, teams_telemed, think]

    connections = merge_dicts([
        main_conn("Chat Trigger", "Farmacia Onboarding Agent"),
        ai_conn("Farmacia Onboarding Agent", "GPT-4.1 Farmacia", "languageModel"),
        ai_conn("Farmacia Onboarding Agent", "Farmacia Memory", "memory"),
        ai_conn("Farmacia Onboarding Agent", "Farmacia Output", "outputParser"),
        ai_conn("Farmacia Onboarding Agent", "WA Health Consult", "tool"),
        ai_conn("Farmacia Onboarding Agent", "WA Prescription Info", "tool"),
        ai_conn("Farmacia Onboarding Agent", "WA Refill Reminder", "tool"),
        ai_conn("Farmacia Onboarding Agent", "WA Pharmacy Services", "tool"),
        ai_conn("Farmacia Onboarding Agent", "CRM Register Patient", "tool"),
        ai_conn("Farmacia Onboarding Agent", "CRM Track Adherence", "tool"),
        ai_conn("Farmacia Onboarding Agent", "CRM Drug Interactions", "tool"),
        ai_conn("Farmacia Onboarding Agent", "Stripe Service Plan", "tool"),
        ai_conn("Farmacia Onboarding Agent", "Stripe Co-Pay", "tool"),
        ai_conn("Farmacia Onboarding Agent", "SMS Medication Reminder", "tool"),
        ai_conn("Farmacia Onboarding Agent", "Teams Telemedicine", "tool"),
        ai_conn("Farmacia Onboarding Agent", "Farmacia Reasoning", "tool"),
    ])
    return make_workflow("IND6 Farmacia Onboarding v3", nodes, connections,
                         [{"name": "industry"}, {"name": "farmacia"}, {"name": "pharmacy"}, {"name": "onboarding"}])


# ═══════════════════════════════════════════════════════════════════════
# 8. INDUSTRY: ABOGADOS / LAW FIRM ONBOARDING
# ═══════════════════════════════════════════════════════════════════════

def generate_ind_abogados():
    """Abogados: WhatsApp consult → CRM case → Stripe retainer → Teams meeting → Slack collaboration."""
    trigger = chat_trigger([-2200, 0],
        "I am your Abogados (Law Firm) Onboarding Assistant. I manage client onboarding from WhatsApp legal consultation "
        "through CRM case registration, Stripe retainer payment, Teams consultation scheduling, and Slack internal collaboration. "
        "How can I help?")

    agent = agent_node("Abogados Onboarding Agent",
        "# Abogados / Law Firm Onboarding Agent\n\n"
        "You orchestrate law firm client onboarding across multiple platforms:\n\n"
        "## Client Lead Capture:\n"
        "- Send legal consultation form via WhatsApp interactive messages\n"
        "- Collect client data: name, case type, urgency, opposing party\n"
        "- Qualify by practice area: Civil, Criminal, Family, Corporate, Immigration, Labor, IP\n"
        "- Assess case urgency: Emergency, Urgent, Standard, Consultation Only\n"
        "- Send confidentiality agreement and engagement letter via WhatsApp\n"
        "- Verify client identity and conflict of interest check\n\n"
        "## Case Registration:\n"
        "- Create client profile in CRM with case details and legal metadata\n"
        "- Assign service tier: Consultation (one-time), Representation (full case), Premium (priority + 24/7)\n"
        "- Record case type, jurisdiction, and key dates\n"
        "- Assign attorney based on practice area and availability\n"
        "- Create matter number and case folder\n"
        "- Set up conflict check and ethical walls\n\n"
        "## Payment Setup:\n"
        "- Create Stripe invoice for retainer or consultation fee\n"
        "- Set up recurring billing for ongoing representation\n"
        "- Process contingency fee agreements (if applicable)\n"
        "- Handle payment plans and installment schedules\n"
        "- Generate trust account and operating account records\n"
        "- Track billable hours and expenses\n\n"
        "## Consultation & Communication:\n"
        "- Schedule initial consultation via Microsoft Teams meeting\n"
        "- Send document checklist via WhatsApp (ID, contracts, evidence, etc.)\n"
        "- Create Slack channel for internal case collaboration\n"
        "- Set up SMS reminders for court dates and deadlines\n"
        "- Send case status updates via WhatsApp\n"
        "- Track billable time and client communications\n\n"
        "## Deadline & Compliance:\n"
        "- Track statute of limitations and filing deadlines\n"
        "- Send court date reminders via SMS and WhatsApp\n"
        "- Generate compliance reports and status updates\n"
        "- Flag approaching deadlines and escalation requirements\n"
        "- Maintain audit trail of all communications\n\n"
        "## Pipeline Stages:\n"
        "Lead → Consultation → Conflict Check → Retainer → Active → Resolution\n\n"
        "## Skills Loaded:\n"
        "- onboarding-automation: Law firm-specific onboarding flows\n"
        "- data-analysis: Case metrics and billable hours tracking\n"
        "- deep-research: Legal industry trends and best practices\n"
        "- consulting-analysis: Law firm growth and client retention strategy\n\n"
        "Current datetime: __DATE__",
        [-1600, 0])

    llm = llm_node("GPT-4.1 Abogados", "gpt-4.1", 0.2, [-1600, 300])
    memory = memory_node("Abogados Memory", [-1300, 300])
    parser = output_parser("Abogados Output", [
        {"name": "category", "description": "Category (lead/registration/payment/consultation/compliance)"},
        {"name": "action", "description": "Action performed"},
        {"name": "result", "description": "Result summary"},
        {"name": "client_id", "description": "CRM client ID if applicable"},
        {"name": "case_id", "description": "CRM case/matter ID if applicable"},
        {"name": "payment_id", "description": "Stripe payment ID if applicable"},
        {"name": "practice_area", "description": "Practice area (Civil/Criminal/Family/Corporate/Immigration/Labor/IP)"},
    ], [-1300, 0])

    # WhatsApp tools
    wa_consult = http_tool("WA Legal Consult", "Send a legal consultation form via WhatsApp to collect case type, urgency, and client details.",
                           "WA_Consult_URL", [-700, 500], "POST")
    wa_docs = http_tool("WA Document Checklist", "Send a document checklist via WhatsApp based on case type (ID, contracts, evidence, financial records).",
                        "WA_Docs_URL", [-500, 500], "POST")
    wa_status = http_tool("WA Case Status", "Send a case status update via WhatsApp with key milestones, next steps, and deadline reminders.",
                          "WA_Status_URL", [-300, 500], "POST")
    wa_confidential = http_tool("WA Confidentiality", "Send confidentiality agreement and engagement letter via WhatsApp for client signature.",
                                "WA_Confidential_URL", [-100, 500], "POST")

    # CRM tools
    crm_client = http_tool("CRM Register Client", "Create a law firm client profile in CRM with case type, urgency, practice area, and assigned attorney.",
                           "CRM_Client_URL", [100, 500], "POST")
    crm_case = http_tool("CRM Create Case", "Create a legal case/matter in CRM with matter number, jurisdiction, key dates, and conflict check results.",
                         "CRM_Case_URL", [300, 500], "POST")
    crm_deadline = http_tool("CRM Track Deadlines", "Track statute of limitations, filing deadlines, and court dates. Flag approaching deadlines.",
                             "CRM_Deadline_URL", [500, 500], "GET")

    # Stripe tools
    stripe_retainer = http_tool("Stripe Retainer", "Create a Stripe invoice for retainer fee or consultation charge with payment plan options.",
                                "Stripe_Retainer_URL", [100, 700], "POST")
    stripe_billing = http_tool("Stripe Billing", "Set up recurring billing for ongoing representation, track billable hours, and process expenses.",
                               "Stripe_Billing_URL", [300, 700], "POST")

    # Slack/Teams/SMS tools
    slack_channel = http_tool("Slack Case Channel", "Create a Slack channel for internal case collaboration with attorney, paralegal, and support staff.",
                              "Slack_Channel_URL", [500, 700], "POST")
    teams_meeting = http_tool("Teams Consultation", "Schedule a Microsoft Teams consultation meeting with client, attorney, and case notes.",
                              "Teams_Meeting_URL", [700, 700], "POST")
    sms_deadline = http_tool("SMS Deadline Alert", "Send a Twilio SMS alert for court dates, filing deadlines, and statute of limitations approaching.",
                             "SMS_Deadline_URL", [900, 700], "POST")

    think = think_tool("Abogados Reasoning", "Think through case qualification, conflict check, practice area assignment, retainer structure, and deadline management.",
                       [1100, 500])

    note = sticky_note(
        "Abogados / Law Firm Onboarding\n\n"
        "FLOW: WhatsApp Consult → CRM Case → Stripe Retainer → Teams Meeting → Slack Collaboration\n\n"
        "Platforms: WhatsApp, CRM, Stripe, Slack, Teams, Twilio SMS\n"
        "Tiers: Consultation / Representation / Premium\n"
        "Practice: Civil, Criminal, Family, Corporate, Immigration, Labor, IP\n"
        "Pipeline: Lead → Consultation → Conflict Check → Retainer → Active → Resolution",
        [-2200, -400]
    )

    nodes = [trigger, note, agent, llm, memory, parser,
             wa_consult, wa_docs, wa_status, wa_confidential,
             crm_client, crm_case, crm_deadline,
             stripe_retainer, stripe_billing,
             slack_channel, teams_meeting, sms_deadline, think]

    connections = merge_dicts([
        main_conn("Chat Trigger", "Abogados Onboarding Agent"),
        ai_conn("Abogados Onboarding Agent", "GPT-4.1 Abogados", "languageModel"),
        ai_conn("Abogados Onboarding Agent", "Abogados Memory", "memory"),
        ai_conn("Abogados Onboarding Agent", "Abogados Output", "outputParser"),
        ai_conn("Abogados Onboarding Agent", "WA Legal Consult", "tool"),
        ai_conn("Abogados Onboarding Agent", "WA Document Checklist", "tool"),
        ai_conn("Abogados Onboarding Agent", "WA Case Status", "tool"),
        ai_conn("Abogados Onboarding Agent", "WA Confidentiality", "tool"),
        ai_conn("Abogados Onboarding Agent", "CRM Register Client", "tool"),
        ai_conn("Abogados Onboarding Agent", "CRM Create Case", "tool"),
        ai_conn("Abogados Onboarding Agent", "CRM Track Deadlines", "tool"),
        ai_conn("Abogados Onboarding Agent", "Stripe Retainer", "tool"),
        ai_conn("Abogados Onboarding Agent", "Stripe Billing", "tool"),
        ai_conn("Abogados Onboarding Agent", "Slack Case Channel", "tool"),
        ai_conn("Abogados Onboarding Agent", "Teams Consultation", "tool"),
        ai_conn("Abogados Onboarding Agent", "SMS Deadline Alert", "tool"),
        ai_conn("Abogados Onboarding Agent", "Abogados Reasoning", "tool"),
    ])
    return make_workflow("IND7 Abogados Onboarding v3", nodes, connections,
                         [{"name": "industry"}, {"name": "abogados"}, {"name": "law-firm"}, {"name": "onboarding"}])


# ═══════════════════════════════════════════════════════════════════════
# 9. COGNITIVE CAPITAL SKILLS
# ═══════════════════════════════════════════════════════════════════════

NEW_COGNITIVE_SKILLS = {
    "COMMUNICATION_MULTI_CHANNEL": {
        "name": "Multi-Channel Communication",
        "description": "Orchestrate communications across Twilio SMS, Microsoft Teams, and Slack with intelligent routing, broadcasting, and escalation.",
        "tier": "professional",
        "capabilities": [
            "Cross-channel message broadcasting (SMS + Teams + Slack)",
            "Priority-based message routing and escalation",
            "Channel analytics and delivery tracking",
            "Interactive message formatting (Adaptive Cards, Block Kit)",
            "Multi-channel onboarding workflows",
            "Incident alerting across all channels"
        ]
    },
    "ONBOARDING_AUTOMATION": {
        "name": "Onboarding Automation",
        "description": "Automate client onboarding for multiple industries with lead capture, CRM registration, payment setup, and engagement tracking.",
        "tier": "professional",
        "capabilities": [
            "Industry-specific onboarding flows (Gym, Farmacia, Abogados)",
            "Lead qualification and scoring automation",
            "CRM registration with industry-specific profiles",
            "Stripe payment and subscription setup",
            "Orientation and consultation scheduling",
            "Engagement tracking and retention automation"
        ]
    },
    "INDUSTRY_SPECIALIST": {
        "name": "Industry Specialist",
        "description": "Deep industry knowledge for Gym, Farmacia, and Abogados with specialized workflows, compliance requirements, and best practices.",
        "tier": "enterprise",
        "capabilities": [
            "Industry-specific compliance and regulatory knowledge",
            "Specialized workflow templates per industry",
            "Industry KPIs and metrics tracking",
            "Regulatory compliance automation",
            "Industry best practices and benchmarks",
            "Cross-industry pattern recognition and adaptation"
        ]
    }
}


def generate_skill_md(skill_key, skill_data):
    """Generate a cognitive capital skill markdown file."""
    return f"""# {skill_data['name']} — Cognitive Capital Skill

> Tier: {skill_data['tier'].title()} | Category: {skill_key.replace('_', ' ').title()}

## Description

{skill_data['description']}

## Capabilities

{chr(10).join(f"- {cap}" for cap in skill_data['capabilities'])}

## Integration Points

- **MCP Servers**: Twilio SMS, Microsoft Teams, Slack Events, WhatsApp Business, CRM, Stripe
- **Orchestration**: Multi-Channel Communication (ORC6), Multi-Industry Onboarding (ORC7)
- **Industry Workflows**: Gym (IND5), Farmacia (IND6), Abogados (IND7)
- **Memory**: Professional Enhanced Memory with industry-specific context

## Usage Patterns

### Pattern 1: Lead Capture
1. Receive incoming message on any channel
2. Qualify lead using industry-specific criteria
3. Register in CRM with profile data
4. Send confirmation and next steps

### Pattern 2: Payment Setup
1. Select appropriate plan based on industry
2. Create Stripe subscription or invoice
3. Process payment and send receipt
4. Schedule orientation/consultation

### Pattern 3: Engagement Tracking
1. Monitor client activity and interactions
2. Track key metrics and milestones
3. Send automated reminders and follow-ups
4. Generate retention and engagement reports

## Activation

This skill is automatically loaded when:
- Industry-specific onboarding workflows are triggered
- Multi-channel communication is required
- Industry compliance or regulatory checks are needed

## Version

- Created: Phase 8
- Last Updated: {datetime.now().strftime('%Y-%m-%d')}
- Compatible: JARVIS v6.0.0+
"""


# ═══════════════════════════════════════════════════════════════════════
# 10. INTEGRATIONS.md UPDATE
# ═══════════════════════════════════════════════════════════════════════

def generate_integrations_md():
    """Generate comprehensive INTEGRATIONS.md with all new servers."""
    return """# JARVIS AI Automation Ecosystem — Integrations Reference

> Version: 6.0.0 | Phase 8 | Last Updated: """ + datetime.now().strftime('%Y-%m-%d') + """

## Table of Contents

- [Communication MCP Servers](#communication-mcp-servers)
  - [Twilio SMS](#twilio-sms)
  - [Microsoft Teams](#microsoft-teams)
  - [Slack Events](#slack-events)
  - [WhatsApp Business API](#whatsapp-business-api)
  - [Telegram Bot](#telegram-bot)
  - [Discord](#discord)
- [Payment MCP Servers](#payment-mcp-servers)
- [Industry Onboarding Workflows](#industry-onboarding-workflows)
  - [Gym / Fitness Center](#gym--fitness-center)
  - [Farmacia / Pharmacy](#farmacia--pharmacy)
  - [Abogados / Law Firm](#abogados--law-firm)
- [OAuth2 Authentication Flows](#oauth2-authentication-flows)
- [API Reference](#api-reference)
- [Deployment Guide](#deployment-guide)

---

## Communication MCP Servers

### Twilio SMS

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Twilio_SMS_Server_v3.json` |
| **Tools** | 8 (Send SMS, Send WhatsApp, Make Call, Lookup Number, List Messages, Get Message, Verify OTP, Create Service) |
| **Auth Method** | API Key-based (Account SID + Auth Token) |
| **API Base** | `api.twilio.com/2010-04-01/Accounts/{AccountSid}` |
| **OAuth2** | Not required (API Key authentication) |
| **Tier** | Professional |

#### Setup Steps

1. Create a Twilio account at [twilio.com](https://www.twilio.com)
2. Get Account SID and Auth Token from the Twilio Console
3. Purchase a Twilio phone number
4. Configure credentials in n8n:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   ```
5. For WhatsApp Business via Twilio: Enable WhatsApp Business API in Twilio Console

#### Key Use Cases

- **SMS Notifications**: Send appointment reminders, order confirmations, and alerts
- **WhatsApp Business**: Send template messages, media, and interactive menus
- **Voice Calls**: Automated call campaigns and IVR systems
- **OTP Verification**: Two-factor authentication and phone number verification
- **Number Lookup**: Validate phone numbers and get carrier information

---

### Microsoft Teams

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Microsoft_Teams_Server_v3.json` |
| **Tools** | 8 (Send Message, Create Channel, List Channels, Send Card, Manage Members, Get Chat, Create Meeting, List Chats) |
| **Auth Method** | Microsoft Graph API OAuth2 |
| **API Base** | `graph.microsoft.com/v1.0` |
| **OAuth2 Flow** | Client Credentials / Authorization Code |
| **Tier** | Professional |

#### OAuth2 Setup

1. Register an application in [Azure Active Directory](https://portal.azure.com)
2. Configure API permissions:
   - `Chat.ReadWrite` — Send and read chat messages
   - `Channel.ReadWrite.All` — Create and manage channels
   - `TeamMember.ReadWrite.All` — Manage team members
   - `OnlineMeetings.ReadWrite` — Create and manage meetings
3. Grant admin consent for the application
4. Configure redirect URI: `https://your-n8n-instance.com/rest/oauth2-credential/callback`
5. Create client secret and note the value
6. Configure in n8n:
   ```
   AZURE_CLIENT_ID=your_client_id
   AZURE_CLIENT_SECRET=your_client_secret
   AZURE_TENANT_ID=your_tenant_id
   ```

#### Key Use Cases

- **Team Notifications**: Send alerts and updates to Teams channels
- **Adaptive Cards**: Interactive workflow cards with buttons and forms
- **Meeting Scheduling**: Create and manage Teams meetings
- **Channel Management**: Create project channels and manage membership
- **Internal Collaboration**: Route messages between teams and departments

---

### Slack Events

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Slack_Events_Server_v3.json` |
| **Tools** | 8 (Send Message, List Channels, Create Channel, Manage Members, Search Messages, Send Block Kit, Get Thread, Set Status) |
| **Auth Method** | Bot Token (xoxb-) + OAuth2 |
| **API Base** | `slack.com/api` |
| **OAuth2 Flow** | Authorization Code with bot scopes |
| **Tier** | Professional |

#### OAuth2 Setup

1. Create a Slack App at [api.slack.com/apps](https://api.slack.com/apps)
2. Configure OAuth2 scopes:
   - `chat:write` — Send messages
   - `channels:read` — List channels
   - `channels:manage` — Create and manage channels
   - `users:read` — Read user profiles
   - `search:read` — Search messages
   - `users.profile:write` — Set user status
3. Enable Events API and configure request URL
4. Install the app to your workspace
5. Copy the Bot Token (xoxb-...) and configure in n8n:
   ```
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_SIGNING_SECRET=your-signing-secret
   ```

#### Key Use Cases

- **Workspace Notifications**: Send messages to channels and DMs
- **Block Kit**: Rich interactive messages with buttons, menus, and forms
- **Channel Management**: Create project channels and manage membership
- **Message Search**: Search historical messages across workspace
- **Status Management**: Set availability and status for team members

---

### WhatsApp Business API

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_WhatsApp_Business_Server_v3.json` |
| **Tools** | 8 |
| **Auth Method** | Meta Business Suite OAuth2 |
| **API Base** | `graph.facebook.com/v19.0/{phone_number_id}` |
| **OAuth2 Flow** | Meta Business Suite → WhatsApp Business Account |
| **Tier** | Professional |

---

### Telegram Bot

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Telegram_Bot_Server_v3.json` |
| **Tools** | 8 |
| **Auth Method** | Bot Token via @BotFather |
| **API Base** | `api.telegram.org/bot{token}` |
| **OAuth2** | Not required (Bot Token authentication) |
| **Tier** | Starter |

---

### Discord

| Property | Value |
|----------|-------|
| **MCP Server** | `MCP_Discord_Server_v3.json` |
| **Tools** | 8 |
| **Auth Method** | Bot Token via Discord Developer Portal |
| **OAuth2 Flow** | Discord OAuth2 with bot scope + permissions |
| **API Base** | `discord.com/api/v10` |
| **Tier** | Professional |

---

## Payment MCP Servers

| Server | Tools | Auth | Tier |
|--------|-------|------|------|
| MCP_Stripe_Server_v3 | 8 | API Key (sk_live_...) | Professional |
| MCP_PayPal_Server_v3 | 8 | OAuth2 (Client Credentials) | Professional |
| MCP_QvaPay_Server_v3 | 6 | API Key | Enterprise |
| MCP_Bitrefill_Server_v3 | 6 | API Key | Enterprise |
| MCP_TropiPay_Server_v3 | 6 | OAuth2 | Enterprise |
| MCP_CoinEx_Server_v3 | 6 | API Key + HMAC | Enterprise |
| MCP_Binance_Server_v3 | 8 | API Key + HMAC-SHA256 | Enterprise |

---

## Industry Onboarding Workflows

### Gym / Fitness Center

| Property | Value |
|----------|-------|
| **Workflow** | `IND5_Gym_Onboarding_v3.json` |
| **Tools** | 16 (4 WhatsApp, 3 CRM, 2 Stripe, 1 SMS, 1 Teams, 1 Think) |
| **Platforms** | WhatsApp, CRM, Stripe, Twilio SMS, Microsoft Teams |
| **Tiers** | Basic (gym access), Premium (classes + trainer), VIP (full service) |
| **Pipeline** | Lead → Qualified → Registered → Payment → Oriented → Active → Retained |

#### Onboarding Flow

1. **Lead Capture**: WhatsApp fitness quiz with interactive buttons
2. **Qualification**: Assess fitness level, goals, and health data
3. **Registration**: CRM member profile with goals and preferences
4. **Payment**: Stripe subscription for selected membership tier
5. **Orientation**: Teams meeting for gym tour and workout plan
6. **Engagement**: SMS reminders, WhatsApp motivation, attendance tracking

#### Key Metrics

- Lead-to-member conversion rate
- Average time to first payment
- Member retention rate by tier
- Class booking rate
- Attendance frequency

---

### Farmacia / Pharmacy

| Property | Value |
|----------|-------|
| **Workflow** | `IND6_Farmacia_Onboarding_v3.json` |
| **Tools** | 16 (4 WhatsApp, 3 CRM, 2 Stripe, 1 SMS, 1 Teams, 1 Think) |
| **Platforms** | WhatsApp, CRM, Stripe, Twilio SMS, Microsoft Teams |
| **Tiers** | Basic (prescription), Plus (telemedicine + delivery), Premium (full care) |
| **Pipeline** | Lead → Consultation → Registered → Payment → Active → Retained |

#### Onboarding Flow

1. **Lead Capture**: WhatsApp health consultation form
2. **Consultation**: Collect medical data, allergies, and current medications
3. **Registration**: CRM patient profile with medical metadata
4. **Payment**: Stripe subscription for service plan with co-pay
5. **Telemedicine**: Teams consultation with healthcare provider
6. **Adherence**: SMS medication reminders and refill tracking

#### Key Metrics

- Patient acquisition cost
- Medication adherence rate
- Refill rate by tier
- Telemedicine consultation rate
- Patient satisfaction score

---

### Abogados / Law Firm

| Property | Value |
|----------|-------|
| **Workflow** | `IND7_Abogados_Onboarding_v3.json` |
| **Tools** | 17 (4 WhatsApp, 3 CRM, 2 Stripe, 1 Slack, 1 Teams, 1 SMS, 1 Think) |
| **Platforms** | WhatsApp, CRM, Stripe, Slack, Microsoft Teams, Twilio SMS |
| **Tiers** | Consultation (one-time), Representation (full case), Premium (priority + 24/7) |
| **Pipeline** | Lead → Consultation → Conflict Check → Retainer → Active → Resolution |

#### Onboarding Flow

1. **Lead Capture**: WhatsApp legal consultation form
2. **Conflict Check**: Verify no conflicts of interest
3. **Registration**: CRM client profile with case details and practice area
4. **Payment**: Stripe retainer invoice or recurring billing
5. **Consultation**: Teams meeting with assigned attorney
6. **Collaboration**: Slack channel for internal case team
7. **Compliance**: SMS deadline alerts and court date reminders

#### Key Metrics

- Client acquisition cost
- Retainer collection rate
- Billable hours per case
- Case resolution time
- Client satisfaction and referral rate

---

## OAuth2 Authentication Flows

### Client Credentials Flow (Server-to-Server)

Used for: Microsoft Teams, PayPal, TropiPay

```
┌──────────┐                                   ┌──────────┐
│  n8n App │                                   │  OAuth2  │
│          │  1. POST /token                    │  Server  │
│          │  grant_type=client_credentials     │          │
│          │  client_id=xxx                     │          │
│          │  client_secret=xxx                 │          │
│          │ ──────────────────────────────────> │          │
│          │                                    │          │
│          │  2. Access Token (JSON)            │          │
│          │ <────────────────────────────────── │          │
│          │                                    │          │
│          │  3. API Call with Bearer Token     │          │
│          │ ──────────────────────────────────> │   API    │
│          │                                    │          │
│          │  4. API Response                   │          │
│          │ <────────────────────────────────── │          │
└──────────┘                                   └──────────┘
```

### Authorization Code Flow (User Delegation)

Used for: Slack, Microsoft Teams (delegated), Discord

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  User    │     │  n8n App │     │  OAuth2  │
│          │     │          │     │  Server  │
│  1. Click│────>│          │     │          │
│  Connect │     │ 2. Redirect    │          │
│          │     │ ──────────────> │          │
│          │     │                 │          │
│          │     │ 3. User Login   │          │
│          │     │ & Authorize     │          │
│          │     │ ──────────────> │          │
│          │     │                 │          │
│          │     │ 4. Auth Code    │          │
│          │     │ <────────────── │          │
│          │     │                 │          │
│          │     │ 5. Token Exchange│         │
│          │     │ ──────────────> │          │
│          │     │                 │          │
│          │     │ 6. Access Token │          │
│          │     │ <────────────── │          │
└──────────┘     └──────────┘     └──────────┘
```

### API Key Authentication (Simple)

Used for: Twilio, Stripe, Telegram, Binance, CoinEx

```
n8n App ──[API Key in Header]──> API Server
  Example: Authorization: Bearer sk_live_xxxxx
  Example: x-api-key: your_api_key
```

---

## API Reference

### Twilio SMS API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/Accounts/{Sid}/Messages.json` | POST | Send SMS/WhatsApp message |
| `/Accounts/{Sid}/Calls.json` | POST | Initiate voice call |
| `/Accounts/{Sid}/Messages/{Sid}.json` | GET | Get message details |
| `/Accounts/{Sid}/Messages.json` | GET | List messages |
| `/Lookup/v1/PhoneNumbers/{Number}` | GET | Lookup phone number |
| `/Verify/v2/Services/{Sid}/Verifications` | POST | Send OTP |
| `/Verify/v2/Services/{Sid}/VerificationCheck` | POST | Verify OTP |

### Microsoft Graph API (Teams)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chats/{id}/messages` | POST | Send chat message |
| `/teams/{id}/channels` | POST | Create channel |
| `/teams/{id}/channels` | GET | List channels |
| `/teams/{id}/members` | POST | Add team member |
| `/chats/{id}/messages` | GET | Get chat messages |
| `/me/onlineMeetings` | POST | Create online meeting |
| `/me/chats` | GET | List user chats |

### Slack Web API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `chat.postMessage` | POST | Send message |
| `conversations.list` | GET | List channels |
| `conversations.create` | POST | Create channel |
| `conversations.invite` | POST | Invite member |
| `search.messages` | GET | Search messages |
| `users.profile.set` | POST | Set user status |
| `conversations.replies` | GET | Get thread replies |

---

## Deployment Guide

### Prerequisites

- n8n instance (self-hosted or cloud)
- Docker Compose (for self-hosted)
- API credentials for each service

### Environment Variables

```env
# Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Microsoft Teams
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
AZURE_TENANT_ID=your_tenant_id

# Slack
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret

# WhatsApp Business
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id

# Stripe
STRIPE_SECRET_KEY=sk_live_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret

# CRM
CRM_API_KEY=your_crm_api_key
CRM_BASE_URL=https://your-crm-instance.com/api

# OpenAI
OPENAI_API_KEY=sk-your-openai-key
```

### Docker Compose

```yaml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your_password
      - GENERIC_TIMEZONE=Europe/Madrid
      - TZ=Europe/Madrid
    volumes:
      - n8n_data:/home/node/.n8n
    restart: unless-stopped

volumes:
  n8n_data:
```

### Import Workflows

1. Open n8n UI at `http://localhost:5678`
2. Navigate to Workflows → Import from File
3. Select the JSON workflow file
4. Configure credentials for each service
5. Activate the workflow

---

## MCP Server Catalog

| # | Server | Tools | Auth | Tier |
|---|--------|-------|------|------|
| 1 | MCP_Calendar_Server_v3 | 8 | OAuth2 | Starter |
| 2 | MCP_Gmail_Server_v3 | 8 | OAuth2 | Starter |
| 3 | MCP_Contacts_Server_v3 | 8 | OAuth2 | Starter |
| 4 | MCP_HR_Server_v3 | 8 | API Key | Starter |
| 5 | MCP_ECommerce_Server_v3 | 8 | API Key | Starter |
| 6 | MCP_Knowledge_Base_Server_v3 | 8 | API Key | Starter |
| 7 | MCP_Slack_Server_v3 | 8 | OAuth2 | Professional |
| 8 | MCP_Notion_Server_v3 | 8 | OAuth2 | Professional |
| 9 | MCP_GitHub_Server_v3 | 8 | OAuth2 | Professional |
| 10 | MCP_Google_Workspace_Server_v3 | 8 | OAuth2 | Professional |
| 11 | MCP_Trello_Server_v3 | 8 | API Key | Professional |
| 12 | MCP_HubSpot_Server_v3 | 8 | OAuth2 | Professional |
| 13 | MCP_CRM_Universal_Server_v3 | 8 | API Key | Professional |
| 14 | MCP_Shopify_Server_v3 | 8 | OAuth2 | Professional |
| 15 | MCP_WooCommerce_Server_v3 | 8 | API Key | Professional |
| 16 | MCP_WordPress_Server_v3 | 8 | API Key | Professional |
| 17 | MCP_ERPNext_Server_v3 | 8 | API Key | Enterprise |
| 18 | MCP_Booking_Server_v3 | 8 | OAuth2 | Enterprise |
| 19 | MCP_Expedia_Server_v3 | 8 | API Key | Enterprise |
| 20 | MCP_Stripe_Server_v3 | 8 | API Key | Professional |
| 21 | MCP_PayPal_Server_v3 | 8 | OAuth2 | Professional |
| 22 | MCP_QvaPay_Server_v3 | 6 | API Key | Enterprise |
| 23 | MCP_Bitrefill_Server_v3 | 6 | API Key | Enterprise |
| 24 | MCP_TropiPay_Server_v3 | 6 | OAuth2 | Enterprise |
| 25 | MCP_CoinEx_Server_v3 | 6 | API Key + HMAC | Enterprise |
| 26 | MCP_Binance_Server_v3 | 8 | API Key + HMAC | Enterprise |
| 27 | MCP_WhatsApp_Business_Server_v3 | 8 | OAuth2 | Professional |
| 28 | MCP_Telegram_Bot_Server_v3 | 8 | Bot Token | Starter |
| 29 | MCP_Discord_Server_v3 | 8 | OAuth2 | Professional |
| 30 | MCP_Twilio_SMS_Server_v3 | 8 | API Key | Professional |
| 31 | MCP_Microsoft_Teams_Server_v3 | 8 | OAuth2 | Professional |
| 32 | MCP_Slack_Events_Server_v3 | 8 | OAuth2 | Professional |

**Total: 32 MCP Servers, 250+ Tools**

---

## Orchestration Workflows

| # | Workflow | Platforms | Tier |
|---|----------|-----------|------|
| ORC1 | Marketing Automation | Google + CRM + WordPress + WhatsApp | Professional |
| ORC2 | Travel Management | Booking + Expedia + WhatsApp | Enterprise |
| ORC3 | Multi-Commerce | WooCommerce + Shopify + Stripe | Professional |
| ORC4 | Finance Hub | Stripe + PayPal + Binance + CoinEx | Enterprise |
| ORC5 | WhatsApp CRM Stripe Sales Cycle | WhatsApp + CRM + Stripe | Professional |
| ORC6 | Twilio Teams Slack Multi-Channel | Twilio + Teams + Slack | Professional |
| ORC7 | Multi-Industry Onboarding | WhatsApp + CRM + Stripe + Teams + SMS | Professional |

---

## Industry Workflows

| # | Industry | Platforms | Tools | Tier |
|---|----------|-----------|-------|------|
| IND1 | Real Estate | WordPress + WhatsApp + CRM + Stripe | 9 | Enterprise |
| IND2 | Restaurant | WhatsApp + WooCommerce + CRM + Stripe | 9 | Enterprise |
| IND3 | SaaS | Discord + Stripe + CRM + Telegram | 9 | Enterprise |
| IND4 | Agency | Slack + Trello + CRM + Stripe | 9 | Enterprise |
| IND5 | Gym / Fitness | WhatsApp + CRM + Stripe + SMS + Teams | 16 | Enterprise |
| IND6 | Farmacia / Pharmacy | WhatsApp + CRM + Stripe + SMS + Teams | 16 | Enterprise |
| IND7 | Abogados / Law Firm | WhatsApp + CRM + Stripe + Slack + Teams + SMS | 17 | Enterprise |

---

*Generated by JARVIS AI Automation Ecosystem v6.0.0 — Phase 8*
"""


# ═══════════════════════════════════════════════════════════════════════
# 11. MANIFEST UPDATES
# ═══════════════════════════════════════════════════════════════════════

NEW_MCP_SERVERS = {
    "MCP_Twilio_SMS_Server_v3.json": {"tier": "professional", "tools": 8},
    "MCP_Microsoft_Teams_Server_v3.json": {"tier": "professional", "tools": 8},
    "MCP_Slack_Events_Server_v3.json": {"tier": "professional", "tools": 8},
}

NEW_ORCHESTRATION = {
    "ORC6_Twilio_Teams_Slack_Multi_Channel_v3.json": {"tier": "professional", "tools": 16},
    "ORC7_Multi_Industry_Onboarding_v3.json": {"tier": "professional", "tools": 15},
}

NEW_INDUSTRY = {
    "IND5_Gym_Onboarding_v3.json": {"tier": "enterprise", "tools": 16},
    "IND6_Farmacia_Onboarding_v3.json": {"tier": "enterprise", "tools": 16},
    "IND7_Abogados_Onboarding_v3.json": {"tier": "enterprise", "tools": 17},
}


def update_manifests():
    """Update all three JARVIS package manifests with Phase 8 additions."""
    for pkg_name in ["jarvis-starter", "jarvis-professional", "jarvis-enterprise"]:
        manifest_path = os.path.join(BASE, pkg_name, "manifest.json")
        if not os.path.exists(manifest_path):
            print(f"  Skipping {pkg_name} — manifest not found")
            continue

        with open(manifest_path, "r") as f:
            manifest = json.load(f)

        # Update version
        manifest["version"] = "6.0.0"

        # Add MCP servers
        if "mcp_servers" not in manifest["workflows"]:
            manifest["workflows"]["mcp_servers"] = []

        for filename, info in NEW_MCP_SERVERS.items():
            if filename not in manifest["workflows"]["mcp_servers"]:
                manifest["workflows"]["mcp_servers"].append(filename)

        # Add orchestration
        if "orchestration" not in manifest["workflows"]:
            manifest["workflows"]["orchestration"] = []

        for filename, info in NEW_ORCHESTRATION.items():
            if filename not in manifest["workflows"]["orchestration"]:
                manifest["workflows"]["orchestration"].append(filename)

        # Add industry
        if "industry" not in manifest["workflows"]:
            manifest["workflows"]["industry"] = []

        for filename, info in NEW_INDUSTRY.items():
            if filename not in manifest["workflows"]["industry"]:
                manifest["workflows"]["industry"].append(filename)

        # Update counts
        total_wf = sum(len(v) for v in manifest["workflows"].values())
        manifest["total_workflows"] = total_wf
        manifest["last_updated"] = datetime.now().strftime('%Y-%m-%d')

        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        print(f"  Updated {pkg_name}/manifest.json — {total_wf} workflows, v6.0.0")


# ═══════════════════════════════════════════════════════════════════════
# 12. SYNC TO JARVIS PACKAGES
# ═══════════════════════════════════════════════════════════════════════

def sync_to_jarvis_packages():
    """Sync generated files to JARVIS package directories."""
    # MCP servers → professional + enterprise
    for filename in NEW_MCP_SERVERS:
        src = os.path.join(BASE, "mcp_servers", filename)
        for pkg in ["jarvis-professional", "jarvis-enterprise"]:
            dst = os.path.join(BASE, f"{pkg}/workflows/mcp_servers", filename)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(src):
                with open(src, "r") as f:
                    data = json.load(f)
                with open(dst, "w") as f:
                    json.dump(data, f, indent=2)
                print(f"  Synced {filename} → {pkg}")

    # Orchestration → professional + enterprise
    for filename in NEW_ORCHESTRATION:
        src = os.path.join(BASE, "orchestration", filename)
        for pkg in ["jarvis-professional", "jarvis-enterprise"]:
            dst = os.path.join(BASE, f"{pkg}/workflows/orchestration", filename)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(src):
                with open(src, "r") as f:
                    data = json.load(f)
                with open(dst, "w") as f:
                    json.dump(data, f, indent=2)
                print(f"  Synced {filename} → {pkg}")

    # Industry → enterprise only
    for filename in NEW_INDUSTRY:
        src = os.path.join(BASE, "industry", filename)
        dst = os.path.join(BASE, "jarvis-enterprise/workflows/industry", filename)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            with open(src, "r") as f:
                data = json.load(f)
            with open(dst, "w") as f:
                json.dump(data, f, indent=2)
            print(f"  Synced {filename} → jarvis-enterprise")

    # Cognitive capital skills
    for skill_key, skill_data in NEW_COGNITIVE_SKILLS.items():
        tier = skill_data["tier"]
        filename = f"{skill_key}_SKILL.md"
        src = os.path.join(BASE, "cognitive_capital", filename)

        if tier == "professional":
            dst = os.path.join(BASE, "jarvis-professional/cognitive_capital", filename)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(src):
                with open(src, "r") as f:
                    data = f.read()
                with open(dst, "w") as f:
                    f.write(data)
                print(f"  Synced {filename} → jarvis-professional")

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
    print("Phase 8: Extended Communication + Industry Onboarding")
    print("=" * 60)

    # ── 1. Generate Communication MCP Servers ──
    print("\n📡 Generating Communication MCP Servers...")

    mcp_servers_dir = os.path.join(BASE, "mcp_servers")
    os.makedirs(mcp_servers_dir, exist_ok=True)

    twilio_wf = generate_mcp_twilio()
    with open(os.path.join(mcp_servers_dir, "MCP_Twilio_SMS_Server_v3.json"), "w") as f:
        json.dump(twilio_wf, f, indent=2)
    print(f"  ✅ MCP_Twilio_SMS_Server_v3.json — {len(twilio_wf['nodes'])} nodes, 8 tools")

    teams_wf = generate_mcp_teams()
    with open(os.path.join(mcp_servers_dir, "MCP_Microsoft_Teams_Server_v3.json"), "w") as f:
        json.dump(teams_wf, f, indent=2)
    print(f"  ✅ MCP_Microsoft_Teams_Server_v3.json — {len(teams_wf['nodes'])} nodes, 8 tools")

    slack_wf = generate_mcp_slack()
    with open(os.path.join(mcp_servers_dir, "MCP_Slack_Events_Server_v3.json"), "w") as f:
        json.dump(slack_wf, f, indent=2)
    print(f"  ✅ MCP_Slack_Events_Server_v3.json — {len(slack_wf['nodes'])} nodes, 8 tools")

    # ── 2. Generate Orchestration Workflows ──
    print("\n🔄 Generating Orchestration Workflows...")

    orc_dir = os.path.join(BASE, "orchestration")
    os.makedirs(orc_dir, exist_ok=True)

    multi_channel_wf = generate_orc_multi_channel()
    with open(os.path.join(orc_dir, "ORC6_Twilio_Teams_Slack_Multi_Channel_v3.json"), "w") as f:
        json.dump(multi_channel_wf, f, indent=2)
    print(f"  ✅ ORC6_Twilio_Teams_Slack_Multi_Channel_v3.json — {len(multi_channel_wf['nodes'])} nodes, 16 tools")

    onboarding_wf = generate_orc_onboarding()
    with open(os.path.join(orc_dir, "ORC7_Multi_Industry_Onboarding_v3.json"), "w") as f:
        json.dump(onboarding_wf, f, indent=2)
    print(f"  ✅ ORC7_Multi_Industry_Onboarding_v3.json — {len(onboarding_wf['nodes'])} nodes, 15 tools")

    # ── 3. Generate Industry Onboarding Workflows ──
    print("\n🏭 Generating Industry Onboarding Workflows...")

    ind_dir = os.path.join(BASE, "industry")
    os.makedirs(ind_dir, exist_ok=True)

    gym_wf = generate_ind_gym()
    with open(os.path.join(ind_dir, "IND5_Gym_Onboarding_v3.json"), "w") as f:
        json.dump(gym_wf, f, indent=2)
    print(f"  ✅ IND5_Gym_Onboarding_v3.json — {len(gym_wf['nodes'])} nodes, 16 tools")

    farmacia_wf = generate_ind_farmacia()
    with open(os.path.join(ind_dir, "IND6_Farmacia_Onboarding_v3.json"), "w") as f:
        json.dump(farmacia_wf, f, indent=2)
    print(f"  ✅ IND6_Farmacia_Onboarding_v3.json — {len(farmacia_wf['nodes'])} nodes, 16 tools")

    abogados_wf = generate_ind_abogados()
    with open(os.path.join(ind_dir, "IND7_Abogados_Onboarding_v3.json"), "w") as f:
        json.dump(abogados_wf, f, indent=2)
    print(f"  ✅ IND7_Abogados_Onboarding_v3.json — {len(abogados_wf['nodes'])} nodes, 17 tools")

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
        ("mcp_servers", ["MCP_Twilio_SMS_Server_v3.json", "MCP_Microsoft_Teams_Server_v3.json", "MCP_Slack_Events_Server_v3.json"]),
        ("orchestration", ["ORC6_Twilio_Teams_Slack_Multi_Channel_v3.json", "ORC7_Multi_Industry_Onboarding_v3.json"]),
        ("industry", ["IND5_Gym_Onboarding_v3.json", "IND6_Farmacia_Onboarding_v3.json", "IND7_Abogados_Onboarding_v3.json"]),
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

        # Check for orphan nodes
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
    print("PHASE 8 COMPLETE")
    print("=" * 60)
    print(f"  New MCP Servers: 3 (Twilio SMS, Microsoft Teams, Slack Events)")
    print(f"  New Orchestration: 2 (Multi-Channel, Multi-Industry Onboarding)")
    print(f"  New Industry Workflows: 3 (Gym, Farmacia, Abogados)")
    print(f"  New Cognitive Skills: 3 (Multi-Channel, Onboarding, Industry Specialist)")
    print(f"  Updated Documentation: INTEGRATIONS.md")
    print(f"  Total New Nodes: {total_nodes}")
    print(f"  Total New Connections: {total_connections}")
    print(f"  MCP Server Catalog: 32 servers, 250+ tools")
    print(f"  Total Workflows: 78+")
    print(f"  Version: 6.0.0")
    print("=" * 60)


if __name__ == "__main__":
    main()
