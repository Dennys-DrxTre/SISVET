from django.contrib import admin
from apps.cashier.models import *

# Register your models here.
admin.site.register(Product)

admin.site.register(Buy_Sale)

admin.site.register(Detail_BS)