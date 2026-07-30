# JARVIS AI Automation Ecosystem — Integrations Reference

> Version: 6.0.0 | Phase 8 | Last Updated: 2026-07-30

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
