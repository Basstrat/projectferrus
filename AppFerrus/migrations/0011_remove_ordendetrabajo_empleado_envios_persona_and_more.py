# Generated by Django 4.1.1 on 2022-10-02 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppFerrus', '0010_envios_cliente_alter_envios_fecha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordendetrabajo',
            name='empleado',
        ),
        migrations.AddField(
            model_name='envios',
            name='persona',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='AppFerrus.persona'),
        ),
        migrations.AddField(
            model_name='ordendetrabajo',
            name='persona',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='AppFerrus.persona'),
        ),
    ]