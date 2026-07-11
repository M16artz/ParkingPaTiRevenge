# Plan técnico — Creación y configuración general de parqueadero

## Propósito de implementación

Permitir al propietario registrar y administrar datos generales de su parqueadero.

## Prioridad

**P1**. La feature se considera necesaria para completar experiencia del MVP.

## Decisiones de diseño

- Se mantiene la separación por capas: controladores, servicios, repositorios, modelos y DTO/serializadores.
- Se evita lógica de negocio en la vista o en rutas.
- Se documentan contratos antes de implementar.
- Se aplican permisos por defecto restrictivos.
- Se escriben pruebas de contrato y permisos antes de cerrar la tarea.

## Tecnologías seleccionadas

DRF ViewSet custom actions, transacciones, React controller hook, validación de formularios.

## Componentes impactados

- `/backend/apps/parqueaderos`
- `/frontend-web/src/views/owner`
- `/frontend-web/src/services/parqueaderoService`

## Contratos

- `POST /api/parqueaderos/` — Crea parqueadero.
- `GET /api/parqueaderos/mios/` — Lista parqueaderos del propietario autenticado.
- `PATCH /api/parqueaderos/{id}/` — Actualiza datos generales.
- `PATCH /api/parqueaderos/{id}/estado/` — Cambia disponibilidad general.

Los contratos detallados están en `contracts/openapi.yaml`.

## UI y navegación

Formulario con datos comerciales, dirección, ubicación y estado.

Prototipos disponibles en:

- `docs/prototypes/configuraci-n-general-de-parqueadero/code.html`
- `docs/prototypes/configuraci-n-general-de-parqueadero/screen.png`

## Flujo entre agentes

1. **Agente de especificación:** valida historias, requisitos y escenarios.
2. **Agente de arquitectura:** revisa este plan y confirma decisiones.
3. **Agente ejecutor:** toma una tarea atómica.
4. **Agente de pruebas:** valida contrato, permisos y escenarios.
5. **Agente revisor:** verifica constitución, `SKILL.md` y checklist.

## Tareas atómicas

- [ ] Crear DTO de creación con dirección y ubicación.
- [ ] Validar propietario autenticado.
- [ ] Crear endpoint `mios`.
- [ ] Crear pantalla de configuración general.
- [ ] Crear selector de disponibilidad.
- [ ] Actualizar servicios frontend.
- [ ] Probar propietario no puede editar parqueadero ajeno.

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

- Crear parqueadero sin ubicación impediría búsqueda cercana.
- Editar estado sin reflejarlo en el mapa público.
- No separar validado/activo/disponibilidad.

## Entregable mínimo

Un PR lógico o paquete de cambios que implemente una sola tarea atómica, incluya prueba o evidencia de verificación y no rompa contratos existentes.
