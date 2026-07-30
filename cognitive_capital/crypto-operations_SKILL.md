# Crypto Operations

> **Tier**: Enterprise | **Category**: Crypto Operations
> **Progressive Disclosure**: Overview -> Details -> Examples -> Best Practices

## Overview

Cryptocurrency exchange operations: spot/futures trading, P2P, market analysis, wallet management across Binance, CoinEx, and Bitrefill.

## Details

### Core Capabilities

This skill provides structured methodology for crypto operations operations across the JARVIS platform. When activated, the agent gains deep understanding of domain-specific workflows, best practices, and integration patterns.

### Integration Points

- **MCP Servers**: Connected via ai_tool connections to relevant MCP servers
- **Memory**: Utilizes tier-appropriate memory for context retention
- **Patterns**: Best served by P2 (Routing) for multi-provider, P3 (Orchestrator) for complex operations

### Activation Triggers

The agent should activate this skill when:
1. User requests involve crypto operations operations
2. Multi-platform integration is needed
3. Domain-specific expertise is required beyond general knowledge

## Examples

### Example 1: Multi-Platform Payment Routing

```
User: "Process a $500 payment from a customer in Cuba"
Agent: [Activates crypto-operations skill]
-> Routes to TropiPay (Caribbean specialist)
-> Creates payment link with USD/CUP conversion
-> Tracks transaction status
-> Logs in CRM activity
```

### Example 2: Crypto Payment Conversion

```
User: "Convert 0.5 BTC to USDT and send via Stripe"
Agent: [Activates crypto-operations skill]
-> Checks Binance BTC/USDT rate
-> Places sell order on Binance
-> Withdraws USDT to bank
-> Creates Stripe payment for customer
```

## Best Practices

1. **Always validate API responses** before processing
2. **Use idempotent operations** for payment writes
3. **Implement retry logic** for rate-limited APIs
4. **Log all operations** for audit trails (Enterprise tier)
5. **Cache frequently accessed data** to reduce API calls
6. **Use batch operations** when available for efficiency
7. **Never store sensitive payment data** — use tokenization
8. **Implement 2FA for high-value operations**

## Error Handling

- **Rate limits**: Implement exponential backoff
- **Auth failures**: Refresh tokens automatically
- **Payment failures**: Implement retry with alternative provider
- **Insufficient funds**: Suggest alternative payment methods
- **Network timeouts**: Queue and retry with deduplication

## Security

- **PCI DSS compliance**: Never log full card numbers
- **API key rotation**: Rotate keys every 90 days
- **Webhook verification**: Validate all webhook signatures
- **IP whitelisting**: Restrict API access by IP where possible
- **Encryption**: Use TLS 1.3 for all API communications

---

*Part of JARVIS Cognitive Capital — Progressive Disclosure Skill System*
