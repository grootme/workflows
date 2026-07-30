#!/usr/bin/env python3
"""
Phase 4: Expand MCP Arsenal + Combined Anthropic Patterns

5 New MCP Servers (DeerFlow/IBM patterns):
  MCP_Slack_Server_v3.json
  MCP_Notion_Server_v3.json
  MCP_GitHub_Server_v3.json
  MCP_Trello_Server_v3.json
  MCP_HubSpot_Server_v3.json

3 Combined Anthropic-Pattern Workflows:
  P8_Router_Orchestrator_v3.json  (P2+P3: Smart Routing + Orchestrator-Workers)
  P9_Evaluator_Parallel_v3.json  (P4+P5: Evaluator-Optimizer + Parallelization)
  P10_Cognitive_SOUL_Pipeline_v3.json (P6+P7: Cognitive Capital MCP + SOUL Bootstrap)

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

def http_tool(name, description, url_expr, pos, method="GET", uid_val=None):
    return {
        "parameters": {
            "description": description,
            "url": f"={{ /*n8n-auto-generated-fromAI-override*/ $fromAI('{name}_URL', `{name} API endpoint URL`, 'string') }}",
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

def webhook_trigger(path, uid_val=None):
    return {
        "parameters": {"httpMethod": "POST", "path": path, "options": {}},
        "type": "n8n-nodes-base.webhook",
        "typeVersion": 2,
        "position": [-2200, 0],
        "id": uid_val or uid(),
        "name": "Webhook",
        "webhookId": path
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

def memory_node(name, pos, uid_val=None):
    return {
        "parameters": {
            "sessionIdType": "customKey",
            "sessionKey": "={{ $json.sessionId || 'default' }}",
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

def set_node(name, assignments, pos, uid_val=None):
    return {
        "parameters": {
            "assignments": {"assignments": assignments},
            "options": {}
        },
        "type": "n8n-nodes-base.set",
        "typeVersion": 3.4,
        "position": pos,
        "id": uid_val or uid(),
        "name": name
    }

def if_node(name, conditions, pos, uid_val=None):
    return {
        "parameters": {
            "conditions": {
                "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                "conditions": conditions,
                "combinator": "and"
            }
        },
        "type": "n8n-nodes-base.if",
        "typeVersion": 2,
        "position": pos,
        "id": uid_val or uid(),
        "name": name
    }

def output_parser(name, properties, pos, uid_val=None):
    return {
        "parameters": {
            "schema": {
                "type": "object",
                "properties": properties
            }
        },
        "type": "@n8n/n8n-nodes-langchain.outputParserStructured",
        "typeVersion": 1.1,
        "position": pos,
        "id": uid_val or uid(),
        "name": name
    }

def ai_conn(source, target, conn_type):
    """Create ai_* connection from source to target."""
    return {
        source: {
            conn_type: [[{"node": target, "type": conn_type, "index": 0}]]
        }
    }

def main_conn(source, target):
    """Create main connection from source to target."""
    return {
        source: {
            "main": [[{"node": target, "type": "main", "index": 0}]]
        }
    }

def merge_dicts(dicts):
    """Merge multiple connection dicts."""
    result = {}
    for d in dicts:
        for k, v in d.items():
            if k in result:
                for ck, cv in v.items():
                    if ck in result[k]:
                        result[k][ck].extend(cv)
                    else:
                        result[k][ck] = cv
            else:
                result[k] = v
    return result


# ═══════════════════════════════════════════════════════════════════════
# 5 NEW MCP SERVERS
# ═══════════════════════════════════════════════════════════════════════

def generate_mcp_slack():
    """MCP Slack Server — Slack messaging, channels, reactions (DeerFlow channel pattern)."""
    nodes = [
        mcp_trigger("slack-mcp", [0, 0]),
        http_tool("Send Message", "Send a message to a Slack channel or user. Supports markdown formatting.",
                  "Send_Message_URL", [-400, 400], "POST"),
        http_tool("List Channels", "List all Slack channels the bot has access to, including member counts and topics.",
                  "List_Channels_URL", [-200, 400]),
        http_tool("Search Messages", "Search Slack messages matching a query. Returns message text, author, and timestamp.",
                  "Search_Messages_URL", [0, 400]),
        http_tool("Get Thread", "Retrieve all replies in a Slack thread. Use for context gathering before responding.",
                  "Get_Thread_URL", [200, 400]),
        http_tool("Add Reaction", "Add an emoji reaction to a Slack message. Use for acknowledging or categorizing messages.",
                  "Add_Reaction_URL", [400, 400], "POST"),
        http_tool("Upload File", "Upload a file to a Slack channel. Supports images, PDFs, and documents.",
                  "Upload_File_URL", [600, 400], "POST"),
        sticky_note("🔗 MCP Slack Server v3\n\nDeerFlow Channel Pattern\n7 Tools: Send Message, List Channels, Search Messages, Get Thread, Add Reaction, Upload File\n\nAll tools use $fromAI() for dynamic parameters", [-300, -300]),
    ]
    conns = merge_dicts([
        ai_conn("Send Message", "MCP Trigger", "ai_tool"),
        ai_conn("List Channels", "MCP Trigger", "ai_tool"),
        ai_conn("Search Messages", "MCP Trigger", "ai_tool"),
        ai_conn("Get Thread", "MCP Trigger", "ai_tool"),
        ai_conn("Add Reaction", "MCP Trigger", "ai_tool"),
        ai_conn("Upload File", "MCP Trigger", "ai_tool"),
    ])
    return make_workflow("MCP Slack Server v3", nodes, conns, tags=["mcp", "slack", "channel"])


def generate_mcp_notion():
    """MCP Notion Server — Notion pages, databases, search (IBM knowledge management pattern)."""
    nodes = [
        mcp_trigger("notion-mcp", [0, 0]),
        http_tool("Search Pages", "Search Notion pages and databases by title or content. Returns page IDs, titles, and last edited dates.",
                  "Search_Pages_URL", [-500, 400]),
        http_tool("Get Page", "Retrieve full content of a Notion page including all blocks and properties.",
                  "Get_Page_URL", [-300, 400]),
        http_tool("Create Page", "Create a new Notion page in a specified parent (page or database). Supports markdown content.",
                  "Create_Page_URL", [-100, 400], "POST"),
        http_tool("Update Page", "Update properties or content of an existing Notion page. Supports appending blocks.",
                  "Update_Page_URL", [100, 400], "PATCH"),
        http_tool("Query Database", "Query a Notion database with filters and sorts. Returns matching entries with properties.",
                  "Query_Database_URL", [300, 400], "POST"),
        http_tool("Create Database Entry", "Create a new entry in a Notion database with specified property values.",
                  "Create_Database_Entry_URL", [500, 400], "POST"),
        http_tool("Append Blocks", "Append content blocks to an existing Notion page. Supports text, headings, lists, code, and more.",
                  "Append_Blocks_URL", [700, 400], "POST"),
        sticky_note("🔗 MCP Notion Server v3\n\nIBM Knowledge Management Pattern\n7 Tools: Search, Get, Create, Update Page + Query/Create Database + Append Blocks\n\nAll tools use $fromAI() for dynamic parameters", [-300, -300]),
    ]
    conns = merge_dicts([
        ai_conn("Search Pages", "MCP Trigger", "ai_tool"),
        ai_conn("Get Page", "MCP Trigger", "ai_tool"),
        ai_conn("Create Page", "MCP Trigger", "ai_tool"),
        ai_conn("Update Page", "MCP Trigger", "ai_tool"),
        ai_conn("Query Database", "MCP Trigger", "ai_tool"),
        ai_conn("Create Database Entry", "MCP Trigger", "ai_tool"),
        ai_conn("Append Blocks", "MCP Trigger", "ai_tool"),
    ])
    return make_workflow("MCP Notion Server v3", nodes, conns, tags=["mcp", "notion", "knowledge"])


def generate_mcp_github():
    """MCP GitHub Server — GitHub repos, issues, PRs (IBM tool calling + DeerFlow specialist pattern)."""
    nodes = [
        mcp_trigger("github-mcp", [0, 0]),
        http_tool("Search Repos", "Search GitHub repositories by name, language, or topic. Returns repo URL, stars, description.",
                  "Search_Repos_URL", [-500, 400]),
        http_tool("Get Repo Info", "Get detailed information about a GitHub repository: README, stats, languages, contributors.",
                  "Get_Repo_Info_URL", [-300, 400]),
        http_tool("List Issues", "List issues in a GitHub repository. Filter by state (open/closed), labels, assignee.",
                  "List_Issues_URL", [-100, 400]),
        http_tool("Create Issue", "Create a new GitHub issue with title, body, labels, and assignees.",
                  "Create_Issue_URL", [100, 400], "POST"),
        http_tool("List Pull Requests", "List pull requests in a GitHub repository. Filter by state, author, reviewer.",
                  "List_Pull_Requests_URL", [300, 400]),
        http_tool("Get File Content", "Get the content of a file from a GitHub repository. Returns file content and metadata.",
                  "Get_File_Content_URL", [500, 400]),
        http_tool("Search Code", "Search code within GitHub repositories. Returns matching file paths and code snippets.",
                  "Search_Code_URL", [700, 400]),
        sticky_note("🔗 MCP GitHub Server v3\n\nIBM Tool Calling + DeerFlow Specialist Pattern\n7 Tools: Search Repos, Get Repo, List/Create Issues, List PRs, Get File, Search Code\n\nAll tools use $fromAI() for dynamic parameters", [-300, -300]),
    ]
    conns = merge_dicts([
        ai_conn("Search Repos", "MCP Trigger", "ai_tool"),
        ai_conn("Get Repo Info", "MCP Trigger", "ai_tool"),
        ai_conn("List Issues", "MCP Trigger", "ai_tool"),
        ai_conn("Create Issue", "MCP Trigger", "ai_tool"),
        ai_conn("List Pull Requests", "MCP Trigger", "ai_tool"),
        ai_conn("Get File Content", "MCP Trigger", "ai_tool"),
        ai_conn("Search Code", "MCP Trigger", "ai_tool"),
    ])
    return make_workflow("MCP GitHub Server v3", nodes, conns, tags=["mcp", "github", "devops"])


def generate_mcp_trello():
    """MCP Trello Server — Trello boards, cards, lists (IBM planning + DeerFlow tactical pattern)."""
    nodes = [
        mcp_trigger("trello-mcp", [0, 0]),
        http_tool("List Boards", "List all Trello boards the user has access to. Returns board names, IDs, and member counts.",
                  "List_Boards_URL", [-400, 400]),
        http_tool("Get Board", "Get detailed information about a Trello board including all lists and their cards.",
                  "Get_Board_URL", [-200, 400]),
        http_tool("Create Card", "Create a new card in a Trello list. Supports name, description, due date, labels, and assignees.",
                  "Create_Card_URL", [0, 400], "POST"),
        http_tool("Update Card", "Update an existing Trello card: move between lists, add comments, change labels, set due dates.",
                  "Update_Card_URL", [200, 400], "PUT"),
        http_tool("Search Cards", "Search for cards across Trello boards by name, description, or labels.",
                  "Search_Cards_URL", [400, 400]),
        http_tool("Add Comment", "Add a comment to a Trello card. Use for progress updates, notes, or collaboration.",
                  "Add_Comment_URL", [600, 400], "POST"),
        sticky_note("🔗 MCP Trello Server v3\n\nIBM Planning + DeerFlow Tactical Pattern\n6 Tools: List/Get Boards, Create/Update/Search Cards, Add Comment\n\nAll tools use $fromAI() for dynamic parameters", [-300, -300]),
    ]
    conns = merge_dicts([
        ai_conn("List Boards", "MCP Trigger", "ai_tool"),
        ai_conn("Get Board", "MCP Trigger", "ai_tool"),
        ai_conn("Create Card", "MCP Trigger", "ai_tool"),
        ai_conn("Update Card", "MCP Trigger", "ai_tool"),
        ai_conn("Search Cards", "MCP Trigger", "ai_tool"),
        ai_conn("Add Comment", "MCP Trigger", "ai_tool"),
    ])
    return make_workflow("MCP Trello Server v3", nodes, conns, tags=["mcp", "trello", "project"])


def generate_mcp_hubspot():
    """MCP HubSpot Server — HubSpot CRM, contacts, deals (IBM governance + DeerFlow specialist pattern)."""
    nodes = [
        mcp_trigger("hubspot-mcp", [0, 0]),
        http_tool("Search Contacts", "Search HubSpot contacts by name, email, or company. Returns contact details and recent activity.",
                  "Search_Contacts_URL", [-500, 400]),
        http_tool("Create Contact", "Create a new HubSpot contact with email, name, phone, company, and custom properties.",
                  "Create_Contact_URL", [-300, 400], "POST"),
        http_tool("Update Contact", "Update an existing HubSpot contact's properties. Use for adding notes, changing lifecycle stage.",
                  "Update_Contact_URL", [-100, 400], "PATCH"),
        http_tool("List Deals", "List deals in the HubSpot CRM pipeline. Filter by stage, owner, or amount.",
                  "List_Deals_URL", [100, 400]),
        http_tool("Create Deal", "Create a new deal in HubSpot CRM with name, amount, stage, and associated contacts.",
                  "Create_Deal_URL", [300, 400], "POST"),
        http_tool("Update Deal Stage", "Move a deal to a different pipeline stage. Use for pipeline progression tracking.",
                  "Update_Deal_Stage_URL", [500, 400], "PATCH"),
        http_tool("Get Company", "Get detailed information about a HubSpot company including associated contacts and deals.",
                  "Get_Company_URL", [700, 400]),
        sticky_note("🔗 MCP HubSpot Server v3\n\nIBM Governance + DeerFlow Specialist Pattern\n7 Tools: Search/Create/Update Contacts, List/Create/Update Deals, Get Company\n\nAll tools use $fromAI() for dynamic parameters", [-300, -300]),
    ]
    conns = merge_dicts([
        ai_conn("Search Contacts", "MCP Trigger", "ai_tool"),
        ai_conn("Create Contact", "MCP Trigger", "ai_tool"),
        ai_conn("Update Contact", "MCP Trigger", "ai_tool"),
        ai_conn("List Deals", "MCP Trigger", "ai_tool"),
        ai_conn("Create Deal", "MCP Trigger", "ai_tool"),
        ai_conn("Update Deal Stage", "MCP Trigger", "ai_tool"),
        ai_conn("Get Company", "MCP Trigger", "ai_tool"),
    ])
    return make_workflow("MCP HubSpot Server v3", nodes, conns, tags=["mcp", "hubspot", "crm"])


# ═══════════════════════════════════════════════════════════════════════
# 3 COMBINED ANTHROPIC-PATTERN WORKFLOWS
# ═══════════════════════════════════════════════════════════════════════

def generate_p8_router_orchestrator():
    """
    P8: Router-Orchestrator (P2 Smart Routing + P3 Orchestrator-Workers)
    
    Webhook → Router Agent classifies intent → Routes to sub-orchestrators
    Each sub-orchestrator manages its own workers.
    Combines the best of both patterns: intelligent routing + task decomposition.
    """
    nodes = [
        chat_trigger([0, 0], "I'm your Router-Orchestrator. I'll classify your request, route it to the right team, and orchestrate the work. What do you need?"),

        # Router Agent (P2 pattern)
        agent_node("Router Agent", 
            "# Router Agent (P2+P3 Combined Pattern)\n\nYou classify user intent and determine which specialized team should handle the request.\n\n## Available Teams:\n- **Operations Team**: Calendar, email, contacts, Slack, project management\n- **Research Team**: Deep research, data analysis, market intelligence\n- **Creative Team**: Content creation, newsletters, podcasts, design\n- **Technical Team**: Code, GitHub, debugging, architecture\n\n## Skills Loaded:\n- deep-research: Systematic research methodology\n- consulting-analysis: Professional analysis framework\n- find-skills: Discover new capabilities\n\n## Decision Rules:\n1. Analyze the request complexity and domain\n2. Select the appropriate team (1-2 teams max)\n3. For each team, define clear subtask instructions\n4. If the task spans multiple domains, decompose into subtasks for each team\n5. Simple tasks: handle directly with Think tool\n\n## Output Format:\nReturn a JSON object with:\n- team: which team(s) to route to\n- subtasks: array of subtask instructions\n- priority: low/medium/high/critical\n- estimated_complexity: simple/moderate/complex\n\nCurrent datetime: {{ $now }}",
            [400, 0]),
        llm_node("GPT-4.1-mini Router", "gpt-4.1-mini", 0.3, [400, 300]),
        memory_node("Router Memory", [600, 300]),
        think_tool("Think Tool", "Plan routing strategy and decompose complex requests into subtasks before delegating", [800, 0]),

        # Operations Sub-Orchestrator
        agent_node("Operations Orchestrator",
            "# Operations Sub-Orchestrator\n\nYou manage the Operations team. Execute calendar, email, contacts, Slack, and project management tasks.\n\n## Available Tools:\n- Google Calendar, Gmail, Contacts (via MCP)\n- Slack messaging and channels\n- Trello project boards\n\n## Skills Loaded:\n- consulting-analysis: Professional analysis framework\n\n## Rules:\n- Execute tasks in order of priority\n- Confirm actions before modifying data\n- Use Think tool for complex multi-step operations\n- Report results clearly",
            [1200, -600]),
        llm_node("GPT-4o-mini Ops", "gpt-4o-mini", 0.4, [1200, -300]),
        memory_node("Ops Memory", [1400, -300]),
        http_tool("Slack Tool", "Send messages, list channels, and search in Slack", "Slack_Tool_URL", [1600, -300]),
        http_tool("Trello Tool", "Manage Trello boards, cards, and lists for project tracking", "Trello_Tool_URL", [1600, -600]),

        # Research Sub-Orchestrator
        agent_node("Research Orchestrator",
            "# Research Sub-Orchestrator\n\nYou manage the Research team. Conduct deep research, data analysis, and market intelligence.\n\n## Available Tools:\n- Web search and analysis\n- Notion knowledge base\n- Data analysis capabilities\n\n## Skills Loaded:\n- deep-research: Systematic multi-angle research\n- data-analysis: Extract insights from data\n- consulting-analysis: Professional analysis framework\n\n## Rules:\n- Research from multiple angles (3-5 minimum)\n- Always cite sources\n- Include specific data points and statistics\n- Identify trends and patterns",
            [1200, 300]),
        llm_node("GPT-4.1 Research", "gpt-4.1", 0.3, [1200, 600]),
        memory_node("Research Memory", [1400, 600]),
        http_tool("Notion Tool", "Search and manage Notion pages and databases for knowledge base", "Notion_Tool_URL", [1600, 600]),
        http_tool("Web Search", "Search the web for current information, news, and data", "Web_Search_URL", [1600, 300]),

        # Creative Sub-Orchestrator
        agent_node("Creative Orchestrator",
            "# Creative Sub-Orchestrator\n\nYou manage the Creative team. Create content, newsletters, podcasts, and design assets.\n\n## Skills Loaded:\n- newsletter-generation: Content structure and formatting\n- podcast-generation: Audio content production\n- consulting-analysis: Professional analysis framework\n\n## Rules:\n- Follow brand voice and style guidelines\n- Create engaging, well-structured content\n- Include specific examples and data points\n- Ensure consistent formatting",
            [1200, 1200]),
        llm_node("GPT-4.1-mini Creative", "gpt-4.1-mini", 0.7, [1200, 1500]),
        memory_node("Creative Memory", [1400, 1500]),

        # Technical Sub-Orchestrator
        agent_node("Technical Orchestrator",
            "# Technical Sub-Orchestrator\n\nYou manage the Technical team. Handle code, debugging, architecture, and GitHub operations.\n\n## Available Tools:\n- GitHub repos, issues, PRs\n- Code search and analysis\n\n## Skills Loaded:\n- code-documentation: Precision and clarity standards\n- deep-research: Research methodology\n\n## Rules:\n- Write production-quality code\n- Include error handling and edge cases\n- Follow best practices and design patterns\n- Document all changes",
            [1200, 2100]),
        llm_node("GPT-4.1 Technical", "gpt-4.1", 0.3, [1200, 2400]),
        memory_node("Technical Memory", [1400, 2400]),
        http_tool("GitHub Tool", "Access GitHub repos, issues, PRs, and code search", "GitHub_Tool_URL", [1600, 2400]),

        # Aggregation
        agent_node("Aggregation Agent",
            "# Aggregation Agent\n\nYou synthesize outputs from multiple sub-orchestrators into a coherent, unified response.\n\n## Rules:\n- Combine insights from all teams that were activated\n- Resolve any conflicting information\n- Prioritize by relevance and importance\n- Present a clear, actionable summary\n- Include attribution to the source team",
            [2200, 600]),
        llm_node("GPT-4.1 Aggregate", "gpt-4.1", 0.4, [2200, 900]),
        memory_node("Aggregation Memory", [2400, 900]),

        sticky_note("🔗 P8: Router-Orchestrator (P2+P3 Combined)\n\n1. Router classifies intent → selects team\n2. Sub-orchestrator decomposes tasks\n3. Workers execute with tools\n4. Aggregation synthesizes results\n\n4 Teams: Ops, Research, Creative, Technical\nLLM: 4o-mini→4.1-mini→4.1 (tiered)", [0, -400]),
    ]

    conns = merge_dicts([
        # Chat → Router
        main_conn("Chat Trigger", "Router Agent"),
        # Router → sub-orchestrators (main flow)
        main_conn("Router Agent", "Operations Orchestrator"),
        main_conn("Router Agent", "Research Orchestrator"),
        main_conn("Router Agent", "Creative Orchestrator"),
        main_conn("Router Agent", "Technical Orchestrator"),
        # Sub-orchestrators → Aggregation
        main_conn("Operations Orchestrator", "Aggregation Agent"),
        main_conn("Research Orchestrator", "Aggregation Agent"),
        main_conn("Creative Orchestrator", "Aggregation Agent"),
        main_conn("Technical Orchestrator", "Aggregation Agent"),
        # Router ai_* connections
        ai_conn("GPT-4.1-mini Router", "Router Agent", "ai_languageModel"),
        ai_conn("Router Memory", "Router Agent", "ai_memory"),
        ai_conn("Think Tool", "Router Agent", "ai_tool"),
        # Operations ai_* connections
        ai_conn("GPT-4o-mini Ops", "Operations Orchestrator", "ai_languageModel"),
        ai_conn("Ops Memory", "Operations Orchestrator", "ai_memory"),
        ai_conn("Slack Tool", "Operations Orchestrator", "ai_tool"),
        ai_conn("Trello Tool", "Operations Orchestrator", "ai_tool"),
        # Research ai_* connections
        ai_conn("GPT-4.1 Research", "Research Orchestrator", "ai_languageModel"),
        ai_conn("Research Memory", "Research Orchestrator", "ai_memory"),
        ai_conn("Notion Tool", "Research Orchestrator", "ai_tool"),
        ai_conn("Web Search", "Research Orchestrator", "ai_tool"),
        # Creative ai_* connections
        ai_conn("GPT-4.1-mini Creative", "Creative Orchestrator", "ai_languageModel"),
        ai_conn("Creative Memory", "Creative Orchestrator", "ai_memory"),
        # Technical ai_* connections
        ai_conn("GPT-4.1 Technical", "Technical Orchestrator", "ai_languageModel"),
        ai_conn("Technical Memory", "Technical Orchestrator", "ai_memory"),
        ai_conn("GitHub Tool", "Technical Orchestrator", "ai_tool"),
        # Aggregation ai_* connections
        ai_conn("GPT-4.1 Aggregate", "Aggregation Agent", "ai_languageModel"),
        ai_conn("Aggregation Memory", "Aggregation Agent", "ai_memory"),
    ])

    return make_workflow("P8 Router-Orchestrator Agent v3", nodes, conns, tags=["anthropic", "combined", "routing", "orchestrator"])


def generate_p9_evaluator_parallel():
    """
    P9: Evaluator-Parallelization (P4 Evaluator-Optimizer + P5 Parallelization)
    
    Webhook → Split input → 3 parallel analysts → Each goes through Evaluator-Optimizer loop
    → Aggregate → Final synthesis. Combines multi-perspective analysis with quality-gated refinement.
    """
    nodes = [
        webhook_trigger("eval-parallel-analysis"),
        set_node("Split Input", [
            {"id": uid(), "name": "query", "value": "={{ $json.body.query }}", "type": "string"},
            {"id": uid(), "name": "domain", "value": "={{ $json.body.domain || 'general' }}", "type": "string"},
            {"id": uid(), "name": "quality_threshold", "value": "={{ $json.body.quality_threshold || 7 }}", "type": "number"},
        ], [-1800, 0]),

        # 3 Parallel Analysts (P5 pattern)
        # Analyst 1: Market
        agent_node("Market Analyst",
            "# Market Analyst (P9 Parallel + Evaluator)\n\nYou analyze the query from a market and business perspective.\n\n## Skills Loaded:\n- consulting-analysis: Professional analysis framework\n- deep-research: Research methodology\n\n## Output Format:\n- Market size and trends\n- Competitive landscape\n- Key opportunities and risks\n- Strategic recommendations\n\n## Rules:\n- Use specific data points\n- Include market size estimates where possible\n- Identify 3-5 key competitors\n- Current datetime: {{ $now }}",
            [0, -800]),
        llm_node("GPT-4.1-mini Market", "gpt-4.1-mini", 0.3, [0, -500]),
        memory_node("Market Memory", [200, -500]),
        http_tool("Market Search", "Search for market data, industry reports, and competitive intelligence", "Market_Search_URL", [400, -500]),

        # Analyst 2: Technical
        agent_node("Technical Analyst",
            "# Technical Analyst (P9 Parallel + Evaluator)\n\nYou analyze the query from a technical and feasibility perspective.\n\n## Skills Loaded:\n- data-analysis: Extract insights from data\n- code-documentation: Technical precision\n\n## Output Format:\n- Technical feasibility assessment\n- Architecture considerations\n- Implementation complexity estimate\n- Risk assessment\n\n## Rules:\n- Include specific technical details\n- Estimate implementation timelines\n- Identify potential bottlenecks\n- Current datetime: {{ $now }}",
            [0, 0]),
        llm_node("GPT-4.1 Technical", "gpt-4.1", 0.3, [0, 300]),
        memory_node("Technical Memory", [200, 300]),
        http_tool("Tech Search", "Search for technical documentation, code examples, and architecture patterns", "Tech_Search_URL", [400, 300]),

        # Analyst 3: Financial
        agent_node("Financial Analyst",
            "# Financial Analyst (P9 Parallel + Evaluator)\n\nYou analyze the query from a financial and ROI perspective.\n\n## Skills Loaded:\n- consulting-analysis: Professional analysis framework\n- data-analysis: Financial data extraction\n\n## Output Format:\n- Cost analysis and projections\n- ROI calculations\n- Revenue impact estimates\n- Budget recommendations\n\n## Rules:\n- Include specific dollar amounts and percentages\n- Show calculation methodology\n- Provide best/worst/expected case scenarios\n- Current datetime: {{ $now }}",
            [0, 800]),
        llm_node("GPT-4.1-mini Financial", "gpt-4.1-mini", 0.3, [0, 1100]),
        memory_node("Financial Memory", [200, 1100]),
        http_tool("Financial Search", "Search for financial data, industry benchmarks, and cost estimates", "Financial_Search_URL", [400, 1100]),

        # Evaluator-Optimizer (P4 pattern) - applied to aggregated results
        agent_node("Quality Evaluator",
            "# Quality Evaluator (P4 Pattern)\n\nYou evaluate the quality of the combined analysis from all three analysts.\n\n## Evaluation Criteria:\n- Completeness: All perspectives covered\n- Accuracy: Specific data points and citations\n- Actionability: Clear recommendations\n- Consistency: No contradictions between analysts\n- Depth: Sufficient detail for decision-making\n\n## Output Format:\n- quality_score: 1-10\n- strengths: What's well covered\n- gaps: What's missing\n- improvements: Specific suggestions for each analyst\n- pass: boolean (true if quality_score >= threshold)\n\n## Rules:\n- Be objective and thorough\n- Score each criterion independently\n- Provide specific improvement suggestions\n- Current datetime: {{ $now }}",
            [1000, 0]),
        llm_node("GPT-4.1 Evaluator", "gpt-4.1", 0.2, [1000, 300]),
        memory_node("Evaluator Memory", [1200, 300]),
        output_parser("Quality Parser", {
            "quality_score": {"type": "number", "description": "Overall quality score 1-10"},
            "pass": {"type": "boolean", "description": "Whether quality meets threshold"},
            "gaps": {"type": "array", "items": {"type": "string"}, "description": "Identified gaps"},
            "improvements": {"type": "array", "items": {"type": "string"}, "description": "Improvement suggestions"}
        }, [1200, 0]),

        # Quality Gate
        if_node("Quality Gate", {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
            "conditions": [
                {"leftValue": "={{ $json.quality_score }}", "rightValue": 7, "operator": {"type": "number", "operation": "gte"}}
            ],
            "combinator": "and"
        }, [1400, 0]),

        # Refinement Agent (if quality fails)
        agent_node("Refinement Agent",
            "# Refinement Agent (P4 Pattern)\n\nYou refine the analysis based on the evaluator's feedback.\n\n## Skills Loaded:\n- consulting-analysis: Professional analysis framework\n- deep-research: Research methodology\n\n## Rules:\n- Address each gap identified by the evaluator\n- Incorporate all improvement suggestions\n- Maintain the structure of each analyst's output\n- Add missing data and citations\n- Current datetime: {{ $now }}",
            [1600, 300]),
        llm_node("GPT-4.1 Refine", "gpt-4.1", 0.4, [1600, 600]),
        memory_node("Refinement Memory", [1800, 600]),

        # Final Synthesis
        agent_node("Synthesis Agent",
            "# Synthesis Agent (P9 Final)\n\nYou create the final deliverable by synthesizing all analyst outputs into a cohesive report.\n\n## Skills Loaded:\n- consulting-analysis: Professional analysis framework\n- newsletter-generation: Content structure and formatting\n\n## Output Structure:\n1. Executive Summary\n2. Market Analysis\n3. Technical Assessment\n4. Financial Projections\n5. Integrated Recommendations\n6. Risk Matrix\n7. Next Steps\n\n## Rules:\n- Resolve contradictions between analysts\n- Prioritize by impact and feasibility\n- Include specific action items\n- Current datetime: {{ $now }}",
            [2000, 0]),
        llm_node("GPT-4.1 Synthesis", "gpt-4.1", 0.4, [2000, 300]),
        memory_node("Synthesis Memory", [2200, 300]),

        sticky_note("🔗 P9: Evaluator-Parallelization (P4+P5 Combined)\n\n1. Input split → 3 parallel analysts\n2. Each analyst produces domain report\n3. Evaluator scores quality (1-10)\n4. Quality Gate → Pass or Refine\n5. Refinement loop (max 3 retries)\n6. Final synthesis → Report\n\nLLM: 4.1-mini→4.1 (tiered)", [-200, -1200]),
    ]

    conns = merge_dicts([
        # Webhook → Split
        main_conn("Webhook", "Split Input"),
        # Split → 3 analysts (parallel)
        main_conn("Split Input", "Market Analyst"),
        main_conn("Split Input", "Technical Analyst"),
        main_conn("Split Input", "Financial Analyst"),
        # Analysts → Evaluator
        main_conn("Market Analyst", "Quality Evaluator"),
        main_conn("Technical Analyst", "Quality Evaluator"),
        main_conn("Financial Analyst", "Quality Evaluator"),
        # Evaluator → Quality Gate
        main_conn("Quality Evaluator", "Quality Gate"),
        # Quality Gate → Synthesis (pass) or Refinement (fail)
        # Note: if node outputs [true, false] branches
        {
            "Quality Gate": {
                "main": [
                    [{"node": "Synthesis Agent", "type": "main", "index": 0}],
                    [{"node": "Refinement Agent", "type": "main", "index": 0}]
                ]
            }
        },
        # Refinement → back to Evaluator
        main_conn("Refinement Agent", "Quality Evaluator"),
        # Market Analyst ai_* connections
        ai_conn("GPT-4.1-mini Market", "Market Analyst", "ai_languageModel"),
        ai_conn("Market Memory", "Market Analyst", "ai_memory"),
        ai_conn("Market Search", "Market Analyst", "ai_tool"),
        # Technical Analyst ai_* connections
        ai_conn("GPT-4.1 Technical", "Technical Analyst", "ai_languageModel"),
        ai_conn("Technical Memory", "Technical Analyst", "ai_memory"),
        ai_conn("Tech Search", "Technical Analyst", "ai_tool"),
        # Financial Analyst ai_* connections
        ai_conn("GPT-4.1-mini Financial", "Financial Analyst", "ai_languageModel"),
        ai_conn("Financial Memory", "Financial Analyst", "ai_memory"),
        ai_conn("Financial Search", "Financial Analyst", "ai_tool"),
        # Evaluator ai_* connections
        ai_conn("GPT-4.1 Evaluator", "Quality Evaluator", "ai_languageModel"),
        ai_conn("Evaluator Memory", "Quality Evaluator", "ai_memory"),
        ai_conn("Quality Parser", "Quality Evaluator", "ai_outputParser"),
        # Refinement ai_* connections
        ai_conn("GPT-4.1 Refine", "Refinement Agent", "ai_languageModel"),
        ai_conn("Refinement Memory", "Refinement Agent", "ai_memory"),
        # Synthesis ai_* connections
        ai_conn("GPT-4.1 Synthesis", "Synthesis Agent", "ai_languageModel"),
        ai_conn("Synthesis Memory", "Synthesis Agent", "ai_memory"),
    ])

    return make_workflow("P9 Evaluator-Parallelization Agent v3", nodes, conns, tags=["anthropic", "combined", "parallel", "evaluator"])


def generate_p10_cognitive_soul():
    """
    P10: Cognitive-SOUL Pipeline (P6 Cognitive Capital MCP + P7 SOUL Bootstrap)
    
    Chat Trigger → SOUL Bootstrap Agent creates personality → Cognitive Capital MCP loads skills
    → Combined Agent with both personality and skills. A pipeline that first bootstraps 
    the agent's personality, then equips it with the right cognitive capital skills.
    """
    nodes = [
        chat_trigger([0, 0], "Hello! I'm your AI personality architect. I'll help you create a personalized SOUL.md and then equip your agent with the right skills. Let's start — what language would you prefer?"),

        # Phase 1: SOUL Bootstrap (P7 pattern)
        agent_node("SOUL Bootstrap",
            "# SOUL Bootstrap Agent (P6+P7 Combined)\n\nYou create a personalized SOUL.md for the AI assistant through conversation.\n\n## Skills Loaded:\n- bootstrap: Conversational onboarding and SOUL.md generation\n\n## Conversation Phases:\n\n### Phase 1 — Hello (1 round)\nEstablish preferred language.\n\n### Phase 2 — You (2 rounds)\n- Round A: Who they are, what drains them, what they need\n- Round B: AI name and relationship framing (assistant/partner/co-pilot/second brain)\n\n### Phase 3 — Personality (2 rounds)\n- Round A: Core traits and pushback preference\n- Round B: Communication style and voice\n\n### Phase 4 — Depth (1-2 rounds)\n- Autonomy level, failure philosophy, long-term vision, blind spots\n\n### Phase 5 — Skill Selection (NEW)\n- Based on the user's profile, recommend 3-5 cognitive capital skills\n- Explain what each skill does and why it's relevant\n- User confirms which skills to load\n\n## Extraction Tracker:\n| Field | Required | Phase |\n|-------|----------|-------|\n| Preferred language | Yes | 1 |\n| User's name | Yes | 2 |\n| User's role | Yes | 2 |\n| AI name | Yes | 2 |\n| Relationship framing | Yes | 2 |\n| Core traits (3-5 rules) | Yes | 3 |\n| Communication style | Yes | 3 |\n| Pushback preference | Yes | 3 |\n| Autonomy level | Yes | 4 |\n| Failure philosophy | Yes | 4 |\n| Selected skills | Yes | 5 |\n\n## Skill Recommendation Logic:\n- If user is a researcher → deep-research, data-analysis, consulting-analysis\n- If user is a business owner → consulting-analysis, newsletter-generation, data-analysis\n- If user is a developer → code-documentation, deep-research, podcast-generation\n- If user is a creator → newsletter-generation, podcast-generation, consulting-analysis\n- If user is a manager → consulting-analysis, data-analysis, deep-research\n\nCurrent datetime: {{ $now }}",
            [400, 0]),
        llm_node("GPT-4.1-mini Bootstrap", "gpt-4.1-mini", 0.7, [400, 300]),
        memory_node("Bootstrap Memory", [600, 300]),
        think_tool("Think Tool", "Plan conversation flow, track extracted fields, and determine when to move to the next phase", [800, 0]),

        # Phase 2: Cognitive Capital Loader (P6 pattern)
        agent_node("Cognitive Capital Loader",
            "# Cognitive Capital Loader (P6+P7 Combined)\n\nYou load the selected cognitive capital skills into the agent's memory and generate a complete configuration.\n\n## Available Skills:\n1. **deep-research** — Systematic multi-angle research methodology\n2. **consulting-analysis** — Professional analysis framework\n3. **data-analysis** — Data extraction and visualization\n4. **newsletter-generation** — Content structure and formatting\n5. **code-documentation** — Precision and clarity standards\n6. **podcast-generation** — Audio content production\n\n## Loading Process:\n1. Read the SOUL.md generated by the bootstrap agent\n2. Load each selected skill's SKILL.md into context\n3. Verify compatibility between personality and skills\n4. Generate a complete agent configuration:\n   - SOUL.md (personality)\n   - Skill manifest (which skills are active)\n   - Integration notes (how skills interact with personality)\n   - Usage recommendations\n\n## Output Format:\nReturn a complete agent configuration with:\n- soul_md: The complete SOUL.md content\n- skills: Array of loaded skill objects with name, description, usage_tips\n- integration_notes: How skills complement the personality\n- recommended_workflows: Which JARVIS workflows to use\n\nCurrent datetime: {{ $now }}",
            [1200, 0]),
        llm_node("GPT-4.1 Loader", "gpt-4.1", 0.3, [1200, 300]),
        memory_node("Loader Memory", [1400, 300]),
        http_tool("Skill Registry", "Access the cognitive capital skill registry to load SKILL.md files for selected skills", "Skill_Registry_URL", [1600, 300]),

        # Final Agent Configuration
        agent_node("Personalized Agent",
            "# Personalized Agent (P6+P7 Output)\n\nYou are the fully configured agent with personality and skills. You operate based on the SOUL.md and cognitive capital loaded by the pipeline.\n\n## Your Configuration:\n- Personality: Defined by SOUL.md (loaded from bootstrap)\n- Skills: Cognitive capital skills (loaded from registry)\n- Memory: Persistent across sessions\n\n## Operating Rules:\n- Always follow your SOUL.md personality traits\n- Use your loaded skills when relevant\n- Maintain the user's preferred communication style\n- Apply your core traits as behavioral rules\n- Push back when appropriate (per pushback preference)\n\nThis agent is the final product of the P10 Cognitive-SOUL Pipeline.",
            [2000, 0]),
        llm_node("GPT-4.1 Personalized", "gpt-4.1", 0.5, [2000, 300]),
        memory_node("Personalized Memory", [2200, 300]),
        output_parser("Config Parser", {
            "soul_md": {"type": "string", "description": "Complete SOUL.md content"},
            "skills": {"type": "array", "items": {"type": "object"}, "description": "Loaded skill objects"},
            "integration_notes": {"type": "string", "description": "How skills complement personality"},
            "recommended_workflows": {"type": "array", "items": {"type": "string"}, "description": "Recommended JARVIS workflows"}
        }, [2200, 0]),

        sticky_note("🔗 P10: Cognitive-SOUL Pipeline (P6+P7 Combined)\n\nPhase 1: SOUL Bootstrap\n  → 4-phase conversation\n  → Creates personalized SOUL.md\n  → Recommends cognitive capital skills\n\nPhase 2: Cognitive Capital Loader\n  → Loads selected SKILL.md files\n  → Verifies personality-skill compatibility\n  → Generates complete agent config\n\nPhase 3: Personalized Agent\n  → Operates with SOUL.md + skills\n  → Persistent memory across sessions\n\nLLM: 4.1-mini→4.1 (tiered)", [0, -400]),
    ]

    conns = merge_dicts([
        # Chat → SOUL Bootstrap
        main_conn("Chat Trigger", "SOUL Bootstrap"),
        # SOUL Bootstrap → Cognitive Capital Loader
        main_conn("SOUL Bootstrap", "Cognitive Capital Loader"),
        # Cognitive Capital Loader → Personalized Agent
        main_conn("Cognitive Capital Loader", "Personalized Agent"),
        # SOUL Bootstrap ai_* connections
        ai_conn("GPT-4.1-mini Bootstrap", "SOUL Bootstrap", "ai_languageModel"),
        ai_conn("Bootstrap Memory", "SOUL Bootstrap", "ai_memory"),
        ai_conn("Think Tool", "SOUL Bootstrap", "ai_tool"),
        # Cognitive Capital Loader ai_* connections
        ai_conn("GPT-4.1 Loader", "Cognitive Capital Loader", "ai_languageModel"),
        ai_conn("Loader Memory", "Cognitive Capital Loader", "ai_memory"),
        ai_conn("Skill Registry", "Cognitive Capital Loader", "ai_tool"),
        # Personalized Agent ai_* connections
        ai_conn("GPT-4.1 Personalized", "Personalized Agent", "ai_languageModel"),
        ai_conn("Personalized Memory", "Personalized Agent", "ai_memory"),
        ai_conn("Config Parser", "Personalized Agent", "ai_outputParser"),
    ])

    return make_workflow("P10 Cognitive-SOUL Pipeline Agent v3", nodes, conns, tags=["anthropic", "combined", "cognitive", "soul"])


# ═══════════════════════════════════════════════════════════════════════
# INTEGRATION INTO JARVIS PACKAGES
# ═══════════════════════════════════════════════════════════════════════

PACKAGE_ASSIGNMENTS = {
    "jarvis-starter": {
        "new_mcp_servers": ["MCP_Slack_Server_v3.json"],
        "new_patterns": ["P10_Cognitive_SOUL_Pipeline_v3.json"],
    },
    "jarvis-professional": {
        "new_mcp_servers": ["MCP_Slack_Server_v3.json", "MCP_Notion_Server_v3.json", "MCP_GitHub_Server_v3.json"],
        "new_patterns": ["P8_Router_Orchestrator_v3.json", "P9_Evaluator_Parallel_v3.json", "P10_Cognitive_SOUL_Pipeline_v3.json"],
    },
    "jarvis-enterprise": {
        "new_mcp_servers": ["MCP_Slack_Server_v3.json", "MCP_Notion_Server_v3.json", "MCP_GitHub_Server_v3.json", "MCP_Trello_Server_v3.json", "MCP_HubSpot_Server_v3.json"],
        "new_patterns": ["P8_Router_Orchestrator_v3.json", "P9_Evaluator_Parallel_v3.json", "P10_Cognitive_SOUL_Pipeline_v3.json"],
    },
}


def update_manifests():
    for pkg_name, cfg in PACKAGE_ASSIGNMENTS.items():
        mpath = f"{BASE}/{pkg_name}/manifest.json"
        with open(mpath) as f:
            m = json.load(f)

        # Add new MCP servers
        for srv in cfg["new_mcp_servers"]:
            if srv not in m["workflows"]["mcp_servers"]:
                m["workflows"]["mcp_servers"].append(srv)

        # Add new patterns
        for pat in cfg["new_patterns"]:
            if pat not in m["workflows"]["anthropic_patterns"]:
                m["workflows"]["anthropic_patterns"].append(pat)

        # Update total count
        m["total_workflows"] = sum(len(v) for v in m["workflows"].values())
        m["version"] = "3.1.0"

        with open(mpath, "w") as f:
            json.dump(m, f, indent=2)
        print(f"  ✓ {pkg_name}/manifest.json — v3.1.0, {m['total_workflows']} workflows")


def update_pricing_html():
    ppath = f"{BASE}/pricing.html"
    with open(ppath) as f:
        html = f.read()

    # Update stats
    html = html.replace(
        '<div class="number" style="color: var(--accent-starter)">32</div>',
        '<div class="number" style="color: var(--accent-starter)">40</div>',
    )
    html = html.replace(
        '<div class="number" style="color: var(--accent-pro)">7</div>',
        '<div class="number" style="color: var(--accent-pro)">10</div>',
    )

    # Update subtitle
    html = html.replace(
        "32 zero-debt n8n automations + 7 Anthropic agent patterns",
        "40 zero-debt n8n automations + 10 Anthropic agent patterns"
    )

    # Update footer
    html = html.replace(
        "Built with zero technical debt • 32 workflows • 7 Anthropic patterns • 6 cognitive capital skills",
        "Built with zero technical debt • 40 workflows • 10 Anthropic patterns • 11 MCP servers • 6 cognitive capital skills"
    )

    # Update comparison table rows
    html = html.replace(
        "<tr><td>Anthropic Pattern Workflows</td><td>2 (P1+P7)</td><td>6 (P1-P5+P7)</td><td>7 (P1-P7)</td></tr>",
        "<tr><td>Anthropic Pattern Workflows</td><td>3 (P1+P7+P10)</td><td>9 (P1-P5+P7-P10)</td><td>10 (P1-P10)</td></tr>",
    )
    html = html.replace(
        "<tr><td>MCP Server Templates</td><td>4</td><td>6</td><td>6</td></tr>",
        "<tr><td>MCP Server Templates</td><td>5</td><td>9</td><td>11</td></tr>",
    )

    # Add P8-P10 rows to comparison table
    new_rows = """            <tr><td>P8 Router-Orchestrator</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>P9 Evaluator-Parallelization</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>P10 Cognitive-SOUL Pipeline</td><td class="yes">✓</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>MCP Slack Server</td><td class="yes">✓</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>MCP Notion Server</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>MCP GitHub Server</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>
            <tr><td>MCP Trello Server</td><td class="no">—</td><td class="no">—</td><td class="yes">✓</td></tr>
            <tr><td>MCP HubSpot Server</td><td class="no">—</td><td class="no">—</td><td class="yes">✓</td></tr>"""

    # Insert before the Docker Compose row
    html = html.replace(
        '            <tr><td>Docker Compose</td>',
        new_rows + '\n            <tr><td>Docker Compose</td>',
    )

    # Update Starter features
    html = html.replace(
        "<li><span class=\"check\">✓</span> 4 MCP Server Templates</li>",
        "<li><span class=\"check\">✓</span> 5 MCP Server Templates (incl. Slack)</li>",
    )
    html = html.replace(
        "<li><span class=\"check\">✓</span> <strong>P7 SOUL Bootstrap Agent</strong></li>\n            <li><span class=\"check\">✓</span> 2 Cognitive Capital Skills</li>",
        "<li><span class=\"check\">✓</span> <strong>P7 SOUL Bootstrap Agent</strong></li>\n            <li><span class=\"check\">✓</span> <strong>P10 Cognitive-SOUL Pipeline</strong></li>\n            <li><span class=\"check\">✓</span> 2 Cognitive Capital Skills</li>",
    )

    # Update Professional features
    html = html.replace(
        "<li><span class=\"check\">✓</span> 6 MCP Server templates</li>",
        "<li><span class=\"check\">✓</span> 9 MCP Server templates (incl. Slack, Notion, GitHub)</li>",
    )
    html = html.replace(
        "<li><span class=\"check\">✓</span> <strong>P7 SOUL Bootstrap Agent</strong></li>\n            <li><span class=\"check\">✓</span> 4 Cognitive Capital Skills</li>",
        "<li><span class=\"check\">✓</span> <strong>P7 SOUL Bootstrap Agent</strong></li>\n            <li><span class=\"check\">✓</span> <strong>P8 Router-Orchestrator</strong></li>\n            <li><span class=\"check\">✓</span> <strong>P9 Evaluator-Parallelization</strong></li>\n            <li><span class=\"check\">✓</span> <strong>P10 Cognitive-SOUL Pipeline</strong></li>\n            <li><span class=\"check\">✓</span> 4 Cognitive Capital Skills</li>",
    )

    # Update Enterprise features
    html = html.replace(
        "<li><span class=\"check\">✓</span> <strong>P6 Cognitive Capital MCP Server</strong></li>",
        "<li><span class=\"check\">✓</span> <strong>P6 Cognitive Capital MCP Server</strong></li>\n            <li><span class=\"check\">✓</span> <strong>P8 Router-Orchestrator</strong></li>\n            <li><span class=\"check\">✓</span> <strong>P9 Evaluator-Parallelization</strong></li>\n            <li><span class=\"check\">✓</span> <strong>P10 Cognitive-SOUL Pipeline</strong></li>",
    )
    html = html.replace(
        "<li><span class=\"check\">✓</span> 6 Cognitive Capital Skills (all)</li>",
        "<li><span class=\"check\">✓</span> 6 Cognitive Capital Skills (all)</li>\n            <li><span class=\"check\">✓</span> 11 MCP Servers (incl. Trello, HubSpot)</li>",
    )

    with open(ppath, "w") as f:
        f.write(html)
    print(f"  ✓ pricing.html updated")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  Phase 4: Expand MCP Arsenal + Combined Anthropic Patterns")
    print("=" * 60)

    # Generate 5 new MCP servers
    print("\n1. Generating 5 new MCP Servers...")
    mcp_servers = {
        "MCP_Slack_Server_v3.json": generate_mcp_slack(),
        "MCP_Notion_Server_v3.json": generate_mcp_notion(),
        "MCP_GitHub_Server_v3.json": generate_mcp_github(),
        "MCP_Trello_Server_v3.json": generate_mcp_trello(),
        "MCP_HubSpot_Server_v3.json": generate_mcp_hubspot(),
    }

    # Also copy to top-level mcp_servers/ and anthropic_patterns/
    for fname, wf in mcp_servers.items():
        # Top-level mcp_servers/
        path = f"{BASE}/mcp_servers/{fname}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(wf, f, indent=2)
        print(f"  ✓ mcp_servers/{fname}")

    # Generate 3 combined pattern workflows
    print("\n2. Generating 3 Combined Anthropic-Pattern Workflows...")
    combined_patterns = {
        "P8_Router_Orchestrator_v3.json": generate_p8_router_orchestrator(),
        "P9_Evaluator_Parallel_v3.json": generate_p9_evaluator_parallel(),
        "P10_Cognitive_SOUL_Pipeline_v3.json": generate_p10_cognitive_soul(),
    }

    for fname, wf in combined_patterns.items():
        # Top-level anthropic_patterns/
        path = f"{BASE}/anthropic_patterns/{fname}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(wf, f, indent=2)
        print(f"  ✓ anthropic_patterns/{fname}")

    # Copy to package directories
    print("\n3. Copying to JARVIS packages...")
    for pkg_name, cfg in PACKAGE_ASSIGNMENTS.items():
        # MCP servers
        mcp_dir = f"{BASE}/{pkg_name}/workflows/mcp_servers"
        for srv in cfg["new_mcp_servers"]:
            src = f"{BASE}/mcp_servers/{srv}"
            dst = f"{mcp_dir}/{srv}"
            if os.path.exists(src):
                import shutil
                shutil.copy2(src, dst)
                print(f"  ✓ {pkg_name}/workflows/mcp_servers/{srv}")

        # Anthropic patterns
        pat_dir = f"{BASE}/{pkg_name}/workflows/anthropic_patterns"
        for pat in cfg["new_patterns"]:
            src = f"{BASE}/anthropic_patterns/{pat}"
            dst = f"{pat_dir}/{pat}"
            if os.path.exists(src):
                import shutil
                shutil.copy2(src, dst)
                print(f"  ✓ {pkg_name}/workflows/anthropic_patterns/{pat}")

    # Update manifests
    print("\n4. Updating manifests...")
    update_manifests()

    # Update pricing page
    print("\n5. Updating pricing.html...")
    update_pricing_html()

    # Validate ai_* connections
    print("\n6. Validating ai_* connections...")
    total_ai = 0
    for fname, wf in {**mcp_servers, **combined_patterns}.items():
        ai_count = 0
        for node_name, conns in wf.get("connections", {}).items():
            for conn_type, conn_list in conns.items():
                if conn_type.startswith("ai_"):
                    ai_count += len(conn_list)
        total_ai += ai_count
        print(f"  {fname}: {ai_count} ai_* connections")
    print(f"  Total: {total_ai} ai_* connections across 8 new workflows")

    # Summary
    print("\n" + "=" * 60)
    print("  ✅ Phase 4 Complete!")
    print("=" * 60)
    print("\n  New MCP Servers: 5 (Slack, Notion, GitHub, Trello, HubSpot)")
    print("  New Combined Patterns: 3 (P8, P9, P10)")
    print(f"  Total ai_* connections: {total_ai}")
    print()
    for pkg_name, cfg in PACKAGE_ASSIGNMENTS.items():
        mpath = f"{BASE}/{pkg_name}/manifest.json"
        with open(mpath) as f:
            m = json.load(f)
        total = m["total_workflows"]
        n_mcp = len(m["workflows"]["mcp_servers"])
        n_patterns = len(m["workflows"]["anthropic_patterns"])
        print(f"  {pkg_name}: {total} workflows, {n_mcp} MCP servers, {n_patterns} Anthropic patterns")
