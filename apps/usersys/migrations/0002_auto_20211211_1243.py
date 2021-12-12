# Generated by Django 3.0.7 on 2021-12-11 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersys', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dollarstatus',
            name='price',
        ),
        migrations.AddField(
            model_name='dollarstatus',
            name='price_dollar',
            field=models.FloatField(default=0.0, verbose_name='Estado del bolivar en dolares'),
            preserve_default=False,
        ),
    ]