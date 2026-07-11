# Plan técnico — Base del monorepo e infraestructura mínima

## Propósito de implementación

Dejar el repositorio maquetado, documentado y ejecutable localmente con configuración segura.

## Prioridad

**P0**. La feature se considera bloqueante para el MVP.

## Decisiones de diseño

- Se mantiene la separación por capas: controladores, servicios, repositorios, modelos y DTO/serializadores.
- Se evita lógica de negocio en la vista o en rutas.
- Se documentan contratos antes de implementar.
- Se aplican permisos por defecto restrictivos.
- Se escriben pruebas de contrato y permisos antes de cerrar la tarea.

## Tecnologías seleccionadas

Django 5.x ASGI, DRF, PostgreSQL 16, Redis 7, tileserver-gl 4.x, Docker Compose, Uvicorn.

## Componentes impactados

- `/.gitignore`
- `/.env.example`
- `/docker/docker-compose.yml`
- `/backend`
- `/docs/dev-setup.md`

## Contratos

- `GET /api/health/` — Verifica que backend, base de datos y caché respondan.

Los contratos detallados están en `contracts/openapi.yaml`.

## UI y navegación

Pantalla técnica simple de estado para validar entorno durante desarrollo.

Prototipos disponibles en:

- `docs/prototypes/estado-de-entorno-base/code.html`
- `docs/prototypes/estado-de-entorno-base/screen.png`

## Flujo entre agentes

1. **Agente de especificación:** valida historias, requisitos y escenarios.
2. **Agente de arquitectura:** revisa este plan y confirma decisiones.
3. **Agente ejecutor:** toma una tarea atómica.
4. **Agente de pruebas:** valida contrato, permisos y escenarios.
5. **Agente revisor:** verifica constitución, `SKILL.md` y checklist.

## Tareas atómicas

- [ ] Crear árbol base del monorepo.
- [ ] Crear `.gitignore` con `.env`, `__pycache__`, `node_modules`, builds y archivos locales.
- [ ] Crear `.env.example` comentado con SECRET_KEY, DB_*, R2_*, CLOUDFLARE_TUNNEL_TOKEN y variables de desarrollo.
- [ ] Crear `docker/docker-compose.yml` con backend, db, redis y tileserver.
- [ ] Crear Dockerfile backend con comando Uvicorn ASGI.
- [ ] Crear endpoint de healthcheck.
- [ ] Documentar comandos de arranque en `docs/dev-setup.md`.

## Criterios de aceptación para agentes

- [ ] La tarea se limita al alcance de esta feature.
- [ ] Los contratos se respetan sin rutas hardcodeadas fuera de configuración.
- [ ] Los mensajes de error están en español.
- [ ] Los permisos impiden acceso cruzado.
- [ ] Las pruebas relevantes pasan.
- [ ] La documentación afectada queda actualizada.
- [ ] No se agregan secretos reales.

## Estrategia de verificación

- Pruebas unitarias para validaciones de datos.
- Pruebas de integración para endpoints.
- Pruebas de permisos por rol/propietario.
- Prueba manual guiada usando el prototipo.
- Revisión de checklist de requisitos.


## Riesgos y mitigaciones

- Desalineación entre nombres de carpetas actuales y estructura objetivo.
- Variables incompletas que impidan levantar el entorno.
- Versiones flotantes de imágenes Docker.

## Entregable mínimo

Un PR lógico o paquete de cambios que implemente una sola tarea atómica, incluya prueba o evidencia de verificación y no rompa contratos existentes.
