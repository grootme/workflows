# JARVIS Family - Definitions and Roles

Este documento centraliza las definiciones originales y las versiones revisadas de los agentes/personalidades: Kaia, Elara, Zoe, Rhea y Nyx.

Propósito: mantener consistencia terminológica y describir claramente el rol de cada componente dentro del ecosistema.

## Decisión Ejecutiva (unificación)
- Nyx: Motor de IA central (backend), responsable del procesamiento, modelos y aprendizaje. No es una interfaz directa con clientes.
- Kaia: Interfaz personal / Asistente conversacional B2C (voz y texto). Amigable y orientada al usuario final.
- Elara: Interfaz profesional / Asistente B2B (analítica, reportes, procesos). Orientada a decisiones empresariales.
- Zoe: Módulo creativo y generativo (imágenes, textos, branding, audio).
- Rhea: Motor de automatización y orquestación (flujos de trabajo, integraciones, n8n patterns).

> Nota: Janus se definirá en `../04-janus/index.md` como el meta-asistente que orquesta y supervisa estos módulos.

## Coherencia y Convenciones

Este documento sigue las definiciones del `../02-architecture/glossary.md` y las reglas de nombrado en `../02-architecture/naming-conventions.md`.
Usa los prefijos y convenciones allí descritos para nombres de workflows, servicios y credenciales.

## Instrucciones de Uso
- Cuando se hable de "motor" o "core" se debe referir a Nyx.
- Los nombres Kaia/Elara son los front-end conversacionales; Zoe/Rhea son módulos funcionales.
- Evitar usar "JARVIS" como nombre público. Usarlo solo como referencia conceptual en marketing si es necesario.

## Próximos pasos
- Detallar APIs y contratos de cada módulo (entrada/salida, formatos JSON, auth).
- Crear ejemplos de prompts y flujos n8n para cada uno.