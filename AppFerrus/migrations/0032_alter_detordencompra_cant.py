# Generated by Django 3.2.9 on 2022-10-19 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppFerrus', '0031_ordencompramaterial_articulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detordencompra',
            name='cant',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
