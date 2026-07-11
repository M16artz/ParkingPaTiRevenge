from django.utils import timezone

from apps.common.repositories import BaseRepository
from apps.documentos.models import Documento


class DocumentoRepository(BaseRepository):
    model = Documento

    def filter_by_cuenta(self, cuenta):
        return self.model.objects.filter(cuenta=cuenta).order_by("-fecha_creacion")

    def get_by_id_for_cuenta(self, documento_id, cuenta):
        return self.model.objects.filter(id=documento_id, cuenta=cuenta).first()

    def get_pending(self):
        return self.model.objects.filter(estado="PENDIENTE").order_by("-fecha_creacion")

    def filter_by_estado(self, estado):
        return self.model.objects.filter(estado=estado).order_by("-fecha_creacion")

    def filter_validos(self, cuenta):
        return self.model.objects.filter(cuenta=cuenta, es_valido=True)

    def filter_vigentes(self, cuenta):
        today = timezone.localdate()
        return self.model.objects.filter(cuenta=cuenta, fecha_expiracion__gte=today)
