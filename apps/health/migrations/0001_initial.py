# Generated by Django 3.0.7 on 2021-12-09 01:15

import apps.entity.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Estado')),
                ('urlsecret', models.SlugField(blank=True, default=apps.entity.models.my_urlsecret, null=True)),
                ('next_visit', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Proxima visita')),
                ('status_notify', models.BooleanField(default=True, verbose_name='Notificador')),
                ('name', models.TextField(max_length=50, verbose_name='Vacuna')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Vacuna')),
                ('total', models.FloatField(default=0, verbose_name='Total')),
                ('date', models.DateField(verbose_name='Fecha Creacion')),
                ('new_date', models.DateField(blank=True, null=True, verbose_name='proxima cita')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.Pet', verbose_name='Paciente')),
            ],
            options={
                'verbose_name': 'Vacunacion',
                'verbose_name_plural': 'Vacunaciones',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Parasite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Estado')),
                ('urlsecret', models.SlugField(blank=True, default=apps.entity.models.my_urlsecret, null=True)),
                ('next_visit', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Proxima visita')),
                ('status_notify', models.BooleanField(default=True, verbose_name='Notificador')),
                ('name', models.TextField(verbose_name='Desparasitante')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Desparasitante')),
                ('total', models.FloatField(default=0, verbose_name='Total')),
                ('date', models.DateField(verbose_name='Fecha Creacion')),
                ('new_date', models.DateField(blank=True, null=True, verbose_name='Proxima cita')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.Pet', verbose_name='Paciente')),
            ],
            options={
                'verbose_name': 'Desparasitacion',
                'verbose_name_plural': 'Desparasitaciones',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Estado')),
                ('urlsecret', models.SlugField(blank=True, default=apps.entity.models.my_urlsecret, null=True)),
                ('next_visit', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Proxima visita')),
                ('status_notify', models.BooleanField(default=True, verbose_name='Notificador')),
                ('motive', models.TextField(verbose_name='Motivo')),
                ('symptom', models.TextField(verbose_name='Sintomas')),
                ('temperature', models.TextField(verbose_name='Temperatura')),
                ('total', models.FloatField(blank=True, null=True, verbose_name='Total')),
                ('date_c', models.DateField(default=datetime.date.today, verbose_name='Fecha Creacion')),
                ('date_u', models.DateField(blank=True, null=True, verbose_name='Fecha Actualizacion')),
                ('diag_pre', models.TextField(blank=True, null=True, verbose_name='Diagnostico preventivo')),
                ('diag_def', models.TextField(blank=True, null=True, verbose_name='Diagnostico definitivo')),
                ('fre_car', models.TextField(blank=True, null=True, verbose_name='Frecuencia cardiaca')),
                ('fre_res', models.TextField(blank=True, null=True, verbose_name='Frecuencia respiratoria')),
                ('examination', models.TextField(blank=True, null=True, verbose_name='Examen')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.Pet', verbose_name='Paciente')),
            ],
            options={
                'verbose_name': 'Consulta',
                'verbose_name_plural': 'Consultas',
                'ordering': ['id'],
            },
        ),
    ]
