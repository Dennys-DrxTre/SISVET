# Generated by Django 3.0.7 on 2021-04-13 18:23

import apps.entity.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0010_provider'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Estado')),
                ('urlsecret', models.SlugField(blank=True, default=apps.entity.models.my_urlsecret, null=True)),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('date_nac', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('gender', models.CharField(choices=[('Hembra', 'Hembra'), ('Macho', 'Macho')], default='Hembra', max_length=20)),
                ('race', models.CharField(max_length=50, verbose_name='Raza')),
                ('weight', models.FloatField(default=0, max_length=10, verbose_name='Peso')),
                ('specie', models.CharField(choices=[('Gato', 'Gato'), ('Perro', 'Perro')], default='Gato', max_length=50)),
                ('date_up', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('substitute', models.CharField(max_length=150, verbose_name='Suplente')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.Client', verbose_name='Propietario')),
            ],
            options={
                'verbose_name': 'Mascota',
                'verbose_name_plural': 'Mascotas',
                'ordering': ['id'],
            },
        ),
    ]