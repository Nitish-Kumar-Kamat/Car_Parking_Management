# Generated by Django 5.1.4 on 2024-12-30 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0006_remove_entry_vehicle_parking_fee'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Vehicle',
        ),
    ]
