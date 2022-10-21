# Generated by Django 3.2.9 on 2022-10-19 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppFerrus', '0027_detordencompra_articulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='cantidadcompra',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='material',
            name='totalcompra',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='ordencompramaterial',
            name='cantidadcompra',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
