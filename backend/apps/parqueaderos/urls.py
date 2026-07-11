from django.urls import path

from apps.parqueaderos.controllers import (
    MisParqueaderosView,
    ParqueaderoDetailView,
    ParqueaderoEstadoView,
    ParqueaderoListCreateView,
)


urlpatterns = [
    path("parqueaderos/", ParqueaderoListCreateView.as_view(), name="parqueaderos-list"),
    path("parqueaderos/mios/", MisParqueaderosView.as_view(), name="parqueaderos-mios"),
    path("parqueaderos/<int:parqueadero_id>/", ParqueaderoDetailView.as_view(), name="parqueaderos-detail"),
    path("parqueaderos/<int:parqueadero_id>/estado/", ParqueaderoEstadoView.as_view(), name="parqueaderos-estado"),
]
