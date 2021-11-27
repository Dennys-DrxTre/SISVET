from django.urls import path
from apps.entity.views.client.views import ClientViews
from apps.entity.views.provider.views import ProviderViews
from apps.entity.views.pet.views import PetViews, detail_pet

app_name = 'entity'

urlpatterns = [
    # CRUD CLIENTS URL
    path('listado_clientes/', ClientViews.as_view(), name = 'clients'),
    # CRUD PROVIDERS URL
    path('listado_proveedores/', ProviderViews.as_view(), name = 'providers'),
    # CRUD PETS URL
    path('listado_mascotas/', PetViews.as_view(), name = 'pets'),
    # DETAIL PET URL
    path('listado_mascotas/detail/<int:id>/', detail_pet, name = 'detail_pet'),

]
