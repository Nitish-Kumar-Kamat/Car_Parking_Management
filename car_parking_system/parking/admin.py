from django.contrib import admin
from .models import Entry_Vehicle

@admin.register(Entry_Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'gate_no', 'entry_time', 'level','slot')
