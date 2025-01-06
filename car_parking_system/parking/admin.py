from django.contrib import admin
from .models import Entry_Vehicle, VehicleExit

@admin.register(Entry_Vehicle)
class EntryVehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'gate_no', 'entry_time', 'exit_time', 'level', 'slot')  # Fields to display in list view
    # list_filter = ('level', 'gate_no')  # Filters on the right side
    # search_fields = ('plate_number',)  # Search bar for plate number
    # ordering = ('-entry_time',)  # Default ordering by entry_time descending


@admin.register(VehicleExit)
class VehicleExitAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'entry_time', 'exit_time', 'duration', 'charges')  # Fields to display in list view
    # list_filter = ('exit_time',)  # Filter by exit time
    # search_fields = ('plate_number',)  # Search bar for plate number
    # ordering = ('-exit_time',)  # Default ordering by exit_time descending
