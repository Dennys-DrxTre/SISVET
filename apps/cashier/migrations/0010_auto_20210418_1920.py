# Generated by Django 3.0.7 on 2021-04-18 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0009_auto_20210417_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy_sale',
            name='date',
            field=models.DateTimeField(verbose_name='Fecha'),
        ),
    ]
