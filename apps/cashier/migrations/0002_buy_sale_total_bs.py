# Generated by Django 3.0.7 on 2021-12-01 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy_sale',
            name='total_bs',
            field=models.FloatField(default=0, verbose_name='Total Bolivares'),
        ),
    ]
