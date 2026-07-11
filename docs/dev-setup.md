# Entorno de desarrollo

Esta guia levanta la base tecnica de ParkingPaTi: backend Django ASGI, frontend Vite, PostgreSQL, Redis y tileserver. Este entregable no incluye autenticacion, parqueaderos, tarifas, mapas ni logica de negocio.

## Requisitos

- Docker Desktop con Docker Compose.
- Python 3.12 para ejecucion local del backend.
- Node.js 20 para ejecucion local del frontend.

## Variables de entorno

Crear el archivo local desde el ejemplo:

```powershell
Copy-Item .env.example .env
```

El archivo `.env` no debe versionarse. Los valores de `.env.example` son placeholders.

Para Docker Compose, los hosts internos son:

```dotenv
DB_HOST=db
REDIS_URL=redis://redis:6379/0
```

Para ejecucion local fuera de Docker, usar temporalmente:

```powershell
$env:DB_HOST="localhost"
$env:REDIS_URL="redis://localhost:6379/0"
```

## Arranque con Docker Compose

Validar la configuracion:

```powershell
docker compose -f docker/docker-compose.yml config
```

Construir e iniciar servicios:

```powershell
docker compose -f docker/docker-compose.yml up --build
```

Aplicar migraciones iniciales de Django:

```powershell
docker compose -f docker/docker-compose.yml exec backend python manage.py migrate
```

Consultar healthcheck:

```powershell
Invoke-RestMethod http://localhost:8000/api/health/
```

Abrir frontend:

```text
http://localhost:5173
```

## Arranque local del backend

Instalar dependencias:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements/development.txt
```

Usar PostgreSQL y Redis locales o levantarlos con Docker:

```powershell
docker compose -f ..\docker\docker-compose.yml up db redis
```

Configurar hosts locales:

```powershell
$env:DJANGO_SETTINGS_MODULE="backend.settings.development"
$env:DB_HOST="localhost"
$env:REDIS_URL="redis://localhost:6379/0"
```

Ejecutar migraciones y servidor ASGI:

```powershell
python manage.py migrate
uvicorn backend.asgi:application --host 0.0.0.0 --port 8000 --workers 2
```

Ejecutar pruebas:

```powershell
pytest
```

## Arranque local del frontend

Instalar dependencias:

```powershell
cd frontend-web
npm install
```

Iniciar Vite:

```powershell
npm run dev
```

Construir frontend:

```powershell
npm run build
```

## Documentos de propietarios

En desarrollo, la carga de documentos usa almacenamiento local bajo `MEDIA_ROOT` y no requiere credenciales externas:

```dotenv
DOCUMENTOS_STORAGE_BACKEND=local
MEDIA_ROOT=backend/media
DOCUMENTOS_LOCAL_SUBDIR=documentos
DOCUMENTOS_MAX_UPLOAD_BYTES=5242880
DOCUMENTOS_ALLOWED_EXTENSIONS=pdf,jpg,jpeg,png
```

Los formatos aceptados son PDF, JPG, JPEG y PNG. Los archivos subidos localmente no deben versionarse; `.gitignore` excluye `backend/media/`.

Para almacenamiento externo compatible con R2, completar los placeholders `R2_*` en el `.env` local. No colocar claves reales en `.env.example`, documentación ni tests.

## Tileserver

El servicio `tileserver` esta definido para la infraestructura base, pero este entregable no implementa mapas. Para usarlo con datos reales en un entregable posterior, colocar el archivo:

```text
docker/tileserver/loja.mbtiles
```

Si el archivo no existe, el contenedor queda en espera y muestra un mensaje en logs. No descarga ni recalcula mapas.

## Diagnostico

Ver logs por servicio:

```powershell
docker compose -f docker/docker-compose.yml logs backend
docker compose -f docker/docker-compose.yml logs frontend-web
docker compose -f docker/docker-compose.yml logs db
docker compose -f docker/docker-compose.yml logs redis
docker compose -f docker/docker-compose.yml logs tileserver
```

Reiniciar un servicio:

```powershell
docker compose -f docker/docker-compose.yml restart backend
```

Verificar puertos ocupados:

```powershell
Get-NetTCPConnection -LocalPort 8000,5173,5432,6379,3000 -ErrorAction SilentlyContinue
```

Detener el entorno:

```powershell
docker compose -f docker/docker-compose.yml down
```

Detener y borrar volumenes locales:

```powershell
docker compose -f docker/docker-compose.yml down -v
```

## Checklist rapido

- `backend/` existe y contiene Django ASGI.
- `frontend-web/` existe y contiene Vite/React.
- `mobile/` existe como estructura reservada.
- `docker/docker-compose.yml` define backend, frontend-web, db, redis y tileserver.
- `.env.example` contiene placeholders y no secretos reales.
- `GET /api/health/` responde con estado tecnico del entorno.
