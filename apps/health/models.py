from django.db import models
from CONFIG.settings import MEDIA_URL
from datetime import datetime
from django.forms import model_to_dict
from django.db.models.signals import post_save, pre_save
from datetime import datetime, date, time, timedelta
import calendar
# Create your models here.
from apps.entity.models import my_urlsecret, Estado, Pet


class Consultation(Estado):
    motive = models.TextField(verbose_name='Motivo')
    symptom = models.TextField(verbose_name='Sintomas')
    temperature = models.TextField( verbose_name='Temperatura')
    total = models.FloatField(null = True, blank=True,verbose_name='Total')
    date_c = models.DateField(default= date.today, verbose_name='Fecha Creacion')
    date_u = models.DateField(null=True, blank= True, verbose_name='Fecha Actualizacion')
    diag_pre = models.TextField(null = True, blank=True, verbose_name='Diagnostico preventivo')
    diag_def = models.TextField(null = True, blank=True, verbose_name='Diagnostico definitivo')
    fre_car = models.TextField( null = True, blank=True, verbose_name='Frecuencia cardiaca')
    fre_res = models.TextField( null = True, blank=True, verbose_name='Frecuencia respiratoria')
    examination = models.TextField(null = True, blank=True, verbose_name='Examen')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Paciente')
    
    def __str__(self): 
        return (self.pet.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['pet'] = {'name': self.pet.name,'id': self.pet.id , 'client': self.pet.client.dni, 'gender': self.pet.gender, 'race': self.pet.race, 'specie': self.pet.specie}
        return item

    class Meta:
        verbose_name_plural = 'Consultas'
        verbose_name = 'Consulta'
        ordering = ['id']   


class Vaccine(Estado):
    name = models.TextField(max_length = 50, verbose_name='Vacuna')
    description = models.TextField(verbose_name='Vacuna', null=True, blank=True)
    total = models.FloatField(default=0, verbose_name='Total')
    date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Fecha Creacion')
    new_date = models.DateField(verbose_name='proxima cita',null = True, blank=True )
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Paciente')

    def __str__(self):
        return (self.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['pet'] = {'name': self.pet.name,'id': self.pet.id , 'client': self.pet.client.dni, 'gender': self.pet.gender, 'race': self.pet.race, 'specie': self.pet.specie, 'new_date':self.new_date}
        return item

    class Meta:
        verbose_name_plural = 'Vacunaciones'
        verbose_name = 'Vacunacion'
        ordering = ['id']   


class Parasite(Estado):
    name = models.TextField(verbose_name='Desparasitante')
    description = models.TextField(verbose_name='Desparasitante', null=True, blank=True)
    total = models.FloatField(default=0, verbose_name='Total')
    date = models.DateField(auto_now_add=False, verbose_name='Fecha Creacion')
    new_date = models.DateField(verbose_name='Proxima cita', null = True, blank=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Paciente')    

    def __str__(self):
        return (self.name)

    def toJSON(self):
        item = model_to_dict(self)
        item['pet'] = {'name': self.pet.name,'id': self.pet.id , 'client': self.pet.client.dni, 'gender': self.pet.gender, 'race': self.pet.race, 'specie': self.pet.specie, 'new_date':self.new_date}
        return item

    class Meta:
        verbose_name_plural = 'Desparasitaciones'
        verbose_name = 'Desparasitacion'
        ordering = ['id']    
    