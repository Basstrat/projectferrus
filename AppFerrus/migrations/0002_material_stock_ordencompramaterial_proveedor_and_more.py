# Generated by Django 4.1.1 on 2022-10-01 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppFerrus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='stock',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='ordencompramaterial',
            name='proveedor',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='AppFerrus.proveedores'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombre',
            field=models.CharField(blank=True, default=1, max_length=45),
        ),
    ]
