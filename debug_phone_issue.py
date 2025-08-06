#!/usr/bin/env python
"""
Debug script to understand the phone validation issue
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from main.forms import BookingForm
from services.models import Service
from areas.models import ServiceArea
from django.utils import timezone

def debug_phone_validation():
    print("Debugging phone validation issue...")
    print("=" * 60)
    
    # Get or create test data
    service, _ = Service.objects.get_or_create(
        name="Test Service",
        defaults={
            'description': 'Test service for validation',
            'is_active': True
        }
    )
    
    service_area, _ = ServiceArea.objects.get_or_create(
        name="Test Area",
        defaults={
            'phone': '+15062345678',
            'email': 'test@example.com',
            'address': '123 Test St',
            'is_active': True
        }
    )
    
    # Test with a problematic phone number
    test_phone = "(506) 234-5678"
    
    form_data = {
        'customer_name': 'John Doe',
        'email': 'john@example.com',
        'phone': test_phone,
        'address': '123 Main St, Test City',
        'service': service.id,
        'service_area': service_area.id,
        'urgency': 'medium',
        'preferred_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        'description': 'Test booking description'
    }
    
    print(f"Testing phone number: '{test_phone}'")
    print("-" * 40)
    
    # Create form and check validation step by step
    form = BookingForm(data=form_data)
    
    print("1. Form created")
    print(f"2. Form is bound: {form.is_bound}")
    
    # Check if form is valid
    print("3. Checking form validity...")
    is_valid = form.is_valid()
    print(f"4. Form is valid: {is_valid}")
    
    if not is_valid:
        print("5. Form errors:")
        for field, errors in form.errors.items():
            print(f"   {field}: {errors}")
        
        # Check specifically phone field validation
        if 'phone' in form.errors:
            print("\n6. Phone field validation details:")
            print(f"   Raw phone data: '{form.data.get('phone')}'")
            
            # Try to manually clean the phone field
            try:
                if hasattr(form, 'clean_phone'):
                    print("   Trying manual phone cleaning...")
                    form.cleaned_data = {}
                    form.cleaned_data['phone'] = form.data.get('phone')
                    cleaned_phone = form.clean_phone()
                    print(f"   Manual clean result: '{cleaned_phone}'")
                else:
                    print("   No clean_phone method found")
            except Exception as e:
                print(f"   Manual clean failed: {e}")
    else:
        print("5. Form is valid!")
        print(f"   Cleaned phone: '{form.cleaned_data['phone']}'")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    debug_phone_validation()