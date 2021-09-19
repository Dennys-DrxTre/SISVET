from django.urls import path
from apps.dashboard.views.dashboard.views import DashboardView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]
