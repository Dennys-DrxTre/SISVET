from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.usersys.models import NotificationStatus

# Register your models here.
@admin.register(NotificationStatus)
class NotificationStatusAdmin(ImportExportModelAdmin):
    pass