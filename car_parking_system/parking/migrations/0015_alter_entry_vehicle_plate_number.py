# Generated by Django 5.1.4 on 2025-01-08 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0014_remove_entry_vehicle_exit_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry_vehicle',
            name='plate_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
