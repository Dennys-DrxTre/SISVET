# Generated by Django 3.0.7 on 2021-04-18 01:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0008_auto_20210415_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy_sale',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 17, 21, 3, 54, 635929), verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='product',
            name='num_sales',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Vendidos'),
        ),
    ]