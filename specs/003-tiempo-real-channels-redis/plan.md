# Plan técnico — Disponibilidad en tiempo real con Channels y Redis

## Propósito de implementación

Garantizar push instantáneo de cambios de espacios por parqueadero.

## Prioridad

**P0**. La feature se considera bloqueante para el MVP.

## Decisiones de diseño

- Se mantiene la separación por capas: controladores, servicios, repositorios, modelos y DTO/serializadores.
- Se evita lógica de negocio en la vista o en rutas.
- Se documentan contratos antes de implementar.
- Se aplican permisos por defecto restrictivos.
- Se escriben pruebas de contrato y permisos antes de cerrar la tarea.

## Tecnologías seleccionadas

Django Channels, channels-redis, Redis, Uvicorn ASGI, WebSocket API del navegador.

## Componentes impactados

- `/backend/config/asgi.py`
- `/backend/config/routing.py`
- `/backend/apps/parqueaderos/consumers.py`
- `/frontend-web/src/hooks`

## Contratos

- `WS /ws/parqueaderos/{parqueadero_id}/` — Suscripción a eventos de disponibilidad.
- `PATCH /api/espacios/{id}/estado/` — Cambiar estado y emitir evento.

Los contratos detallados están en `contracts/openapi.yaml`.

## UI y navegación

Una pantalla de prueba muestra conexión, último evento y log de mensajes.

Prototipos disponibles en:

- `docs/prototypes/consola-de-eventos-websocket/code.html`
- `docs/prototypes/consola-de-eventos-websocket/screen.png`

## Flujo entre agentes

1. **Agente de especificación:** valida historias, requisitos y escenarios.
2. **Agente de arquitectura:** revisa este plan y confirma decisiones.
3. **Agente ejecutor:** toma una tarea atómica.
4. **Agente de pruebas:** valida contrato, permisos y escenarios.
5. **Agente revisor:** verifica constitución, `SKILL.md` y checklist.

## Tareas atómicas

- [ ] Configurar `CHANNEL_LAYERS` con Redis.
- [ ] Crear `ParkingConsumer` o adaptar `DisponibilidadConsumer`.
- [ ] Definir grupos por `parqueadero_id`.
- [ ] Emitir payload `{espacio_id, parqueadero_id, estado, disponibles}`.
- [ ] Agregar signal o publicación desde servicio al cambiar estado.
- [ ] Crear script JS de prueba.
- [ ] Probar latencia menor a 5 segundos.

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
- Prueba WebSocket de publicación/recepción y medición de latencia.

## Riesgos y mitigaciones

- Usar Gunicorn/WSGI impediría WebSockets.
- Emitir eventos desde signal sin detectar cambios reales puede duplicar mensajes.
- Múltiples workers requieren Redis, no InMemoryChannelLayer.

## Entregable mínimo

Un PR lógico o paquete de cambios que implemente una sola tarea atómica, incluya prueba o evidencia de verificación y no rompa contratos existentes.
