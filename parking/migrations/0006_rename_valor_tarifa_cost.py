# Generated by Django 4.2.7 on 2024-10-08 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0005_rename_cost_tarifa_valor_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarifa',
            old_name='valor',
            new_name='cost',
        ),
    ]
