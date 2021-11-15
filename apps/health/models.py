from django.db import models
from CONFIG.settings import MEDIA_URL
from datetime import datetime, date, timedelta
from django.forms import model_to_dict
from apps.entity.models import my_urlsecret, Estado, Pet

# Create your models here.

class Consultation(Estado):
    motive = models.CharField(max_length = 30, verbose_name='Motivo')
    symptom = models.CharField(max_length = 60, verbose_name='Sintomas')
    temperature = models.FloatField(default=0, verbose_name='Temperatura')
    total = models.FloatField(default=0, verbose_name='Total')
    date_c = models.DateField(auto_now_add=False, verbose_name='Fecha Creacion')
    date_u = models.DateField(auto_now=False, verbose_name='Fecha Actualizacion')
    diag_pre = models.CharField(max_length = 50, null = True, blank=True, verbose_name='Diagnostico preventivo')
    diag_def = models.CharField(max_length = 50, null = True, blank=True, verbose_name='Diagnostico definitivo')
    fre_car = models.FloatField(default=0, null = True, blank=True, verbose_name='Frecuencia cardiaca')
    fre_res = models.FloatField(default=0, null = True, blank=True, verbose_name='Frecuencia respiratoria')
    examination = models.CharField(max_length = 50, null = True, blank=True, verbose_name='Examen')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Paciente')
    
    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['pet'] = {'id':self.pet.id, 'name': self.pet.name}
        return item

    class Meta:
        verbose_name_plural = 'Consultas'
        verbose_name = 'Consulta'
        ordering = ['id']   

class Vaccine(Estado):
    name = models.CharField(max_length = 50, verbose_name='Vacuna')
    description = models.TextField(verbose_name='Vacuna', null=True, blank=True)
    total = models.FloatField(default=0, verbose_name='Total')
    date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Fecha Creacion')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Paciente')

    def __str__(self):
        return (self.id)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name_plural = 'Vacunaciones'
        verbose_name = 'Vacunacion'
        ordering = ['id']   

class Parasite(Estado):
    name = models.CharField(max_length = 50, verbose_name='Desparasitante')
    description = models.TextField(verbose_name='Desparasitante', null=True, blank=True)
    total = models.FloatField(default=0, verbose_name='Total')
    date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Fecha Creacion')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Paciente')    

    def __str__(self):
        return (self.id)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name_plural = 'Desparasitaciones'
        verbose_name = 'Desparasitacion'
        ordering = ['id']    
    
    
    
    
    
    