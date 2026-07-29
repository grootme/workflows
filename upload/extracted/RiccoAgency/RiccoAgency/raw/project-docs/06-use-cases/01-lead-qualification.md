# Lead Qualification Pipeline (MVP)

Resumen
-------
Un pipeline para recibir leads desde formularios y canales (webhooks, email, Facebook/WhatsApp), enriquecerlos (enriquecimiento por API), clasificarlos (score), y posteriormente asignarlos a comerciales o sistemas CRM.

Actores y Agentes
-----------------
- Nyx (core): orquesta y persistencia de estado.
- Rhea (automation): workflows n8n responsables de la lógica y llamadas externas.
- Elara (B2B): interfaz para equipos comerciales (dashboards).
- Kaia (B2C): si hay interacción con clientes finales para confirmación y follow-ups.

Problema de negocio
--------------------
Equipos de ventas reciben leads inconsistentes y mal priorizados. Este pipeline automatiza clasificación y enruta leads para aumentar la conversión.

MVP Scope (SOW)
----------------
- Ingesta de leads vía webhook n8n (desde forms y Zapier-like).
- Enriquecimiento usando Clearbit/FullContact (opcional).
- Scoring por reglas simples (empresa, cargo, tamaño, keywords).
- Persistencia en PostgreSQL y Vector DB (para semántica futura).
- Notificación/Asignación: enviar a Slack + crear lead en CRM (HubSpot/Zoho) según reglas.

Arquitectura Técnica
--------------------
- Entradas: Webhook, Email parser, Facebook/WhatsApp adapters.
- Procesamiento: n8n workflow que valida, enriquece y scorea.
- Almacenamiento: PostgreSQL (leads table), Redis (short cache), Qdrant/Chroma (embeddings).
- Integraciones: HubSpot API, Slack, Clearbit.

Flujo n8n - Paso a Paso
----------------------
1. Webhook Trigger (HTTP Request node)
2. Function/Set node: normalize payload (name, email, phone, source)
3. HTTP request to Enrichment API (Clearbit) -> merge
4. Scoring Function: apply rules and compute score
5. Conditional node: if score > 70 -> High Priority, else Normal
6. Create/Update Lead in PostgreSQL (Postgres node)
7. Create in CRM via HTTP Request (HubSpot)
8. Send notification to Slack (Webhook)
9. If low score: store vector embedding and add to nurture queue (Redis)

Data Contracts
--------------
Lead object (normalized):
- id: uuid
- name: string
- email: string
- phone: string
- company: string
- title: string
- source: string
- enrichment: object
- score: integer
- created_at: timestamp

Requisitos
----------
- n8n instance with Webhook nodes enabled.
- Postgres DB and credentials.
- Clearbit API key (optional).
- HubSpot API key / OAuth app.
- Slack incoming webhook.

Métricas de Éxito
-----------------
- Time to lead assignment < 2 minutes
- Conversion rate uplift after automation +10%
- Reduction in manual triage load by 60%

Siguientes pasos
----------------
- Producir n8n JSON exportable para este workflow.
- Crear tabla SQL para leads y migración.
- Implementar pruebas end-to-end en staging.

