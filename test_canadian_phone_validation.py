#!/usr/bin/env python
"""
Test Canadian phone number validation
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from main.forms import ContactForm, BookingForm
from areas.models import ServiceArea
from services.models import Service
from datetime import datetime, timedelta
from django.utils import timezone

def test_canadian_phone_validation():
    print("Testing Canadian Phone Number Validation")
    print("=" * 60)
    
    # Setup test data
    service_area, _ = ServiceArea.objects.get_or_create(
        name="Test Area",
        defaults={
            'phone': '+15062345678',
            'email': 'test@example.com',
            'address': '123 Test St',
            'is_active': True
        }
    )
    
    service, _ = Service.objects.get_or_create(
        name="Test Service",
        defaults={
            'description': 'Test service',
            'is_active': True
        }
    )
    
    # Test cases: Valid Canadian phone numbers
    print("1. Testing VALID Canadian phone numbers:")
    print("-" * 40)
    
    valid_phones = [
        "(506) 234-5678",  # New Brunswick
        "416-555-1234",    # Toronto
        "604.555.9876",    # Vancouver
        "514 555 4321",    # Montreal
        "4165551234",      # Toronto (no formatting)
        "+1 506 234 5678", # International format
        "+1-416-555-1234", # International with dashes
        "1-506-234-5678",  # North American format
    ]
    
    for phone in valid_phones:
        contact_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': phone,
            'subject': 'Test Subject',
            'message': 'Test message',
            'service_area': service_area.id
        }
        
        form = ContactForm(contact_data)
        if form.is_valid():
            print(f"   ✓ PASS: '{phone}' → '{form.cleaned_data['phone']}'")
        else:
            print(f"   ✗ FAIL: '{phone}' - {form.errors.get('phone', ['Unknown error'])[0]}")
    
    print()
    
    # Test cases: Invalid phone numbers
    print("2. Testing INVALID phone numbers:")
    print("-" * 40)
    
    invalid_phones = [
        "455 334-6677",    # Invalid area code (455 not assigned)
        "123 456-7890",    # Invalid area code (starts with 1)
        "012 345-6789",    # Invalid area code (starts with 0)
        "555 012-3456",    # Invalid exchange (starts with 0)
        "555 123-456",     # Too short
        "555 123-45678",   # Too long
        "abc def-ghij",    # Non-numeric
        "555-123",         # Incomplete
        "",                # Empty (should be valid for optional fields)
    ]
    
    for phone in invalid_phones:
        contact_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': phone,
            'subject': 'Test Subject',
            'message': 'Test message',
            'service_area': service_area.id
        }
        
        form = ContactForm(contact_data)
        if phone == "":  # Empty phone should be valid (optional field)
            if form.is_valid():
                print(f"   ✓ PASS: Empty phone is valid (optional field)")
            else:
                print(f"   ✗ FAIL: Empty phone should be valid - {form.errors}")
        else:
            if not form.is_valid() and 'phone' in form.errors:
                print(f"   ✓ PASS: '{phone}' correctly rejected")
                print(f"          Error: {form.errors['phone'][0]}")
            else:
                print(f"   ✗ FAIL: '{phone}' should be invalid but was accepted")
    
    print()
    
    # Test with BookingForm (required phone field)
    print("3. Testing BookingForm (required phone field):")
    print("-" * 40)
    
    booking_data = {
        'customer_name': 'John Doe',
        'email': 'john@example.com',
        'phone': '(506) 234-5678',
        'address': '123 Main St, Test City',
        'service': service.id,
        'service_area': service_area.id,
        'urgency': 'medium',
        'preferred_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        'description': 'Test booking description'
    }
    
    booking_form = BookingForm(booking_data)
    if booking_form.is_valid():
        print(f"   ✓ PASS: Valid booking form with Canadian phone")
        print(f"          Phone cleaned to: '{booking_form.cleaned_data['phone']}'")
    else:
        print(f"   ✗ FAIL: Booking form should be valid")
        for field, errors in booking_form.errors.items():
            print(f"          {field}: {errors[0]}")
    
    # Test empty phone in required field
    booking_data['phone'] = ''
    booking_form_empty = BookingForm(booking_data)
    if not booking_form_empty.is_valid() and 'phone' in booking_form_empty.errors:
        print(f"   ✓ PASS: Empty phone correctly rejected in required field")
    else:
        print(f"   ✗ FAIL: Empty phone should be rejected in required field")
    
    print()
    print("=" * 60)
    print("✅ Canadian phone validation testing completed!")
    print()
    print("Key improvements made:")
    print("• Phone validation now specifically targets Canadian numbers")
    print("• Clear error messages mention 'Canadian phone number'")
    print("• Placeholders show Canadian format examples")
    print("• Both contact forms now use Django form fields for proper error display")
    print("• Invalid area codes (like 455) are properly rejected")

if __name__ == "__main__":
    test_canadian_phone_validation()