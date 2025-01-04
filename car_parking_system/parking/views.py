import os
from django.conf import settings
from django.shortcuts import render,get_object_or_404,redirect
from .models import Entry_Vehicle
from django.utils.timezone import now
from .utils import detect_number_plate,get_ocr_model
from django.contrib import messages

from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string

def process_image(request):
    ocr_model = get_ocr_model() 

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




# Vehicle exit view
def vehicle_exit(request, license_plate):
    # Find the vehicle by its license plate
    vehicle = get_object_or_404(Vehicle, license_plate=license_plate, exit_time__isnull=True)
    
    # Set exit time and calculate parking fee
    vehicle.exit_time = now()
    
    # Example fee calculation based on hours parked
    duration = (vehicle.exit_time - vehicle.entry_time).total_seconds() / 3600  # Duration in hours
    vehicle.parking_fee = round(duration * 10, 2)  # Example fee: $10 per hour
    
    # Save the updated vehicle record
    vehicle.save()
    
    # Receipt data to display
    receipt_data = {
        'license_plate': vehicle.license_plate,
        'entry_time': vehicle.entry_time,
        'exit_time': vehicle.exit_time,
        'parking_fee': vehicle.parking_fee,
    }
    
    return render(request, 'exit_receipt.html', {'receipt': receipt_data})

def parking_manage(request):
    vehicles=Entry_Vehicle.objects.all
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('main/parking_manage.html',{'vehicles':vehicles})
        return JsonResponse({'html': html})
    return render(request, 'main/parking_manage.html')



def file_settings(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('main/file_settings.html')
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
<<<<<<< HEAD


             #return redirect('vehicle_list')
             #vehicles = Entry_Vehicle.objects.all()
        #     return render(request,'main/parking_manage.html',{'vehicles':vehicles})
        # return render(request,"main/parking_manage.html",{'numnot':plate_number})
    # Fetch all vehicles for display
    vehicles = Entry_Vehicle.objects.all()
    return render(request, 'main/base.html', {'vehicles': vehicles})
    #return render(request, 'main/parking_manage.html', {'vehicles': vehicles, 'message': message})
=======
            # messages.success(request,"Records successfully Submitted!")
            return redirect('/vehicle_list/')
            # vehicles = Entry_Vehicle.objects.all()
            # return render(request,'main/parking_manage.html',{'vehicles':vehicles})
        return render(request,"main/parking_manage.html",{'numnot':plate_number})
>>>>>>> d627b70e221aca2d127e9fdb2da5e07df999d1c9


def vehicle_list(request):
    vehicles = Entry_Vehicle.objects.all()
    return render(request,'main/parking_manage.html',{'vehicles':vehicles})


