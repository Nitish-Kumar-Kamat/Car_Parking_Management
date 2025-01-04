from django.db import models

# class Vehicle(models.Model):
#     license_plate = models.CharField(max_length=20)
#     entry_time = models.DateTimeField(auto_now_add=True)  # Automatically set when the vehicle is created
#     exit_time = models.DateTimeField(null=True, blank=True)  # Can be set later
#     parking_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional field for fee

#     def __str__(self):
#         return self.license_plate or "Unknown Vehicle"

class Entry_Vehicle(models.Model):
    plate_number = models.CharField(max_length=20)
    gate_no = models.IntegerField()
    entry_time = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=20,
        choices=[
        ('Basement','Basement'),
        ('Ground Floor','Ground Floor'),
        ('First Floor','First Floor'),
        ('Second Floor','Second Floor'),
        ])
    slot = models.CharField(max_length=20,default="Slot1")
