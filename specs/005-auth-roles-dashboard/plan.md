# Plan técnico — Inicio de sesión y dashboard por roles

## Propósito de implementación

Permitir acceso seguro y redirección correcta por rol.

## Prioridad

**P0**. La feature se considera bloqueante para el MVP.

## Decisiones de diseño

- Se mantiene la separación por capas: controladores, servicios, repositorios, modelos y DTO/serializadores.
- Se evita lógica de negocio en la vista o en rutas.
- Se documentan contratos antes de implementar.
- Se aplican permisos por defecto restrictivos.
- Se escriben pruebas de contrato y permisos antes de cerrar la tarea.

## Tecnologías seleccionadas

SimpleJWT, React Router guards, Zustand/React Query, almacenamiento seguro móvil.

## Componentes impactados

- `/backend/apps/usuarios`
- `/frontend-web/src/views/auth`
- `/frontend-web/src/config/routes`
- `/mobile`

## Contratos

- `POST /api/auth/token/` — Obtiene tokens.
- `POST /api/auth/refresh/` — Renueva access.
- `GET /api/cuentas/me/` — Obtiene perfil autenticado.

Los contratos detallados están en `contracts/openapi.yaml`.

## UI y navegación

Pantallas de login, dashboard por rol y home pública.

Prototipos disponibles en:

- `docs/prototypes/inicio-de-sesi-n/code.html`
- `docs/prototypes/inicio-de-sesi-n/screen.png`

## Flujo entre agentes

1. **Agente de especificación:** valida historias, requisitos y escenarios.
2. **Agente de arquitectura:** revisa este plan y confirma decisiones.
3. **Agente ejecutor:** toma una tarea atómica.
4. **Agente de pruebas:** valida contrato, permisos y escenarios.
5. **Agente revisor:** verifica constitución, `SKILL.md` y checklist.

## Tareas atómicas

- [ ] Crear servicio central de autenticación.
- [ ] Guardar tokens de forma segura para web y móvil.
- [ ] Crear guardas de rutas por rol.
- [ ] Redirigir propietario a panel propietario.
- [ ] Redirigir administrador a panel administrador.
- [ ] Permitir home anónimo sin token.
- [ ] Crear pruebas de rutas protegidas.

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

- Guardar tokens de forma insegura.
- No renovar access token y forzar logout prematuro.
- Confundir usuario anónimo con rol persistente.

## Entregable mínimo

Un PR lógico o paquete de cambios que implemente una sola tarea atómica, incluya prueba o evidencia de verificación y no rompa contratos existentes.
