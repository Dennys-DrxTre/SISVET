from django.db import models

# Create your models here.
class NotificationStatus(models.Model):
    status = models.BooleanField(default=True, verbose_name='Estado de Notificación')

    class Meta:
        verbose_name_plural = 'Estado de Notificación'
        verbose_name = 'Estado de Notificación'
<<<<<<< HEAD
        ordering = ['id']

class DollarStatus(models.Model):
    price_dollar = models.FloatField(verbose_name='Estado del bolivar en dolares')

    class Meta:
        verbose_name_plural = 'Estado del Dolar'
        verbose_name = 'Estado del Dolar'
=======
>>>>>>> b0891a40af8565bd3fc0e1b635d55a867dbce1e5
        ordering = ['id']