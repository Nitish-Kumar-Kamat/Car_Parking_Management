# Generated by Django 5.1.4 on 2024-12-30 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0005_entry_vehicle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry_vehicle',
            name='parking_fee',
        ),
    ]