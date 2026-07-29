# Agente de IA: Ally

## 1. Rol Principal
**Interfaz Humana y Coach Proactivo**

Ally es la cara visible y conversacional del ecosistema. Es el "JARVIS" con el que el usuario interactúa directamente. Su función principal es servir de puente entre la intención humana y las capacidades técnicas del sistema, presentando la información de una manera intuitiva, contextual y proactiva.

## 2. Funciones Clave

*   **Traducción de Intención**: Interpreta las solicitudes del usuario en lenguaje natural y las traduce en comandos ejecutables para Nyx y Rhea.
*   **Interfaz de Usuario Contextual (HUD)**: Manifiesta la información a través de un "Heads-Up Display" que se adapta al contexto del usuario, mostrando datos relevantes sin ser intrusivo.
*   **Presentación de Resultados**: Sintetiza los análisis complejos de Nyx y los resultados de las acciones de Rhea en respuestas claras, concisas y visualmente atractivas.
*   **Coaching Personal (Modo Kaia)**: Monitoriza el bienestar, la productividad y los patrones de comportamiento del usuario para ofrecer recomendaciones que prevengan el burnout y mejoren el rendimiento.
*   **Gestión de Notificaciones**: Filtra y prioriza las alertas del sistema para asegurar que el usuario solo reciba la información crítica en el momento adecuado.

## 3. Componentes Tecnológicos

*   **Frontend**: La interfaz visual del HUD se construye con **Tauri** (para aplicaciones de escritorio ligeras y seguras) y un framework web moderno como **React** o **SvelteKit**.
*   **SDK de IA Conversacional**: Se utiliza el **Vercel AI SDK** o herramientas similares para gestionar el streaming de respuestas y el estado de la conversación.
*   **Conectividad**: Se comunica con Nyx y Rhea a través de un **API Gateway** interno, asegurando una comunicación fluida y segura.

## 4. Flujo de Interacción Típico

1.  **Recepción**: Ally recibe un comando del usuario (ej: "Ally, analiza las ventas de este trimestre").
2.  **Delegación a Nyx**: Ally envía la solicitud a Nyx para que realice el análisis de datos.
3.  **Recepción de Análisis**: Nyx devuelve un análisis estructurado (datos, conclusiones, gráficos).
4.  **Delegación a Rhea (Opcional)**: Si se requiere una acción (ej: "envía el informe por email"), Ally ordena a Rhea que ejecute el workflow correspondiente.
5.  **Síntesis y Presentación**: Ally toma la información de Nyx y el estado de Rhea para componer una respuesta final y la presenta al usuario a través del HUD.
