import os
from django.conf import settings
from django.shortcuts import render,get_object_or_404,redirect
from .models import Entry_Vehicle, VehicleExit
from django.utils.timezone import now
from .utils import detect_number_plate,get_ocr_model
from django.contrib import messages

from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from datetime import datetime
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

def process_image(request):
    ocr_model = get_ocr_model() 

@never_cache
@login_required(login_url='/auth/login/')
def home(request):
    return render(request, 'main/base.html')



def registrations(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('main/registrations.html')
        return JsonResponse({'html': html})
    return render(request, 'main/registrations.html')


# def scan_vehicle(request):
#     if request.method == 'POST':
#         uploaded_file = request.FILES['image']

#         # Save the uploaded image to the media directory
#         file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
#         with open(file_path, 'wb+') as destination:
#             for chunk in uploaded_file.chunks():
#                 destination.write(chunk)
        
#         # Use YOLO-based detection to find number plates
#         number_plate = detect_number_plate(file_path)
        
        
#         if number_plate is None:
#             number_plate = "Number Plate Not detected!"
#         else:           # Save entry to database
#             vehicle = Vehicle.objects.create(
#               license_plate=number_plate,
#               entry_time=now(),  # Automatically set the current time
#               )

#             receipt_data = {
#             'image_name': uploaded_file.name,
#             'number_plate': number_plate,
#             'entry_time': vehicle.entry_time,
#             # 'image_url': f"{settings.MEDIA_URL}{uploaded_file.name}",
#             'image_url': f"/media/vehicles/{uploaded_file.name}",
            
#             }
#             return render(request, 'main/receipt.html', {'receipt': receipt_data})
#         return render(request,"main/receipt.html",{'numnot':number_plate})
    
    # return render(request, 'main/registrations.html')


def parking_manage(request):
    vehicles=Entry_Vehicle.objects.all
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('main/parking_manage.html',{'vehicles':vehicles})
        return JsonResponse({'html': html})
    return render(request, 'main/parking_manage.html')



def file_settings(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('main/file_settings.html', request=request)
        return JsonResponse({'html': html})
    return render(request, 'main/file_settings.html')

# Predefined slots for each level
SLOTS = {
    "Basement": ["Slot1", "Slot2", "Slot3", "Slot4"],
    "Ground Floor": ["Slot1", "Slot2", "Slot3", "Slot4"],
    "First Floor": ["Slot1", "Slot2", "Slot3", "Slot4"],
    "Second Floor": ["Slot1", "Slot2", "Slot3", "Slot4"],
}

def get_available_slots(request):
    selected_level = request.GET.get('level')
    booked_slots = Entry_Vehicle.objects.filter(level=selected_level).values_list('slot', flat=True)
    available_slots = [slot for slot in SLOTS[selected_level] if slot not in booked_slots]
    return JsonResponse({'slots': available_slots})



def entry(request):
    return render(request, 'main/entry.html')

def entry_vehicle(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        gate_no = request.POST.get('gate_no')
        level = request.POST.get('level')
        slot = request.POST['slot']

        # Save the uploaded image to the media directory
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Use YOLO-based detection to find number plates
        plate_number = detect_number_plate(file_path)
    
        if plate_number is None:
            plate_number = "Number Plate Not detected!"
        else:           # Save entry to database
            Entry_Vehicle.objects.create(
              plate_number=plate_number,
              gate_no=gate_no,
              level = level,
              slot = slot,
              entry_time=now(),  # Automatically set the current time
              )
            return redirect('/vehicle_list/')
            # vehicles = Entry_Vehicle.objects.all()
            # return render(request,'main/parking_manage.html',{'vehicles':vehicles})
        return render(request,"main/parking_manage.html",{'numnot':plate_number})


def vehicle_list(request):
    vehicles = Entry_Vehicle.objects.all()
    return render(request,'main/parking_manage.html',{'vehicles':vehicles})

def exit(request):
    return render(request,"main/exit_form.html")

def vehicle_exit_view(request):
    if request.method == "POST":
        # Ensure an image file is provided
        if 'image' not in request.FILES:
            return render(request, 'exit_error.html', {"error": "No image file provided"})

        uploaded_file = request.FILES['image']

        # Save the uploaded image to the media directory
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        try:
            plate_number = detect_number_plate(file_path)
        except Exception as e:
            return render(request, 'main/exit_error.html', {"error": "Number plate detection failed"})

        # Check if the vehicle exists in Entry_Vehicle
        try:
            entry_record = Entry_Vehicle.objects.get(plate_number=plate_number)
        except Entry_Vehicle.DoesNotExist:
            return render(request, 'main/exit_error.html', {"error": "Vehicle not found in entry records"})

        # Calculate duration and charges
        entry_time = entry_record.entry_time
        exit_time = now()
        duration = (exit_time - entry_time).total_seconds() / 60  # Duration in minutes
        charges = calculate_charges(duration)

        # Save to VehicleExit table
        exit_record = VehicleExit.objects.create(
            plate_number=plate_number,
            entry_time=entry_time,
            exit_time=exit_time,
            duration=round(duration),
            charges=charges
        )
        entry_record.delete()
        return render(request, 'main/exit_receipt.html', {"exit_record": [exit_record]})

    # If not POST request, return error page
    return render(request, 'main/exit_receipt', {"error": "Invalid request"})


def calculate_charges(duration):
    hourly_rate = 60   # example: 60 rs per hours
    return round((duration / 60) * hourly_rate, 2)
