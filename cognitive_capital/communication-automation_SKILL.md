# Communication Automation

> **Category**: Communication | **Tier**: Professional | **Version**: 3.0

## Overview

Multi-channel communication orchestration across WhatsApp Business API, Telegram Bot, and Discord. Manages inbound/outbound messaging, interactive menus, media delivery, contact segmentation, and cross-platform notification routing.

## Core Capabilities

### WhatsApp Business API
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
- **Message Search**: Advanced search with filters for audit and reference

## Integration Points

### WhatsApp Business API
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
- **Intents**: Required for message content and member events

## OAuth2 & Authentication

### WhatsApp Business API — OAuth2 Flow
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
```

## Workflow Patterns

### Pattern 1: Lead Capture (WhatsApp → CRM)
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
```

## Best Practices

1. **WhatsApp 24h Window**: Free-form messages only within 24h of last user message; use templates outside
2. **Telegram Rate Limits**: 30 msg/sec per bot, 20 msg/min per group; use sleep between batches
3. **Discord Rate Limits**: 5 req/sec per route; respect X-RateLimit-Remaining headers
4. **Template Pre-Approval**: WhatsApp templates must be approved before use (24-48h review)
5. **Opt-In Compliance**: Always obtain consent before sending messages on any platform
6. **Error Retry**: Implement exponential backoff for rate limit errors (429 status)
7. **Message Deduplication**: Track message IDs to prevent duplicate sends
8. **Media Optimization**: Compress images/videos before sending; use thumbnails for large files
9. **Webhook Security**: Verify webhook signatures (WhatsApp: X-Hub-Signature-256, Discord: signature verification)
10. **Session Management**: Track conversation state per user across platforms

## Error Handling

### WhatsApp Error Codes
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
- **429**: Rate limited → Use X-RateLimit-Reset-After header

## Metrics & KPIs

### Communication KPIs
- **Response Time**: Average time to first response (target: <2 min)
- **Resolution Rate**: % of inquiries resolved in first contact (target: >80%)
- **Message Volume**: Messages sent/received per day/week/month
- **Engagement Rate**: % of messages read/replied (WhatsApp: read receipts)
- **Conversion Rate**: % of conversations leading to CRM deal creation
- **Channel Distribution**: Message volume by platform (WhatsApp/Telegram/Discord)
- **Template Performance**: Open rate and response rate per WhatsApp template
- **Bot Accuracy**: % of correctly handled inquiries without human escalation
- **Uptime**: Service availability (target: 99.9%)
- **Error Rate**: % of API calls resulting in errors (target: <0.1%)

---

*Generated by JARVIS AI Automation Platform v5.0.0 — Zero Technical Debt*
