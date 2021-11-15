from django.db import models
from CONFIG.settings import MEDIA_URL
from datetime import datetime, date
from django.forms import model_to_dict
from apps.entity.choices import type_client, gender_choices, gender_pet, species_pet

import secrets

# Create your models here.

def my_urlsecret():
    return secrets.token_urlsafe(32)

class Estado(models.Model):
    status = models.BooleanField(default=True, verbose_name='Estado')
    urlsecret = models.SlugField(max_length=50, default=my_urlsecret , null=True , blank=True)
    next_visit = models.DateField(default=date.today, verbose_name='Proxima visita', null=True , blank=True)

    
    class Meta:
        abstract=True

class Client(Estado):
    dni = models.CharField(max_length=8, verbose_name='Cedula', unique=True)
    gender = models.CharField(max_length=15, choices=gender_choices )
    type_name = models.CharField(max_length=10, choices=type_client, default = 'V-')
    first_name = models.CharField(verbose_name="Nombres", max_length=40)
    last_name = models.CharField(verbose_name="Apellidos", max_length=40)
    address = models.CharField(verbose_name="Direccion Habitacional", max_length=100, null=True, blank=True)
    mobile = models.CharField(verbose_name="Número de Celular",  max_length=11 , null = True, blank=True)
    tlf = models.CharField(verbose_name="Número de Telefonico", max_length=11 , null = True, blank=True)
    Email = models.EmailField(verbose_name= "Correo Electronico", null = True, blank=True)
    fechaa = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de edición")

    def __str__(self):
        return (self.dni)

    def get_gender_display(self):
        if self.gender:
            return '{}'.format(self.gender)
    

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = self.get_gender_display()
        return item

    class Meta:
        verbose_name_plural = 'Clientes'
        verbose_name = 'Cliente'
        ordering = ['id']

class Provider(Estado):
    name = models.CharField(verbose_name="Nombres", max_length=40)
    rif = models.CharField(max_length =100, unique =True, verbose_name='RIF', null = True, blank=True)
    mobile = models.CharField(verbose_name="Número de Celular",  max_length=11 , null = True, blank=True)
    tlf = models.CharField(verbose_name="Número de Telefonico", max_length=11 , null = True, blank=True)
    Email = models.EmailField(verbose_name= "Correo Electronico", null = True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de edición")

    def __str__(self):
        return (self.name)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name_plural = 'Proveedores'
        verbose_name = 'Proveedor'
        ordering = ['id']

class Pet(Estado):
    name = models.CharField(max_length = 50, verbose_name='Nombre')
    date_nac = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Fecha de Nacimiento')
    gender = models.CharField(max_length = 20, choices=gender_pet, default='Hembra')
    race = models.CharField(max_length = 50, verbose_name='Raza')
    weight = models.FloatField(max_length = 10, verbose_name='Peso', default=0)
    specie = models.CharField(max_length = 50, choices=species_pet, default='Gato')
    date_up = models.DateField(auto_now=False, verbose_name='Fecha visita')
    substitute = models.CharField(max_length = 150, verbose_name='Suplente', null = True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Propietario')

    def __str__(self):
        return (self.name)


    def toJSON(self):
        item = model_to_dict(self)
        item['client'] = {'id':self.client.id, 'dni': self.client.dni}
        return item

    class Meta:
        verbose_name_plural = 'Mascotas'
        verbose_name = 'Mascota'
        ordering = ['id']   
    
    