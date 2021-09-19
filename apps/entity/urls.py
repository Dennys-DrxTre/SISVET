from django.urls import path
from apps.entity.views.client.views import ClientViews
from apps.entity.views.provider.views import ProviderViews
from apps.entity.views.pet.views import PetViews


app_name = 'entity'

urlpatterns = [
    # CRUD CLIENTS URL
    path('listado_clientes/', ClientViews.as_view(), name = 'clients'),
    # CRUD PROVIDERS URL
    path('listado_proveedores/', ProviderViews.as_view(), name = 'providers'),
    # CRUD PETS URL
    path('listado_mascotas/', PetViews.as_view(), name = 'pets'),

]
