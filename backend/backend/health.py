from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.db.utils import OperationalError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        database_status = self._database_status()
        cache_status = self._cache_status()
        status = "ok" if database_status == "ok" and cache_status == "ok" else "degradado"
        http_status = 200 if status == "ok" else 503

        payload = {
            "status": status,
            "database": database_status,
            "cache": cache_status,
            "version": settings.APP_VERSION,
        }

        if status != "ok":
            payload["detail"] = (
                "El entorno base no esta listo. Revisa la configuracion de base de datos, "
                "Redis y variables de entorno antes de continuar."
            )

        return Response(payload, status=http_status)

    @staticmethod
    def _database_status() -> str:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        except OperationalError:
            return "error"
        return "ok"

    @staticmethod
    def _cache_status() -> str:
        try:
            cache.set("healthcheck", "ok", timeout=5)
            return "ok" if cache.get("healthcheck") == "ok" else "error"
        except Exception:
            return "error"

