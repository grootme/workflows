# Janus - Meta-Assistant Overview

Janus es el "Co-fundador Digital" y meta-asistente que orquesta, supervisa y aconseja sobre el negocio. Integra los módulos Nyx, Kaia, Elara, Zoe y Rhea.

## Responsabilidades Principales
- Supervisión Operacional (Rhea): salud de proyectos, cumplimiento de los 5 pilares.
- Inteligencia de Mercado (Nyx): monitorización de competidores, novedades tecnológicas y análisis de impacto.
- Analítica Estratégica (Core Janus): cruzar datos internos y externos para recomendaciones.
- Coaching Personal (Kaia-Mode): journaling, estado emocional, prevención de burnout.

## Arquitectura de Alto Nivel
- Data Ingest: agentes web (news, blogs, tweets), webhooks (n8n), métricas internas (Notion/Trello/Asana), logs y métricas.
- Vector DB: Qdrant para embeddings de documentos y alertas.
- Orquestador: n8n + microservicios.
- LLMs: en la capa de Nyx y Janus (RAG patterns).

## Interacción
- Panel web: dashboard con alertas, recomendaciones y tareas.
- Notificaciones: Slack/Telegram/Email para alertas críticas.
- Conversación: interfaz Kaia/Elara para diálogo y coaching.

## Prioridades de Implementación
1. Nyx: monitor de mercado
2. Rhea: digitalizar procesos y KPIs
3. Janus core: reglas de decisión y RAG
4. Kaia: journaling y coaching
5. Zoe: integración creativa (opcional post-MVP)

## Riesgos y Mitigaciones
- Dependencia de fuentes: diversificar fuentes de Nyx.
- Privacidad: cifrado y control de accesos.
- Falsos positivos en alertas: calibrado y thresholds adaptativos.

> En archivos siguientes se detallarán APIs, prompts, flujos y esquemas de datos.