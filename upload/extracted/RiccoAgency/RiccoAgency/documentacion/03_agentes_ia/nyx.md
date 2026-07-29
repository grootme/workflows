# Agente de IA: Nyx

## 1. Rol Principal
**El Cerebro Analítico y Estratégico**

Nyx es el motor de inteligencia central del ecosistema. Opera en segundo plano, procesando grandes volúmenes de información para realizar análisis complejos, generar insights y actuar como un sistema de alerta temprana. No interactúa directamente con el usuario, sino que provee la inteligencia que Ally presenta.

## 2. Funciones Clave

*   **Procesamiento de Lenguaje Natural (PLN)**: Analiza y comprende el lenguaje de las solicitudes del usuario, documentos, emails y fuentes de datos externas.
*   **Análisis Predictivo**: Utiliza modelos de machine learning para predecir resultados, como la probabilidad de fallo de una máquina o el riesgo de churn de un cliente.
*   **Retrieval-Augmented Generation (RAG)**: Enriquece las respuestas de los LLMs con información específica de la base de conocimiento vectorial, garantizando respuestas precisas y contextualizadas.
*   **Inteligencia de Mercado**: Monitoriza de forma autónoma a la competencia, las tendencias tecnológicas y las oportunidades de mercado, actuando como un centinela estratégico.
*   **Lógica Compleja**: Resuelve problemas que requieren razonamiento en múltiples pasos, descomponiendo tareas complejas en sub-tareas ejecutables.

## 3. Componentes Tecnológicos

*   **Orquestación de IA**: Se utiliza **LangChain** o **LlamaIndex** para construir las cadenas de lógica que conectan los modelos de lenguaje, las bases de datos y las herramientas.
*   **Modelos de Lenguaje (LLMs)**: Accede a un router de modelos que puede utilizar APIs de **OpenAI (GPT-4o)**, **Anthropic (Claude 3)** o modelos de código abierto según la tarea.
*   **Base de Datos Vectorial**: Utiliza **Qdrant** en producción para el almacenamiento y la búsqueda semántica de información no estructurada.
*   **Agentes Web**: Despliega agentes autónomos para escanear fuentes de información en la web.

## 4. Flujo de Interacción Típico

1.  **Recepción de Tarea**: Nyx recibe una solicitud de análisis de Ally (ej: "Analiza el impacto de la nueva API de Google en nuestro producto").
2.  **Recopilación de Datos**: Nyx utiliza sus agentes web para recopilar la documentación de la nueva API y artículos de análisis del mercado.
3.  **Análisis Interno**: Cruza la información externa con los datos internos del producto almacenados en su base de conocimiento.
4.  **Generación de Insights**: Utiliza un LLM para sintetizar la información y generar un informe estructurado con: Resumen, Análisis de Impacto, Riesgos y Oportunidades.
5.  **Envío a Ally**: Nyx envía el informe estructurado a Ally para que esta lo presente al usuario de forma comprensible.
