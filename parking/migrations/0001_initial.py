# Generated by Django 5.0.7 on 2024-09-03 12:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id_vehiculo', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('tipo_vehiculo', models.CharField(choices=[('Automóvil', 'Automóvil'), ('Moto', 'Moto')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioFrecuente',
            fields=[
                ('id_usuario', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre_U', models.CharField(max_length=100)),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('contraseña', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('id_vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking.vehiculo')),
            ],
        ),
    ]