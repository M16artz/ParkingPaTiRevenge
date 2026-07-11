# Tasks: 002-backend-dominio-base

**Feature**: Backend base de dominio  
**Ruta solicitada**: `specs/002-backend-dominio-base/`  
**Fuente tecnica usada**: `specs/002-backend-dominio-base-api/spec.md`, `plan.md`, `data-model.md` y `contracts/openapi.yaml`  
**Alcance**: crear la base de dominio del backend sin UI, sin WebSocket y sin busqueda por mapa. Las tareas deben respetar la arquitectura por capas: controller -> service -> repository -> model.

## Formato

- `[ ] T###` tarea secuencial.
- `[P]` puede ejecutarse en paralelo cuando sus archivos no dependen de otra tarea pendiente.
- Cada tarea debe cerrar con evidencia de verificacion en la nota del agente.

## Reglas de ejecucion

- No implementar pantallas frontend ni modificar `frontend-web/`.
- No implementar WebSocket, consumers, routing WS, signals de tiempo real ni pruebas WS.
- No implementar busqueda por mapa, cercania, Nominatim, tiles ni calculo de distancia.
- No duplicar entidades existentes: si una app, modelo, migracion, serializer, servicio o repositorio ya existe, extenderlo de forma compatible.
- Mantener microdominios separados y capas claras: `controllers`/views solo orquestan, `services` contienen reglas de aplicacion, `repositories` encapsulan consultas, `models` contienen persistencia e invariantes simples.
- Los errores visibles deben estar en espanol y sugerir accion correctiva.
- No versionar `.env`, credenciales, tokens, documentos reales ni archivos generados pesados.
- Los endpoints privados deben quedar protegidos por defecto si se agregan controllers; los endpoints completos de autenticacion pueden planificarse, pero no son obligatorios para cerrar esta base de dominio.

## Fase 0: Inventario y preparacion

- [ ] T001 Inventariar el backend actual antes de crear archivos.
  - Archivos esperados: no crea archivos.
  - Verificacion: registrar apps existentes bajo `backend/`, modelos existentes, migraciones existentes y rutas importables para evitar duplicados.

- [ ] T002 Confirmar el namespace objetivo para apps de dominio.
  - Archivos esperados: no crea archivos o nota corta en la evidencia del agente.
  - Verificacion: decidir entre `backend/apps/<app>/` o estructura existente equivalente; la decision debe respetar imports actuales y no romper `manage.py check`.

- [ ] T003 Actualizar dependencias backend solo si falta soporte necesario para dominio.
  - Archivos esperados: `backend/requirements/base.txt`, `backend/requirements/development.txt` si aplica.
  - Verificacion: dependencias requeridas para DRF, pytest, SimpleJWT y drf-spectacular estan presentes o se documenta que ya existian.

- [ ] T004 Registrar las apps de dominio en settings sin activar logica fuera de alcance.
  - Depende de: T002.
  - Archivos esperados: `backend/backend/settings/base.py` o settings equivalente.
  - Verificacion: `python manage.py check` carga todas las apps sin errores.

## Fase 1: Usuarios y seguridad

- [ ] T005 Crear o adaptar la app `usuarios` para identidad y acceso.
  - Depende de: T001-T004.
  - Archivos esperados: `backend/apps/usuarios/apps.py` o ruta equivalente.
  - Verificacion: la app existe, esta registrada y no duplica una app previa de usuarios.

- [ ] T006 Crear modelos base `Persona`, `Rol` y `Cuenta` o mapearlos a modelos existentes.
  - Depende de: T005.
  - Archivos esperados: `backend/apps/usuarios/models.py` o modelos equivalentes.
  - Verificacion: `Persona` incluye nombre, apellido, tipo_identificacion, identificacion y estado; `Cuenta` incluye persona, username, correo, rol, estado y password_hash o integracion documentada con el usuario de Django; `Rol` cubre al menos `ADMINISTRADOR`, `PROPIETARIO` y `CONDUCTOR`.

- [ ] T007 Agregar managers, validaciones e indices minimos de usuarios.
  - Depende de: T006.
  - Archivos esperados: `models.py` o modulo de managers del microdominio.
  - Verificacion: identificacion, username y correo tienen unicidad o restriccion documentada; estados usan catalogo controlado.

- [ ] T008 Crear repositorio de usuarios.
  - Depende de: T006.
  - Archivos esperados: `backend/apps/usuarios/repositories.py`.
  - Verificacion: incluye metodos de lectura por id, username/correo y filtros por rol/estado sin exponer `request.data`.

- [ ] T009 Crear servicio base de usuarios/seguridad.
  - Depende de: T008.
  - Archivos esperados: `backend/apps/usuarios/services.py`.
  - Verificacion: el servicio orquesta creacion/consulta basica y devuelve errores en espanol para datos invalidos.

- [ ] T010 Crear serializers base de usuarios.
  - Depende de: T006.
  - Archivos esperados: `backend/apps/usuarios/serializers.py`.
  - Verificacion: serializers separan lectura y escritura; campos sensibles como password_hash no se exponen en lectura.

- [ ] T011 Crear permisos base de seguridad.
  - Depende de: T006.
  - Archivos esperados: `backend/apps/usuarios/permissions.py` o `backend/apps/common/permissions.py`.
  - Verificacion: existen permisos reutilizables para autenticado, administrador y propietario del recurso.

## Fase 2: Parqueaderos y configuracion

- [ ] T012 Crear o adaptar la app `parqueaderos`.
  - Depende de: T001-T004.
  - Archivos esperados: `backend/apps/parqueaderos/apps.py` o ruta equivalente.
  - Verificacion: la app existe, esta registrada y no duplica entidades previas.

- [ ] T013 Crear modelos base `Direccion`, `Ubicacion` y `Parqueadero`.
  - Depende de: T012.
  - Archivos esperados: `backend/apps/parqueaderos/models.py`.
  - Verificacion: `Parqueadero` incluye nombre, estado, validado, disponibilidad, direccion y ubicacion; `Direccion` incluye calle_principal, calle_secundaria y nro_lote; `Ubicacion` incluye latitud y longitud.

- [ ] T014 Agregar validaciones e indices de parqueaderos.
  - Depende de: T013.
  - Archivos esperados: `backend/apps/parqueaderos/models.py`.
  - Verificacion: coordenadas validan rangos; hay indices para estado, validado, disponibilidad y nombre o busqueda textual simple sin implementar cercania.

- [ ] T015 Crear repositorio de parqueaderos.
  - Depende de: T013.
  - Archivos esperados: `backend/apps/parqueaderos/repositories.py`.
  - Verificacion: incluye consultas por propietario/cuenta, estado, validado y disponibilidad; no contiene logica de permisos de controller.

- [ ] T016 Crear servicio base de parqueaderos/configuracion.
  - Depende de: T015.
  - Archivos esperados: `backend/apps/parqueaderos/services.py`.
  - Verificacion: valida configuracion basica del parqueadero y centraliza errores de dominio en espanol.

- [ ] T017 Crear serializers base de parqueaderos.
  - Depende de: T013.
  - Archivos esperados: `backend/apps/parqueaderos/serializers.py`.
  - Verificacion: serializers de lectura y escritura no permiten modificar campos administrativos sin permiso.

## Fase 3: Espacios

- [ ] T018 Crear o adaptar la app `espacios`.
  - Depende de: T001-T004, T013.
  - Archivos esperados: `backend/apps/espacios/apps.py` o ruta equivalente.
  - Verificacion: la app existe y no contiene WebSocket ni publicacion de eventos.

- [ ] T019 Crear modelo `Espacio`.
  - Depende de: T018.
  - Archivos esperados: `backend/apps/espacios/models.py`.
  - Verificacion: incluye parqueadero, numero_espacio y estado; tiene unicidad por `(parqueadero, numero_espacio)`.

- [ ] T020 Agregar indices y catalogo de estados de espacios.
  - Depende de: T019.
  - Archivos esperados: `backend/apps/espacios/models.py`.
  - Verificacion: existe indice compuesto por `(parqueadero, estado)`; estados se limitan a catalogo controlado.

- [ ] T021 Crear repositorio de espacios.
  - Depende de: T019.
  - Archivos esperados: `backend/apps/espacios/repositories.py`.
  - Verificacion: incluye consultas por parqueadero, estado y numero_espacio.

- [ ] T022 Crear servicio base de espacios sin tiempo real.
  - Depende de: T021.
  - Archivos esperados: `backend/apps/espacios/services.py`.
  - Verificacion: permite validar cambio de estado a nivel de dominio, pero no publica eventos WebSocket.

- [ ] T023 Crear serializers base de espacios.
  - Depende de: T019.
  - Archivos esperados: `backend/apps/espacios/serializers.py`.
  - Verificacion: serializers separan campos de lectura y escritura; no aceptan cambio de parqueadero cruzado sin pasar por servicio.

## Fase 4: Horarios

- [ ] T024 Crear o adaptar la app `horarios`.
  - Depende de: T001-T004, T013.
  - Archivos esperados: `backend/apps/horarios/apps.py` o ruta equivalente.
  - Verificacion: la app existe y esta registrada.

- [ ] T025 Crear modelo `HorarioAtencion`.
  - Depende de: T024.
  - Archivos esperados: `backend/apps/horarios/models.py`.
  - Verificacion: incluye parqueadero, dia, hora_apertura y hora_cierre; tiene unicidad por `(parqueadero, dia)`.

- [ ] T026 Agregar validaciones de horarios.
  - Depende de: T025.
  - Archivos esperados: `backend/apps/horarios/models.py` o `services.py`.
  - Verificacion: hora_apertura debe ser anterior a hora_cierre salvo regla futura documentada; dia pertenece a catalogo controlado.

- [ ] T027 Crear repositorio de horarios.
  - Depende de: T025.
  - Archivos esperados: `backend/apps/horarios/repositories.py`.
  - Verificacion: incluye consultas por parqueadero y dia.

- [ ] T028 Crear servicio base de horarios.
  - Depende de: T027.
  - Archivos esperados: `backend/apps/horarios/services.py`.
  - Verificacion: centraliza validacion de rangos y duplicados con mensajes en espanol.

- [ ] T029 Crear serializers base de horarios.
  - Depende de: T025.
  - Archivos esperados: `backend/apps/horarios/serializers.py`.
  - Verificacion: serializers validan formato y no duplican reglas que pertenecen al servicio.

## Fase 5: Tarifas

- [ ] T030 Crear o adaptar la app `tarifas`.
  - Depende de: T001-T004, T013.
  - Archivos esperados: `backend/apps/tarifas/apps.py` o ruta equivalente.
  - Verificacion: la app existe y esta registrada.

- [ ] T031 Crear modelo `CategoriaTarifa` con enum `TipoCategoriaTarifa`.
  - Depende de: T030.
  - Archivos esperados: `backend/apps/tarifas/models.py`.
  - Verificacion: usa categorias `GENERAL`, `PREFERENCIAL` y `PESADOS`; incluye parqueadero y precio_hora.

- [ ] T032 Agregar restricciones e indices de tarifas.
  - Depende de: T031.
  - Archivos esperados: `backend/apps/tarifas/models.py`.
  - Verificacion: existe unicidad por `(parqueadero, codigo)`, indice compuesto por `(parqueadero, codigo)` y validacion de precio_hora positivo.

- [ ] T033 Crear repositorio de tarifas.
  - Depende de: T031.
  - Archivos esperados: `backend/apps/tarifas/repositories.py`.
  - Verificacion: incluye consultas por parqueadero, codigo y listado activo/base.

- [ ] T034 Crear servicio base de tarifas.
  - Depende de: T033.
  - Archivos esperados: `backend/apps/tarifas/services.py`.
  - Verificacion: valida categorias duplicadas y montos positivos con errores en espanol.

- [ ] T035 Crear serializers base de tarifas.
  - Depende de: T031.
  - Archivos esperados: `backend/apps/tarifas/serializers.py`.
  - Verificacion: serializers usan Decimal para dinero y no aceptan valores negativos.

## Fase 6: Documentos

- [ ] T036 Crear o adaptar la app `documentos`.
  - Depende de: T001-T004, T006.
  - Archivos esperados: `backend/apps/documentos/apps.py` o ruta equivalente.
  - Verificacion: la app existe y no almacena documentos reales en el repo.

- [ ] T037 Crear modelo `Documento`.
  - Depende de: T036.
  - Archivos esperados: `backend/apps/documentos/models.py`.
  - Verificacion: incluye cuenta o propietario relacionado, es_valido, fecha_expiracion, ruta y file_id; no guarda binarios en base de datos.

- [ ] T038 Agregar restricciones de documento vigente.
  - Depende de: T037.
  - Archivos esperados: `backend/apps/documentos/models.py`.
  - Verificacion: existe restriccion o validacion para un documento vigente por cuenta en el MVP, o queda documentada la razon tecnica si se pospone.

- [ ] T039 Crear repositorio de documentos.
  - Depende de: T037.
  - Archivos esperados: `backend/apps/documentos/repositories.py`.
  - Verificacion: incluye consultas por cuenta, vigencia y estado de validacion.

- [ ] T040 Crear servicio base de documentos.
  - Depende de: T039.
  - Archivos esperados: `backend/apps/documentos/services.py`.
  - Verificacion: valida metadata del documento, no manipula archivos reales y usa placeholders/configuracion para storage.

- [ ] T041 Crear serializers base de documentos.
  - Depende de: T037.
  - Archivos esperados: `backend/apps/documentos/serializers.py`.
  - Verificacion: serializers no exponen rutas privadas innecesarias y separan metadata publica/privada.

## Fase 7: Controllers base y rutas internas

- [ ] T042 Crear controllers/ViewSets base por microdominio solo si el contrato de API se mantiene en este entregable.
  - Depende de: T010, T017, T023, T029, T035, T041.
  - Archivos esperados: `controllers.py` o `views.py` por app.
  - Verificacion: controllers delegan en servicios y repositorios; no contienen reglas de negocio ni consultas complejas.

- [ ] T043 Registrar routers/rutas API base sin romper healthcheck ni schema.
  - Depende de: T042.
  - Archivos esperados: `backend/backend/urls.py` o modulo de rutas de apps.
  - Verificacion: toda ruta agregada tiene serializer y permiso por defecto; `python manage.py check` pasa.

- [ ] T044 Actualizar OpenAPI/schema solo para endpoints realmente agregados.
  - Depende de: T042-T043.
  - Archivos esperados: configuracion drf-spectacular o contrato en `specs/002-backend-dominio-base-api/contracts/openapi.yaml` si cambia el alcance.
  - Verificacion: no se documentan endpoints que no existen; schema genera sin errores.

## Fase 8: Migraciones

- [ ] T045 Generar migraciones iniciales por app de dominio.
  - Depende de: modelos cerrados en T006, T013, T019, T025, T031, T037.
  - Archivos esperados: `backend/apps/*/migrations/0001_initial.py` o migraciones equivalentes.
  - Verificacion: migraciones son pequenas, revisables y no mezclan datos con esquema.

- [ ] T046 Revisar migraciones para dependencias cruzadas.
  - Depende de: T045.
  - Archivos esperados: migraciones ajustadas si aplica.
  - Verificacion: dependencias entre usuarios, parqueaderos, espacios, horarios, tarifas y documentos son explicitas y no circulares.

- [ ] T047 Ejecutar `python manage.py makemigrations --check --dry-run`.
  - Depende de: T045-T046.
  - Archivos esperados: no crea archivos nuevos.
  - Verificacion: no quedan cambios de modelo sin migracion.

- [ ] T048 Ejecutar `python manage.py migrate` en entorno de prueba/desarrollo.
  - Depende de: T047.
  - Archivos esperados: no versionar base local.
  - Verificacion: migraciones aplican desde cero sin errores.

## Fase 9: Tests minimos de modelos

- [ ] T049 Crear factories o helpers minimos para pruebas de dominio.
  - Depende de: T045.
  - Archivos esperados: `backend/tests/factories.py` o factories por app.
  - Verificacion: helpers no dependen de endpoints ni UI.

- [ ] T050 Probar modelos de usuarios/seguridad.
  - Depende de: T006, T049.
  - Archivos esperados: `backend/apps/usuarios/tests/test_models.py` o ruta equivalente.
  - Verificacion: prueba unicidad de identificacion/correo/username, catalogo de rol y ocultamiento de datos sensibles en representacion.

- [ ] T051 Probar modelos de parqueaderos/configuracion.
  - Depende de: T013, T049.
  - Archivos esperados: `backend/apps/parqueaderos/tests/test_models.py`.
  - Verificacion: prueba validacion de coordenadas, estado, validado/disponibilidad e indices esperados.

- [ ] T052 Probar modelo `Espacio`.
  - Depende de: T019, T049.
  - Archivos esperados: `backend/apps/espacios/tests/test_models.py`.
  - Verificacion: prueba unicidad por `(parqueadero, numero_espacio)` y catalogo de estado.

- [ ] T053 Probar modelo `HorarioAtencion`.
  - Depende de: T025, T049.
  - Archivos esperados: `backend/apps/horarios/tests/test_models.py`.
  - Verificacion: prueba unicidad por `(parqueadero, dia)` y validacion hora_apertura < hora_cierre.

- [ ] T054 Probar modelo `CategoriaTarifa`.
  - Depende de: T031, T049.
  - Archivos esperados: `backend/apps/tarifas/tests/test_models.py`.
  - Verificacion: prueba unicidad por `(parqueadero, codigo)`, categorias requeridas y precio positivo.

- [ ] T055 Probar modelo `Documento`.
  - Depende de: T037, T049.
  - Archivos esperados: `backend/apps/documentos/tests/test_models.py`.
  - Verificacion: prueba metadata obligatoria, estado de validacion y regla de documento vigente por cuenta si se implemento.

## Fase 10: Verificacion final

- [ ] T056 Ejecutar checks de Django.
  - Depende de: T001-T055.
  - Verificacion: `python manage.py check` termina sin errores.

- [ ] T057 Ejecutar tests minimos de modelos.
  - Depende de: T049-T055.
  - Verificacion: `pytest` pasa para tests de modelos y healthcheck existente.

- [ ] T058 Ejecutar revision de alcance prohibido.
  - Depende de: T001-T057.
  - Verificacion: no hay cambios en `frontend-web/`; no existen consumers/routing WebSocket nuevos; no hay endpoints de cercania/mapa/Nominatim; no se versionan documentos reales.

- [ ] T059 Ejecutar revision de arquitectura por capas.
  - Depende de: T001-T057.
  - Verificacion: controllers no hacen consultas directas complejas; services no importan `request`; repositories no devuelven errores HTTP; models no dependen de serializers/controllers.

- [ ] T060 Ejecutar revision de no duplicacion.
  - Depende de: T001-T057.
  - Verificacion: no existen dos modelos que representen la misma entidad; imports usan una sola fuente canonica por microdominio.

## Dependencias sugeridas

- T001-T004 antes de crear cualquier app o migracion.
- Usuarios/seguridad (T005-T011) antes de documentos (T036-T041).
- Parqueaderos (T012-T017) antes de espacios, horarios y tarifas.
- Modelos completos antes de migraciones.
- Migraciones antes de tests con base de datos.
- Controllers/rutas son opcionales para este alcance y solo deben cerrarse si el equipo decide mantener API base en este entregable.

## Paralelizacion segura

- T005-T011 y T012-T017 pueden avanzar en paralelo despues de T001-T004 si no comparten archivos.
- T018-T023, T024-T029 y T030-T035 pueden avanzar en paralelo despues de cerrar `Parqueadero`.
- T036-T041 puede avanzar en paralelo despues de cerrar `Cuenta`.
- Tests T050-T055 pueden escribirse en paralelo cuando sus modelos y factories esten listos.

