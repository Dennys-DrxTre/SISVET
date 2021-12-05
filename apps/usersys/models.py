from django.db import models

# Create your models here.
class NotificationStatus(models.Model):
    status = models.BooleanField(default=True, verbose_name='Estado de Notificación')

    class Meta:
        verbose_name_plural = 'Estado de Notificación'
        verbose_name = 'Estado de Notificación'
        ordering = ['id']