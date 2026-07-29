# Naming Conventions y Convenciones de Roles

Objetivo: Establecer reglas claras para nombrar carpetas, agentes, endpoints y recursos para mantener coherencia.

1. Agentes y Módulos
- Prefijo por dominio: `nyx-` para servicios core, `rhea-` para flujos, `kaia-` para B2C, `elara-` para B2B, `zoe-` para marketing, `janus-` para meta-asistente.
- Ejemplos: `rhea-workflow-lead-qual`, `nyx-service-auth`, `kaia-ui-chat`.

2. Repositorios y carpetas
- Archivo raíz: use `project-docs/` para documentación y `services/` para código.
- Use kebab-case para carpetas y archivos (minúsculas, guiones). Ej: `project-docs/11-n8n-workflows/lead-qualification.json`.

3. APIs y endpoints
- Use versión semántica en la ruta: `/api/v1/nyx/auth`, `/api/v1/rhea/workflow-trigger`.

4. Credentials y secrets
- Referenciados por nombre coherente: `cred/nyx-db`, `cred/hubspot-oauth`, `cred/clearbit-key`.

5. n8n nodes y workflows
- Nombre del workflow: `rhea-<usecase>-v1`.
- Identificadores internos: node names should be human readable and short: `webhook_lead`, `normalize`, `clearbit_enrich`, `score`.

6. Database objects
- Tables: plural, snake_case: `leads`, `users`, `agent_sessions`.
- Indexes: `idx_<table>_<column>`.

7. Documentation
- Title-case for top-level docs: `project-docs/02-architecture/README.md`.
- Use front-matter with `title`, `tags`, and `last_updated` for important pages.

8. Semantic Versioning for Agents
- Agents should include a version in their deployment name: `kaia-v1.0.0`.

Regla de cambio: si se necesita renombrar, documentar el cambio en `project-docs/02-architecture/rename-log.md` y actualizar el `glossary.md`.

