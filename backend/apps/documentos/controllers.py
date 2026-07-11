from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.exceptions import DomainValidationError
from apps.documentos.models import EstadoDocumento
from apps.documentos.permissions import IsAdministradorCuenta, IsPropietarioCuenta
from apps.documentos.serializers import (
    DocumentoReadSerializer,
    DocumentoUploadSerializer,
    DocumentoValidacionSerializer,
)
from apps.documentos.services import DocumentoService
from apps.usuarios.models import CodigoRol
from apps.usuarios.permissions import get_request_cuenta


class DocumentoListCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    service = DocumentoService()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsPropietarioCuenta()]
        return [IsAuthenticated()]

    def get(self, request):
        cuenta = get_request_cuenta(request)
        if cuenta.rol.codigo == CodigoRol.ADMINISTRADOR:
            documentos = self.service.listar_pendientes()
        else:
            documentos = self.service.listar_propios(cuenta)
        return Response(DocumentoReadSerializer(documentos, many=True).data)

    def post(self, request):
        cuenta = get_request_cuenta(request)
        serializer = DocumentoUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            documento = self.service.subir_documento(cuenta, serializer.validated_data["archivo"])
        except DomainValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(DocumentoReadSerializer(documento).data, status=status.HTTP_201_CREATED)


class DocumentoDetailView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsPropietarioCuenta]
    service = DocumentoService()

    def patch(self, request, documento_id):
        cuenta = get_request_cuenta(request)
        serializer = DocumentoUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            documento = self.service.reemplazar_documento(cuenta, documento_id, serializer.validated_data["archivo"])
        except DomainValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        return Response(DocumentoReadSerializer(documento).data)


class DocumentoValidarView(APIView):
    permission_classes = [IsAuthenticated, IsAdministradorCuenta]
    service = DocumentoService()

    def post(self, request, documento_id):
        serializer = DocumentoValidacionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            documento = self.service.validar_documento(
                documento_id,
                serializer.validated_data["estado"],
                serializer.validated_data.get("motivo_rechazo", ""),
            )
        except DomainValidationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        status_code = status.HTTP_200_OK
        if documento.estado == EstadoDocumento.RECHAZADO and not documento.motivo_rechazo:
            documento.motivo_rechazo = "Documento rechazado por revision administrativa."
            documento.save(update_fields=["motivo_rechazo", "fecha_actualizacion"])
        return Response(DocumentoReadSerializer(documento).data, status=status_code)

