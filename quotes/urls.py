from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.quote_calculator, name='quote_calculator'),
    path('api/calculator/<int:service_id>/', views.get_calculator_data, name='calculator_data'),
    path('api/submit/', views.submit_quote_request, name='submit_quote'),
]