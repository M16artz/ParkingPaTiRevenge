from django.urls import path

from apps.documentos.controllers import DocumentoDetailView, DocumentoListCreateView, DocumentoValidarView


urlpatterns = [
    path("documentos/", DocumentoListCreateView.as_view(), name="documentos-list"),
    path("documentos/<int:documento_id>/", DocumentoDetailView.as_view(), name="documentos-detail"),
    path("documentos/<int:documento_id>/validar/", DocumentoValidarView.as_view(), name="documentos-validar"),
]

