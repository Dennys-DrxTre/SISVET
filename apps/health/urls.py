from django.urls import path
from apps.health.views.consultation.views import ConsultViews

app_name = 'health'


urlpatterns = [
    path('Consultations/', ConsultViews.as_view(), name='consultations')
]
