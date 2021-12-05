from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.entity.models import Client, Provider, Pet

# Register your models here.

@admin.register(Provider)
class ProviderAdmin(ImportExportModelAdmin):
    pass

@admin.register(Pet)
class PetAdmin(ImportExportModelAdmin):
    pass

@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    pass