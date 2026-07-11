# Tasks: 003-autenticacion-jwt-roles

**Feature**: Autenticacion JWT y roles  
**Ruta solicitada**: `specs/003-autenticacion-jwt-roles/`  
**Fuente tecnica usada**: `specs/005-auth-roles-dashboard/spec.md`, `plan.md`, `data-model.md` y `contracts/openapi.yaml`; base de dominio esperada en `backend/apps/usuarios`.  
**Alcance**: registro base de cuenta, login JWT, refresh token, roles, redireccion frontend por rol, rutas protegidas, persistencia segura de sesion en frontend y pruebas de permisos.

## Formato

- `[ ] T###` tarea secuencial.
- `[P]` puede ejecutarse en paralelo cuando sus archivos no dependen de otra tarea pendiente.
- Cada tarea debe cerrar con evidencia de verificacion en la nota del agente.

## Reglas de ejecucion

- No implementar subida de documentos.
- No implementar creacion, edicion ni configuracion de parqueaderos.
- No implementar tarifas, horarios ni espacios.
- No implementar WebSocket, consumers, canales ni eventos en tiempo real.
- Mantener arquitectura backend por capas: controller -> service -> repository -> model.
- No poner reglas de negocio en `urls.py` ni en controllers/ViewSets.
- Todo endpoint privado debe exigir autenticacion.
- Los errores visibles deben estar en espanol y sugerir una accion correctiva.
- No guardar secretos reales, `.env`, tokens reales ni credenciales.
- En frontend, no almacenar access token en lugares innecesariamente persistentes; preferir memoria para access y persistencia controlada para refresh/session metadata segun decision documentada.

## Contratos objetivo

- `POST /api/auth/register/` registra una cuenta base.
- `POST /api/auth/token/` autentica credenciales y devuelve tokens.
- `POST /api/auth/refresh/` renueva access token.
- `GET /api/cuentas/me/` devuelve perfil autenticado y rol.

## Roles objetivo

- `ADMINISTRADOR`: acceso a rutas administrativas.
- `PROPIETARIO`: acceso a rutas de propietario.
- `CONDUCTOR`: usuario registrado sin permisos administrativos ni de propietario.
- `ANONIMO`: estado frontend sin sesion; no debe persistirse como rol en backend salvo decision explicita documentada.

## Fase 0: Inventario y alineacion

- [ ] T001 Inventariar implementacion actual de `backend/apps/usuarios`.
  - Archivos esperados: no crea archivos.
  - Verificacion: registrar modelos, serializers, repositories, services, permissions y tests existentes para no duplicar `Persona`, `Cuenta` ni `Rol`.

- [ ] T002 Inventariar frontend actual de autenticacion/rutas.
  - Archivos esperados: no crea archivos.
  - Verificacion: registrar si existen `frontend-web/src/config`, router, store, servicios API y pantallas; no modificar vistas no relacionadas.

- [ ] T003 Confirmar dependencias JWT.
  - Archivos esperados: `backend/requirements/base.txt` si falta dependencia.
  - Verificacion: `djangorestframework-simplejwt` esta instalado/configurado o se agrega sin duplicar dependencia.

- [ ] T004 Definir mapa de redireccion por rol.
  - Archivos esperados: `frontend-web/src/config/routes.ts` o documento/config equivalente.
  - Verificacion: `ADMINISTRADOR -> /admin`, `PROPIETARIO -> /propietario`, `CONDUCTOR -> /`, `ANONIMO -> /login` para rutas protegidas.

## Fase 1: Backend JWT y registro

- [ ] T005 Configurar SimpleJWT con access token de 15 minutos.
  - Depende de: T003.
  - Archivos esperados: `backend/backend/settings/base.py`.
  - Verificacion: `SIMPLE_JWT.ACCESS_TOKEN_LIFETIME` es 15 minutos; refresh tiene duracion definida; no usa secretos hardcodeados distintos de `SECRET_KEY`.

- [ ] T006 Configurar autenticacion DRF por JWT.
  - Depende de: T005.
  - Archivos esperados: `backend/backend/settings/base.py`.
  - Verificacion: `DEFAULT_AUTHENTICATION_CLASSES` incluye JWTAuthentication y permisos por defecto siguen siendo autenticados salvo endpoints publicos explicitos.

- [ ] T007 Crear serializer de registro base.
  - Depende de: T001.
  - Archivos esperados: `backend/apps/usuarios/serializers.py` o `backend/apps/usuarios/auth_serializers.py`.
  - Verificacion: acepta datos minimos de `Persona` y `Cuenta`; permite rol `CONDUCTOR` o `PROPIETARIO` segun flujo base; no permite registrar `ADMINISTRADOR` desde endpoint publico.

- [ ] T008 Crear servicio de registro de cuenta.
  - Depende de: T007.
  - Archivos esperados: `backend/apps/usuarios/services.py` o `backend/apps/usuarios/auth_services.py`.
  - Verificacion: crea `Persona` y `Cuenta` transaccionalmente; hashea password; inicializa rol permitido; errores de duplicado se devuelven en espanol.

- [ ] T009 Crear repositorio auxiliar de autenticacion si falta.
  - Depende de: T001.
  - Archivos esperados: `backend/apps/usuarios/repositories.py`.
  - Verificacion: permite buscar cuenta por username/correo y rol sin acceder a `request`.

- [ ] T010 Crear serializer/token claims con datos de rol.
  - Depende de: T005, T001.
  - Archivos esperados: `backend/apps/usuarios/serializers.py` o `auth_serializers.py`.
  - Verificacion: token incluye `cuenta_id` y `rol` o la respuesta del login incluye perfil suficiente para redireccion; no expone `password_hash`.

- [ ] T011 Crear endpoint/controller de registro.
  - Depende de: T008.
  - Archivos esperados: `backend/apps/usuarios/controllers.py` o `views.py`, `backend/apps/usuarios/urls.py`.
  - Verificacion: controller delega al servicio; endpoint es publico; no contiene reglas de negocio ni writes manuales fuera del servicio.

- [ ] T012 Crear endpoints de login y refresh JWT.
  - Depende de: T005, T010.
  - Archivos esperados: `backend/apps/usuarios/controllers.py` o `views.py`, `backend/apps/usuarios/urls.py`.
  - Verificacion: `POST /api/auth/token/` y `POST /api/auth/refresh/` responden segun contrato; errores invalidos en espanol.

- [ ] T013 Crear endpoint `GET /api/cuentas/me/`.
  - Depende de: T001, T006.
  - Archivos esperados: `backend/apps/usuarios/controllers.py` o `views.py`, serializer de perfil.
  - Verificacion: requiere JWT valido; devuelve id, username/correo seguro y rol; no expone password_hash.

- [ ] T014 Registrar rutas de autenticacion.
  - Depende de: T011-T013.
  - Archivos esperados: `backend/backend/urls.py`, `backend/apps/usuarios/urls.py`.
  - Verificacion: `urls.py` solo registra rutas; no contiene logica de negocio.

- [ ] T015 Actualizar OpenAPI para autenticacion.
  - Depende de: T011-T014.
  - Archivos esperados: `specs/003-autenticacion-jwt-roles/contracts/openapi.yaml` o actualizacion del contrato fuente si se decide consolidar.
  - Verificacion: documenta register, token, refresh y me; no documenta documentos, parqueaderos, tarifas, horarios, espacios ni WebSocket.

## Fase 2: Backend roles y permisos

- [ ] T016 Validar catalogo de roles backend.
  - Depende de: T001.
  - Archivos esperados: `backend/apps/usuarios/models.py` si requiere ajuste.
  - Verificacion: existen `ADMINISTRADOR`, `PROPIETARIO` y `CONDUCTOR`; `ANONIMO` no se guarda como cuenta persistente salvo decision documentada.

- [ ] T017 Crear o ajustar permisos base por rol.
  - Depende de: T016.
  - Archivos esperados: `backend/apps/usuarios/permissions.py`.
  - Verificacion: permisos `IsAdministrador`, `IsPropietario`, `IsConductorOAutenticado` o equivalentes no consultan datos fuera de su responsabilidad.

- [ ] T018 Crear endpoint de prueba interna de permisos solo si es necesario para tests.
  - Depende de: T017.
  - Archivos esperados: test-only URL o vista dentro de tests, no ruta productiva innecesaria.
  - Verificacion: no se agrega superficie publica artificial si los permisos pueden probarse con endpoints reales.

- [ ] T019 Crear seeds/factory de roles para tests.
  - Depende de: T016.
  - Archivos esperados: `backend/tests/factories.py` o factories de usuarios.
  - Verificacion: tests pueden crear cuentas administrador, propietario y conductor sin duplicacion.

## Fase 3: Frontend servicio de sesion

- [ ] T020 Centralizar endpoints de autenticacion.
  - Depende de: T002.
  - Archivos esperados: `frontend-web/src/config/endpoints.ts`.
  - Verificacion: contiene URLs para register, token, refresh y me; las vistas no construyen URLs manualmente.

- [ ] T021 Crear cliente API con interceptor de Authorization.
  - Depende de: T020.
  - Archivos esperados: `frontend-web/src/services/api.ts` o equivalente.
  - Verificacion: access token se inyecta solo cuando existe; no rompe llamadas publicas.

- [ ] T022 Crear servicio frontend de auth.
  - Depende de: T020-T021.
  - Archivos esperados: `frontend-web/src/services/authService.ts`.
  - Verificacion: implementa register, login, refresh, me y logout; no contiene HTML ni decisiones visuales.

- [ ] T023 Crear store/controlador de sesion.
  - Depende de: T022.
  - Archivos esperados: `frontend-web/src/store/authStore.ts` o hook equivalente.
  - Verificacion: mantiene access token en memoria o estrategia segura documentada; persiste solo lo necesario para restaurar sesion; limpia estado en logout.

- [ ] T024 Implementar persistencia segura de sesion web.
  - Depende de: T023.
  - Archivos esperados: `frontend-web/src/services/sessionStorage.ts` o modulo equivalente.
  - Verificacion: no guarda password ni datos sensibles innecesarios; documenta tradeoff si usa `localStorage`; refresh se maneja con expiracion/limpieza.

- [ ] T025 Implementar refresh automatico controlado.
  - Depende de: T021-T024.
  - Archivos esperados: cliente API/store.
  - Verificacion: ante 401 por access vencido intenta refresh una vez; si falla, cierra sesion y redirige a login.

## Fase 4: Frontend rutas, login y redireccion

- [ ] T026 Crear configuracion de rutas por rol.
  - Depende de: T004.
  - Archivos esperados: `frontend-web/src/config/routes.ts`.
  - Verificacion: rutas protegidas declaran roles permitidos; home anonimo sigue publico.

- [ ] T027 Crear guard de ruta autenticada.
  - Depende de: T023, T026.
  - Archivos esperados: `frontend-web/src/routes/ProtectedRoute.tsx` o equivalente.
  - Verificacion: sin sesion redirige a `/login`; con rol incorrecto redirige a ruta segura o muestra estado no autorizado.

- [ ] T028 Crear guard de ruta por rol.
  - Depende de: T027.
  - Archivos esperados: `frontend-web/src/routes/RoleRoute.tsx` o integrado en ProtectedRoute.
  - Verificacion: `ADMINISTRADOR` no entra a rutas de propietario por accidente y viceversa.

- [ ] T029 Crear pantalla/flujo minimo de login.
  - Depende de: T022-T024.
  - Archivos esperados: `frontend-web/src/views/auth/LoginView.tsx` o ruta equivalente.
  - Verificacion: maneja loading, error en espanol y exito; no incluye dashboard completo.

- [ ] T030 Crear flujo minimo de registro base.
  - Depende de: T022.
  - Archivos esperados: `frontend-web/src/views/auth/RegisterView.tsx` o ruta equivalente.
  - Verificacion: permite crear cuenta base sin documentos, sin parqueadero y sin datos de tarifas/horarios/espacios.

- [ ] T031 Implementar redireccion post-login por rol.
  - Depende de: T004, T023, T026.
  - Archivos esperados: hook/controlador de auth o router.
  - Verificacion: administrador va a `/admin`, propietario a `/propietario`, conductor a `/`, anonimo no accede a rutas protegidas.

- [ ] T032 Crear placeholders funcionales de rutas destino solo si no existen.
  - Depende de: T026-T031.
  - Archivos esperados: vistas minimas para `/admin`, `/propietario`, `/login`, `/register`.
  - Verificacion: placeholders no implementan dashboard, documentos, parqueaderos, tarifas, horarios ni espacios; solo permiten validar navegacion.

## Fase 5: Pruebas backend

- [ ] T033 Probar registro exitoso de conductor o propietario base.
  - Depende de: T011, T019.
  - Archivos esperados: `backend/apps/usuarios/tests/test_auth_api.py`.
  - Verificacion: crea cuenta, hashea password y no expone password_hash.

- [ ] T034 Probar que registro publico no permite ADMINISTRADOR.
  - Depende de: T011.
  - Archivos esperados: `backend/apps/usuarios/tests/test_auth_api.py`.
  - Verificacion: respuesta 400/403 con mensaje en espanol y accion correctiva.

- [ ] T035 Probar login JWT exitoso.
  - Depende de: T012.
  - Archivos esperados: `backend/apps/usuarios/tests/test_auth_api.py`.
  - Verificacion: devuelve access, refresh y perfil/rol suficiente para frontend.

- [ ] T036 Probar login con credenciales invalidas.
  - Depende de: T012.
  - Archivos esperados: `backend/apps/usuarios/tests/test_auth_api.py`.
  - Verificacion: respuesta no revela si usuario o password especifico fallo; mensaje en espanol.

- [ ] T037 Probar refresh token.
  - Depende de: T012.
  - Archivos esperados: `backend/apps/usuarios/tests/test_auth_api.py`.
  - Verificacion: refresh valido devuelve nuevo access; refresh invalido falla de forma segura.

- [ ] T038 Probar `GET /api/cuentas/me/` autenticado.
  - Depende de: T013.
  - Archivos esperados: `backend/apps/usuarios/tests/test_auth_api.py`.
  - Verificacion: devuelve datos seguros de cuenta y rol.

- [ ] T039 Probar `GET /api/cuentas/me/` sin token.
  - Depende de: T013.
  - Archivos esperados: `backend/apps/usuarios/tests/test_auth_api.py`.
  - Verificacion: devuelve 401.

- [ ] T040 Probar permisos por rol.
  - Depende de: T017-T019.
  - Archivos esperados: `backend/apps/usuarios/tests/test_permissions.py`.
  - Verificacion: administrador pasa permiso administrador; propietario no pasa permiso administrador; anonimo no pasa permisos autenticados.

## Fase 6: Pruebas frontend

- [ ] T041 Configurar utilidades de test frontend si faltan.
  - Depende de: T002.
  - Archivos esperados: `frontend-web` testing setup si aplica.
  - Verificacion: comandos de test frontend corren sin depender de backend real.

- [ ] T042 Probar auth service.
  - Depende de: T022.
  - Archivos esperados: tests de `authService`.
  - Verificacion: login, refresh, me y logout usan endpoints centralizados.

- [ ] T043 Probar persistencia/limpieza de sesion.
  - Depende de: T023-T024.
  - Archivos esperados: tests de store/session storage.
  - Verificacion: logout borra tokens/session metadata; no guarda password.

- [ ] T044 Probar ProtectedRoute sin sesion.
  - Depende de: T027.
  - Archivos esperados: tests de rutas.
  - Verificacion: redirige a `/login`.

- [ ] T045 Probar redireccion por rol.
  - Depende de: T031.
  - Archivos esperados: tests de router/auth hook.
  - Verificacion: admin, propietario y conductor redirigen segun mapa acordado.

- [ ] T046 Probar acceso denegado por rol incorrecto.
  - Depende de: T028.
  - Archivos esperados: tests de rutas.
  - Verificacion: propietario no accede a ruta admin y administrador no queda atrapado en ruta propietario.

## Fase 7: Verificacion final

- [ ] T047 Ejecutar checks backend.
  - Depende de: T005-T040.
  - Verificacion: `python manage.py check` pasa.

- [ ] T048 Ejecutar migraciones/check backend.
  - Depende de: T005-T040.
  - Verificacion: `python manage.py makemigrations --check` no deja cambios pendientes y `python manage.py migrate` aplica correctamente.

- [ ] T049 Ejecutar tests backend.
  - Depende de: T033-T040.
  - Verificacion: `pytest` pasa para autenticacion, permisos y tests existentes.

- [ ] T050 Ejecutar build/tests frontend.
  - Depende de: T041-T046.
  - Verificacion: `npm run build` pasa y tests frontend pasan si fueron configurados.

- [ ] T051 Revisar alcance prohibido.
  - Depende de: T047-T050.
  - Verificacion: no hay cambios de subida de documentos, creacion de parqueadero, tarifas, horarios, espacios ni WebSocket.

- [ ] T052 Revisar seguridad de sesion.
  - Depende de: T047-T050.
  - Verificacion: no hay passwords/tokens hardcodeados; no se imprime token en consola; errores no filtran datos sensibles.

- [ ] T053 Revisar arquitectura por capas.
  - Depende de: T047-T050.
  - Verificacion: controllers solo validan entrada/salida y delegan; services no importan componentes React ni request; repositories no devuelven respuestas HTTP.

## Dependencias sugeridas

- T001-T004 antes de cualquier implementacion.
- Backend JWT T005-T015 antes de pruebas backend T033-T039.
- Permisos T016-T019 antes de T040.
- Frontend service/store T020-T025 antes de guards y vistas.
- Guards T026-T028 antes de pruebas de rutas.
- Verificacion final solo despues de backend y frontend.

## Paralelizacion segura

- Backend T005-T019 y frontend T020-T032 pueden avanzar en paralelo despues de T001-T004 si el contrato de respuesta de login queda acordado.
- Tests backend T033-T040 pueden escribirse en paralelo por endpoint/permiso.
- Tests frontend T042-T046 pueden escribirse en paralelo cuando store y router esten listos.

