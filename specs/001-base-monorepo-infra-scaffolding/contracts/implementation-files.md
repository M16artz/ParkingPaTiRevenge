# Contrato de archivos base — Entregable E01

Este archivo describe los archivos de implementación mínimos que un agente debe crear en el monorepo real.

## Árbol objetivo

```text
parkingpati/
├── backend/
├── frontend-web/
├── mobile/
├── docker/
│   ├── docker-compose.yml
│   ├── backend/
│   │   └── Dockerfile
│   └── tileserver/
│       └── config.json
├── docs/
│   └── dev-setup.md
├── .gitignore
└── .env.example
```

## `.gitignore`

```gitignore
# Entornos y secretos
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.venv/
venv/
env/
backend/staticfiles/
backend/media/

# Node
node_modules/
frontend-web/node_modules/
mobile/node_modules/
dist/
build/
coverage/

# Sistema
.DS_Store
Thumbs.db

# Docker/local
docker/data/
*.log
```

## `.env.example`

```dotenv
# =========================================================
# ParkingPaTi — variables de entorno de ejemplo
# Copiar como .env y completar. NO versionar el .env real.
# =========================================================

# Backend
DJANGO_SETTINGS_MODULE=config.settings.development
SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos PostgreSQL
DB_NAME=parkingpati
DB_USER=parkingpati
DB_PASSWORD=change-me
DB_HOST=db
DB_PORT=5432

# Redis / Channels
REDIS_URL=redis://redis:6379/0

# JWT
JWT_ACCESS_MINUTES=15
JWT_REFRESH_DAYS=7

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Cloudflare R2 — almacenamiento de documentos
R2_ACCESS_KEY_ID=change-me
R2_SECRET_ACCESS_KEY=change-me
R2_BUCKET_NAME=parkingpati-docs
R2_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
R2_PUBLIC_BASE_URL=https://files.parkingpati.example

# Fallback temporal si se mantiene Google Drive
GOOGLE_DRIVE_CREDENTIALS_PATH=/run/secrets/google-drive.json
GOOGLE_DRIVE_FOLDER_ID=change-me

# Cloudflare Tunnel
CLOUDFLARE_TUNNEL_TOKEN=change-me

# Frontend web
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_BASE_URL=ws://localhost:8000/ws
VITE_TILESERVER_URL=http://localhost:3000/styles/osm-bright/{z}/{x}/{y}.png
VITE_NOMINATIM_URL=https://nominatim.openstreetmap.org
```

## `docker/docker-compose.yml`

```yaml
services:
  backend:
    build:
      context: ../backend
      dockerfile: ../docker/backend/Dockerfile
    command: uvicorn backend.asgi:application --host 0.0.0.0 --port 8000 --workers 2
    env_file:
      - ../.env
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    volumes:
      - ../backend:/app

  db:
    image: postgres:16.3-alpine
    environment:
      POSTGRES_DB: ${DB_NAME:-parkingpati}
      POSTGRES_USER: ${DB_USER:-parkingpati}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-parkingpati}
    ports:
      - "5432:5432"
    volumes:
      - parkingpati_postgres:/var/lib/postgresql/data

  redis:
    image: redis:7.2-alpine
    ports:
      - "6379:6379"
    volumes:
      - parkingpati_redis:/data

  tileserver:
    image: maptiler/tileserver-gl:v4.11.1
    command: ["--config", "/data/config.json"]
    ports:
      - "3000:8080"
    volumes:
      - ./tileserver:/data

volumes:
  parkingpati_postgres:
  parkingpati_redis:
```

## `docker/backend/Dockerfile`

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir -r requirements/base.txt

COPY . /app

CMD ["uvicorn", "backend.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

## Criterio de aceptación

- `docker compose -f docker/docker-compose.yml config` no muestra errores.
- `.env.example` contiene todos los placeholders solicitados.
- `.gitignore` impide versionar secretos y dependencias.
- El backend usa ASGI/Uvicorn, no WSGI/Gunicorn.
