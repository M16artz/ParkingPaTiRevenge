# Plan técnico — Gestión de horarios de atención

## Propósito de implementación

Permitir configurar horarios semanales por parqueadero.

## Prioridad

**P1**. La feature se considera necesaria para completar experiencia del MVP.

## Decisiones de diseño

- Se mantiene la separación por capas: controladores, servicios, repositorios, modelos y DTO/serializadores.
- Se evita lógica de negocio en la vista o en rutas.
- Se documentan contratos antes de implementar.
- Se aplican permisos por defecto restrictivos.
- Se escriben pruebas de contrato y permisos antes de cerrar la tarea.

## Tecnologías seleccionadas

Django TimeField, serializers con validate, React controlled forms.

## Componentes impactados

- `/backend/apps/horarios`
- `/frontend-web/src/views/components/owner`
- `/frontend-web/src/services/horarioService`

## Contratos

- `GET /api/horarios/?parqueadero={id}` — Lista horarios.
- `POST /api/horarios/` — Crea horario.
- `PATCH /api/horarios/{id}/` — Actualiza horario.
- `DELETE /api/horarios/{id}/` — Elimina horario.

Los contratos detallados están en `contracts/openapi.yaml`.

## UI y navegación

Semana editable con hora apertura/cierre y switch por día.

Prototipos disponibles en:

- `docs/prototypes/gesti-n-de-horarios/code.html`
- `docs/prototypes/gesti-n-de-horarios/screen.png`

## Flujo entre agentes

1. **Agente de especificación:** valida historias, requisitos y escenarios.
2. **Agente de arquitectura:** revisa este plan y confirma decisiones.
3. **Agente ejecutor:** toma una tarea atómica.
4. **Agente de pruebas:** valida contrato, permisos y escenarios.
5. **Agente revisor:** verifica constitución, `SKILL.md` y checklist.

## Tareas atómicas

- [ ] Asegurar unique `(parqueadero, dia)`.
- [ ] Validar apertura menor a cierre.
- [ ] Crear UI por días de semana.
- [ ] Permitir activar/desactivar día mediante creación/eliminación lógica o física.
- [ ] Sincronizar carga inicial con `mios`.
- [ ] Probar duplicado y horario inválido.

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

- Usar campos inconsistentes `dia` vs `dia_semana`.
- Permitir horarios duplicados.
- No contemplar parqueaderos 24h si apertura igual cierre.

## Entregable mínimo

Un PR lógico o paquete de cambios que implemente una sola tarea atómica, incluya prueba o evidencia de verificación y no rompa contratos existentes.
