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
import razorpay
from django.views.decorators.csrf import csrf_exempt
import logging

def process_image(request):
    ocr_model = get_ocr_model() 

@never_cache
@login_required(login_url='/auth/login/')
def home(request):
    return render(request, 'main/base.html')


def parking_manage(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('main/parking_manage.html')
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
        return render(request,"main/in_out.html",{'numnot':plate_number})


def vehicle_list(request):
    vehicles = Entry_Vehicle.objects.all()
    return render(request,"main/in_out.html",{'vehicles':vehicles})

def exit(request):
    return render(request,"main/exit_form.html")


def create_razorpay_order(charges_in_paise):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
    order_data = {
        'amount': charges_in_paise,  # Amount in paise
        'currency': 'INR',
        'payment_capture': '1'  # Automatic payment capture
    }
    order = client.order.create(data=order_data)
    return order['id']


# Razorpay client setup
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

# Logging setup
logger = logging.getLogger(__name__)

def vehicle_exit_view(request):
    if request.method == "POST":
        if 'image' not in request.FILES:
            return render(request, 'main/exit_error.html', {"error": "No image file provided"})

        uploaded_file = request.FILES['image']
        file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        try:
            plate_number = detect_number_plate(file_path)
        except Exception as e:
            return render(request, 'main/exit_error.html', {"error": "Number plate detection failed"})

        try:
            entry_record = Entry_Vehicle.objects.get(plate_number=plate_number)
        except Entry_Vehicle.DoesNotExist:
            return render(request, 'main/exit_error.html', {"error": "Vehicle not found in entry records"})

        entry_time = entry_record.entry_time
        exit_time = now()
        duration = (exit_time - entry_time).total_seconds() / 60
        charges = calculate_charges(duration)

        # Create VehicleExit record with a temporary razorpay_order_id
        exit_record = VehicleExit.objects.create(
            plate_number=plate_number,
            entry_time=entry_time,
            exit_time=exit_time,
            duration=round(duration),
            charges=charges,
            razorpay_order_id="temporary_order_id"  # Add temporary razorpay_order_id here for now
        )

        entry_record.delete()

        # Razorpay order ID creation
        razorpay_order_id = create_razorpay_order(int(charges * 100))  # Convert to integer
        print("Razorpay Order ID:", razorpay_order_id)

        # Update the exit_record with the generated razorpay_order_id
        exit_record.razorpay_order_id = razorpay_order_id
        exit_record.save()

        return render(request, 'main/exit_receipt.html', {
            "exit_record": exit_record,
            "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID,
            "razorpay_order_id": razorpay_order_id,
            "charges_in_paise": charges * 100
        })

    return render(request, 'main/exit_error.html', {"error": "Invalid request"})

def calculate_charges(duration):
    hourly_rate = 60
    return round((duration / 60) * hourly_rate, 2)


@csrf_exempt
def payment_success_view(request):
    if request.method == "GET":
        # Get Razorpay details from the query parameters
        payment_id = request.GET.get("payment_id")
        order_id = request.GET.get("order_id")
        payment_signature = request.GET.get("signature")

        if not payment_id or not order_id or not payment_signature:
            return render(request, 'main/payment_error.html', {
                'error': "Missing payment details."
            })

        # Log the received order_id to compare it with the stored one
        logger.debug(f"Received order_id from query parameters: {order_id}")

        # Verify the payment signature
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': payment_signature
        }

        try:
            # Razorpay's built-in signature verification
            client.utility.verify_payment_signature(params_dict)

            # Fetch payment details from Razorpay
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                # Log the payment status and try to fetch the exit record
                logger.debug(f"Payment captured for order_id: {order_id}")

                # Check if the VehicleExit record exists
                try:
                    # Ensure that the 'razorpay_order_id' is not null
                    exit_record = VehicleExit.objects.get(razorpay_order_id=order_id)

                    logger.debug(f"Found VehicleExit record: {exit_record}")

                    # Update the exit record with payment details
                    exit_record.payment_id = payment_id
                    exit_record.payment_status = 'Success'
                    exit_record.save()

                    # Render success page
                    return render(request, 'main/payment_success.html', {
                        'exit_record': exit_record,
                        'charges_in_paise': float(exit_record.charges),  # Convert charges to paise
                        'razorpay_order_id': order_id,
                    })

                except VehicleExit.DoesNotExist:
                    # Log missing record details for debugging
                    logger.error(f"VehicleExit record not found for order_id: {order_id}")
                    return render(request, 'main/payment_error.html', {
                        'error': "VehicleExit record not found."
                    })

            else:
                # Payment status is not 'captured'
                logger.error(f"Payment failed for order_id: {order_id}, status: {payment['status']}")
                return render(request, 'main/payment_error.html', {
                    'error': f"Payment status is '{payment['status']}'."  # payment['status'] is dynamic
                })

        except razorpay.errors.SignatureVerificationError:
            logger.error(f"Signature verification failed for order_id: {order_id}")
            return render(request, 'main/payment_error.html', {
                'error': "Payment signature verification failed."
            })

        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            return render(request, 'main/payment_error.html', {
                'error': f"An unexpected error occurred: {str(e)}"
            })

    return HttpResponse("Invalid request method", status=405)



 