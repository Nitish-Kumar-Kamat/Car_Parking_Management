# Generated by Django 5.1.4 on 2025-01-04 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0012_vehicleexit_remove_entry_vehicle_parking_fee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicleexit',
            old_name='vehicle_number',
            new_name='plate_number',
        ),
    ]
