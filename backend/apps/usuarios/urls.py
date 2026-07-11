from django.urls import path

from apps.usuarios.controllers import CuentaMeView, RegistroCuentaView, TokenObtainView, TokenRefreshView


urlpatterns = [
    path("auth/register/", RegistroCuentaView.as_view(), name="auth-register"),
    path("auth/token/", TokenObtainView.as_view(), name="auth-token"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("cuentas/me/", CuentaMeView.as_view(), name="cuenta-me"),
]
