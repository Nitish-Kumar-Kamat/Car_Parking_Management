# Generated by Django 5.1.4 on 2025-01-07 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0013_rename_vehicle_number_vehicleexit_plate_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry_vehicle',
            name='exit_time',
        ),
    ]
