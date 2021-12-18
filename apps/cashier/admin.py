from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.cashier.models import *
from apps.usersys.models import DollarStatus

# Register your models here.

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    pass

@admin.register(Buy_Sale)
class Buy_SaleAdmin(ImportExportModelAdmin):
    pass

@admin.register(Detail_BS)
class Detail_BSAdmin(ImportExportModelAdmin):
    pass

@admin.register(ChildProduct)
class ChildProductAdmin(ImportExportModelAdmin):
    pass

@admin.register(VaccineDay)
class VaccineDayAdmin(ImportExportModelAdmin):
    pass

@admin.register(Det_VaccineDay)
class Det_VaccineDayAdmin(ImportExportModelAdmin):
    pass
<<<<<<< HEAD

@admin.register(DollarStatus)
class DollarAdmin(ImportExportModelAdmin):
    pass
=======
>>>>>>> b0891a40af8565bd3fc0e1b635d55a867dbce1e5
