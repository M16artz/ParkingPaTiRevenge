# Plan técnico — Gestión de espacios de parqueadero

## Propósito de implementación

Permitir administrar cantidad y estado de espacios individuales.

## Prioridad

**P0**. La feature se considera bloqueante para el MVP.

## Decisiones de diseño

- Se mantiene la separación por capas: controladores, servicios, repositorios, modelos y DTO/serializadores.
- Se evita lógica de negocio en la vista o en rutas.
- Se documentan contratos antes de implementar.
- Se aplican permisos por defecto restrictivos.
- Se escriben pruebas de contrato y permisos antes de cerrar la tarea.

## Tecnologías seleccionadas

DRF actions, database indexes, Channels group_send, React hook `useDisponibilidadSocket`.

## Componentes impactados

- `/backend/apps/parqueaderos`
- `/frontend-web/src/controllers/useEspacioController`
- `/frontend-web/src/hooks/useDisponibilidadSocket`

## Contratos

- `GET /api/espacios/?parqueadero={id}` — Lista espacios.
- `POST /api/espacios/` — Crea espacio.
- `PATCH /api/espacios/{id}/estado/` — Cambia estado.
- `DELETE /api/espacios/{id}/` — Elimina espacio.

Los contratos detallados están en `contracts/openapi.yaml`.

## UI y navegación

Grid de espacios con colores y acciones rápidas.

Prototipos disponibles en:

- `docs/prototypes/gesti-n-de-espacios/code.html`
- `docs/prototypes/gesti-n-de-espacios/screen.png`

## Flujo entre agentes

1. **Agente de especificación:** valida historias, requisitos y escenarios.
2. **Agente de arquitectura:** revisa este plan y confirma decisiones.
3. **Agente ejecutor:** toma una tarea atómica.
4. **Agente de pruebas:** valida contrato, permisos y escenarios.
5. **Agente revisor:** verifica constitución, `SKILL.md` y checklist.

## Tareas atómicas

- [ ] Crear o ajustar índice por `(parqueadero, estado)`.
- [ ] Validar unique `(parqueadero, numero_espacio)`.
- [ ] Crear sincronización de cantidad.
- [ ] Crear modal de cambio de estado.
- [ ] Emitir evento WebSocket al cambiar estado.
- [ ] Actualizar badges de disponibilidad.
- [ ] Probar concurrencia básica.

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

- Eliminar espacios ocupados sin confirmación.
- No publicar evento al cambio de estado.
- Estado local divergente del servidor.

## Entregable mínimo

Un PR lógico o paquete de cambios que implemente una sola tarea atómica, incluya prueba o evidencia de verificación y no rompa contratos existentes.
