# Agente de IA: Rhea

## 1. Rol Principal
**La Orquestadora de Acciones y Flujos de Trabajo**

Rhea es el motor de automatización del ecosistema. Es la "capa de acción" que conecta la inteligencia de Nyx y las intenciones del usuario (traducidas por Ally) con el mundo digital y físico. Su función es ejecutar tareas de forma fiable, conectar sistemas y automatizar procesos de negocio.

## 2. Funciones Clave

*   **Ejecución de Workflows**: Opera como el motor principal para los flujos de trabajo de n8n, ejecutando secuencias de tareas predefinidas o dinámicas.
*   **Integración de APIs**: Se especializa en conectar con una amplia gama de APIs de terceros (CRMs, ERPs, plataformas de comunicación, etc.), gestionando la autenticación y el formateo de datos.
*   **Automatización de Tareas**: Realiza tareas repetitivas como enviar emails, actualizar bases de datos, generar informes o gestionar archivos.
*   **Gestión de Tareas Programadas**: Ejecuta trabajos en segundo plano basados en tiempo (Cron Jobs) o en eventos.
*   **Creación de Conectores**: Permite el desarrollo y la gestión de conectores personalizados para sistemas legacy o APIs privadas.

## 3. Componentes Tecnológicos

*   **Motor de Orquestación**: Utiliza una instancia auto-hospedada de **n8n (Enterprise Edition)** para garantizar la escalabilidad, seguridad y gestión de múltiples workflows.
*   **Conectores**: Aprovecha el ecosistema de nodos pre-construidos de n8n y permite el desarrollo de **nodos personalizados** en TypeScript/JavaScript para necesidades específicas.
*   **Colas de Mensajes (Opcional)**: Para cargas de trabajo muy altas, puede integrarse con **Redis Streams** o **RabbitMQ** para gestionar colas de tareas de forma asíncrona.

## 4. Flujo de Interacción Típico

1.  **Recepción de Orden**: Rhea recibe una orden de Ally (ej: "Crea un nuevo lead en el CRM con estos datos").
2.  **Selección de Workflow**: Identifica el workflow de n8n apropiado para la tarea ("Crear-Lead-HubSpot").
3.  **Ejecución**: Inicia el workflow, que sigue los siguientes pasos:
    a.  **Validar Datos**: Asegura que la información del lead esté completa.
    b.  **Autenticar con API**: Utiliza las credenciales almacenadas de HubSpot.
    c.  **Llamada a la API**: Envía la solicitud para crear el nuevo lead.
    d.  **Manejo de Respuesta**: Confirma que el lead se creó correctamente y obtiene su ID.
4.  **Reporte de Estado**: Rhea informa a Ally del resultado de la operación (ej: "Éxito: Lead #12345 creado en HubSpot").
5.  **Ally Presenta**: Ally notifica al usuario que la acción se ha completado.
