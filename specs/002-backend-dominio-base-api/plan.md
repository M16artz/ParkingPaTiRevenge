# Plan técnico — Backend base de dominio y API

## Propósito de implementación

Crear y validar la base del dominio de usuarios, parqueaderos, espacios, horarios y tarifas.

## Prioridad

**P0**. La feature se considera bloqueante para el MVP.

## Decisiones de diseño

- Se mantiene la separación por capas: controladores, servicios, repositorios, modelos y DTO/serializadores.
- Se evita lógica de negocio en la vista o en rutas.
- Se documentan contratos antes de implementar.
- Se aplican permisos por defecto restrictivos.
- Se escriben pruebas de contrato y permisos antes de cerrar la tarea.

## Tecnologías seleccionadas

Django REST Framework, SimpleJWT, drf-spectacular, PostgreSQL, pytest.

## Componentes impactados

- `/backend/apps/*`
- `/backend/config/settings`
- `/backend/config/urls.py`
- `/backend/requirements/*`

## Contratos

- `POST /api/auth/token/` — Iniciar sesión.
- `POST /api/auth/refresh/` — Renovar token.
- `POST /api/auth/register/` — Registrar cuenta.
- `GET /api/parqueaderos/` — Listar parqueaderos según permisos.
- `GET /api/espacios/` — Listar espacios.
- `GET /api/horarios/` — Listar horarios.
- `GET /api/tarifas/` — Listar tarifas.

Los contratos detallados están en `contracts/openapi.yaml`.

## UI y navegación

No es una feature de usuario final; el prototipo representa un explorador de API para agentes.

Prototipos disponibles en:

- `docs/prototypes/explorador-t-cnico-de-api/code.html`
- `docs/prototypes/explorador-t-cnico-de-api/screen.png`

## Flujo entre agentes

1. **Agente de especificación:** valida historias, requisitos y escenarios.
2. **Agente de arquitectura:** revisa este plan y confirma decisiones.
3. **Agente ejecutor:** toma una tarea atómica.
4. **Agente de pruebas:** valida contrato, permisos y escenarios.
5. **Agente revisor:** verifica constitución, `SKILL.md` y checklist.

## Tareas atómicas

- [ ] Crear apps de dominio o mapear las existentes sin romper imports.
- [ ] Agregar índices de búsqueda en Parqueadero y Espacio.
- [ ] Configurar JWT con access token de 15 minutos.
- [ ] Crear serializers/DTO para lectura y escritura.
- [ ] Crear ViewSets con permisos por defecto.
- [ ] Agregar drf-spectacular y endpoint de schema.
- [ ] Crear pruebas de autenticación y permisos.

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

- Mass assignment si se aceptan `request.data` crudos.
- Permisos insuficientes para endpoints de gestión.
- Migraciones inconsistentes con modelos ya existentes.

## Entregable mínimo

Un PR lógico o paquete de cambios que implemente una sola tarea atómica, incluya prueba o evidencia de verificación y no rompa contratos existentes.
