# Glosario de Términos

Este glosario define los términos y roles usados en el proyecto para evitar ambigüedades.

- Nyx: Núcleo de backend y orquestación. Gestiona estado, colas, persistencia, trazabilidad y reglas centrales. Responsable de las integraciones con la base de datos, vector store y servicios de identidad.
- Rhea: Módulo de automatización y orquestación de flujos; implementado principalmente con n8n y custom nodes. Rhea es responsable de ejecutar flujos, reconectar errores y auditar ejecuciones.
- Kaia: Interfaz y asistentes orientados al usuario final (B2C). Maneja conversaciones directas, notificaciones al usuario, y UX personalizadas.
- Elara: Interfaz y servicios orientados a clientes empresariales (B2B). Dashboards, gestión de equipos comerciales, roles y permisos empresariales.
- Zoe: Módulo creativo y de generación de contenido (marketing, multimedia). Responsable de prompts, assets generation, A/B testing de creativos.
- Janus: Meta-asistente y monitor. Supervisa riesgos, competidores, métricas empresariales y el estado personal del founder. Orquesta acciones proactivas y recomienda contramedidas.
- MCP (Model Context Protocol): Gateway y contract registry para exponer modelos, herramientas y acciones a través de un contrato estándar. Incluye autenticación, tool registry y ejecución segura.
- RAG: Retrieval-Augmented Generation. Técnica para combinar recuperación de vectores y LLM para respuesta basada en contexto.
- Vector DB: Base de datos para almacenar embeddings (Qdrant/Chroma). Usada por Nyx para memoria semántica y búsqueda.
- Agent: Componente software con capacidades autónomas o semi-autónomas (p. ej. JARVIS instances: Kaia, Elara) que realiza tareas en nombre del usuario o empresa.

