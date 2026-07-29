# Análisis y Diseño — Tabla de Contenidos (TOC)

Propósito: este TOC organiza la fase de análisis y diseño para la plataforma (Nyx, Rhea, Kaia, Elara, Zoe, Janus). Cada sección incluye una breve descripción, entregables y criterios de aceptación (DoD).

1. Executive Summary
   - Descripción: Resumen final de objetivos, alcance, priorización y decisiones clave.
   - Entregables: 1 página de resumen ejecutivo.
   - Criterio de aceptación: Aprobación ejecutiva.

2. Alcance y Requisitos Funcionales
   - Descripción: Lista priorizada de funcionalidades (MVP y post-MVP) por módulo.
   - Entregables: Documento de requisitos (MVP scope), tabla de priorización (MoSCoW).
   - DoD: Cada requisito tiene owner, prioridad y criterio de validación.

3. Requisitos No-Funcionales
   - Descripción: SLA, rendimiento, seguridad, privacidad, cumplimiento (GDPR, local), escalabilidad.
   - Entregables: NFR matrix, SLOs y restricciones.
   - DoD: Valores numéricos definidos (p99, RTO, RPO, etc.).

4. Arquitectura Lógica y Componentes
   - Descripción: Diagrama y explicación de cada componente (Nyx, Rhea, Kaia, Elara, Zoe, Janus, MCP).
   - Entregables: Diagramas (C4/mermaid), lista de responsabilidades por componente.
   - DoD: Diagrama revisado y aprobado.

5. Flujos y Casos de Uso Detallados
   - Descripción: Flujos paso a paso para casos de uso principales (Lead Qualification, Appointment Booking, Document RAG, Domótica).
   - Entregables: Use-case docs con diagramas y n8n pseudo-flows.
   - DoD: Flujos claros, entradas/salidas y pruebas manuales definidas.

6. Diseño de Integraciones y APIs
   - Descripción: Contratos API, esquemas JSON, autenticación, rate limits.
   - Entregables: OpenAPI specs para Nyx APIs, event definitions para Rhea.
   - DoD: OpenAPI lint/validation sin errores.

7. Model Strategy y RAG
   - Descripción: Selección de modelos, estrategia de embeddings, vector DB y patrón RAG.
   - Entregables: Modelo hipotético por caso de uso, métricas de calidad, fallback strategy.
   - DoD: Propuesta con trade-offs y plan de pruebas.

8. Orquestación y Agent Patterns
   - Descripción: Diseño de agentes (autonomía, permisos, sandboxing), workflow engine decisions (n8n vs Flowise), agent safety.
   - Entregables: Patterns, safe-execution playbooks, action whitelist.
   - DoD: Playbooks definidos y revisados.

9. Infraestructura y DevOps
   - Descripción: Infra mínima para MVP (docker-compose) y producción (K8s), CI/CD, observability.
   - Entregables: docker-compose.yml, Helm charts, GitHub Actions templates.
   - DoD: Manifiestos que permiten deploy reproducible en staging.

10. Seguridad, Gobernanza y Auditoría
    - Descripción: Secret management, data flow policies, audit logs, model governance.
    - Entregables: Policy docs, retention rules, compliance checklist.
    - DoD: Lista de requisitos regulatorios con responsables.

11. Costeo y TCO
    - Descripción: Estimación detallada de costes por componente (OSS vs managed), cálculos TCO a 12 y 36 meses.
    - Entregables: Spreadsheet / tabla con supuestos, costes infra, licencias, horas de trabajo.
    - DoD: Estimaciones con supuestos claros y sensibilidad +/-20%.

12. Roadmap de Desarrollo
    - Descripción: Fases, milestones, hitos y criterios de salida.
    - Entregables: Roadmap Gantt / timeline, owners, backlog inicial.
    - DoD: Fechas y responsables asignados.

13. Operaciones y Runbooks
    - Descripción: Runbooks para despliegue, recovery, escalado y respuesta a incidentes.
    - Entregables: Runbooks y playbooks.
    - DoD: Pruebas de runbook completadas en staging.

14. Plantillas Legales y Comerciales
    - Descripción: SOW, MSA, tarifas, modelos de licenciamiento.
    - Entregables: SOW-MVP-template.md, MSA-template.md, pricing model.
    - DoD: Plantillas listas para revisión legal.

15. Bibliografía y Referencias
    - Descripción: Lista completa de referencias usadas (IBM, vendor docs, papers, OSS docs).
    - Entregables: bibliography.md con enlaces citables.
    - DoD: Todas las referencias citadas y verificables.


Proceso propuesto para esta fase
- Workshop 1: Requisitos y Prioridades (stakeholders)
- Workshop 2: Seguridad y Cumplimiento
- Workshop 3: Arquitectura y APIs
- Workshop 4: Roadmap & Costing

Aceptación final de la fase
- Documento consolidado aprobado por stakeholders, con backlog y owners asignados.

