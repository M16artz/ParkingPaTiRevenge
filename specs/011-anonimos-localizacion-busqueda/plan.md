# Plan técnico — Usuarios anónimos: localización y búsqueda de parqueaderos

## Propósito de implementación

Permitir a conductores sin cuenta buscar parqueaderos y ver información pública.

## Prioridad

**P1**. La feature se considera necesaria para completar experiencia del MVP.

## Decisiones de diseño

- Se mantiene la separación por capas: controladores, servicios, repositorios, modelos y DTO/serializadores.
- Se evita lógica de negocio en la vista o en rutas.
- Se documentan contratos antes de implementar.
- Se aplican permisos por defecto restrictivos.
- Se escriben pruebas de contrato y permisos antes de cerrar la tarea.

## Tecnologías seleccionadas

Geolocation API, React Native permissions, Leaflet, WebSocket, endpoint público con filtros.

## Componentes impactados

- `/docker/tileserver`
- `/frontend-web/src/views`
- `/mobile`
- `/backend/apps/parqueaderos`

## Contratos

- `GET /api/parqueaderos/?lat={lat}&lon={lon}&radio={metros}` — Búsqueda pública cercana.
- `GET /api/parqueaderos/{id}/publico/` — Detalle público.
- `WS /ws/parqueaderos/{parqueadero_id}/` — Disponibilidad en vivo del detalle.

Los contratos detallados están en `contracts/openapi.yaml`.

## UI y navegación

Flujo conductor anónimo optimizado para búsqueda rápida.

Prototipos disponibles en:

- `docs/prototypes/home-an-nimo/code.html`
- `docs/prototypes/home-an-nimo/screen.png`

## Flujo entre agentes

1. **Agente de especificación:** valida historias, requisitos y escenarios.
2. **Agente de arquitectura:** revisa este plan y confirma decisiones.
3. **Agente ejecutor:** toma una tarea atómica.
4. **Agente de pruebas:** valida contrato, permisos y escenarios.
5. **Agente revisor:** verifica constitución, `SKILL.md` y checklist.

## Tareas atómicas

- [ ] Crear home pública con CTA de búsqueda.
- [ ] Solicitar ubicación solo al usar buscar cerca.
- [ ] Permitir buscar por dirección si rechaza ubicación.
- [ ] Mostrar lista y mapa.
- [ ] Mostrar detalle con tarifas, horarios y espacios libres.
- [ ] Suscribirse a WebSocket en detalle.
- [ ] Probar máximo 3 toques hasta resultados.

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

- Solicitar permisos demasiado pronto.
- Mostrar parqueaderos no validados.
- No degradar correctamente si falla ubicación o mapa.

## Entregable mínimo

Un PR lógico o paquete de cambios que implemente una sola tarea atómica, incluya prueba o evidencia de verificación y no rompa contratos existentes.
