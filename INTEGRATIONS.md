# JARVIS AI Automation — Integrations & OAuth2 Reference

> **Version**: 5.0.0 | **Zero Technical Debt** | **26 MCP Servers** | **300+ Connections**
> **Last Updated**: 2026-07-30
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
