from django.urls import path
from apps.dashboard.views.dashboard.views import DashboardView, ChartsView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('estadisticas/', ChartsView.as_view(), name='charts'),
]
