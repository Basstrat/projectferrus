# Generated by Django 4.1.1 on 2022-10-11 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppFerrus', '0012_remove_ordendetrabajo_correlativo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detordentrabajo',
            name='idordendetrabajo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppFerrus.ordendetrabajo'),
        ),
    ]
