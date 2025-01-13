from django.db import models

class Entry_Vehicle(models.Model):
    plate_number = models.CharField(max_length=20,unique=True)
    gate_no = models.IntegerField()
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)  # Exit time for when vehicle leaves
    level = models.CharField(
        max_length=20,
        choices=[
            ('Basement', 'Basement'),
            ('Ground Floor', 'Ground Floor'),
            ('First Floor', 'First Floor'),
            ('Second Floor', 'Second Floor'),
        ]
    )
    slot = models.CharField(max_length=20, default="Slot1")  # Parking slot

    def __str__(self):
        return f"{self.plate_number} - {self.level} - {self.slot}"


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
