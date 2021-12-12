# Generated by Django 3.0.7 on 2021-12-09 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DollarStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=True, verbose_name='Estado del bolivar en dolares')),
            ],
            options={
                'verbose_name': 'Estado del Dolar',
                'verbose_name_plural': 'Estado del Dolar',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='NotificationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Estado de Notificación')),
            ],
            options={
                'verbose_name': 'Estado de Notificación',
                'verbose_name_plural': 'Estado de Notificación',
                'ordering': ['id'],
            },
        ),
    ]
