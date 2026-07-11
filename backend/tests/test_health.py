from django.core.cache import cache
from django.db import connection
from django.test import override_settings
from django.urls import reverse


def test_health_endpoint_reports_ready_environment(client, monkeypatch):
    monkeypatch.setattr(connection, "cursor", lambda *args, **kwargs: _CursorContext())
    monkeypatch.setattr(cache, "set", lambda key, value, timeout=None: None)
    monkeypatch.setattr(cache, "get", lambda key: "ok")

    response = client.get(reverse("health"))

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "ok",
        "cache": "ok",
        "version": "0.1.0",
    }


@override_settings(APP_VERSION="test-version")
def test_health_endpoint_does_not_require_authentication(client, monkeypatch):
    monkeypatch.setattr(connection, "cursor", lambda *args, **kwargs: _CursorContext())
    monkeypatch.setattr(cache, "set", lambda key, value, timeout=None: None)
    monkeypatch.setattr(cache, "get", lambda key: "ok")

    response = client.get("/api/health/")

    assert response.status_code == 200
    assert response.json()["version"] == "test-version"


class _CursorContext:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def execute(self, query):
        self.query = query

    def fetchone(self):
        return (1,)
