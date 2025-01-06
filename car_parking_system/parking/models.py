from django.db import models

class Entry_Vehicle(models.Model):
    plate_number = models.CharField(max_length=20)
    gate_no = models.IntegerField()
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)  # Exit time for when vehicle leaves
    level = models.CharField(max_length=20,
        choices=[
            ('Basement','Basement'),
            ('Ground Floor','Ground Floor'),
            ('First Floor','First Floor'),
            ('Second Floor','Second Floor'),
        ])
    slot = models.CharField(max_length=20, default="Slot1")  # Parking slot



class VehicleExit(models.Model):
    plate_number = models.CharField(max_length=20)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()  # in minutes
    charges = models.DecimalField(max_digits=10, decimal_places=2)
