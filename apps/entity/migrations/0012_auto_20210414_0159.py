# Generated by Django 3.0.7 on 2021-04-14 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0011_pet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='entity.Client', verbose_name='Propietario'),
        ),
    ]
