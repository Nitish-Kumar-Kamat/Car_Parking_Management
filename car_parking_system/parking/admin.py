from django.contrib import admin
from .models import Entry_Vehicle, VehicleExit, Payment,Project,Tower,Floor,ParkingNumber

@admin.register(Entry_Vehicle)
class EntryVehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'gate_no', 'entry_time', 'level', 'parking_number')  # Fields to display in list view
    # list_filter = ('level', 'gate_no')  # Filters on the right side
    # search_fields = ('plate_number',)  # Search bar for plate number
    # ordering = ('-entry_time',)  # Default ordering by entry_time descending


@admin.register(VehicleExit)
class VehicleExitAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'entry_time', 'exit_time', 'duration', 'charges','razorpay_order_id')  # Fields to display in list view
    # list_filter = ('exit_time',)  # Filter by exit time
    # search_fields = ('plate_number',)  # Search bar for plate number
    # ordering = ('-exit_time',)  # Default ordering by exit_time descending

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_exit', 'razorpay_order_id', 'charges', 'duration', 'entry_time', 'exit_time')
    search_fields = ('vehicle_exit__plate_number', 'razorpay_order_id')  # Searching by vehicle plate number or Razorpay order ID
    list_filter = ('entry_time', 'exit_time')  # Filter by entry or exit time
    ordering = ('-entry_time',)  # Ordering by entry time in descending order
    readonly_fields = ('vehicle_exit', 'razorpay_order_id')  # Fields that should be readonly
    
    # Add additional fieldsets if needed for customization
    fieldsets = (
        (None, {
            'fields': ('vehicle_exit', 'razorpay_order_id', 'charges', 'duration', 'entry_time', 'exit_time')
        }),
    )

# Register the Payment model to the admin
# admin.site.register(Payment, PaymentAdmin)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'create_date', 'create_by', 'modify_date', 'modify_by')
    

@admin.register(Tower)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project', 'tower_name')
    

@admin.register(Floor)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('tower', 'floor_name')
    

@admin.register(ParkingNumber)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('floor', 'parking_number')
    
