# Plan técnico — Mapas, tiles y búsqueda cercana

## Propósito de implementación

Permitir búsqueda geográfica de parqueaderos y renderizado de mapa base local.

## Prioridad

**P1**. La feature se considera necesaria para completar experiencia del MVP.

## Decisiones de diseño

- Se mantiene la separación por capas: controladores, servicios, repositorios, modelos y DTO/serializadores.
- Se evita lógica de negocio en la vista o en rutas.
- Se documentan contratos antes de implementar.
- Se aplican permisos por defecto restrictivos.
- Se escriben pruebas de contrato y permisos antes de cerrar la tarea.

## Tecnologías seleccionadas

tileserver-gl, tilemaker, Leaflet/react-leaflet, Nominatim público, PostgreSQL, cálculo Haversine o earthdistance.

## Componentes impactados

- `/docker/tileserver`
- `/frontend-web/src/views`
- `/mobile`
- `/backend/apps/parqueaderos`

## Contratos

- `GET /api/parqueaderos/?lat={lat}&lon={lon}&radio={metros}` — Lista parqueaderos cercanos ordenados por distancia.
- `GET /api/parqueaderos/{id}/` — Detalle público de parqueadero.

Los contratos detallados están en `contracts/openapi.yaml`.

## UI y navegación

Mapa con buscador, marcador de usuario, marcadores coloreados y lista lateral.

Prototipos disponibles en:

- `docs/prototypes/mapa-de-parqueaderos-cercanos/code.html`
- `docs/prototypes/mapa-de-parqueaderos-cercanos/screen.png`

## Flujo entre agentes

1. **Agente de especificación:** valida historias, requisitos y escenarios.
2. **Agente de arquitectura:** revisa este plan y confirma decisiones.
3. **Agente ejecutor:** toma una tarea atómica.
4. **Agente de pruebas:** valida contrato, permisos y escenarios.
5. **Agente revisor:** verifica constitución, `SKILL.md` y checklist.

## Tareas atómicas

- [ ] Descargar extract Ecuador OSM PBF.
- [ ] Limitar el mapa a la Ciudad de Loja
- [ ] Convertir a MBTiles con tilemaker.
- [ ] Montar tileserver-gl con estilo osm-bright.
- [ ] Instalar e integrar Leaflet en web.
- [ ] Crear buscador con Nominatim, debounce 800 ms y 1 req/s.
- [ ] Crear endpoint de cercanía con distancia y filtros públicos.
- [ ] Crear marcadores por disponibilidad.

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

- Nominatim público impone políticas de uso; debe limitarse tasa.
- Generar MBTiles puede ser pesado; no hacerlo en runtime.
- Distancias en Python pueden degradarse si el dataset crece mucho.

## Entregable mínimo

Un PR lógico o paquete de cambios que implemente una sola tarea atómica, incluya prueba o evidencia de verificación y no rompa contratos existentes.
