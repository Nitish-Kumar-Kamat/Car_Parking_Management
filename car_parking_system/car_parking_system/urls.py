from django.contrib import admin
from django.urls import path,include
from parking import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('auth_app.urls')),
    path('', views.home, name='home'),
    # AJAX endpoints for loading content
    path('parking_manage/',views.parking_manage, name='parking_manage'),
    path('file_settings/', views.file_settings, name='file_settings'),
    path('entry/',views.entry, name='entry'),
    path('entry_vehicle/',views.entry_vehicle, name='entry_vehicle'),
    path('vehicle_list/',views.vehicle_list, name='vehicle_list'),
    path('get_available_parks/', views.get_available_parks, name='get_available_park'),
    path('exit/',views.exit, name='exit'),
    path('vehicle_exit/', views.vehicle_exit_view, name='vehicle_exit'),
    path('payment_success/', views.payment_success_view, name='payment_success'),
    
    path('create_project/',views.create_project, name='create_project'),
    path('project_list/',views.project_list, name='project_list'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

