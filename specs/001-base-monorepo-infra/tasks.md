# Tasks: 001-base-monorepo-infra

**Feature**: Base del monorepo e infraestructura minima  
**Ruta solicitada**: `specs/001-base-monorepo-infra/`  
**Fuente tecnica usada**: `specs/001-base-monorepo-infra-scaffolding/spec.md`, `plan.md`, `research.md` y `contracts/implementation-files.md`  
**Alcance**: preparar solo la base del proyecto. No implementar logica de negocio, modelos de dominio, flujos de usuarios, permisos por rol especificos ni pantallas productivas.

## Formato

- `[ ] T###` tarea secuencial.
- `[P]` puede ejecutarse en paralelo si sus archivos no dependen de otra tarea pendiente.
- Cada tarea debe cerrar con evidencia de verificacion en la nota del agente.

## Reglas de ejecucion

- No versionar `.env`, credenciales reales, tokens, documentos reales ni archivos generados pesados.
- Usar placeholders comentados para secretos y variables sensibles.
- Mantener mensajes visibles en espanol cuando se agreguen respuestas o errores.
- Fijar versiones de imagenes Docker; no usar tags flotantes como `latest`.
- El backend debe usar ASGI con Uvicorn.
- El tileserver debe montar archivos `.mbtiles` o configuracion local; no debe recalcular datos en cada arranque.
- No agregar apps de negocio como parqueaderos, tarifas, horarios, documentos o espacios en este entregable.

## Fase 1: Preparacion del monorepo

- [ ] T001 Crear la estructura base del monorepo con las carpetas `backend/`, `frontend-web/`, `mobile/`, `docker/` y `docs/`, agregando archivos de conservacion si una carpeta quedaria vacia.
  - Archivos esperados: `backend/.gitkeep`, `frontend-web/.gitkeep`, `mobile/.gitkeep`, `docker/.gitkeep`, `docs/.gitkeep` cuando aplique.
  - Verificacion: `Test-Path backend, frontend-web, mobile, docker, docs` devuelve verdadero para todas las rutas.

- [ ] T002 Crear `.gitignore` en la raiz para secretos, entornos locales, caches Python, dependencias Node, builds, coverage, logs, datos Docker locales y archivos del sistema.
  - Archivos esperados: `.gitignore`.
  - Verificacion: `.env`, `.env.*`, `__pycache__/`, `.venv/`, `node_modules/`, `dist/`, `build/`, `coverage/`, `docker/data/` y `*.log` estan ignorados; `.env.example` no esta ignorado.

- [ ] T003 Crear `.env.example` comentado con placeholders seguros para backend, PostgreSQL, Redis, JWT, CORS, Cloudflare R2, Google Drive temporal, Cloudflare Tunnel, frontend web, WebSocket, tileserver y Nominatim.
  - Archivos esperados: `.env.example`.
  - Verificacion: contiene `SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `REDIS_URL`, `JWT_ACCESS_MINUTES`, `JWT_REFRESH_DAYS`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`, `R2_ENDPOINT_URL`, `CLOUDFLARE_TUNNEL_TOKEN`, `VITE_API_BASE_URL`, `VITE_WS_BASE_URL`, `VITE_TILESERVER_URL` y `VITE_NOMINATIM_URL`, sin valores reales.

## Fase 2: Dependencias y scaffolding backend

- [ ] T004 Crear archivos de dependencias base del backend para Python 3.12 y Django ASGI, sin dependencias de negocio.
  - Archivos esperados: `backend/requirements/base.txt`, `backend/requirements/development.txt`.
  - Verificacion: `base.txt` incluye Django 5.x, Django REST Framework, Channels, channels-redis, Uvicorn, psycopg, django-cors-headers, drf-spectacular y soporte de variables de entorno; `development.txt` incluye pytest y pytest-django.

- [ ] T005 Crear scaffolding minimo de proyecto Django compatible con `uvicorn backend.asgi:application`.
  - Archivos esperados: `backend/manage.py`, `backend/backend/__init__.py`, `backend/backend/asgi.py`, `backend/backend/wsgi.py`, `backend/backend/urls.py`, `backend/backend/settings/__init__.py`, `backend/backend/settings/base.py`, `backend/backend/settings/development.py`.
  - Verificacion: la ruta de importacion `backend.asgi:application` existe y no requiere apps de negocio para cargar.

- [ ] T006 Configurar settings base del backend para variables de entorno, PostgreSQL, Redis/Channels, DRF, CORS, OpenAPI y ASGI.
  - Archivos esperados: `backend/backend/settings/base.py`, `backend/backend/settings/development.py`.
  - Verificacion: la configuracion lee `SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DB_*`, `REDIS_URL` y `CORS_ALLOWED_ORIGINS`; no contiene secretos hardcodeados.

- [ ] T007 Crear endpoint tecnico `GET /api/health/` para validar backend, base de datos y cache sin exponer datos privados.
  - Archivos esperados: `backend/backend/health.py` o modulo equivalente de infraestructura, `backend/backend/urls.py`.
  - Verificacion: respuesta exitosa incluye `status`, `database`, `cache` y `version`; errores deben estar en espanol y sugerir revisar configuracion o servicios.

- [ ] T008 Crear prueba minima del endpoint de healthcheck y de carga de configuracion.
  - Archivos esperados: `backend/tests/test_health.py`, `backend/pytest.ini` o configuracion equivalente.
  - Verificacion: `pytest` ejecuta la prueba de `GET /api/health/` sin depender de modelos de negocio.

## Fase 3: Docker e infraestructura local

- [ ] T009 Crear Dockerfile del backend con Python 3.12, instalacion de dependencias y comando productivo Uvicorn.
  - Archivos esperados: `docker/backend/Dockerfile`.
  - Verificacion: el comando final usa `uvicorn backend.asgi:application --host 0.0.0.0 --port 8000 --workers 2`.

- [ ] T010 Crear configuracion base de tileserver-gl.
  - Archivos esperados: `docker/tileserver/config.json`, `docker/tileserver/.gitkeep` o placeholder documentado para `.mbtiles`.
  - Verificacion: la configuracion referencia un archivo `.mbtiles` montado y no descarga ni recalcula mapas durante el arranque.

- [ ] T011 Crear `docker/docker-compose.yml` con servicios `backend`, `db`, `redis` y `tileserver`.
  - Archivos esperados: `docker/docker-compose.yml`.
  - Verificacion: `backend` usa el Dockerfile local y `.env`; `db` usa PostgreSQL 16 con volumen persistente; `redis` usa Redis 7 con volumen persistente; `tileserver` usa `maptiler/tileserver-gl:v4.11.1` o version fija equivalente.

- [ ] T012 Validar sintaxis de Docker Compose y corregir rutas relativas si falla.
  - Archivos esperados: no necesariamente crea archivos nuevos; puede ajustar `docker/docker-compose.yml`.
  - Verificacion: `docker compose -f docker/docker-compose.yml config` termina sin errores.

## Fase 4: Documentacion operativa

- [ ] T013 Crear `docs/dev-setup.md` con comandos de preparacion del entorno local.
  - Archivos esperados: `docs/dev-setup.md`.
  - Verificacion: documenta como copiar `.env.example` a `.env`, instalar dependencias backend, levantar Docker Compose, ejecutar migraciones iniciales, correr tests y consultar `/api/health/`.

- [ ] T014 Documentar comandos de diagnostico y solucion de problemas comunes.
  - Archivos esperados: `docs/dev-setup.md`.
  - Verificacion: incluye comandos para revisar logs de `backend`, `db`, `redis` y `tileserver`, reiniciar servicios, validar variables faltantes y verificar puertos ocupados.

- [ ] T015 Actualizar el contrato operativo de implementacion si los nombres finales de archivos difieren del contrato fuente.
  - Archivos esperados: `specs/001-base-monorepo-infra-scaffolding/contracts/implementation-files.md` o nota equivalente en `docs/dev-setup.md`.
  - Verificacion: el arbol documentado coincide con los archivos realmente creados.

## Fase 5: Revision final del entregable

- [ ] T016 Ejecutar verificacion integral de alcance.
  - Depende de: T001-T015.
  - Verificacion: confirmar que existen las carpetas base, `.gitignore`, `.env.example`, Docker Compose, Dockerfile backend, configuracion tileserver, scaffolding Django ASGI, dependencias base y `docs/dev-setup.md`.

- [ ] T017 Ejecutar verificacion de no negocio.
  - Depende de: T001-T015.
  - Verificacion: no existen modelos, serializers, viewsets, migraciones o pantallas de `parqueaderos`, `tarifas`, `horarios`, `documentos`, `espacios`, autenticacion de usuarios o administracion.

- [ ] T018 Ejecutar verificacion de secretos.
  - Depende de: T001-T015.
  - Verificacion: `git status --short` no muestra `.env`; busqueda manual confirma que no hay claves reales, tokens ni credenciales en archivos versionables.

- [ ] T019 Ejecutar comandos finales y registrar evidencia.
  - Depende de: T001-T018.
  - Verificacion: registrar resultados de `docker compose -f docker/docker-compose.yml config`, `pytest` desde `backend/` si aplica, y una consulta manual o automatizada a `GET /api/health/` si el entorno se levanta.

## Dependencias sugeridas

- T001 antes de cualquier tarea que escriba dentro de carpetas base.
- T003 antes de T011 para que Compose pueda referenciar variables.
- T004 antes de T005, T006, T007 y T008.
- T005 y T006 antes de T007.
- T007 antes de T008.
- T009 y T010 antes de T011.
- T011 antes de T012.
- T013 antes de T014.
- T016-T019 solo al cierre.

## Paralelizacion segura

- T002 y T003 pueden ejecutarse en paralelo despues de T001.
- T009 y T010 pueden ejecutarse en paralelo despues de T001.
- T013 puede empezar en paralelo cuando T003, T009, T010 y T011 tengan rutas estables.
- T017 y T018 pueden ejecutarse en paralelo durante la revision final.

