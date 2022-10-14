# Generated by Django 4.1.1 on 2022-10-14 04:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppFerrus', '0018_alter_venta_cliente_detordencompra'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordencompramaterial',
            name='fecha',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Fecha_venta'),
        ),
        migrations.AddField(
            model_name='ordencompramaterial',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='ordencompramaterial',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
