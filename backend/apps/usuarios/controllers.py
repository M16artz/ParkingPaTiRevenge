from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from apps.common.exceptions import DomainValidationError
from apps.usuarios.serializers import (
    LoginSerializer,
    PerfilCuentaSerializer,
    RegistroCuentaSerializer,
    TokenRefreshRequestSerializer,
)
from apps.usuarios.services import AuthService


class RegistroCuentaView(APIView):
    permission_classes = [AllowAny]
    auth_service = AuthService()

    def post(self, request):
        serializer = RegistroCuentaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            cuenta = self.auth_service.registrar_cuenta(serializer.validated_data)
        except DomainValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(PerfilCuentaSerializer(cuenta).data, status=status.HTTP_201_CREATED)


class TokenObtainView(APIView):
    permission_classes = [AllowAny]
    auth_service = AuthService()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = self.auth_service.login(
                serializer.validated_data["username"],
                serializer.validated_data["password"],
            )
        except DomainValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            {
                "access": result["access"],
                "refresh": result["refresh"],
                "cuenta": PerfilCuentaSerializer(result["cuenta"]).data,
            }
        )


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        request_serializer = TokenRefreshRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        serializer = TokenRefreshSerializer(data=request_serializer.validated_data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return Response(
                {"detail": "El refresh token no es valido o expiro. Inicia sesion nuevamente."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(serializer.validated_data)


class CuentaMeView(APIView):
    permission_classes = [IsAuthenticated]
    auth_service = AuthService()

    def get(self, request):
        try:
            cuenta = self.auth_service.perfil_desde_user(request.user)
        except DomainValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        return Response(PerfilCuentaSerializer(cuenta).data)

