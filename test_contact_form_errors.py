#!/usr/bin/env python
"""
Test script to verify contact form error display is working
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from main.forms import ContactForm
from areas.models import ServiceArea

def test_contact_form_errors():
    print("Testing contact form error display...")
    print("=" * 50)
    
    # Get or create test service area
    service_area, _ = ServiceArea.objects.get_or_create(
        name="Test Area",
        defaults={
            'phone': '+15062345678',
            'email': 'test@example.com',
            'address': '123 Test St',
            'is_active': True
        }
    )
    
    # Test 1: Empty form (should have validation errors)
    print("1. Testing empty form submission:")
    empty_form = ContactForm({})
    if empty_form.is_valid():
        print("   ✗ FAIL - Empty form should not be valid")
    else:
        print("   ✓ PASS - Empty form has validation errors:")
        for field, errors in empty_form.errors.items():
            print(f"     - {field}: {errors[0]}")
    
    print()
    
    # Test 2: Invalid phone number
    print("2. Testing invalid phone number:")
    invalid_phone_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '123',  # Invalid phone
        'subject': 'Test Subject',
        'message': 'Test message',
        'service_area': service_area.id
    }
    
    invalid_phone_form = ContactForm(invalid_phone_data)
    if invalid_phone_form.is_valid():
        print("   ✗ FAIL - Invalid phone should not be valid")
    else:
        print("   ✓ PASS - Invalid phone has validation errors:")
        for field, errors in invalid_phone_form.errors.items():
            print(f"     - {field}: {errors[0]}")
    
    print()
    
    # Test 3: Valid form with various phone formats
    print("3. Testing valid phone formats:")
    valid_phones = [
        "(506) 234-5678",
        "506-234-5678",
        "506.234.5678",
        "506 234 5678",
        "5062345678"
    ]
    
    for phone in valid_phones:
        valid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': phone,
            'subject': 'Test Subject',
            'message': 'Test message',
            'service_area': service_area.id
        }
        
        valid_form = ContactForm(valid_data)
        if valid_form.is_valid():
            print(f"   ✓ PASS - Phone '{phone}' is valid")
            print(f"     Cleaned to: '{valid_form.cleaned_data['phone']}'")
        else:
            print(f"   ✗ FAIL - Phone '{phone}' should be valid")
            for field, errors in valid_form.errors.items():
                print(f"     - {field}: {errors[0]}")
    
    print()
    print("=" * 50)
    print("✅ Contact form error testing completed!")
    print("\nThe contact form template now uses Django form fields,")
    print("so validation errors should display properly in the browser.")

if __name__ == "__main__":
    test_contact_form_errors()