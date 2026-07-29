Lead Qualification - Import & Quick Test

Pasos rápidos para importar y validar el workflow en n8n (local o cloud):

1) Importar el workflow
- En n8n: Workflows -> Import -> subir `lead-qualification.json`.
- Verifica que las credenciales referenciadas existan: `nyx-db` (Postgres), `clearbit_api`, `hubspot-oauth`, `slack-webhook`.

2) Crear tabla SQL (ejemplo)

```sql
CREATE TABLE public.leads (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text,
  email text,
  phone text,
  company text,
  title text,
  source text,
  score integer,
  created_at timestamptz DEFAULT now()
);
```

3) Probar el webhook
- Local n8n: exponer webhook con ngrok y enviar POST a `https://<ngrok>/webhook/webhook-lead` con JSON de prueba.
- Ejemplo payload:

```json
{
  "name": "Ana Perez",
  "email": "ana.perez@example.com",
  "phone": "+34123456789",
  "company": "Acme S.A.",
  "title": "Sales Manager",
  "source": "landing_page"
}
```

4) Ver resultados
- Ver en la ejecución del workflow en n8n: que los nodos se ejecuten sin errores.
- Validar que la fila se insertó en Postgres.
- Revisar notificación Slack / lead creado en HubSpot.

Notas
- Reemplaza los placeholders de credenciales por las credenciales reales en n8n. Sigue las convenciones de `project-docs/02-architecture/naming-conventions.md`.
- Si usas n8n.cloud, crea las credenciales usando su UI; si es self-hosted, añade las credenciales en `~/.n8n` o en la UI de n8n.
