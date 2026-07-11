from django.core.exceptions import ValidationError

from apps.common.exceptions import DomainValidationError


class BaseService:
    repository = None

    @staticmethod
    def validate(instance):
        try:
            instance.full_clean()
        except ValidationError as exc:
            raise DomainValidationError("Los datos no son validos. Revisa los campos enviados.") from exc
        return instance

