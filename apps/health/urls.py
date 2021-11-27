from django.urls import path
from apps.health.views.consultas.views import ConsultaViews
from apps.health.views.desparacitacion.views import DesparacitacionViews 
from apps.health.views.vacunacion.views import VacunaViews
from apps.health.views.vaccine.views import VaccineDayViews, Create_VaccineDay, Edit_VaccineDay

app_name = 'health'

urlpatterns = [
    path("consultas/", ConsultaViews.as_view(), name="consultas"),
    path("desparacitacion/", DesparacitacionViews.as_view(), name="desparacitacion"),
    path("vacunacion/", VacunaViews.as_view(), name="vacunas"),
    # LIST, DETAIL AND DELETE VACCINE DAY
    path('listado_jornada_vacunacion/', VaccineDayViews.as_view(), name='vaccinedays'),
    # CREATE VACCINE DAY
    path('registrar_jornada_vacunacion/', Create_VaccineDay.as_view(), name='add_vaccineday'),
    # EDIT VACCINE DAY
    path('editar_jornada_vacunacion/<int:pk>/', Edit_VaccineDay.as_view(), name='edit_vaccineday'),
]
