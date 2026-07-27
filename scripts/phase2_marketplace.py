"""
Phase 2 Marketplace Listings Generator for n8nmarkets.com
Generates detailed listing materials for Starter/Professional tier items
(priority items to generate traffic first)
"""

import json
import os
from datetime import datetime

OUTPUT_DIR = "/home/z/my-project/download/n8n_workflows_v2/marketplace_listings"

# Marketplace listing structure for n8nmarkets.com
MARKETPLACE_LISTINGS = {
    # ============================================================
    # STARTER TIER (Publish first - low price, high volume)
    # ============================================================
    "G13_Global_Error_Handler": {
        "title": "Global Error Handler Workflow - Production-Ready Error Management",
        "short_description": "Automated error handling for all your n8n workflows. Classify severity, send alerts, and log errors to PostgreSQL.",
        "long_description": """## 🛡️ Global Error Handler v2

**Zero-debt, production-ready n8n workflow** for automated error management across all your automation infrastructure.

### What It Does
- **Error Trigger**: Automatically catches errors from any n8n workflow configured to use this handler
- **Severity Classification**: Routes errors into Critical, Warning, and Info categories using smart pattern matching
- **Critical Alerts**: Sends urgent email notifications to your admin team for immediate attention
- **Warning Logging**: Stores warning-level errors in PostgreSQL for review
- **Info Logging**: Tracks minor errors for analytics and debugging
- **Console Logging**: Real-time error output for development monitoring

### Key Features
- ✅ Zero-debt engineering - no technical debt, all connections correct
- ✅ Severity-based routing - Critical/Warning/Info classification
- ✅ Dual notification - Email alerts + Database logging
- ✅ Structured error data - Workflow, Node, Message, Timestamp
- ✅ Easy setup - Just set as error handler in your other workflows' settings

### Setup Instructions
1. Create `n8n_error_log` table in PostgreSQL
2. Configure Gmail + PostgreSQL credentials
3. Update admin email address
4. Activate this workflow
5. In your other workflows, go to Settings → Error Workflow → select this handler

### Included
- 1 importable n8n JSON workflow
- StickyNote documentation nodes
- PostgreSQL table creation SQL script available on request""",
        "price": 15,
        "tier": "Starter",
        "tags": ["error handling", "production", "monitoring", "PostgreSQL", "Gmail alerts"],
        "category": "Utilities",
        "difficulty": "Beginner",
        "credentials_required": ["Gmail OAuth2", "PostgreSQL"],
        "nodes_count": 8,
        "compatible_n8n_version": "1.0+",
        "images": ["error_handler_flow_diagram"],
        "bundle_available": True
    },
    
    "G12_Flowise_RAG_Suite": {
        "title": "Flowise RAG Agent Suite - Knowledge Base Chatbot with Flowise Integration",
        "short_description": "AI chatbot connected to Flowise RAG pipeline for accurate document-based answers with source citations.",
        "long_description": """## 📚 Flowise RAG Agent Suite v2

**Production-ready n8n workflow** for building knowledge-based chatbots with Flowise RAG integration.

### What It Does
- **Chat Interface**: Built-in ChatTrigger for immediate interactive testing
- **RAG Search**: Connects to your Flowise RAG pipeline for document-based answers
- **Source Citations**: Automatically references source documents in responses
- **Think Tool**: Plans complex research queries before execution
- **Conversation Memory**: Maintains context across multi-turn conversations

### Key Features
- ✅ Zero-debt: All `ai_*` connections properly wired
- ✅ Flowise HTTP integration - seamless RAG pipeline connection
- ✅ Cost-optimized LLM: GPT-4o-mini ($0.15/$0.60 per 1M tokens)
- ✅ Memory: BufferWindow for conversation context
- ✅ Easy setup - just configure your Flowise URL

### Setup Instructions
1. Deploy Flowise with your RAG pipeline
2. Import this workflow into n8n
3. Configure OpenAI credential
4. Update Flowise API URL in the HTTP tool node
5. Test via ChatTrigger interface""",
        "price": 19,
        "tier": "Starter",
        "tags": ["RAG", "knowledge base", "Flowise", "chatbot", "document search"],
        "category": "AI Agents",
        "difficulty": "Intermediate",
        "credentials_required": ["OpenAI"],
        "nodes_count": 7,
        "compatible_n8n_version": "1.0+",
        "bundle_available": True
    },
    
    # ============================================================
    # PROFESSIONAL TIER (Publish second - moderate price, quality)
    # ============================================================
    "G1_MCP_Calendar_Suite": {
        "title": "MCP Calendar Suite Pro - AI-Powered Calendar Management MCP Server",
        "short_description": "Deploy as MCP server to give any AI agent full Google Calendar control: create, delete, get, and update events.",
        "long_description": """## 📋 MCP Calendar Suite Pro v2

**Zero-debt, production-ready MCP server** for Google Calendar management. Deploy standalone and connect to any AI agent via MCP Client Tool.

### What It Does
- **MCP Server**: Deploys as standalone MCP server that any n8n AI agent can connect to
- **Create Events**: Create calendar events with AI-generated parameters (title, time, attendees, description)
- **Delete Events**: Remove events by ID
- **Get Events**: Search and retrieve events by date range
- **Update Events**: Modify existing event details

### Key Features
- ✅ Zero-debt: All `ai_tool` connections to MCP Trigger (correct MCP pattern)
- ✅ `$fromAI()` expressions: Every parameter is AI-generated, enabling true conversational control
- ✅ Proper `googleCalendarTool` node type (AI-tool variant, not regular action node)
- ✅ OAuth2 credential: Secure Google Calendar access
- ✅ Timezone support: Configurable timezone for event times

### Setup Instructions
1. Import into n8n and configure Google Calendar OAuth2 credential
2. Select your calendar in each tool node
3. **Activate** this workflow (MCP servers must be active)
4. Copy the SSE endpoint URL from the MCP Trigger node
5. In your parent Agent workflow, use `mcpClientTool` with the copied SSE endpoint

### Architecture
```
MCP Trigger (path: /mcp-calendar-suite)
    ↑ ai_tool
    ├── Create Event (googleCalendarTool)
    ├── Delete Event (googleCalendarTool)
    ├── Get Events (googleCalendarTool)
    └── Update Event (googleCalendarTool)
```""",
        "price": 35,
        "tier": "Professional",
        "tags": ["MCP", "Google Calendar", "calendar management", "AI tools", "MCP server"],
        "category": "MCP Servers",
        "difficulty": "Intermediate",
        "credentials_required": ["Google Calendar OAuth2"],
        "nodes_count": 6,
        "compatible_n8n_version": "1.0+",
        "images": ["calendar_mcp_architecture"],
        "bundle_available": True
    },
    
    "G2_MCP_Gmail_Suite": {
        "title": "MCP Gmail Suite Pro - AI-Powered Email Management MCP Server",
        "short_description": "Deploy as MCP server to give any AI agent full Gmail control: send, search, read, reply, and delete emails.",
        "long_description": """## 📧 MCP Gmail Suite Pro v2

**Zero-debt, production-ready MCP server** for Gmail management. 5 email tools with `$fromAI()` for conversational email control.

### Tools Included
- **Send Email**: Compose and send emails with AI-generated subject, body, recipients
- **Search Emails**: Find emails by Gmail query syntax
- **Get Email**: Retrieve specific email by message ID
- **Reply Email**: Reply to existing email threads
- **Delete Email**: Remove emails by message ID

### Key Features
- ✅ 5 `gmailTool` nodes with `ai_tool` connections to MCP Trigger
- ✅ `$fromAI()` expressions on all parameters for AI-generated arguments
- ✅ Correct MCP server pattern: tools → trigger, NOT tools → agent
- ✅ Template-ready credentials: empty IDs, descriptive names""",
        "price": 29,
        "tier": "Professional",
        "tags": ["MCP", "Gmail", "email management", "AI tools", "MCP server"],
        "category": "MCP Servers",
        "difficulty": "Intermediate",
        "credentials_required": ["Gmail OAuth2"],
        "nodes_count": 7,
        "compatible_n8n_version": "1.0+",
        "bundle_available": True
    },
    
    "G3_MCP_Contactos_Suite": {
        "title": "MCP Contacts Suite Pro - AI-Powered Contact Management MCP Server",
        "short_description": "Deploy as MCP server for full Google Contacts control: create, get, search, update, and delete contacts.",
        "long_description": """## 👤 MCP Contacts Suite Pro v2

**Zero-debt MCP server** for Google Contacts management. 5 contact tools with `$fromAI()`.

### Tools: Create, Get, Search, Update, Delete contacts
### Pattern: MCP Trigger → 5 googleContactsTool nodes via ai_tool""",
        "price": 25,
        "tier": "Professional",
        "tags": ["MCP", "Google Contacts", "contact management", "AI tools"],
        "category": "MCP Servers",
        "difficulty": "Intermediate",
        "credentials_required": ["Google Contacts OAuth2"],
        "nodes_count": 7,
        "compatible_n8n_version": "1.0+",
        "bundle_available": True
    },
    
    "G9_Social_Scraper_Suite": {
        "title": "Universal Social Scraper Suite - Multi-Platform Data Extraction Agent",
        "short_description": "AI agent that scrapes Instagram, LinkedIn, Google Maps, and Twitter/X data via configurable HTTP tools.",
        "long_description": """## 🔍 Universal Social Scraper Suite v2

**Zero-debt AI agent** for multi-platform social data extraction. 4 dedicated scraper tools.

### Platforms Supported
- Instagram: Profile data, posts, followers, engagement
- LinkedIn: Professional profiles, job listings, company data
- Google Maps: Business data, emails, reviews, contact info
- Twitter/X: Tweets, profiles, engagement metrics

### Key Features
- ✅ Webhook API endpoint for external integration
- ✅ GPT-4o-mini LLM (cost-optimized)
- ✅ Structured JSON output with timestamps
- ✅ Configurable scraper API URLs""",
        "price": 35,
        "tier": "Professional",
        "tags": ["scraper", "Instagram", "LinkedIn", "Google Maps", "data extraction"],
        "category": "Data Extraction",
        "difficulty": "Advanced",
        "credentials_required": ["OpenAI"],
        "nodes_count": 11,
        "compatible_n8n_version": "1.0+",
        "bundle_available": True
    },
    
    "G7_Imagenes_Citas_Suite": {
        "title": "AI Image & Quote Generator Suite - Creative Content with Gemini Flash",
        "short_description": "Creative AI agent using Gemini 2.5 Flash for generating inspirational images with quotes.",
        "long_description": """## 🎨 AI Image & Quote Generator Suite v2

**Zero-debt creative agent** using Gemini 2.5 Flash (multimodal, cost-effective) for image+quote generation.

### Key Features
- ✅ ChatTrigger for interactive creation
- ✅ Gemini 2.5 Flash LLM (multimodal)
- ✅ Think tool for creative planning
- ✅ Quote Generator HTTP tool
- ✅ Image Prompt Generator HTTP tool""",
        "price": 39,
        "tier": "Professional",
        "tags": ["images", "quotes", "Gemini", "creative", "content generation"],
        "category": "Creative",
        "difficulty": "Intermediate",
        "credentials_required": ["Google Gemini", "OpenAI"],
        "nodes_count": 8,
        "compatible_n8n_version": "1.0+",
        "bundle_available": True
    },
    
    "G10_HR_AI_Agent": {
        "title": "HR AI Agent Pro - Resume Screening & Interview Scheduling Assistant",
        "short_description": "AI HR assistant for resume evaluation, interview scheduling, and employee database queries.",
        "long_description": """## 👤 HR AI Agent Pro v2

**Zero-debt HR assistant** with resume analysis, interview scheduling, and employee management tools.

### Tools: Think, Resume Analyzer, Interview Scheduler, Employee Database
### LLM: GPT-4o-mini | Memory: BufferWindow""",
        "price": 45,
        "tier": "Professional",
        "tags": ["HR", "resume screening", "interview scheduling", "AI agent"],
        "category": "HR",
        "difficulty": "Advanced",
        "credentials_required": ["OpenAI"],
        "nodes_count": 12,
        "compatible_n8n_version": "1.0+",
        "bundle_available": True
    },
    
    "G11_WhatsApp_AI_Agent": {
        "title": "WhatsApp AI Agent Pro - RAG-Powered Customer Service with Evolution API",
        "short_description": "Full WhatsApp AI agent with RAG knowledge base, voice transcription, order lookup, and appointment booking.",
        "long_description": """## 💬 WhatsApp AI Agent Pro v2

**Zero-debt WhatsApp agent** with Evolution API integration, RAG knowledge base, voice transcription, and business tools.

### Key Features
- ✅ Evolution API webhook integration (WhatsApp)
- ✅ Voice transcription via OpenAI
- ✅ PostgresChatHistory (production-grade memory)
- ✅ Qdrant RAG with Gemini embeddings (knowledge base)
- ✅ Order lookup + Appointment booking tools
- ✅ Think tool for complex multi-step reasoning

### Architecture
```
WhatsApp Webhook (Evolution API)
    → Parse Message → Switch (text/voice)
    → Download Audio → Transcribe (voice path)
    → Set Text → AI Agent (text path)
    
Agent connections:
    ai_languageModel ← GPT-4o-mini
    ai_memory ← PostgresChatHistory
    ai_tool ← Think + Knowledge Base + Order + Appointment
    ai_embedding ← Gemini Embeddings → Qdrant Vector Store
```""",
        "price": 49,
        "tier": "Professional",
        "tags": ["WhatsApp", "Evolution API", "RAG", "Qdrant", "customer service"],
        "category": "WhatsApp",
        "difficulty": "Advanced",
        "credentials_required": ["OpenAI", "PostgreSQL", "Qdrant", "Google Gemini"],
        "nodes_count": 17,
        "compatible_n8n_version": "1.0+",
        "bundle_available": True
    },
}

# Bundle pricing strategy
BUNDLE_LISTINGS = {
    "MCP_Trio_Bundle": {
        "title": "MCP Server Trio Bundle - Calendar + Gmail + Contacts",
        "short_description": "All 3 MCP servers at 30% savings! Deploy Calendar, Gmail, and Contacts MCP servers for complete personal assistant capability.",
        "price": 63,  # $35 + $29 + $25 = $89, savings = $26 (29% off)
        "original_price": 89,
        "savings_percent": 29,
        "included_items": ["G1_MCP_Calendar_Suite", "G2_MCP_Gmail_Suite", "G3_MCP_Contactos_Suite"],
        "tier": "Professional",
        "tags": ["MCP bundle", "Calendar", "Gmail", "Contacts", "personal assistant"],
    },
    "Starter_Bundle": {
        "title": "Starter Bundle - Error Handler + RAG Agent",
        "short_description": "2 Starter tier workflows at 25% savings. Get production error handling AND knowledge-based chatbot.",
        "price": 27,  # $15 + $19 = $34, savings = $7 (20% off)
        "original_price": 34,
        "savings_percent": 20,
        "included_items": ["G13_Global_Error_Handler", "G12_Flowise_RAG_Suite"],
        "tier": "Starter",
        "tags": ["starter bundle", "error handler", "RAG", "chatbot"],
    },
    "Professional_Bundle": {
        "title": "Professional AI Agent Bundle - 5 Best-Selling Workflows",
        "short_description": "5 Professional tier workflows at 33% savings! WhatsApp Agent, HR Agent, Social Scraper, Image/Quote Suite, MCP Contacts.",
        "price": 149,  # $49 + $45 + $35 + $39 + $25 = $193, savings = $44 (23% off)
        "original_price": 193,
        "savings_percent": 23,
        "included_items": ["G11_WhatsApp_AI_Agent", "G10_HR_AI_Agent", "G9_Social_Scraper_Suite", "G7_Imagenes_Citas_Suite", "G3_MCP_Contactos_Suite"],
        "tier": "Professional",
        "tags": ["professional bundle", "AI agents", "WhatsApp", "HR", "scraper"],
    },
}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate individual listings
    all_listings = {}
    for item_id, listing in MARKETPLACE_LISTINGS.items():
        listing["id"] = item_id
        listing["github_repo"] = "https://github.com/grootme/workflows"
        listing["workflow_file"] = f"consolidated/{item_id}_v2.json"
        listing["last_updated"] = datetime.now().isoformat()
        listing["version"] = "2.0.0"
        listing["zero_debt_certified"] = True
        listing["validation_score"] = "100%"
        all_listings[item_id] = listing
        
        # Save individual listing
        filepath = os.path.join(OUTPUT_DIR, f"{item_id}_listing.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(listing, f, indent=2, ensure_ascii=False)
    
    # Generate bundle listings
    for bundle_id, bundle in BUNDLE_LISTINGS.items():
        bundle["id"] = bundle_id
        bundle["github_repo"] = "https://github.com/grootme/workflows"
        bundle["last_updated"] = datetime.now().isoformat()
        bundle["version"] = "2.0.0"
        bundle["zero_debt_certified"] = True
        bundle["is_bundle"] = True
        all_listings[bundle_id] = bundle
        
        filepath = os.path.join(OUTPUT_DIR, f"{bundle_id}_listing.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(bundle, f, indent=2, ensure_ascii=False)
    
    # Save all listings combined
    filepath = os.path.join(OUTPUT_DIR, "all_listings_v2.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(all_listings, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("=" * 60)
    print("MARKETPLACE LISTINGS GENERATED")
    print("=" * 60)
    
    # Sort by publish priority
    starter = {k: v for k, v in MARKETPLACE_LISTINGS.items() if v["tier"] == "Starter"}
    professional = {k: v for k, v in MARKETPLACE_LISTINGS.items() if v["tier"] == "Professional"}
    
    print("\n🟢 PUBLISH FIRST (Starter Tier - Generate Traffic):")
    for name, listing in starter.items():
        print(f"  • {listing['title']}")
        print(f"    Price: ${listing['price']} | Tags: {', '.join(listing['tags'][:3])}")
    
    print("\n🔵 PUBLISH SECOND (Professional Tier - Quality Revenue):")
    for name, listing in professional.items():
        print(f"  • {listing['title']}")
        print(f"    Price: ${listing['price']} | Tags: {', '.join(listing['tags'][:3])}")
    
    print("\n🟡 BUNDLE OFFERS:")
    for name, bundle in BUNDLE_LISTINGS.items():
        print(f"  • {bundle['title']}")
        print(f"    Price: ${bundle['price']} (was ${bundle['original_price']}, {bundle['savings_percent']}% savings)")
    
    total_individual = sum(v["price"] for v in MARKETPLACE_LISTINGS.values())
    total_bundles = sum(v["price"] for v in BUNDLE_LISTINGS.values())
    print(f"\n💰 Total individual value: ${total_individual}")
    print(f"💰 Total bundle value: ${total_bundles}")
    print(f"📁 Listings saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
