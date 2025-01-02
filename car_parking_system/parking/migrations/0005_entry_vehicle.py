# Generated by Django 5.1.4 on 2024-12-28 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0004_alter_vehicle_license_plate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry_Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate_number', models.CharField(max_length=20)),
                ('gate_no', models.IntegerField()),
                ('entry_time', models.DateTimeField(auto_now_add=True)),
                ('parking_fee', models.FloatField()),
            ],
        ),
    ]
