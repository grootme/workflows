#!/usr/bin/env python3
"""
Phase 5: Zeus Meta-Orchestrator — DeerFlow-style top-level orchestrator

A single workflow that dynamically selects and executes the correct Anthropic
pattern (P1-P10) based on the user's request. This is the "Zeus" of the system.

Architecture:
  Chat Trigger → Zeus Agent (classifies intent + selects pattern)
  → Switch node (10 branches, one per pattern)
  → 10 Pattern Executor Agents (each with correct LLM, memory, tools, skills)
  → Synthesis Agent (combines results)
  → Output Parser (structured response)

DeerFlow Zeus pattern: Top-level orchestrator that delegates to specialized
sub-orchestrators based on domain analysis and task complexity.

Package assignment:
  - Professional: Zeus (P1-P5 + P7-P10, no P6)
  - Enterprise: Zeus (P1-P10, full)
"""

import json
import os
import uuid
import shutil

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

def ai_conn(source, target, conn_type):
    return {source: {conn_type: [[{"node": target, "type": conn_type, "index": 0}]]}}

def main_conn(source, target):
    return {source: {"main": [[{"node": target, "type": "main", "index": 0}]]}}

def merge_dicts(dicts):
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


# ── Pattern Definitions ────────────────────────────────────────────────
PATTERNS = {
    "P1": {
        "name": "Prompt Chaining Executor",
        "llm": "gpt-4.1-mini",
        "temp": 0.5,
        "system_msg": """# P1: Prompt Chaining Executor

You execute the Prompt Chaining pattern: Research → Gate → Draft → Gate → Polish.

## Process:
1. **Research Phase**: Gather comprehensive information about the topic
2. **Quality Gate**: Verify research is sufficient (minimum 200 chars of substance)
3. **Draft Phase**: Create a well-structured draft using the research
4. **Quality Gate**: Verify draft meets quality standards
5. **Polish Phase**: Refine for clarity, accuracy, and impact

## Skills Loaded:
- deep-research: Systematic multi-angle research methodology
- consulting-analysis: Professional analysis framework
- newsletter-generation: Content structure and formatting

## Output Format:
- headline: The main headline
- content: The polished content in markdown
- sources: Source URLs referenced
- quality_score: Self-assessed quality score 1-10

Current datetime: {{ $now }}""",
        "tools": ["Web Search", "Think Tool"],
        "pos": [0, -2700],
        "llm_pos": [0, -2400],
        "mem_pos": [200, -2400],
    },
    "P2": {
        "name": "Smart Routing Executor",
        "llm": "gpt-4.1-mini",
        "temp": 0.3,
        "system_msg": """# P2: Smart Routing Executor

You execute the Smart Routing pattern: Classify intent → Route to specialist.

## Available Routes:
- calendar: Schedule, events, time management
- email: Send, read, search emails
- research: Deep research, data gathering
- ecommerce: Product management, orders, inventory
- creative: Content creation, writing, design
- technical: Code, debugging, architecture
- hr: Employee management, recruitment, onboarding

## Skills Loaded:
- deep-research: Research methodology
- find-skills: Discover new capabilities

## Rules:
1. Classify the user's intent accurately
2. Select the most appropriate specialist route
3. Execute the task within that domain
4. If the task spans multiple domains, handle the primary one

Current datetime: {{ $now }}""",
        "tools": ["Web Search", "Think Tool"],
        "pos": [0, -2100],
        "llm_pos": [0, -1800],
        "mem_pos": [200, -1800],
    },
    "P3": {
        "name": "Orchestrator-Workers Executor",
        "llm": "gpt-4.1",
        "temp": 0.5,
        "system_msg": """# P3: Orchestrator-Workers Executor

You execute the Orchestrator-Workers pattern: Break down complex tasks → Delegate to workers.

## Available Workers:
- Research Worker: Deep research, data gathering, analysis
- Creative Worker: Content creation, writing, design
- Technical Worker: Code, debugging, technical tasks
- Data Worker: Data analysis, visualization, reports

## Skills Loaded:
- deep-research: Systematic multi-angle research
- consulting-analysis: Professional analysis framework
- find-skills: Discover new capabilities

## Decision Rules:
1. Analyze task complexity
2. Identify which workers are needed
3. Define clear subtask instructions for each worker
4. Synthesize all outputs into a coherent response
5. Simple tasks: handle directly with Think tool

Current datetime: {{ $now }}""",
        "tools": ["Web Search", "Think Tool", "Notion Tool"],
        "pos": [0, -1500],
        "llm_pos": [0, -1200],
        "mem_pos": [200, -1200],
    },
    "P4": {
        "name": "Evaluator-Optimizer Executor",
        "llm": "gpt-4.1",
        "temp": 0.5,
        "system_msg": """# P4: Evaluator-Optimizer Executor

You execute the Evaluator-Optimizer pattern: Generate → Evaluate → Refine loop.

## Process:
1. **Generate**: Create initial content/output
2. **Evaluate**: Assess quality against criteria (1-10 scale)
3. **Quality Gate**: If score >= 7, output. If < 7, refine.
4. **Refine**: Incorporate evaluation feedback into improved version
5. **Loop**: Max 3 refinement iterations

## Skills Loaded:
- consulting-analysis: Professional analysis framework
- newsletter-generation: Content structure and formatting
- deep-research: Research methodology

## Quality Criteria:
- Accuracy: Factual correctness
- Completeness: All aspects covered
- Clarity: Easy to understand
- Actionability: Specific recommendations
- Depth: Sufficient detail for decisions

Current datetime: {{ $now }}""",
        "tools": ["Web Search", "Think Tool"],
        "pos": [0, -900],
        "llm_pos": [0, -600],
        "mem_pos": [200, -600],
    },
    "P5": {
        "name": "Parallelization Executor",
        "llm": "gpt-4.1",
        "temp": 0.4,
        "system_msg": """# P5: Parallelization Executor

You execute the Parallelization pattern: Analyze from multiple perspectives simultaneously.

## Analysis Perspectives:
- **Financial**: Cost analysis, ROI, budget implications
- **Market**: Market size, trends, competitive landscape
- **Technical**: Feasibility, architecture, implementation

## Skills Loaded:
- data-analysis: Extract insights from data
- consulting-analysis: Professional analysis framework
- deep-research: Research methodology

## Process:
1. Analyze the query from all 3 perspectives
2. For each perspective, gather specific data points
3. Identify patterns and contradictions between perspectives
4. Synthesize into a unified analysis with recommendations

Current datetime: {{ $now }}""",
        "tools": ["Web Search", "Think Tool"],
        "pos": [0, -300],
        "llm_pos": [0, 0],
        "mem_pos": [200, 0],
    },
    "P6": {
        "name": "Cognitive Capital MCP Executor",
        "llm": "gpt-4.1",
        "temp": 0.3,
        "system_msg": """# P6: Cognitive Capital MCP Executor

You execute the Cognitive Capital MCP pattern: Load skills as tools for agent consumption.

## Available Skills (as MCP tools):
- deep-research: Systematic multi-angle research methodology
- consulting-analysis: Professional analysis framework
- data-analysis: Data extraction and visualization
- newsletter-generation: Content structure and formatting
- code-documentation: Precision and clarity standards
- podcast-generation: Audio content production

## Process:
1. Identify which skills are needed for the task
2. Load and activate relevant skills
3. Execute the task using the loaded skill methodology
4. Follow the progressive disclosure pattern (3 levels)
5. Return results with skill attribution

Current datetime: {{ $now }}""",
        "tools": ["Web Search", "Think Tool", "GitHub Tool"],
        "pos": [0, 300],
        "llm_pos": [0, 600],
        "mem_pos": [200, 600],
    },
    "P7": {
        "name": "SOUL Bootstrap Executor",
        "llm": "gpt-4.1-mini",
        "temp": 0.7,
        "system_msg": """# P7: SOUL Bootstrap Executor

You execute the SOUL Bootstrap pattern: Conversational onboarding for AI personality creation.

## Conversation Phases:
1. **Hello**: Establish preferred language
2. **You**: Learn who they are, what they need, AI name, relationship framing
3. **Personality**: Core traits, pushback preference, communication style
4. **Depth**: Autonomy level, failure philosophy, long-term vision

## Skills Loaded:
- bootstrap: Conversational onboarding and SOUL.md generation

## Generation Rules:
- One phase at a time, 1-3 questions max per round
- Converse, don't interrogate
- Mirror their energy and vocabulary
- When all required fields collected, generate SOUL.md
- SOUL.md must be under 300 words
- Core Traits are behavioral rules, not adjectives

Current datetime: {{ $now }}""",
        "tools": ["Think Tool"],
        "pos": [0, 900],
        "llm_pos": [0, 1200],
        "mem_pos": [200, 1200],
    },
    "P8": {
        "name": "Router-Orchestrator Executor",
        "llm": "gpt-4.1",
        "temp": 0.5,
        "system_msg": """# P8: Router-Orchestrator Executor (P2+P3 Combined)

You execute the Router-Orchestrator combined pattern: Smart routing + sub-orchestrator delegation.

## Teams:
- **Operations Team**: Calendar, email, Slack, project management
- **Research Team**: Deep research, data analysis, market intelligence
- **Creative Team**: Content creation, newsletters, podcasts
- **Technical Team**: Code, GitHub, debugging, architecture

## Process:
1. Classify the request domain
2. Route to the appropriate team
3. Each team decomposes tasks and executes
4. Aggregate results from all activated teams

## Skills Loaded:
- deep-research: Research methodology
- consulting-analysis: Professional analysis
- find-skills: Discover new capabilities

Current datetime: {{ $now }}""",
        "tools": ["Web Search", "Think Tool", "Slack Tool", "Notion Tool"],
        "pos": [0, 1500],
        "llm_pos": [0, 1800],
        "mem_pos": [200, 1800],
    },
    "P9": {
        "name": "Evaluator-Parallelization Executor",
        "llm": "gpt-4.1",
        "temp": 0.4,
        "system_msg": """# P9: Evaluator-Parallelization Executor (P4+P5 Combined)

You execute the Evaluator-Parallelization combined pattern: Multi-perspective analysis with quality-gated refinement.

## Process:
1. **Parallel Analysis**: Analyze from Financial, Market, and Technical perspectives
2. **Quality Evaluation**: Score overall quality (1-10)
3. **Quality Gate**: If score >= 7, proceed to synthesis. If < 7, refine.
4. **Refinement**: Address gaps and improve each perspective
5. **Synthesis**: Combine all perspectives into unified report

## Skills Loaded:
- consulting-analysis: Professional analysis framework
- data-analysis: Extract insights from data
- deep-research: Research methodology

## Output Structure:
1. Executive Summary
2. Market Analysis
3. Technical Assessment
4. Financial Projections
5. Integrated Recommendations
6. Risk Matrix

Current datetime: {{ $now }}""",
        "tools": ["Web Search", "Think Tool"],
        "pos": [0, 2100],
        "llm_pos": [0, 2400],
        "mem_pos": [200, 2400],
    },
    "P10": {
        "name": "Cognitive-SOUL Pipeline Executor",
        "llm": "gpt-4.1",
        "temp": 0.5,
        "system_msg": """# P10: Cognitive-SOUL Pipeline Executor (P6+P7 Combined)

You execute the Cognitive-SOUL Pipeline: Bootstrap personality + load cognitive capital skills.

## Process:
1. **SOUL Bootstrap**: If no personality exists, create one through conversation
   - Phase 1: Hello (language preference)
   - Phase 2: You (name, role, AI name, relationship)
   - Phase 3: Personality (traits, pushback, voice)
   - Phase 4: Depth (autonomy, failure philosophy)
2. **Cognitive Capital Loading**: Load relevant skills based on user profile
   - Researcher → deep-research, data-analysis, consulting-analysis
   - Business owner → consulting-analysis, newsletter-generation, data-analysis
   - Developer → code-documentation, deep-research, podcast-generation
   - Creator → newsletter-generation, podcast-generation, consulting-analysis
3. **Configuration**: Generate complete agent config (SOUL.md + skills manifest)

## Skills Loaded:
- bootstrap: Conversational onboarding
- deep-research: Research methodology
- consulting-analysis: Professional analysis

Current datetime: {{ $now }}""",
        "tools": ["Think Tool", "Web Search"],
        "pos": [0, 2700],
        "llm_pos": [0, 3000],
        "mem_pos": [200, 3000],
    },
}


def generate_zeus():
    """Generate the Zeus Meta-Orchestrator workflow."""
    nodes = []
    connections = []

    # ── Chat Trigger ────────────────────────────────────────────────
    nodes.append({
        "parameters": {
            "initialMessages": [{
                "role": "assistant",
                "content": "I am Zeus, your meta-orchestrator. I analyze your request and automatically select the best AI pattern to execute it. Whether you need research, content creation, analysis, routing, or personality bootstrapping — I handle it all. What would you like me to work on?"
            }]
        },
        "type": "n8n-nodes-base.chatTrigger",
        "typeVersion": 1.1,
        "position": [-2200, 0],
        "id": uid(),
        "name": "Chat Trigger"
    })

    # ── Zeus Agent (Meta-Orchestrator) ─────────────────────────────
    zeus_id = uid()
    nodes.append({
        "parameters": {
            "promptType": "define",
            "text": "={{ $json.chatInput }}",
            "options": {
                "systemMessage": """=# Zeus Meta-Orchestrator (DeerFlow Pattern)

You are Zeus, the top-level meta-orchestrator. You analyze user requests and select the optimal Anthropic agent pattern to execute them.

## Pattern Selection Guide:

| Pattern | When to Use | Complexity |
|---------|------------|------------|
| **P1 Prompt Chaining** | Multi-step content pipelines (research→draft→polish) | Medium |
| **P2 Smart Routing** | Multi-domain intent classification (calendar, email, research, etc.) | Medium-High |
| **P3 Orchestrator-Workers** | Complex task decomposition (break into subtasks for workers) | High |
| **P4 Evaluator-Optimizer** | Quality-gated iterative refinement (generate→evaluate→refine loop) | Medium-High |
| **P5 Parallelization** | Multi-perspective analysis (financial, market, technical views) | Medium |
| **P6 Cognitive Capital MCP** | Skill-as-a-service (load skills dynamically for agents) | Medium |
| **P7 SOUL Bootstrap** | AI personality creation (conversational onboarding → SOUL.md) | Low |
| **P8 Router-Orchestrator** | Smart routing + task delegation to specialized teams | High |
| **P9 Evaluator-Parallel** | Multi-perspective analysis with quality-gated refinement | High |
| **P10 Cognitive-SOUL** | Bootstrap personality + load cognitive capital skills | Medium |

## Decision Algorithm:

1. **Simple requests** (single task, one domain) → P1 or P7
2. **Multi-domain requests** (needs routing) → P2 or P8
3. **Complex tasks** (needs decomposition) → P3 or P8
4. **Quality-critical tasks** (needs iteration) → P4 or P9
5. **Multi-perspective analysis** (needs parallel views) → P5 or P9
6. **Skill/personality tasks** (needs bootstrapping) → P6, P7, or P10
7. **Combined patterns** (routing + orchestration) → P8
8. **Combined patterns** (parallel + quality) → P9

## Skills Loaded:
- deep-research: Systematic research methodology
- consulting-analysis: Professional analysis framework
- find-skills: Discover new capabilities

## Output Format:
You MUST return a JSON object with:
- pattern: The selected pattern code (P1-P10)
- confidence: Your confidence level (0.0-1.0)
- reasoning: Why you selected this pattern
- task_summary: A brief summary of the task for the executor

Current datetime: {{ $now }}"""
            }
        },
        "type": "@n8n/n8n-nodes-langchain.agent",
        "typeVersion": 1.8,
        "position": [-1600, 0],
        "id": zeus_id,
        "name": "Zeus Agent"
    })

    # Zeus LLM
    zeus_llm_id = uid()
    nodes.append({
        "parameters": {
            "model": {"__rl": True, "value": "gpt-4.1", "mode": "list"},
            "options": {"temperature": 0.2}
        },
        "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
        "typeVersion": 1.2,
        "position": [-1600, 300],
        "id": zeus_llm_id,
        "name": "GPT-4.1 Zeus",
        "credentials": {"openAiApi": {"id": "", "name": "OpenAI"}}
    })

    # Zeus Memory
    zeus_mem_id = uid()
    nodes.append({
        "parameters": {
            "sessionIdType": "customKey",
            "sessionKey": "={{ $json.sessionId || 'zeus' }}",
            "options": {}
        },
        "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
        "typeVersion": 1.3,
        "position": [-1400, 300],
        "id": zeus_mem_id,
        "name": "Zeus Memory"
    })

    # Zeus Think Tool
    zeus_think_id = uid()
    nodes.append({
        "parameters": {"description": "Analyze the request complexity, domain, and select the optimal Anthropic pattern. Consider task type, required quality level, and whether multi-perspective analysis is needed."},
        "type": "@n8n/n8n-nodes-langchain.toolThink",
        "typeVersion": 1,
        "position": [-1200, 300],
        "id": zeus_think_id,
        "name": "Zeus Think"
    })

    # Zeus Web Search Tool
    zeus_web_id = uid()
    nodes.append({
        "parameters": {
            "description": "Search the web for current information to help classify and understand the user's request",
            "url": "={ /*n8n-auto-generated-fromAI-override*/ $fromAI('Search_URL', `The search API endpoint URL`, 'string') }",
            "method": "GET",
            "options": {}
        },
        "type": "@n8n/n8n-nodes-langchain.toolHttpRequest",
        "typeVersion": 1.1,
        "position": [-1000, 300],
        "id": zeus_web_id,
        "name": "Zeus Web Search"
    })

    # Zeus Output Parser
    zeus_parser_id = uid()
    nodes.append({
        "parameters": {
            "schema": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Selected pattern code P1-P10"},
                    "confidence": {"type": "number", "description": "Confidence level 0.0-1.0"},
                    "reasoning": {"type": "string", "description": "Why this pattern was selected"},
                    "task_summary": {"type": "string", "description": "Brief task summary for executor"}
                }
            }
        },
        "type": "@n8n/n8n-nodes-langchain.outputParserStructured",
        "typeVersion": 1.1,
        "position": [-800, 300],
        "id": zeus_parser_id,
        "name": "Zeus Parser"
    })

    # ── Switch Node (Pattern Router) ────────────────────────────────
    switch_id = uid()
    switch_rules = []
    for i, (code, pattern) in enumerate(PATTERNS.items()):
        switch_rules.append({
            "value": code,
            "output": i,
            "operator": {
                "type": "string",
                "operation": "equals"
            }
        })

    nodes.append({
        "parameters": {
            "dataType": "string",
            "value1": "={{ $json.pattern }}",
            "rules": {
                "rules": switch_rules
            },
            "fallbackOutput": 0,
            "options": {}
        },
        "type": "n8n-nodes-base.switch",
        "typeVersion": 3,
        "position": [-800, 0],
        "id": switch_id,
        "name": "Pattern Router"
    })

    # ── Pattern Executor Agents (P1-P10) ────────────────────────────
    # Shared tools
    shared_tools = {}

    # Web Search Tool (shared by multiple executors)
    web_search_id = uid()
    nodes.append({
        "parameters": {
            "description": "Search the web for current information, news, and data about any topic",
            "url": "={ /*n8n-auto-generated-fromAI-override*/ $fromAI('Web_Search_URL', `Search API endpoint URL`, 'string') }",
            "method": "GET",
            "options": {}
        },
        "type": "@n8n/n8n-nodes-langchain.toolHttpRequest",
        "typeVersion": 1.1,
        "position": [800, 0],
        "id": web_search_id,
        "name": "Web Search"
    })

    # Think Tool
    think_id = uid()
    nodes.append({
        "parameters": {"description": "Plan strategy, analyze options, and organize thoughts before executing"},
        "type": "@n8n/n8n-nodes-langchain.toolThink",
        "typeVersion": 1,
        "position": [1000, 0],
        "id": think_id,
        "name": "Think Tool"
    })

    # Slack Tool
    slack_id = uid()
    nodes.append({
        "parameters": {
            "description": "Send messages, list channels, and search in Slack",
            "url": "={ /*n8n-auto-generated-fromAI-override*/ $fromAI('Slack_Tool_URL', `Slack API endpoint URL`, 'string') }",
            "method": "GET",
            "options": {}
        },
        "type": "@n8n/n8n-nodes-langchain.toolHttpRequest",
        "typeVersion": 1.1,
        "position": [1200, 0],
        "id": slack_id,
        "name": "Slack Tool"
    })

    # Notion Tool
    notion_id = uid()
    nodes.append({
        "parameters": {
            "description": "Search and manage Notion pages and databases for knowledge base",
            "url": "={ /*n8n-auto-generated-fromAI-override*/ $fromAI('Notion_Tool_URL', `Notion API endpoint URL`, 'string') }",
            "method": "GET",
            "options": {}
        },
        "type": "@n8n/n8n-nodes-langchain.toolHttpRequest",
        "typeVersion": 1.1,
        "position": [1400, 0],
        "id": notion_id,
        "name": "Notion Tool"
    })

    # GitHub Tool
    github_id = uid()
    nodes.append({
        "parameters": {
            "description": "Access GitHub repos, issues, PRs, and code search",
            "url": "={ /*n8n-auto-generated-fromAI-override*/ $fromAI('GitHub_Tool_URL', `GitHub API endpoint URL`, 'string') }",
            "method": "GET",
            "options": {}
        },
        "type": "@n8n/n8n-nodes-langchain.toolHttpRequest",
        "typeVersion": 1.1,
        "position": [1600, 0],
        "id": github_id,
        "name": "GitHub Tool"
    })

    # Build executor agents
    conn_list = []

    # Chat → Zeus
    conn_list.append(main_conn("Chat Trigger", "Zeus Agent"))

    # Zeus ai_* connections
    conn_list.append(ai_conn("GPT-4.1 Zeus", "Zeus Agent", "ai_languageModel"))
    conn_list.append(ai_conn("Zeus Memory", "Zeus Agent", "ai_memory"))
    conn_list.append(ai_conn("Zeus Think", "Zeus Agent", "ai_tool"))
    conn_list.append(ai_conn("Zeus Web Search", "Zeus Agent", "ai_tool"))
    conn_list.append(ai_conn("Zeus Parser", "Zeus Agent", "ai_outputParser"))

    # Zeus → Pattern Router
    conn_list.append(main_conn("Zeus Agent", "Pattern Router"))

    # Pattern Router → Executor Agents (10 branches)
    for i, (code, pattern) in enumerate(PATTERNS.items()):
        executor_id = uid()
        llm_id = uid()
        mem_id = uid()

        # Executor Agent
        nodes.append({
            "parameters": {
                "promptType": "define",
                "text": "={{ $('Zeus Agent').item.json.task_summary || $json.chatInput || $json.query }}",
                "options": {
                    "systemMessage": f"={pattern['system_msg']}"
                }
            },
            "type": "@n8n/n8n-nodes-langchain.agent",
            "typeVersion": 1.8,
            "position": pattern["pos"],
            "id": executor_id,
            "name": pattern["name"]
        })

        # Executor LLM
        nodes.append({
            "parameters": {
                "model": {"__rl": True, "value": pattern["llm"], "mode": "list"},
                "options": {"temperature": pattern["temp"]}
            },
            "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
            "typeVersion": 1.2,
            "position": pattern["llm_pos"],
            "id": llm_id,
            "name": f"{code} LLM",
            "credentials": {"openAiApi": {"id": "", "name": "OpenAI"}}
        })

        # Executor Memory
        nodes.append({
            "parameters": {
                "sessionIdType": "customKey",
                "sessionKey": f"={{ $json.sessionId || '{code.lower()}' }}",
                "options": {}
            },
            "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
            "typeVersion": 1.3,
            "position": pattern["mem_pos"],
            "id": mem_id,
            "name": f"{code} Memory"
        })

        # Pattern Router → Executor (switch output)
        conn_list.append({
            "Pattern Router": {
                "main": [[{"node": pattern["name"], "type": "main", "index": 0}]]
            }
        })

        # Executor ai_* connections
        conn_list.append(ai_conn(f"{code} LLM", pattern["name"], "ai_languageModel"))
        conn_list.append(ai_conn(f"{code} Memory", pattern["name"], "ai_memory"))

        # Tool connections for this executor
        for tool_name in pattern["tools"]:
            if tool_name == "Web Search":
                conn_list.append(ai_conn("Web Search", pattern["name"], "ai_tool"))
            elif tool_name == "Think Tool":
                conn_list.append(ai_conn("Think Tool", pattern["name"], "ai_tool"))
            elif tool_name == "Slack Tool":
                conn_list.append(ai_conn("Slack Tool", pattern["name"], "ai_tool"))
            elif tool_name == "Notion Tool":
                conn_list.append(ai_conn("Notion Tool", pattern["name"], "ai_tool"))
            elif tool_name == "GitHub Tool":
                conn_list.append(ai_conn("GitHub Tool", pattern["name"], "ai_tool"))

        # Executor → Synthesis
        conn_list.append(main_conn(pattern["name"], "Synthesis Agent"))

    # ── Synthesis Agent ─────────────────────────────────────────────
    synth_id = uid()
    nodes.append({
        "parameters": {
            "promptType": "define",
            "text": "={{ $json.output || $json.chatInput }}",
            "options": {
                "systemMessage": """=# Synthesis Agent (Zeus Pipeline)

You are the final synthesis agent in the Zeus pipeline. You receive the output from the pattern executor and create a polished, comprehensive response.

## Skills Loaded:
- consulting-analysis: Professional analysis framework
- newsletter-generation: Content structure and formatting

## Process:
1. Review the pattern executor's output
2. Identify which pattern was used (from context)
3. Ensure the output is complete and well-structured
4. Add any missing context or transitions
5. Format for the user's preferred output style
6. Include a brief note about which pattern was used and why

## Output Format:
- If the executor already produced a structured output, preserve it
- If the output is raw, structure it with clear sections
- Always include a brief "Pattern Used" note at the end
- Maintain the voice and style consistent with the user's preferences

Current datetime: {{ $now }}"""
            }
        },
        "type": "@n8n/n8n-nodes-langchain.agent",
        "typeVersion": 1.8,
        "position": [2200, 0],
        "id": synth_id,
        "name": "Synthesis Agent"
    })

    # Synthesis LLM
    synth_llm_id = uid()
    nodes.append({
        "parameters": {
            "model": {"__rl": True, "value": "gpt-4.1", "mode": "list"},
            "options": {"temperature": 0.4}
        },
        "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
        "typeVersion": 1.2,
        "position": [2200, 300],
        "id": synth_llm_id,
        "name": "GPT-4.1 Synthesis",
        "credentials": {"openAiApi": {"id": "", "name": "OpenAI"}}
    })

    # Synthesis Memory
    synth_mem_id = uid()
    nodes.append({
        "parameters": {
            "sessionIdType": "customKey",
            "sessionKey": "={{ $json.sessionId || 'synthesis' }}",
            "options": {}
        },
        "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
        "typeVersion": 1.3,
        "position": [2400, 300],
        "id": synth_mem_id,
        "name": "Synthesis Memory"
    })

    # Synthesis ai_* connections
    conn_list.append(ai_conn("GPT-4.1 Synthesis", "Synthesis Agent", "ai_languageModel"))
    conn_list.append(ai_conn("Synthesis Memory", "Synthesis Agent", "ai_memory"))

    # ── Sticky Notes ────────────────────────────────────────────────
    nodes.append({
        "parameters": {
            "content": "⚡ ZEUS META-ORCHESTRATOR (DeerFlow Pattern)\n\nChat → Zeus Agent (classifies + selects pattern)\n→ Pattern Router (10 branches)\n→ P1-P10 Executor Agents\n→ Synthesis Agent\n\n10 Anthropic Patterns:\nP1: Prompt Chaining\nP2: Smart Routing\nP3: Orchestrator-Workers\nP4: Evaluator-Optimizer\nP5: Parallelization\nP6: Cognitive Capital MCP\nP7: SOUL Bootstrap\nP8: Router-Orchestrator\nP9: Evaluator-Parallel\nP10: Cognitive-SOUL Pipeline\n\nLLM: GPT-4.1 (Zeus) → tiered per pattern",
            "width": 400,
            "height": 400
        },
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [-2600, -400],
        "id": uid(),
        "name": "Sticky Note"
    })

    nodes.append({
        "parameters": {
            "content": "📊 Pattern Selection Logic\n\nSimple → P1, P7\nMulti-domain → P2, P8\nComplex → P3, P8\nQuality-critical → P4, P9\nMulti-perspective → P5, P9\nSkill/personality → P6, P7, P10\nCombined → P8, P9, P10",
            "width": 300,
            "height": 250
        },
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": [-2600, 400],
        "id": uid(),
        "name": "Sticky Note 2"
    })

    # Merge all connections
    connections = merge_dicts(conn_list)

    return make_workflow(
        "Zeus Meta-Orchestrator v3",
        nodes,
        connections,
        tags=["zeus", "meta-orchestrator", "deerflow", "anthropic", "all-patterns"]
    )


# ── Integration ────────────────────────────────────────────────────────

def integrate_into_packages():
    """Add Zeus to Professional and Enterprise packages."""
    wf = generate_zeus()

    fname = "Zeus_Meta_Orchestrator_v3.json"

    # Save to top-level anthropic_patterns/
    path = f"{BASE}/anthropic_patterns/{fname}"
    with open(path, "w") as f:
        json.dump(wf, f, indent=2)
    print(f"  ✓ anthropic_patterns/{fname}")

    # Save to Professional and Enterprise
    for pkg in ["jarvis-professional", "jarvis-enterprise"]:
        dest = f"{BASE}/{pkg}/workflows/anthropic_patterns/{fname}"
        shutil.copy2(path, dest)
        print(f"  ✓ {pkg}/workflows/anthropic_patterns/{fname}")

    # Update manifests
    for pkg in ["jarvis-professional", "jarvis-enterprise"]:
        mpath = f"{BASE}/{pkg}/manifest.json"
        with open(mpath) as f:
            m = json.load(f)

        if fname not in m["workflows"]["anthropic_patterns"]:
            m["workflows"]["anthropic_patterns"].append(fname)

        m["total_workflows"] = sum(len(v) for v in m["workflows"].values())
        m["version"] = "3.2.0"

        with open(mpath, "w") as f:
            json.dump(m, f, indent=2)

        total = m["total_workflows"]
        n_patterns = len(m["workflows"]["anthropic_patterns"])
        print(f"  ✓ {pkg}/manifest.json — v3.2.0, {total} workflows, {n_patterns} patterns")

    # Update pricing.html
    update_pricing()

    # Count ai_* connections
    ai_count = 0
    for node_name, conns in wf.get("connections", {}).items():
        for conn_type, conn_list_val in conns.items():
            if conn_type.startswith("ai_"):
                ai_count += len(conn_list_val)
    print(f"\n  Zeus ai_* connections: {ai_count}")

    return wf


def update_pricing():
    ppath = f"{BASE}/pricing.html"
    with open(ppath) as f:
        html = f.read()

    # Update stats
    html = html.replace(
        '<div class="number" style="color: var(--accent-starter)">40</div>',
        '<div class="number" style="color: var(--accent-starter)">42</div>',
    )

    # Update subtitle
    html = html.replace(
        "40 zero-debt n8n automations + 10 Anthropic agent patterns",
        "42 zero-debt n8n automations + 11 Anthropic patterns (incl. Zeus Meta-Orchestrator)"
    )

    # Update footer
    html = html.replace(
        "Built with zero technical debt • 40 workflows • 10 Anthropic patterns • 11 MCP servers • 6 cognitive capital skills",
        "Built with zero technical debt • 42 workflows • 11 Anthropic patterns • 11 MCP servers • 6 cognitive capital skills • Zeus Meta-Orchestrator"
    )

    # Update comparison table
    html = html.replace(
        "<tr><td>Anthropic Pattern Workflows</td><td>3 (P1+P7+P10)</td><td>9 (P1-P5+P7-P10)</td><td>10 (P1-P10)</td></tr>",
        "<tr><td>Anthropic Pattern Workflows</td><td>3 (P1+P7+P10)</td><td>10 (P1-P10 + Zeus)</td><td>11 (P1-P10 + Zeus)</td></tr>",
    )

    # Add Zeus row to comparison table
    html = html.replace(
        '            <tr><td>P10 Cognitive-SOUL Pipeline</td><td class="yes">✓</td><td class="yes">✓</td><td class="yes">✓</td></tr>',
        '            <tr><td>P10 Cognitive-SOUL Pipeline</td><td class="yes">✓</td><td class="yes">✓</td><td class="yes">✓</td></tr>\n            <tr><td>⚡ Zeus Meta-Orchestrator</td><td class="no">—</td><td class="yes">✓</td><td class="yes">✓</td></tr>',
    )

    # Update Professional features
    html = html.replace(
        "<li><span class=\"check\">✓</span> <strong>P10 Cognitive-SOUL Pipeline</strong></li>\n            <li><span class=\"check\">✓</span> 4 Cognitive Capital Skills</li>",
        "<li><span class=\"check\">✓</span> <strong>P10 Cognitive-SOUL Pipeline</strong></li>\n            <li><span class=\"check\">✓</span> <strong>⚡ Zeus Meta-Orchestrator</strong></li>\n            <li><span class=\"check\">✓</span> 4 Cognitive Capital Skills</li>",
    )

    # Update Enterprise features
    html = html.replace(
        "<li><span class=\"check\">✓</span> <strong>P10 Cognitive-SOUL Pipeline</strong></li>\n            <li><span class=\"check\">✓</span> <strong>P8 Router-Orchestrator</strong></li>",
        "<li><span class=\"check\">✓</span> <strong>P10 Cognitive-SOUL Pipeline</strong></li>\n            <li><span class=\"check\">✓</span> <strong>⚡ Zeus Meta-Orchestrator</strong></li>\n            <li><span class=\"check\">✓</span> <strong>P8 Router-Orchestrator</strong></li>",
    )

    with open(ppath, "w") as f:
        f.write(html)
    print(f"  ✓ pricing.html updated")


# ── Main ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  Phase 5: Zeus Meta-Orchestrator")
    print("  DeerFlow-style top-level orchestrator")
    print("=" * 60)

    print("\n1. Generating Zeus Meta-Orchestrator workflow...")
    wf = integrate_into_packages()

    print("\n2. Node count:", len(wf["nodes"]))
    print("3. Connection groups:", len(wf["connections"]))

    # Count total ai_* connections
    ai_total = 0
    for node_name, conns in wf["connections"].items():
        for conn_type, conn_list_val in conns.items():
            if conn_type.startswith("ai_"):
                ai_total += len(conn_list_val)
    print(f"4. Total ai_* connections: {ai_total}")

    print("\n" + "=" * 60)
    print("  ✅ Zeus Meta-Orchestrator generated!")
    print("=" * 60)
    print()
    print("  Architecture:")
    print("    Chat Trigger → Zeus Agent (GPT-4.1, temp=0.2)")
    print("    → Pattern Router (10 branches)")
    print("    → P1-P10 Executor Agents (tiered LLMs)")
    print("    → Synthesis Agent (GPT-4.1)")
    print()
    print("  Package Distribution:")
    print("    Starter: Not included (needs Pro+ for complexity)")
    print("    Professional: Zeus included (P1-P10)")
    print("    Enterprise: Zeus included (P1-P10)")
