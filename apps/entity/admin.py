from django.contrib import admin
from apps.entity.models import Client, Provider, Pet

# Register your models here.

admin.site.register(Client)

admin.site.register(Provider)

admin.site.register(Pet)