# Generated by Django 3.0.7 on 2021-11-27 16:31

import apps.entity.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entity', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buy_Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Estado')),
                ('urlsecret', models.SlugField(blank=True, default=apps.entity.models.my_urlsecret, null=True)),
                ('next_visit', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Proxima visita')),
                ('status_notify', models.BooleanField(default=True, verbose_name='Notificador')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Fecha')),
                ('total', models.FloatField(default=0, verbose_name='Total')),
                ('iva', models.FloatField(default=0, verbose_name='IVA')),
                ('sub_total', models.FloatField(default=0, verbose_name='Sub Total')),
                ('type_bs', models.CharField(choices=[('Compra', 'Compra'), ('Venta', 'Venta')], max_length=30, verbose_name='Tipo')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='entity.Client', verbose_name='Cliente')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='entity.Provider', verbose_name='Proveedor')),
            ],
            options={
                'verbose_name': 'Compra_Venta',
                'verbose_name_plural': 'Compras_Ventas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ChildProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Estado')),
                ('urlsecret', models.SlugField(blank=True, default=apps.entity.models.my_urlsecret, null=True)),
                ('next_visit', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Proxima visita')),
                ('status_notify', models.BooleanField(default=True, verbose_name='Notificador')),
                ('stock', models.IntegerField(default=0, verbose_name='Cantidad')),
                ('price_buy', models.FloatField(default=0, verbose_name='Precio Compra')),
                ('price_sale', models.FloatField(default=0, verbose_name='Precio Venta')),
                ('date_conquered', models.DateField(verbose_name='Vencimiento')),
                ('profit', models.FloatField(default=0, verbose_name='Ganancia')),
            ],
            options={
                'verbose_name': 'Cantidad_Producto',
                'verbose_name_plural': 'Cantidad_Productos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Estado')),
                ('urlsecret', models.SlugField(blank=True, default=apps.entity.models.my_urlsecret, null=True)),
                ('next_visit', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Proxima visita')),
                ('status_notify', models.BooleanField(default=True, verbose_name='Notificador')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre Producto')),
                ('stock', models.IntegerField(blank=True, default=0, null=True, verbose_name='Cantidad')),
                ('num_sales', models.IntegerField(blank=True, default=0, null=True, verbose_name='Vendidos')),
                ('type_stock', models.CharField(choices=[('Litro(s)', 'Litro(s)'), ('Unidad(es)', 'Unidad(es)'), ('cm', 'cm'), ('g', 'g'), ('galon(es)', 'galon(es)'), ('kg', 'kg'), ('Libra(s)', 'Libra(s)'), ('onza(s)', 'onza(s)'), ('μg', 'μg'), ('mg', 'mg'), ('ml,', 'ml')], max_length=40, verbose_name='Unidad Medida')),
                ('quantity', models.FloatField(blank=True, default=0, null=True, verbose_name='Cantidad de medidad')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='VaccineDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Estado')),
                ('urlsecret', models.SlugField(blank=True, default=apps.entity.models.my_urlsecret, null=True)),
                ('next_visit', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Proxima visita')),
                ('status_notify', models.BooleanField(default=True, verbose_name='Notificador')),
                ('date', models.DateField(verbose_name='Fecha Creacion')),
                ('description', models.TextField(blank=True, max_length=100, null=True, verbose_name='Descripción')),
                ('quantity', models.FloatField(blank=True, null=True, verbose_name='Cantidad de medidad')),
                ('quantity_usage', models.IntegerField(blank=True, null=True, verbose_name='Cantidad usada')),
                ('quantity_pet', models.IntegerField(blank=True, null=True, verbose_name='Cantidad por mascota')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cashier.ChildProduct', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Jornada de Vacunaciones',
                'verbose_name_plural': 'Jornada de Vacunacion',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Detail_BS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Estado')),
                ('urlsecret', models.SlugField(blank=True, default=apps.entity.models.my_urlsecret, null=True)),
                ('next_visit', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Proxima visita')),
                ('status_notify', models.BooleanField(default=True, verbose_name='Notificador')),
                ('stock', models.IntegerField(default=0, verbose_name='Cantidad')),
                ('total', models.FloatField(default=0, verbose_name='Total')),
                ('profit', models.FloatField(default=0, verbose_name='Ganancia')),
                ('buy_sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cashier.Buy_Sale', verbose_name='Compra Venta')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cashier.ChildProduct', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Detalle_CV',
                'verbose_name_plural': 'Detalles_CV',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Det_VaccineDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Estado')),
                ('urlsecret', models.SlugField(blank=True, default=apps.entity.models.my_urlsecret, null=True)),
                ('next_visit', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Proxima visita')),
                ('status_notify', models.BooleanField(default=True, verbose_name='Notificador')),
                ('quantity', models.FloatField(blank=True, null=True, verbose_name='Cantidad de medidad')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entity.Pet', verbose_name='Paciente')),
                ('vaccineday', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cashier.VaccineDay', verbose_name='Jornada de vacunacion')),
            ],
            options={
                'verbose_name': 'Detalle Jornada de Vacunaciones',
                'verbose_name_plural': 'Detalle Jornada de Vacunacion',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='childproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cashier.Product', verbose_name='Producto'),
        ),
    ]
