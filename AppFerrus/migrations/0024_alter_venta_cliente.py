# Generated by Django 3.2.9 on 2022-10-17 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppFerrus', '0023_auto_20221017_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='cliente',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='AppFerrus.cliente'),
        ),
    ]
