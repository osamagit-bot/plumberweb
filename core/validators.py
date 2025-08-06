"""
Custom validators for the plumber website
"""
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

try:
    import phonenumbers
    from phonenumbers import NumberParseException
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False


def validate_phone_number(phone):
    """
    Canadian phone number validation.
    Accepts formats like (506) 234-5678, 506-234-5678, etc.
    Uses phonenumbers library for proper validation.
    """
    if not phone:
        return phone
    
    phone = phone.strip()
    
    # First, try basic format validation
    pattern = r'^(\+?1[\s\-\.]?)?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}$'
    
    if not re.match(pattern, phone):
        raise ValidationError("Enter a valid Canadian phone number (e.g. (506) 234-5678)")
    
    # If phonenumbers library is available, use it for proper validation
    if PHONENUMBERS_AVAILABLE:
        try:
            parsed_number = phonenumbers.parse(phone, 'CA')
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError("The phone number entered is not valid. Please enter a valid Canadian phone number (e.g. (506) 234-5678)")
        except NumberParseException:
            raise ValidationError("Enter a valid Canadian phone number (e.g. (506) 234-5678)")
    
    return phone


# Create a reusable RegexValidator for forms
# Note: This is a simplified regex for basic validation. For comprehensive validation, use validate_phone_number function
phone_validator = RegexValidator(
    regex=r'^(\+?1[\s\-\.]?)?[\s\-\.]?\(?[2-9]\d{2}\)?[\s\-\.]?[2-9]\d{2}[\s\-\.]?\d{4}$|^\+[2-9]\d{6,14}$',
    message="Enter a valid Canadian phone number (e.g. (506) 234-5678)"
)


def clean_phone_number(phone):
    """
    Clean and format phone number for storage.
    This function can be used in form clean methods.
    Works with PhoneNumberField by ensuring proper formatting.
    """
    if not phone:
        return phone
    
    # Handle PhoneNumber objects from PhoneNumberField
    if hasattr(phone, 'as_e164'):
        # It's already a PhoneNumber object, just return it
        return phone
    
    # Convert to string if it's not already
    phone = str(phone).strip()
    
    # Validate first
    validate_phone_number(phone)
    
    if PHONENUMBERS_AVAILABLE:
        try:
            # Parse and format the number for consistency
            parsed_number = phonenumbers.parse(phone, 'CA')
            if phonenumbers.is_valid_number(parsed_number):
                # Return in E164 format for PhoneNumberField compatibility
                return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except NumberParseException:
            pass
    
    # If phonenumbers library is not available or parsing fails, 
    # try to normalize the format for North American numbers
    cleaned = re.sub(r'[\s\-\.\(\)]+', '', phone)
    
    # If it's a 10-digit number, add +1 prefix for international format
    if re.match(r'^[2-9]\d{9}$', cleaned):
        return f'+1{cleaned}'
    
    # If it already has +1 or 1 prefix, ensure it starts with +1
    if re.match(r'^1[2-9]\d{9}$', cleaned):
        return f'+{cleaned}'
    
    # Return as-is if it already has + prefix
    if phone.startswith('+'):
        return phone
    
    # Return the original format if we can't normalize it
    return phone