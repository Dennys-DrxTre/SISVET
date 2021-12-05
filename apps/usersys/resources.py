from import_export import resources
from apps.entity.models import Client, Pet, Provider
from apps.health.models import Consultation, Vaccine, Parasite
from apps.cashier.models import Product, ChildProduct, Buy_Sale, Detail_BS, VaccineDay, Det_VaccineDay


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client

class PetResource(resources.ModelResource):
    class Meta:
        model = Pet

class ProviderResource(resources.ModelResource):
    class Meta:
        model = Provider

class ConsultationResource(resources.ModelResource):
    class Meta:
        model = Consultation

class VaccineResource(resources.ModelResource):
    class Meta:
        model = Vaccine

class ParasiteResource(resources.ModelResource):
    class Meta:
        model = Parasite

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ChildProductResource(resources.ModelResource):
    class Meta:
        model = ChildProduct

class Buy_SaleResource(resources.ModelResource):
    class Meta:
        model = Buy_Sale

class Detail_BSResource(resources.ModelResource):
    class Meta:
        model = Detail_BS

class VaccineDayResource(resources.ModelResource):
    class Meta:
        model = VaccineDay

class Det_VaccineDayResource(resources.ModelResource):
    class Meta:
        model = Det_VaccineDay