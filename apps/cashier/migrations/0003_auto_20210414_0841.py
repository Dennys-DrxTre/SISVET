# Generated by Django 3.0.7 on 2021-04-14 13:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0002_auto_20210414_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy_sale',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 14, 8, 41, 19, 280909), verbose_name='Fecha'),
        ),
    ]