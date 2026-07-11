# Plan técnico — Registro de usuarios y envío de documentos

## Propósito de implementación

Permitir registro de propietarios y carga de documentos verificables.

## Prioridad

**P0**. La feature se considera bloqueante para el MVP.

## Decisiones de diseño

- Se mantiene la separación por capas: controladores, servicios, repositorios, modelos y DTO/serializadores.
- Se evita lógica de negocio en la vista o en rutas.
- Se documentan contratos antes de implementar.
- Se aplican permisos por defecto restrictivos.
- Se escriben pruebas de contrato y permisos antes de cerrar la tarea.

## Tecnologías seleccionadas

DRF MultiPartParser, Cloudflare R2 S3-compatible o adaptador Google Drive, React form validation.

## Componentes impactados

- `/backend/apps/documentos`
- `/frontend-web/src/views/auth`
- `/frontend-web/src/services/documentoService`

## Contratos

- `POST /api/auth/register/` — Crea persona y cuenta.
- `POST /api/documentos/` — Sube documento.
- `GET /api/documentos/` — Consulta documento propio.
- `PATCH /api/documentos/{id}/` — Reemplaza documento.
- `POST /api/documentos/{id}/validar/` — Valida documento como administrador.

Los contratos detallados están en `contracts/openapi.yaml`.

## UI y navegación

Registro de propietario y panel de documento pendiente/validado.

Prototipos disponibles en:

- `docs/prototypes/registro-de-propietario/code.html`
- `docs/prototypes/registro-de-propietario/screen.png`

## Flujo entre agentes

1. **Agente de especificación:** valida historias, requisitos y escenarios.
2. **Agente de arquitectura:** revisa este plan y confirma decisiones.
3. **Agente ejecutor:** toma una tarea atómica.
4. **Agente de pruebas:** valida contrato, permisos y escenarios.
5. **Agente revisor:** verifica constitución, `SKILL.md` y checklist.

## Tareas atómicas

- [ ] Crear validaciones de identificación y correo.
- [ ] Crear formulario de registro.
- [ ] Crear servicio de subida multipart.
- [ ] Validar extensión PDF/JPG/PNG y tamaño máximo.
- [ ] Marcar documento como pendiente al subir o reemplazar.
- [ ] Crear vista de estado de validación.
- [ ] Crear pruebas de permisos y tamaño de archivo.

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

- Subir archivo a storage y fallar BD sin rollback.
- Permitir múltiples documentos si la regla es uno por cuenta.
- Exponer documentos a usuarios no autorizados.

## Entregable mínimo

Un PR lógico o paquete de cambios que implemente una sola tarea atómica, incluya prueba o evidencia de verificación y no rompa contratos existentes.
