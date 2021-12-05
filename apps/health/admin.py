from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.health.models import *

# Register your models here.

@admin.register(Consultation)
class ConsultationAdmin(ImportExportModelAdmin):
    pass

@admin.register(Vaccine)
class VaccineAdmin(ImportExportModelAdmin):
    pass

@admin.register(Parasite)
class ParasiteAdmin(ImportExportModelAdmin):
    pass

