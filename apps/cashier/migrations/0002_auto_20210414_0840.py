# Generated by Django 3.0.7 on 2021-04-14 13:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy_sale',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 14, 8, 40, 29, 30706), verbose_name='Fecha'),
        ),
    ]
