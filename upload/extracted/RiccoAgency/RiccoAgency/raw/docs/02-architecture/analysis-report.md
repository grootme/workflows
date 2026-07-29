# Análisis y Priorización — Informe

Estado: Borrador inicial (fase de análisis en progreso)

Objetivo
--------
Realizar un análisis exhaustivo de requisitos, gaps, riesgos y coste (TCO) para priorizar el backlog y definir el alcance del MVP y los siguientes lanzamientos.

1. Alcance actual
- Basado en discusiones: Priorizar Lead Qualification y Appointment Booking; incluir Document Ingestion (RAG) y Marketing assets (Zoe) como segundo bloque.

2. Gap Analysis (alta prioridad)
- Infra para LLM local: GPU/servicios y pipelines de inferencia.
- Integraciones: con CRMs (HubSpot/Salesforce) con nodos estandar en n8n.
- Observabilidad: falta configuración reproducible para Prometheus/Grafana.
- Seguridad: secret management (Vault) no desplegado.

3. Backlog priorizado (MoSCoW)
- Must:
  - Ingesta de leads y scoring automático (Lead Qualification).
  - Infra mínima: Postgres, Redis, Qdrant, n8n, modelo LLM local (quantized runtime).
  - Seguridad básica: secret store y roles en n8n.
- Should:
  - Appointment booking workflow con calendar/confirmation.
  - Document ingestion pipeline con embeddings.
- Could:
  - Flowise integration for LLM chaining experiments.
  - Zoe creative agent MVP.
- Won't this release:
  - Multi-tenant support.

4. Riesgo / Mitigación (matriz)
- Coste inferencia (alto): Mitigación: quantized models, caching, fallback local.
- Data leakage (alto): Mitigación: PII filters, DLP rules, no-send policy.
- Operational complexity (medium): Mitigación: start with docker-compose → Helm.

5. Supuestos TCO (Borrador)
- Infra base: 2 x VM (4vCPU, 16GB) + 1 x GPU (8GB) ≈ USD 300–600/m
- Managed services opcionales: Pinecone ≈ USD 200–1000/m según uso; OpenAI variable.
- Ingeniería: 1 FTE por 3 meses ≈ salario local (estimado por usuario).

6. Priorización primera ola (entregables)
- 1: Lead Qualification (workflow + storage + notifications)
- 2: Appointment Booking
- 3: Document ingestion (RAG) basic

7. Artefactos a producir
- `prioritized-backlog.md` (detallado por historias)
- `tco-spreadsheet.xlsx` (supuestos y sensibilidad)
- `risk-register.md`


