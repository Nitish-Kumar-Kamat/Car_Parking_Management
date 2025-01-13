from django.contrib import admin
from django.urls import path
from parking import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # path('scan/', views.scan_vehicle, name='scan_vehicle'),   
    # AJAX endpoints for loading content
    path('registrations/', views.registrations, name='registrations'),
    path('parking_manage/',views.parking_manage, name='parking_manage'),
    path('file_settings/', views.file_settings, name='file_settings'),
    path('entry/',views.entry, name='entry'),
    path('entry_vehicle/',views.entry_vehicle, name='entry_vehicle'),
    path('vehicle_list/',views.vehicle_list, name='vehicle_list'),
    path('get_available_slots/', views.get_available_slots, name='get_available_slots'),
    path('exit/',views.exit, name='exit'),
    path('vehicle_exit/', views.vehicle_exit_view, name='vehicle_exit'),
    path('payment_success/', views.payment_success_view, name='payment_success'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

