from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Entry_Vehicle(models.Model):
    plate_number = models.CharField(max_length=20,unique=True)
    gate_no = models.IntegerField()
    entry_time = models.DateTimeField(auto_now_add=True)
    level = models.CharField(
        max_length=20,
        choices=[
            ('Basement', 'Basement'),
            ('Ground Floor', 'Ground Floor'),
            ('First Floor', 'First Floor'),
            ('Second Floor', 'Second Floor'),
        ]
    )
    parking_number = models.CharField(max_length=20, default="Park1")  # Parking slot

    def __str__(self):
        return f"{self.plate_number} - {self.level} - {self.parking_number}"


class VehicleExit(models.Model):
    plate_number = models.CharField(max_length=20)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()  # in minutes
    charges = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Razorpay order ID to link the payment
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"Exit {self.id} - {self.plate_number} - {self.charges}"


class Payment(models.Model):
    # Linking the Payment to a specific VehicleExit using OneToOneField
    vehicle_exit = models.OneToOneField('VehicleExit', on_delete=models.CASCADE, related_name='payment')
    
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    charges = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)  # Duration in minutes or seconds
    entry_time = models.DateTimeField(null=True, blank=True)
    exit_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment {self.id} - {self.razorpay_order_id}"


# Configurations here 

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(User, related_name='created_projects', on_delete=models.CASCADE)
    modify_date = models.DateTimeField(auto_now=True)
    modify_by = models.ForeignKey(User, related_name='modified_projects', on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name


class Tower(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tower_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tower_name

class Floor(models.Model):
    tower = models.ForeignKey(Tower, on_delete=models.CASCADE)
    floor_name = models.CharField(max_length=100)

    def __str__(self):
        return self.floor_name

class ParkingNumber(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    parking_number = models.CharField(max_length=50)

    def __str__(self):
        return self.parking_number
