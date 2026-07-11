# Tasks: 005-parqueadero-configuracion-general

**Feature**: Parqueadero - configuracion general  
**Ruta solicitada**: `specs/005-parqueadero-configuracion-general/`  
**Fuente funcional usada**: `specs/007-parqueadero-configuracion-estado/spec.md`, `plan.md`, `data-model.md`, `contracts/openapi.yaml`; base de dominio existente en `backend/apps/parqueaderos`.  
**Alcance**: crear parqueadero, editar datos generales, direccion, ubicacion, estado general abierto/cerrado/lleno segun modelo definido, endpoint `mios` y permisos de propietario.

## Formato

- `[ ] T###` tarea secuencial.
- `[P]` puede ejecutarse en paralelo cuando sus archivos no dependen de otra tarea pendiente.
- Cada tarea debe cerrar con evidencia de verificacion en la nota del agente.

## Reglas de ejecucion

- Depende de autenticacion y roles ya implementados; reutilizar JWT, `get_request_cuenta`, `IsPropietario` y guards existentes.
- No modificar la logica JWT salvo bloqueo comprobado.
- No duplicar `Parqueadero`, `Direccion`, `Ubicacion`, `Cuenta` ni `Rol`.
- Mantener arquitectura backend por capas: controller -> service -> repository -> model.
- No poner reglas de negocio en `urls.py`, controllers ni componentes visuales.
- Todo endpoint de gestion de parqueaderos debe exigir usuario autenticado con rol `PROPIETARIO`.
- El propietario solo puede listar, editar y cambiar estado de sus propios parqueaderos.
- Los errores visibles deben estar en espanol y sugerir una accion correctiva.
- No implementar tarifas, horarios, espacios, WebSocket ni mapa publico.
- No exponer endpoint publico de busqueda ni datos de parqueaderos para usuarios anonimos en esta feature.

## Contratos objetivo

- `POST /api/parqueaderos/` crea un parqueadero para el propietario autenticado.
- `GET /api/parqueaderos/mios/` lista parqueaderos del propietario autenticado.
- `PATCH /api/parqueaderos/{id}/` edita datos generales, direccion y ubicacion de un parqueadero propio.
- `PATCH /api/parqueaderos/{id}/estado/` cambia estado general de un parqueadero propio.

## Estados objetivo

El modelo actual define `DisponibilidadParqueadero` como:

- `DISPONIBLE`: representa abierto/disponible para atencion.
- `CERRADO`: representa cerrado.
- `LLENO`: representa lleno.

No renombrar el catalogo sin migracion justificada. En UI se puede mostrar `Abierto`, `Cerrado` y `Lleno` mapeando a los codigos existentes.

## Fase 0: Inventario y alineacion

- [ ] T001 Inventariar backend actual de `backend/apps/parqueaderos`.
  - Archivos esperados: no crea archivos.
  - Verificacion: registrar modelos, serializers, repositories, services, migraciones y tests existentes; confirmar que no se duplican `Direccion`, `Ubicacion` ni `Parqueadero`.

- [ ] T002 Inventariar permisos y perfil de usuario propietario.
  - Archivos esperados: no crea archivos.
  - Verificacion: confirmar uso de `apps.usuarios.permissions.get_request_cuenta` y permiso de rol propietario; no modificar JWT.

- [ ] T003 Inventariar frontend propietario existente.
  - Archivos esperados: no crea archivos.
  - Verificacion: identificar `PropietarioView`, `endpoints.ts`, cliente API, store de sesion y rutas protegidas.

- [ ] T004 Crear contrato local de parqueaderos.
  - Archivos esperados: `specs/005-parqueadero-configuracion-general/contracts/openapi.yaml`.
  - Verificacion: documenta crear, `mios`, editar y estado; no documenta tarifas, horarios, espacios, WebSocket ni mapa publico.

- [ ] T005 Definir payload anidado de direccion y ubicacion.
  - Depende de: T001, T004.
  - Archivos esperados: contrato OpenAPI y/o serializers.
  - Verificacion: payload contiene `nombre`, `direccion.calle_principal`, `direccion.calle_secundaria`, `direccion.nro_lote`, `ubicacion.latitud`, `ubicacion.longitud`, `disponibilidad`.

## Fase 1: Backend serializers y validaciones

- [ ] T006 Revisar catalogos de estado del modelo.
  - Depende de: T001.
  - Archivos esperados: `backend/apps/parqueaderos/models.py` solo si falta algun valor requerido.
  - Verificacion: existen valores para cerrado y lleno; abierto se representa con `DISPONIBLE` o se documenta decision si se agrega `ABIERTO`.

- [ ] T007 Crear serializer de creacion de parqueadero.
  - Depende de: T005.
  - Archivos esperados: `backend/apps/parqueaderos/serializers.py`.
  - Verificacion: acepta datos anidados de direccion y ubicacion; no permite que el cliente asigne `propietario`, `validado` ni campos fuera de alcance.

- [ ] T008 Crear serializer de edicion general.
  - Depende de: T007.
  - Archivos esperados: `backend/apps/parqueaderos/serializers.py`.
  - Verificacion: permite editar nombre, direccion, ubicacion y disponibilidad; no permite editar propietario ni validacion administrativa.

- [ ] T009 Crear serializer de cambio de estado general.
  - Depende de: T006.
  - Archivos esperados: `backend/apps/parqueaderos/serializers.py`.
  - Verificacion: acepta solo `DISPONIBLE`, `CERRADO`, `LLENO` o catalogo vigente; devuelve error en espanol ante estado invalido.

- [ ] T010 Ajustar serializer de lectura.
  - Depende de: T007-T009.
  - Archivos esperados: `backend/apps/parqueaderos/serializers.py`.
  - Verificacion: devuelve id, nombre, estado, validado, disponibilidad, direccion, ubicacion y fechas utiles; no incluye tarifas, horarios ni espacios.

- [ ] T011 Validar coordenadas en payload de API.
  - Depende de: T007-T008.
  - Archivos esperados: serializers o service.
  - Verificacion: latitud fuera de `-90..90` y longitud fuera de `-180..180` devuelven 400 con mensaje en espanol.

## Fase 2: Backend repositorios y servicios

- [ ] T012 Ampliar repositorio de parqueaderos para propiedad.
  - Depende de: T001.
  - Archivos esperados: `backend/apps/parqueaderos/repositories.py`.
  - Verificacion: incluye `get_by_id_for_propietario` y `filter_by_propietario` ordenado de forma estable.

- [ ] T013 Crear servicio de creacion transaccional.
  - Depende de: T007, T012.
  - Archivos esperados: `backend/apps/parqueaderos/services.py`.
  - Verificacion: crea `Direccion`, `Ubicacion` y `Parqueadero` en una transaccion; asigna propietario desde `request.user`/cuenta; no permite propietario enviado por cliente.

- [ ] T014 Crear servicio de edicion general transaccional.
  - Depende de: T008, T012.
  - Archivos esperados: `backend/apps/parqueaderos/services.py`.
  - Verificacion: actualiza parqueadero propio, direccion y ubicacion; falla con mensaje accionable si no existe o no pertenece al propietario.

- [ ] T015 Crear servicio de cambio de estado general.
  - Depende de: T009, T012.
  - Archivos esperados: `backend/apps/parqueaderos/services.py`.
  - Verificacion: cambia solo disponibilidad general; no modifica espacios ni emite eventos WebSocket.

- [ ] T016 Mantener `validado` fuera del flujo propietario.
  - Depende de: T013-T015.
  - Archivos esperados: tests o services.
  - Verificacion: crear/editar no permite marcar `validado=True`; la validacion administrativa queda fuera de alcance.

## Fase 3: Backend permisos y endpoints

- [ ] T017 Crear o reutilizar permiso de propietario.
  - Depende de: T002.
  - Archivos esperados: `backend/apps/parqueaderos/permissions.py` o reutilizacion explicita de `apps/usuarios/permissions.py`.
  - Verificacion: solo rol `PROPIETARIO` accede a endpoints de gestion; conductor, administrador sin regla explicita y anonimo no crean/editar parqueaderos.

- [ ] T018 Crear controller de parqueaderos.
  - Depende de: T013-T017.
  - Archivos esperados: `backend/apps/parqueaderos/controllers.py` o `views.py`.
  - Verificacion: controller valida serializers, aplica permisos y delega en services; no contiene writes manuales de modelos.

- [ ] T019 Implementar `POST /api/parqueaderos/`.
  - Depende de: T018.
  - Archivos esperados: controller y urls.
  - Verificacion: propietario autenticado crea parqueadero con direccion y ubicacion; devuelve 201 y serializer de lectura.

- [ ] T020 Implementar `GET /api/parqueaderos/mios/`.
  - Depende de: T018.
  - Archivos esperados: controller y urls.
  - Verificacion: devuelve solo parqueaderos del propietario autenticado; anonimo recibe 401.

- [ ] T021 Implementar `PATCH /api/parqueaderos/{id}/`.
  - Depende de: T018.
  - Archivos esperados: controller y urls.
  - Verificacion: propietario edita solo parqueadero propio; acceso cruzado devuelve 403 o 404 sin filtrar informacion sensible.

- [ ] T022 Implementar `PATCH /api/parqueaderos/{id}/estado/`.
  - Depende de: T018.
  - Archivos esperados: controller y urls.
  - Verificacion: cambia disponibilidad entre `DISPONIBLE`, `CERRADO`, `LLENO`; no toca tarifas, horarios, espacios ni WebSocket.

- [ ] T023 Registrar urls de parqueaderos.
  - Depende de: T019-T022.
  - Archivos esperados: `backend/apps/parqueaderos/urls.py`, `backend/backend/urls.py`.
  - Verificacion: `urls.py` solo registra rutas bajo `/api/parqueaderos/`.

- [ ] T024 Actualizar contrato OpenAPI local.
  - Depende de: T019-T023.
  - Archivos esperados: `specs/005-parqueadero-configuracion-general/contracts/openapi.yaml`.
  - Verificacion: contrato refleja payloads/respuestas reales y errores 400/401/403/404.

## Fase 4: Frontend servicios y estado

- [ ] T025 Centralizar endpoints de parqueaderos.
  - Depende de: T004.
  - Archivos esperados: `frontend-web/src/config/endpoints.ts`.
  - Verificacion: contiene `parqueaderos.create`, `parqueaderos.mios`, `parqueaderos.detail(id)`, `parqueaderos.estado(id)`; las vistas no construyen URLs manualmente.

- [ ] T026 Crear servicio frontend de parqueaderos.
  - Depende de: T025.
  - Archivos esperados: `frontend-web/src/services/parqueaderoService.ts`.
  - Verificacion: implementa crear, listar mios, editar y cambiar estado; usa cliente API autenticado y no contiene HTML.

- [ ] T027 Crear validacion cliente para formulario general.
  - Depende de: T026.
  - Archivos esperados: `frontend-web/src/services/parqueaderoValidation.ts` o helper equivalente.
  - Verificacion: valida nombre requerido, direccion requerida y coordenadas numericas en rango; backend sigue siendo fuente final.

- [ ] T028 Definir etiquetas UI de disponibilidad.
  - Depende de: T006.
  - Archivos esperados: `frontend-web/src/config/parqueaderoEstados.ts` o dentro del servicio/config.
  - Verificacion: `DISPONIBLE -> Abierto`, `CERRADO -> Cerrado`, `LLENO -> Lleno`; no introduce estados inexistentes.

## Fase 5: Frontend pantalla propietario

- [ ] T029 Crear componente de formulario de parqueadero.
  - Depende de: T026-T028.
  - Archivos esperados: `frontend-web/src/components/parqueaderos/ParqueaderoForm.tsx`.
  - Verificacion: permite crear/editar nombre, direccion, ubicacion y disponibilidad; no muestra tarifas, horarios ni espacios.

- [ ] T030 Crear componente de selector de estado general.
  - Depende de: T028.
  - Archivos esperados: `frontend-web/src/components/parqueaderos/EstadoGeneralControl.tsx`.
  - Verificacion: permite abierto/cerrado/lleno segun catalogo; muestra loading, exito y error claro.

- [ ] T031 Integrar listado `mios` en panel propietario.
  - Depende de: T026.
  - Archivos esperados: `frontend-web/src/views/private/PropietarioView.tsx` o vista especifica protegida.
  - Verificacion: propietario ve sus parqueaderos; si no tiene, ve accion para crear; no se muestra mapa publico.

- [ ] T032 Integrar creacion de parqueadero en UI.
  - Depende de: T029, T031.
  - Archivos esperados: `PropietarioView.tsx` o vista de configuracion general.
  - Verificacion: formulario crea parqueadero y actualiza listado con mensaje de exito.

- [ ] T033 Integrar edicion de datos generales.
  - Depende de: T029, T031.
  - Archivos esperados: vista/controlador frontend.
  - Verificacion: propietario puede editar nombre, direccion y ubicacion; errores se muestran en espanol.

- [ ] T034 Integrar cambio de estado general.
  - Depende de: T030-T031.
  - Archivos esperados: vista/controlador frontend.
  - Verificacion: cambio a abierto/cerrado/lleno actualiza UI; no invoca endpoints de espacios ni WebSocket.

- [ ] T035 Mantener ruta protegida de propietario.
  - Depende de: T031-T034.
  - Archivos esperados: `frontend-web/src/main.tsx`, `frontend-web/src/config/routes.ts` solo si requiere ajuste.
  - Verificacion: usuario sin sesion redirige a login; usuario no propietario no accede al flujo.

## Fase 6: Pruebas backend

- [ ] T036 Probar creacion de parqueadero por propietario.
  - Depende de: T019.
  - Archivos esperados: `backend/apps/parqueaderos/tests/test_parqueaderos_api.py`.
  - Verificacion: crea `Direccion`, `Ubicacion`, `Parqueadero`; propietario se toma del token; `validado` queda `False`.

- [ ] T037 Probar creacion sin sesion.
  - Depende de: T019.
  - Archivos esperados: `backend/apps/parqueaderos/tests/test_parqueaderos_api.py`.
  - Verificacion: anonimo recibe 401.

- [ ] T038 Probar creacion con rol no propietario.
  - Depende de: T017-T019.
  - Archivos esperados: tests de permisos.
  - Verificacion: conductor no crea parqueadero; respuesta 403 con mensaje en espanol.

- [ ] T039 Probar `GET /api/parqueaderos/mios/`.
  - Depende de: T020.
  - Archivos esperados: `backend/apps/parqueaderos/tests/test_parqueaderos_api.py`.
  - Verificacion: propietario solo recibe sus parqueaderos.

- [ ] T040 Probar edicion general propia.
  - Depende de: T021.
  - Archivos esperados: tests de API.
  - Verificacion: cambia nombre, direccion y ubicacion del parqueadero propio.

- [ ] T041 Probar acceso cruzado denegado.
  - Depende de: T021-T022.
  - Archivos esperados: `backend/apps/parqueaderos/tests/test_parqueaderos_permissions.py`.
  - Verificacion: propietario A no edita ni cambia estado del parqueadero de propietario B.

- [ ] T042 Probar cambio de estado general.
  - Depende de: T022.
  - Archivos esperados: tests de API.
  - Verificacion: acepta `DISPONIBLE`, `CERRADO`, `LLENO`; rechaza estado invalido.

- [ ] T043 Probar validaciones de ubicacion por API.
  - Depende de: T011, T019-T021.
  - Archivos esperados: tests de API.
  - Verificacion: coordenadas fuera de rango devuelven 400.

- [ ] T044 Probar que no se implementan relaciones fuera de alcance.
  - Depende de: T019-T022.
  - Archivos esperados: tests o revision documentada.
  - Verificacion: respuestas no incluyen tarifas, horarios, espacios ni eventos WebSocket.

## Fase 7: Pruebas frontend

- [ ] T045 Configurar tests frontend si faltan.
  - Depende de: T003.
  - Archivos esperados: setup de test en `frontend-web` solo si no existe.
  - Verificacion: comando de test corre con mocks sin backend real.

- [ ] T046 Probar servicio frontend de parqueaderos.
  - Depende de: T026.
  - Archivos esperados: tests de `parqueaderoService`.
  - Verificacion: usa endpoints centralizados y maneja 400/401/403.

- [ ] T047 Probar validacion cliente del formulario.
  - Depende de: T027.
  - Archivos esperados: tests de `parqueaderoValidation`.
  - Verificacion: campos requeridos y coordenadas invalidas fallan antes de enviar.

- [ ] T048 Probar formulario de creacion/edicion.
  - Depende de: T029, T032-T033.
  - Archivos esperados: tests de componente/vista.
  - Verificacion: muestra errores claros, loading y exito.

- [ ] T049 Probar control de estado general.
  - Depende de: T030, T034.
  - Archivos esperados: tests de componente/vista.
  - Verificacion: abierto/cerrado/lleno llaman al endpoint correcto y actualizan UI.

- [ ] T050 Probar ruta protegida de propietario.
  - Depende de: T035.
  - Archivos esperados: tests de router/ProtectedRoute si existe setup.
  - Verificacion: sin sesion redirige a `/login`; conductor no entra al flujo de configuracion.

## Fase 8: Verificacion final

- [ ] T051 Ejecutar checks backend.
  - Depende de: T006-T044.
  - Verificacion: `python manage.py check` pasa.

- [ ] T052 Ejecutar migraciones/check backend.
  - Depende de: T006-T044.
  - Verificacion: `python manage.py makemigrations --check` no deja cambios pendientes y `python manage.py migrate` aplica correctamente.

- [ ] T053 Ejecutar tests backend.
  - Depende de: T036-T044.
  - Verificacion: `pytest` pasa para parqueaderos, usuarios y tests existentes.

- [ ] T054 Ejecutar build/tests frontend.
  - Depende de: T045-T050.
  - Verificacion: `npm run build` pasa y tests frontend pasan si fueron configurados.

- [ ] T055 Ejecutar smoke local o Docker Compose.
  - Depende de: T051-T054.
  - Verificacion: backend y frontend levantan; propietario crea parqueadero, lo ve en `mios`, edita datos y cambia estado.

- [ ] T056 Revisar seguridad y permisos.
  - Depende de: T051-T055.
  - Verificacion: no hay acceso anonimo ni acceso cruzado; no se exponen secretos ni datos fuera de alcance.

- [ ] T057 Revisar alcance prohibido.
  - Depende de: T051-T056.
  - Verificacion: no hay cambios de tarifas, horarios, espacios, WebSocket ni mapa publico.

- [ ] T058 Revisar arquitectura por capas.
  - Depende de: T051-T057.
  - Verificacion: controllers delegan en services; services usan repositories/modelos; frontend services no contienen HTML; vistas no construyen URLs manualmente.

## Dependencias sugeridas

- T001-T005 antes de cualquier implementacion.
- Serializers T006-T011 antes de services y controllers.
- Repositories/services T012-T016 antes de endpoints.
- Endpoints T017-T024 antes de pruebas backend de API.
- Frontend service/config T025-T028 antes de componentes y vistas.
- UI T029-T035 antes de pruebas frontend.
- Verificacion final T051-T058 solo despues de backend y frontend.

## Paralelizacion segura

- T001, T002 y T003 pueden hacerse en paralelo.
- T004-T005 pueden avanzar mientras se inventarian capas existentes.
- T025-T028 pueden avanzar en paralelo con T006-T016 cuando el contrato queda acordado.
- T036-T044 pueden escribirse por endpoint/permiso en paralelo despues de T017-T024.
- T046-T050 pueden escribirse en paralelo cuando servicios y componentes frontend esten disponibles.

