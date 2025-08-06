#!/usr/bin/env python
"""
Test specific phone number validation
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

import phonenumbers
from phonenumbers import NumberParseException
from main.forms import ContactForm
from areas.models import ServiceArea

def test_specific_phone():
    print("Testing specific phone number: 455 334-6677")
    print("=" * 50)
    
    phone = "455 334-6677"
    
    # Test with phonenumbers library directly
    print("1. Testing with phonenumbers library:")
    try:
        parsed = phonenumbers.parse(phone, 'CA')
        print(f"   Parsed: {parsed}")
        print(f"   Is valid: {phonenumbers.is_valid_number(parsed)}")
        print(f"   Is possible: {phonenumbers.is_possible_number(parsed)}")
        if phonenumbers.is_valid_number(parsed):
            print(f"   E164 format: {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)}")
    except NumberParseException as e:
        print(f"   Parse error: {e}")
    
    print()
    
    # Test with our form
    print("2. Testing with ContactForm:")
    service_area, _ = ServiceArea.objects.get_or_create(
        name="Test Area",
        defaults={
            'phone': '+15062345678',
            'email': 'test@example.com',
            'address': '123 Test St',
            'is_active': True
        }
    )
    
    form_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': phone,
        'subject': 'Test Subject',
        'message': 'Test message',
        'service_area': service_area.id
    }
    
    form = ContactForm(form_data)
    if form.is_valid():
        print(f"   ✓ PASS - Form is valid")
        print(f"   Cleaned phone: '{form.cleaned_data['phone']}'")
    else:
        print(f"   ✗ FAIL - Form validation errors:")
        for field, errors in form.errors.items():
            print(f"     - {field}: {errors[0]}")
    
    print()
    
    # Test some other potentially problematic numbers
    print("3. Testing other edge case numbers:")
    test_numbers = [
        "123 456-7890",  # Invalid area code (starts with 1)
        "012 345-6789",  # Invalid area code (starts with 0)
        "555 012-3456",  # Invalid exchange (starts with 0)
        "555 123-4567",  # Valid format
        "800 555-1212",  # Valid toll-free
    ]
    
    for test_phone in test_numbers:
        try:
            parsed = phonenumbers.parse(test_phone, 'CA')
            is_valid = phonenumbers.is_valid_number(parsed)
            print(f"   {test_phone}: {'Valid' if is_valid else 'Invalid'}")
        except NumberParseException:
            print(f"   {test_phone}: Parse error")

if __name__ == "__main__":
    test_specific_phone()