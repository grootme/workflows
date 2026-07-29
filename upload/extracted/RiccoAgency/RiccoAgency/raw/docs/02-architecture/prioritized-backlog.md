# Prioritized Backlog — Primera Ola (Lead Qualification, Appointment Booking, Document RAG)

Estado: Primera versión (borrador para revisión en workshop)

Resumen
-------
Este backlog prioriza funcionalidades para la primera ola (MVP) siguiendo MoSCoW. Cada historia incluye: descripción, prioridad, criterios de aceptación (DoD), dependencias, esfuerzo estimado (T-shirt) y pruebas propuestas.

Convenciones
- Priority: Must / Should / Could / Won't
- Estimación: S (1-2d), M (3-7d), L (2-4w)
- Owner: rol responsable (PM/Eng/DevOps)

1) Lead Qualification — Ingesta y Scoring (Must)
- ID: LQ-001
- Descripción: Recibir leads desde webhook/forms, normalizar, enriquecer (Clearbit opcional), calcular score, persistir en Postgres, notificar equipo (Slack) y crear contacto en CRM (HubSpot).
- Owner: Eng (Backend) + Rhea (n8n)
- Dependencias: Postgres provisionado, n8n running, credentials for HubSpot/Slack, model/enrichment keys (Clearbit optional).
- Estimación: M
- Criterios de aceptación (DoD):
  - Se puede enviar un POST al webhook y observar ejecución completa en n8n sin errores.
  - Lead insertado en tabla `leads` con campos obligatorios (name,email,score,created_at).
  - Notificación enviada a Slack y contacto creado en HubSpot (si credenciales configuradas).
  - Score calculado por reglas (email presence, company, seniority) y valor numérico entre 0-100.
  - Tests: 3 payloads de ejemplo (alta prioridad, media, baja) con verificación automatizada.

2) Appointment Booking — Reserva y Confirmación (Must)
- ID: AB-001
- Descripción: Workflow para gestionar reservas: recibir solicitud (webhook/form), validar disponibilidad contra calendario (Google Calendar / Office 365), reservar slot, enviar confirmación cliente (email/SMS) y recordatorios.
- Owner: Eng + Rhea (n8n)
- Dependencias: Calendar API credentials, SMTP or Twilio, Postgres (reservas).
- Estimación: M
- Criterios de aceptación:
  - Reserva creada y persistida en `appointments` con estado `confirmed`.
  - Cliente recibe confirmación por email/SMS dentro de 1 minuto.
  - Double-booking prevented: system rejects overlapping confirmed slots.
  - Tests: Simulación de reservas concurrentes (2 requests same slot) para validar locking.

3) Document Ingestion & RAG — Ingest, Embed, Query (Must)
- ID: RAG-001
- Descripción: Pipeline para ingestión de documentos (pdf, docx, txt), extracción de texto, generación de embeddings, almacenamiento en Vector DB (Qdrant), y endpoint/query para respuestas RAG.
- Owner: Eng (Backend) + Data Eng
- Dependencias: Qdrant instance, sentence-transformers model, OCR library (tesseract optional), storage (S3-compatible)
- Estimación: L
- Criterios de aceptación:
  - Document uploaded and parsed; text available in storage.
  - Embeddings generated and inserted into Qdrant index.
  - Query endpoint returns top-K relevant chunks and LLM prompt returns coherent answers in at least 70% of test queries (manual evaluation set).
  - Tests: dataset of 20 documents and 30 queries with ground-truth relevance checks.

4) Basic Nyx Core APIs — Auth, Lead API, Appointment API (Must)
- ID: NYX-API-001
- Descripción: Exponer APIs REST para leads and appointments with OAuth2 protected endpoints, and health endpoints.
- Owner: Eng
- Dependencias: Auth provider (OAuth2), Postgres
- Estimación: M
- DoD:
  - Endpoints documented in OpenAPI, linted and versioned (/api/v1/).
  - Auth enforced; unauthorized requests receive 401.
  - Health check returns service status.

5) Rhea Workflow Observability & Retries (Should)
- ID: RHEA-OBS-001
- Descripción: Instrumentar n8n workflows to emit traces/metrics, retry strategy for failed tasks, and dead-letter queue for persistent failures.
- Owner: DevOps
- Dependencias: Prometheus + Grafana, Redis for queues
- Estimación: M
- DoD: Retries implemented; failures visible in dashboard and DLQ entries accessible.

6) Embeddings Quality & Fallback Strategy (Should)
- ID: EMB-001
- Descripción: Integrate sentence-transformers for baseline embeddings and implement fallback to managed embeddings (OpenAI) when quality threshold OK.
- Owner: ML Eng
- Estimación: M
- DoD: Baseline evaluation report with metrics (precision@k, MRR) comparing local vs managed embeddings.

7) Zoe Creative Agent — Simple Campaign Generator (Could)
- ID: ZOE-001
- Descripción: Generate marketing copy and images for a campaign using local LLM + image model (optional managed).
- Owner: Product/Marketing
- Estimación: L
- DoD: Generate 5 variations for a brief, include A/B test plan.

8) Flowise Experiments (Could)
- ID: FLOW-001
- Descripción: Spin up Flowise for 2-3 LLM chaining experiments and compare with LangChain implementations.
- Owner: ML Eng
- Estimación: S
- DoD: Experiment report and sample flows saved.

9) Hardening & Security (Future - won't this release)
- ID: SEC-001
- Descripción: Full pentest, IDS/IPS integration and formal privacy impact assessment (PIA).
- Priority: Won't for first release (plan in phase 3-4)

Appendix: Test Cases (examples)
- Lead Qualification
  - Test A (High priority): payload with company, email, senior title -> expect score >= 80, HubSpot contact created, Slack notified.
  - Test B (Low priority): payload with only phone -> expect score < 30, saved to nurture queue.
- Appointment Booking
  - Test A: Book available slot -> confirmed
  - Test B: Two concurrent bookings -> one confirmed, one rejected with error
- Document RAG
  - Evaluation dataset: 20 documents, 30 queries; target precision@5 >= 0.6

Deliverables for each story
- n8n workflow JSON (where applicable)
- DB schema migrations (SQL)
- API OpenAPI spec (for Nyx endpoints)
- Test scripts (Postman/newman or pytest)

