# Generated by Django 3.0.7 on 2021-04-15 16:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0006_auto_20210414_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail_bs',
            name='iva',
            field=models.FloatField(default=0, verbose_name='IVA'),
        ),
        migrations.AddField(
            model_name='detail_bs',
            name='sub_total',
            field=models.FloatField(default=0, verbose_name='Sub Total'),
        ),
        migrations.AlterField(
            model_name='buy_sale',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 15, 11, 12, 8, 713737), verbose_name='Fecha'),
        ),
    ]