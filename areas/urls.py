from django.urls import path
from . import views

urlpatterns = [
    path('<slug:location_slug>/', views.location_home, name='location_home'),
    path('<slug:location_slug>/services/', views.location_services, name='location_services'),
    path('<slug:location_slug>/booking/', views.location_booking, name='location_booking'),
    path('<slug:location_slug>/contact/', views.location_contact, name='location_contact'),
]