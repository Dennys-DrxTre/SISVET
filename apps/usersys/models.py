from django.db import models

# Create your models here.
class NotificationStatus(models.Model):
    status = models.BooleanField(default=True, verbose_name='Estado de Notificación')

    class Meta:
        verbose_name_plural = 'Estado de Notificación'
        verbose_name = 'Estado de Notificación'
        ordering = ['id']

class DollarStatus(models.Model):
    price_dollar = models.FloatField(verbose_name='Estado del bolivar en dolares')

    class Meta:
        verbose_name_plural = 'Estado del Dolar'
        verbose_name = 'Estado del Dolar'
        ordering = ['id']