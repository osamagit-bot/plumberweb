from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from services.models import Service
from .models import QuoteCalculator, QuoteRequest
import json


def quote_calculator(request):
    services = Service.objects.filter(is_active=True, calculator__isnull=False)
    return render(request, 'quotes/calculator.html', {'services': services})


def get_calculator_data(request, service_id):
    calculator = get_object_or_404(QuoteCalculator, service_id=service_id, is_active=True)
    data = {
        'base_price': float(calculator.base_price),
        'labor_rate': float(calculator.labor_rate_per_hour),
        'estimated_hours': float(calculator.estimated_hours),
        'options': [
            {
                'id': option.id,
                'name': option.name,
                'description': option.description,
                'price': float(option.price_modifier),
                'required': option.is_required,
            }
            for option in calculator.options.all()
        ]
    }
    return JsonResponse(data)


@csrf_exempt
def submit_quote_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        quote_request = QuoteRequest.objects.create(
            service_id=data['service_id'],
            customer_name=data['customer_name'],
            email=data['email'],
            phone=data['phone'],
            address=data['address'],
            selected_options=data['selected_options'],
            estimated_total=data['estimated_total'],
            notes=data.get('notes', ''),
        )
        return JsonResponse({'success': True, 'quote_id': quote_request.id})
    return JsonResponse({'success': False})