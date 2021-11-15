from django.contrib import admin
from apps.cashier.models import Product, Buy_Sale, Detail_BS, ChildProduct

# Register your models here.
admin.site.register(Product)

admin.site.register(Buy_Sale)

admin.site.register(Detail_BS)

admin.site.register(ChildProduct)