# MCP Server - Overview

## Qué es
MCP (Model Context Protocol) server es una capa estándar que expone herramientas y APIs como "habilidades" para agentes de IA. Permite que los modelos descubran y usen funciones de forma segura y consistente.

## Beneficios
- Abstrae integraciones con APIs legacy
- Control fino de permisos y scopes
- Auditoría y trazabilidad de llamadas
- Facilidad para exponer acciones complejas como "tools" al LLM

## Componentes
- Gateway HTTP (OAuth2/JWT)
- Registry de herramientas (descubrimiento)
- Executor Sandbox (ejecución segura)
- Auditoría y logs

## Ejemplo de Endpoint
POST /mcp/register-tool
{
  "name": "create_appointment",
  "description": "Create appointment in Clinic CRM",
  "schema": { /* input JSON schema */ }
}

## Próximos pasos
- Definir contrato API (OpenAPI)
- Implementar ejemplo de adapter para WooCommerce y Odoo
- Documentar procesos de seguridad y rate-limits