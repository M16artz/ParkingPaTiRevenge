from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.exceptions import DomainValidationError
from apps.parqueaderos.serializers import (
    ParqueaderoCreateSerializer,
    ParqueaderoEstadoSerializer,
    ParqueaderoReadSerializer,
    ParqueaderoUpdateSerializer,
)
from apps.parqueaderos.services import ParqueaderoService
from apps.usuarios.permissions import IsAdministrador, IsPropietario, get_request_cuenta


class ParqueaderoListCreateView(APIView):
    service = ParqueaderoService()

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsAdministrador()]
        return [IsAuthenticated(), IsPropietario()]

    def get(self, request):
        parqueaderos = self.service.listar_para_admin()
        return Response(ParqueaderoReadSerializer(parqueaderos, many=True).data)

    def post(self, request):
        cuenta = get_request_cuenta(request)
        serializer = ParqueaderoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            parqueadero = self.service.crear(cuenta, serializer.validated_data)
        except DomainValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ParqueaderoReadSerializer(parqueadero).data, status=status.HTTP_201_CREATED)


class MisParqueaderosView(APIView):
    permission_classes = [IsAuthenticated, IsPropietario]
    service = ParqueaderoService()

    def get(self, request):
        cuenta = get_request_cuenta(request)
        parqueaderos = self.service.listar_mios(cuenta)
        return Response(ParqueaderoReadSerializer(parqueaderos, many=True).data)


class ParqueaderoDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPropietario]
    service = ParqueaderoService()

    def patch(self, request, parqueadero_id):
        cuenta = get_request_cuenta(request)
        serializer = ParqueaderoUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            parqueadero = self.service.editar_general(cuenta, parqueadero_id, serializer.validated_data)
        except DomainValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        return Response(ParqueaderoReadSerializer(parqueadero).data)


class ParqueaderoEstadoView(APIView):
    permission_classes = [IsAuthenticated, IsPropietario]
    service = ParqueaderoService()

    def patch(self, request, parqueadero_id):
        cuenta = get_request_cuenta(request)
        serializer = ParqueaderoEstadoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            parqueadero = self.service.cambiar_estado_general(
                cuenta,
                parqueadero_id,
                serializer.validated_data["disponibilidad"],
            )
        except DomainValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        return Response(ParqueaderoReadSerializer(parqueadero).data)
