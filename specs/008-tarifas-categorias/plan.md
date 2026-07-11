# Plan técnico — Gestión de tarifas por categoría

## Propósito de implementación

Permitir tarifas paralelas por tipo de vehículo/beneficio.

## Prioridad

**P1**. La feature se considera necesaria para completar experiencia del MVP.

## Decisiones de diseño

- Se mantiene la separación por capas: controladores, servicios, repositorios, modelos y DTO/serializadores.
- Se evita lógica de negocio en la vista o en rutas.
- Se documentan contratos antes de implementar.
- Se aplican permisos por defecto restrictivos.
- Se escriben pruebas de contrato y permisos antes de cerrar la tarea.

## Tecnologías seleccionadas

Django model, DecimalField, índices compuestos, DRF ViewSet, React form.

## Componentes impactados

- `/backend/apps/tarifas`
- `/frontend-web/src/views/components/owner`
- `/frontend-web/src/services/tarifaService`

## Contratos

- `GET /api/categorias-tarifa/?parqueadero={id}` — Lista categorías por parqueadero.
- `POST /api/categorias-tarifa/` — Crea categoría de tarifa.
- `PATCH /api/categorias-tarifa/{id}/` — Actualiza precio.
- `DELETE /api/categorias-tarifa/{id}/` — Elimina categoría.

Los contratos detallados están en `contracts/openapi.yaml`.

## UI y navegación

Tabla/formulario de tarifas General, Preferencial y Pesados.

Prototipos disponibles en:

- `docs/prototypes/gesti-n-de-tarifas/code.html`
- `docs/prototypes/gesti-n-de-tarifas/screen.png`

## Flujo entre agentes

1. **Agente de especificación:** valida historias, requisitos y escenarios.
2. **Agente de arquitectura:** revisa este plan y confirma decisiones.
3. **Agente ejecutor:** toma una tarea atómica.
4. **Agente de pruebas:** valida contrato, permisos y escenarios.
5. **Agente revisor:** verifica constitución, `SKILL.md` y checklist.

## Tareas atómicas

- [ ] Agregar modelo `TipoCategoriaTarifa`.
- [ ] Agregar modelo `CategoriaTarifa`.
- [ ] Crear migración con unique `(parqueadero, codigo)`.
- [ ] Crear serializer y ViewSet.
- [ ] Crear permisos por propietario.
- [ ] Crear UI para tres categorías simultáneas.
- [ ] Probar duplicado por categoría y parqueadero.

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

- Reusar jerarquía `EstrategiaTarifa` rompería simultaneidad de categorías.
- Duplicar categorías por parqueadero generaría ambigüedad en precios.
- Mezclar porcentaje y precio final sin regla clara.

## Entregable mínimo

Un PR lógico o paquete de cambios que implemente una sola tarea atómica, incluya prueba o evidencia de verificación y no rompa contratos existentes.
