# Tasks: 004-registro-usuario-documentos

**Feature**: Registro de propietario y documentos  
**Ruta solicitada**: `specs/004-registro-usuario-documentos/`  
**Fuente funcional usada**: `specs/006-registro-documentos/spec.md`, `plan.md`, `data-model.md`, `contracts/openapi.yaml`; depende de `specs/003-autenticacion-jwt-roles/tasks.md` ya implementado.  
**Alcance**: formulario de registro de propietario, carga de documento, validacion de extension y tamano, almacenamiento configurado, estado pendiente de validacion, endpoints de documentos y feedback visual en frontend.

## Formato

- `[ ] T###` tarea secuencial.
- `[P]` puede ejecutarse en paralelo cuando sus archivos no dependen de otra tarea pendiente.
- Cada tarea debe cerrar con evidencia de verificacion en la nota del agente.

## Reglas de ejecucion

- Depende de `003-autenticacion-jwt-roles`; reutilizar `POST /api/auth/register/`, login, refresh, store de sesion y guards existentes.
- No modificar la logica JWT salvo que sea estrictamente necesario para corregir un bloqueo comprobado.
- No duplicar `Persona`, `Cuenta`, `Rol` ni `Documento`; adaptar lo existente si hace falta.
- Mantener arquitectura backend por capas: controller -> service -> repository -> model.
- No poner reglas de negocio en controllers, urls ni componentes visuales.
- Todo endpoint de documentos debe exigir JWT valido, salvo que un contrato indique explicitamente lo contrario.
- Los propietarios solo pueden consultar, subir o reemplazar sus propios documentos.
- La validacion administrativa de documentos exige rol `ADMINISTRADOR`.
- Los errores visibles deben estar en espanol y sugerir una accion correctiva.
- No versionar documentos reales, `.env`, credenciales, tokens ni claves de storage.
- No implementar parqueaderos, tarifas, horarios, espacios, mapas ni WebSocket en esta feature.

## Contratos objetivo

- `POST /api/auth/register/` registra una cuenta `PROPIETARIO` si el contrato de 003 ya lo soporta.
- `POST /api/documentos/` sube un documento del propietario autenticado.
- `GET /api/documentos/` consulta documentos propios del usuario autenticado.
- `PATCH /api/documentos/{id}/` reemplaza un documento propio.
- `POST /api/documentos/{id}/validar/` valida o rechaza documento como administrador.

## Estados objetivo de documento

- `PENDIENTE`: estado inicial despues de subir o reemplazar documento.
- `VALIDADO`: estado administrativo aprobado.
- `RECHAZADO`: estado administrativo no aprobado, con motivo visible si el modelo/contrato lo permite.

Si el modelo actual solo contiene `es_valido`, agregar un campo de estado explicito o documentar una migracion minima que preserve compatibilidad.

## Fase 0: Inventario y alineacion

- [ ] T001 Inventariar autenticacion implementada de 003.
  - Archivos esperados: no crea archivos.
  - Verificacion: confirmar rutas `auth/register`, `auth/token`, `auth/refresh`, `cuentas/me`, store frontend y guards; registrar cualquier ajuste necesario sin cambiar JWT por defecto.

- [ ] T002 Inventariar la app `backend/apps/documentos`.
  - Archivos esperados: no crea archivos.
  - Verificacion: registrar modelo, serializer, repository, service, migraciones y tests existentes; confirmar que no se duplicara `Documento`.

- [ ] T003 Inventariar frontend actual de registro y dashboards.
  - Archivos esperados: no crea archivos.
  - Verificacion: identificar `RegisterView`, `PropietarioView`, servicios API, store y rutas donde integrar feedback de documentos.

- [ ] T004 Revisar contrato fuente de documentos y crear contrato local si falta.
  - Archivos esperados: `specs/004-registro-usuario-documentos/contracts/openapi.yaml`.
  - Verificacion: contrato incluye endpoints de registro propietario y documentos; no incluye parqueaderos, tarifas, horarios, espacios, mapas ni WebSocket.

- [ ] T005 Definir limites de archivo documentados.
  - Depende de: T004.
  - Archivos esperados: `specs/004-registro-usuario-documentos/tasks.md` o contrato/configuracion si se decide ajustar.
  - Verificacion: quedan definidos formatos permitidos `pdf`, `jpg`, `jpeg`, `png` y tamano maximo configurable; no se hardcodean secretos ni rutas absolutas locales.

## Fase 1: Configuracion de almacenamiento

- [ ] T006 Agregar variables de storage a `.env.example`.
  - Archivos esperados: `.env.example`.
  - Verificacion: contiene placeholders para backend de storage, bucket, endpoint, region, access key y secret key; todos son valores ficticios o vacios comentados.

- [ ] T007 Crear configuracion backend de archivos y storage.
  - Depende de: T006.
  - Archivos esperados: `backend/backend/settings/base.py` o modulo de settings equivalente.
  - Verificacion: define `MEDIA_ROOT`/`MEDIA_URL` local para desarrollo y variables configurables para storage externo; no contiene credenciales reales.

- [ ] T008 Crear adaptador de almacenamiento de documentos.
  - Depende de: T007.
  - Archivos esperados: `backend/apps/documentos/storage.py` o modulo equivalente.
  - Verificacion: expone funciones o clase para guardar y reemplazar archivos; retorna `ruta`, `file_id`, `nombre_original`, `content_type` y `tamano`; permite mock en tests.

- [ ] T009 Documentar comando y modo local de storage.
  - Depende de: T007-T008.
  - Archivos esperados: `docs/dev-setup.md` o `docs/documentos.md`.
  - Verificacion: explica como usar storage local en desarrollo y como configurar placeholders externos sin secretos.

## Fase 2: Backend modelo, migraciones y validaciones

- [ ] T010 Ajustar modelo `Documento` para estado de validacion explicito.
  - Depende de: T002.
  - Archivos esperados: `backend/apps/documentos/models.py`.
  - Verificacion: existe estado `PENDIENTE`, `VALIDADO`, `RECHAZADO` o equivalente; documentos nuevos/reemplazados inician pendientes; compatibilidad con `es_valido` queda resuelta o migrada.

- [ ] T011 Agregar metadata de archivo al modelo si falta.
  - Depende de: T010.
  - Archivos esperados: `backend/apps/documentos/models.py`.
  - Verificacion: registra nombre original, extension/content type, tamano y ruta/file_id; no almacena binarios en base de datos.

- [ ] T012 Agregar indice y restriccion para consulta por cuenta y estado.
  - Depende de: T010-T011.
  - Archivos esperados: `backend/apps/documentos/models.py`.
  - Verificacion: existe indice por `cuenta` y `estado`; se preserva la regla de un documento vigente/validado por cuenta si aplica al MVP.

- [ ] T013 Crear migracion de documentos.
  - Depende de: T010-T012.
  - Archivos esperados: `backend/apps/documentos/migrations/0002_*.py`.
  - Verificacion: `python manage.py makemigrations --check` queda limpio despues de generar la migracion.

- [ ] T014 Crear validador de extension y tamano.
  - Depende de: T005.
  - Archivos esperados: `backend/apps/documentos/validators.py` o `services.py`.
  - Verificacion: rechaza extensiones fuera de PDF/JPG/JPEG/PNG y archivos sobre el limite con mensajes en espanol.

- [ ] T015 Crear serializer de carga multipart.
  - Depende de: T014.
  - Archivos esperados: `backend/apps/documentos/serializers.py`.
  - Verificacion: acepta `archivo` y metadata minima; no permite que el cliente asigne `cuenta`, `estado`, `es_valido`, `ruta` ni `file_id`.

- [ ] T016 Crear serializer de lectura de documentos.
  - Depende de: T010-T011.
  - Archivos esperados: `backend/apps/documentos/serializers.py`.
  - Verificacion: devuelve id, estado, fecha, nombre, tamano y motivo si existe; no expone rutas privadas ni credenciales.

## Fase 3: Backend repositorios, servicios y endpoints

- [ ] T017 Ampliar repositorio de documentos.
  - Depende de: T010-T012.
  - Archivos esperados: `backend/apps/documentos/repositories.py`.
  - Verificacion: incluye consultas por cuenta, id y estado; evita filtrar documentos de otras cuentas para flujo propietario.

- [ ] T018 Crear servicio de subida de documento.
  - Depende de: T008, T014-T017.
  - Archivos esperados: `backend/apps/documentos/services.py`.
  - Verificacion: valida archivo, guarda en storage, crea metadata transaccional y marca estado `PENDIENTE`; no recibe decisiones desde controller.

- [ ] T019 Crear servicio de reemplazo de documento.
  - Depende de: T018.
  - Archivos esperados: `backend/apps/documentos/services.py`.
  - Verificacion: solo reemplaza documento propio, reinicia estado a `PENDIENTE` y maneja fallo de storage/base con error accionable.

- [ ] T020 Crear servicio de validacion administrativa.
  - Depende de: T017.
  - Archivos esperados: `backend/apps/documentos/services.py`.
  - Verificacion: permite aprobar o rechazar con rol administrador; rechazo guarda motivo si el modelo/contrato lo contempla.

- [ ] T021 Crear permisos de documentos.
  - Depende de: T001, T017.
  - Archivos esperados: `backend/apps/documentos/permissions.py` o reutilizacion explicita de `apps/usuarios/permissions.py`.
  - Verificacion: propietario accede solo a sus documentos; administrador puede validar; anonimo recibe 401.

- [ ] T022 Crear controllers/endpoints de documentos.
  - Depende de: T015-T021.
  - Archivos esperados: `backend/apps/documentos/controllers.py` o `views.py`.
  - Verificacion: controllers usan serializers, permisos y services; no guardan archivos directamente ni contienen reglas de negocio.

- [ ] T023 Configurar parsers multipart.
  - Depende de: T022.
  - Archivos esperados: controller o configuracion DRF.
  - Verificacion: `POST /api/documentos/` y `PATCH /api/documentos/{id}/` aceptan `multipart/form-data`.

- [ ] T024 Registrar rutas de documentos.
  - Depende de: T022-T023.
  - Archivos esperados: `backend/apps/documentos/urls.py`, `backend/backend/urls.py`.
  - Verificacion: rutas quedan bajo `/api/documentos/`; `urls.py` solo registra rutas.

- [ ] T025 Actualizar OpenAPI local de la feature.
  - Depende de: T015-T024.
  - Archivos esperados: `specs/004-registro-usuario-documentos/contracts/openapi.yaml`.
  - Verificacion: documenta multipart, errores 400/401/403, respuesta pendiente y validacion admin; coincide con endpoints implementados.

## Fase 4: Frontend registro de propietario

- [ ] T026 Centralizar endpoints de documentos.
  - Depende de: T004.
  - Archivos esperados: `frontend-web/src/config/endpoints.ts`.
  - Verificacion: contiene endpoints de documentos; las vistas no construyen URLs manualmente.

- [ ] T027 Crear servicio frontend de documentos.
  - Depende de: T026.
  - Archivos esperados: `frontend-web/src/services/documentoService.ts`.
  - Verificacion: implementa listar propio, subir, reemplazar y validar si aplica; usa cliente API autenticado y no contiene HTML.

- [ ] T028 Agregar validacion cliente de archivo.
  - Depende de: T005, T027.
  - Archivos esperados: `frontend-web/src/services/documentoValidation.ts` o modulo equivalente.
  - Verificacion: valida extension y tamano antes de enviar; el backend sigue siendo fuente final de validacion.

- [ ] T029 Ajustar formulario de registro para propietario.
  - Depende de: T001, T003.
  - Archivos esperados: `frontend-web/src/views/auth/RegisterView.tsx`.
  - Verificacion: permite elegir o fijar rol `PROPIETARIO` para este flujo; no permite registrar administrador; muestra errores en espanol.

- [ ] T030 Integrar carga de documento al flujo post-registro.
  - Depende de: T027-T029.
  - Archivos esperados: `RegisterView.tsx` o vista/hook de flujo de registro propietario.
  - Verificacion: despues de registro exitoso, el usuario puede subir documento autenticado o se le guia a login/subida segun la sesion disponible.

- [ ] T031 Crear componente de selector de documento.
  - Depende de: T028.
  - Archivos esperados: `frontend-web/src/components/documentos/DocumentoUploader.tsx` o ruta equivalente.
  - Verificacion: muestra nombre, tamano, extension, estados de carga/error/exito y no permite enviar archivo invalido.

- [ ] T032 Crear vista de estado de validacion para propietario.
  - Depende de: T027.
  - Archivos esperados: `frontend-web/src/views/private/DocumentoEstadoView.tsx` o integracion en `PropietarioView.tsx`.
  - Verificacion: muestra `PENDIENTE`, `VALIDADO` o `RECHAZADO` con mensaje accionable; no implementa gestion de parqueadero.

- [ ] T033 Agregar feedback visual en dashboard propietario.
  - Depende de: T032.
  - Archivos esperados: `frontend-web/src/views/private/PropietarioView.tsx` y estilos existentes.
  - Verificacion: propietario ve proximo paso segun estado del documento; no se muestran controles administrativos.

- [ ] T034 Agregar ruta protegida de documentos de propietario si aplica.
  - Depende de: T032.
  - Archivos esperados: `frontend-web/src/main.tsx`, `frontend-web/src/config/routes.ts`.
  - Verificacion: solo `PROPIETARIO` accede; usuario sin sesion redirige a `/login`.

## Fase 5: Frontend administracion minima de validacion

- [ ] T035 Crear servicio/admin action de validacion.
  - Depende de: T027.
  - Archivos esperados: `frontend-web/src/services/documentoService.ts`.
  - Verificacion: envia aprobar/rechazar a endpoint admin; no expone secretos ni rutas manuales.

- [ ] T036 Crear feedback minimo en dashboard administrador.
  - Depende de: T035.
  - Archivos esperados: `frontend-web/src/views/private/AdminView.tsx`.
  - Verificacion: permite visualizar que hay documentos pendientes o deja placeholder funcional conectado al servicio si el listado admin no esta en contrato; no implementa parqueaderos.

## Fase 6: Pruebas backend

- [ ] T037 Probar validador de extension permitida.
  - Depende de: T014.
  - Archivos esperados: `backend/apps/documentos/tests/test_validators.py`.
  - Verificacion: PDF, JPG/JPEG y PNG pasan; extension no permitida falla en espanol.

- [ ] T038 Probar validador de tamano maximo.
  - Depende de: T014.
  - Archivos esperados: `backend/apps/documentos/tests/test_validators.py`.
  - Verificacion: archivo bajo limite pasa; archivo sobre limite falla en espanol.

- [ ] T039 Probar subida de documento autenticado.
  - Depende de: T018, T022-T024.
  - Archivos esperados: `backend/apps/documentos/tests/test_documentos_api.py`.
  - Verificacion: `POST /api/documentos/` crea documento pendiente y devuelve metadata segura.

- [ ] T040 Probar subida sin sesion.
  - Depende de: T022-T024.
  - Archivos esperados: `backend/apps/documentos/tests/test_documentos_api.py`.
  - Verificacion: usuario anonimo recibe 401.

- [ ] T041 Probar consulta de documentos propios.
  - Depende de: T017, T022-T024.
  - Archivos esperados: `backend/apps/documentos/tests/test_documentos_api.py`.
  - Verificacion: propietario ve sus documentos y no ve documentos de otra cuenta.

- [ ] T042 Probar reemplazo de documento propio.
  - Depende de: T019, T022-T024.
  - Archivos esperados: `backend/apps/documentos/tests/test_documentos_api.py`.
  - Verificacion: `PATCH /api/documentos/{id}/` actualiza metadata y vuelve a estado `PENDIENTE`.

- [ ] T043 Probar acceso cruzado denegado.
  - Depende de: T021-T024.
  - Archivos esperados: `backend/apps/documentos/tests/test_documentos_permissions.py`.
  - Verificacion: propietario A no puede reemplazar ni consultar detalle de documento de propietario B.

- [ ] T044 Probar validacion administrativa.
  - Depende de: T020-T024.
  - Archivos esperados: `backend/apps/documentos/tests/test_documentos_permissions.py`.
  - Verificacion: administrador puede aprobar/rechazar; propietario no puede validar; anonimo recibe 401.

- [ ] T045 Probar registro propietario sigue funcionando.
  - Depende de: T029 o backend existente de 003.
  - Archivos esperados: tests existentes de `usuarios` o nuevo test de integracion.
  - Verificacion: `POST /api/auth/register/` permite `PROPIETARIO` y no permite `ADMINISTRADOR`; no se cambia semantica JWT.

## Fase 7: Pruebas frontend

- [ ] T046 Configurar tests frontend si faltan.
  - Depende de: T003.
  - Archivos esperados: setup de test en `frontend-web` solo si no existe.
  - Verificacion: comando de test corre sin backend real mediante mocks.

- [ ] T047 Probar servicio de documentos.
  - Depende de: T027.
  - Archivos esperados: tests de `documentoService`.
  - Verificacion: usa endpoints centralizados, envia `FormData` y maneja errores 400/401/403.

- [ ] T048 Probar validacion cliente de archivo.
  - Depende de: T028.
  - Archivos esperados: tests de `documentoValidation`.
  - Verificacion: extension y tamano se validan antes de llamar API.

- [ ] T049 Probar registro de propietario con feedback.
  - Depende de: T029-T031.
  - Archivos esperados: tests de `RegisterView` o flujo equivalente.
  - Verificacion: muestra loading, exito, error de archivo invalido y siguiente paso de documento.

- [ ] T050 Probar ruta privada de documento.
  - Depende de: T034.
  - Archivos esperados: tests de router/ProtectedRoute.
  - Verificacion: sin sesion redirige a login; conductor/admin no entra a flujo propietario salvo reglas explicitadas.

## Fase 8: Verificacion final

- [ ] T051 Ejecutar checks backend.
  - Depende de: T010-T045.
  - Verificacion: `python manage.py check` pasa.

- [ ] T052 Ejecutar migraciones/check backend.
  - Depende de: T013.
  - Verificacion: `python manage.py makemigrations --check` no deja cambios pendientes y `python manage.py migrate` aplica correctamente.

- [ ] T053 Ejecutar tests backend.
  - Depende de: T037-T045.
  - Verificacion: `pytest` pasa para documentos, usuarios y permisos relacionados.

- [ ] T054 Ejecutar build/tests frontend.
  - Depende de: T046-T050.
  - Verificacion: `npm run build` pasa y tests frontend pasan si fueron configurados.

- [ ] T055 Ejecutar smoke local o Docker Compose.
  - Depende de: T051-T054.
  - Verificacion: backend y frontend levantan; un propietario puede registrarse, iniciar sesion, subir documento valido y ver estado pendiente.

- [ ] T056 Revisar seguridad de archivos y secretos.
  - Depende de: T051-T055.
  - Verificacion: no hay documentos reales, tokens, credenciales ni `.env` versionados; storage usa placeholders y configuracion.

- [ ] T057 Revisar alcance prohibido.
  - Depende de: T051-T056.
  - Verificacion: no se modifico logica JWT salvo correccion justificada; no hay implementacion de parqueaderos, tarifas, horarios, espacios, mapas ni WebSocket.

- [ ] T058 Revisar arquitectura por capas.
  - Depende de: T051-T057.
  - Verificacion: controllers delegan en services; services usan repositories/storage; repositories consultan models; frontend services no contienen HTML.

## Dependencias sugeridas

- T001-T005 antes de cualquier implementacion.
- Storage T006-T009 antes de servicios de subida/reemplazo.
- Modelo y migraciones T010-T013 antes de serializers, repositories y endpoints.
- Backend endpoints T014-T025 antes de pruebas backend de API.
- Frontend service T026-T028 antes de vistas y feedback.
- Vistas T029-T036 antes de pruebas frontend.
- Verificacion final T051-T058 solo despues de backend y frontend.

## Paralelizacion segura

- T001, T002 y T003 pueden hacerse en paralelo.
- T006-T009 puede avanzar en paralelo con T026-T028 despues de fijar contrato y limites.
- T014-T016 puede avanzar en paralelo con T017 si el modelo final esta acordado.
- T037-T038 pueden escribirse en paralelo con T039-T045 usando fixtures/mocks.
- T047-T050 pueden escribirse en paralelo cuando servicios y rutas frontend esten disponibles.

