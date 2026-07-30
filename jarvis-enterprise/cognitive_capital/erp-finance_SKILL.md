# ERP & Finance

> **Tier**: Enterprise | **Category**: ERP & Finance
> **Progressive Disclosure**: Overview → Details → Examples → Best Practices

## Overview

General ledger, accounts payable/receivable, inventory management, HR operations, and financial reporting (ERPNext)

## Details

### Core Capabilities

This skill provides structured methodology for erp & finance operations across the JARVIS platform. When activated, the agent gains deep understanding of domain-specific workflows, best practices, and integration patterns.

### Integration Points

- **MCP Servers**: Connected via ai_tool connections to relevant MCP servers
- **Memory**: Utilizes tier-appropriate memory for context retention
- **Patterns**: Best served by P2 (Routing) for multi-domain, P3 (Orchestrator) for complex tasks

### Activation Triggers

The agent should activate this skill when:
1. User requests involve erp & finance operations
2. Multi-platform integration is needed
3. Domain-specific expertise is required beyond general knowledge

## Examples

### Example 1: Multi-Platform Query

```
User: "Show me all products that are low on stock across WooCommerce and Shopify"
Agent: [Activates erp-finance skill]
→ Queries WooCommerce MCP (List Products, filter stock < 10)
→ Queries Shopify MCP (List Products, filter inventory < 10)
→ Consolidates results with cross-platform comparison
```

### Example 2: Automated Workflow

```
User: "When a new order comes in, update inventory and send a Slack notification"
Agent: [Activates erp-finance skill]
→ Monitors order events via MCP
→ Updates inventory via respective platform MCP
→ Sends Slack notification via MCP
```

## Best Practices

1. **Always validate API responses** before processing
2. **Use idempotent operations** for critical writes
3. **Implement retry logic** for rate-limited APIs
4. **Log all operations** for audit trails (Enterprise tier)
5. **Cache frequently accessed data** to reduce API calls
6. **Use batch operations** when available for efficiency

## Error Handling

- **Rate limits**: Implement exponential backoff
- **Auth failures**: Refresh tokens automatically
- **Data conflicts**: Use ETags/If-Match headers
- **Partial failures**: Implement compensating transactions

---

*Part of JARVIS Cognitive Capital — Progressive Disclosure Skill System*
