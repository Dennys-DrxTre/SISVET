# Generated by Django 3.0.7 on 2021-04-14 13:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0003_auto_20210414_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy_sale',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 14, 8, 44, 17, 188726), verbose_name='Fecha'),
        ),
    ]