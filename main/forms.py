from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div
from services.models import Service, Testimonial
from bookings.models import Booking, ContactMessage
from areas.models import ServiceArea
from core.constants import URGENCY_CHOICES, RATING_CHOICES


class BookingForm(forms.ModelForm):
    preferred_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }
        ),
        help_text="Select your preferred date and time"
    )
    
    class Meta:
        model = Booking
        fields = [
            'customer_name', 'email', 'phone', 'address', 
            'service', 'service_area', 'urgency', 'preferred_date', 'description'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your full address',
                'rows': 3
            }),
            'service': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'service_area': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'urgency': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Describe your plumbing issue in detail',
                'rows': 4
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.all()
        self.fields['service_area'].queryset = ServiceArea.objects.filter(is_active=True)
        self.fields['service_area'].required = False

    def clean_preferred_date(self):
        from django.utils import timezone
        preferred_date = self.cleaned_data['preferred_date']
        if preferred_date:
            # Make the datetime timezone-aware if it's naive
            if timezone.is_naive(preferred_date):
                preferred_date = timezone.make_aware(preferred_date)
            
            # Check if the date is in the past
            if preferred_date < timezone.now():
                raise forms.ValidationError("Preferred date cannot be in the past.")
        return preferred_date

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Basic phone validation
        import re
        phone_pattern = re.compile(r'^[\+]?[1-9][\d]{0,15}$')
        cleaned_phone = re.sub(r'[^\d+]', '', phone)
        if not phone_pattern.match(cleaned_phone):
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message', 'service_area']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your phone number (optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter message subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your message',
                'rows': 5
            }),
            'service_area': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_area'].queryset = ServiceArea.objects.filter(is_active=True)
        self.fields['service_area'].required = False
        self.fields['phone'].required = False

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if phone:
            # Basic phone validation if provided
            import re
            phone_pattern = re.compile(r'^[\+]?[1-9][\d]{0,15}$')
            cleaned_phone = re.sub(r'[^\d+]', '', phone)
            if not phone_pattern.match(cleaned_phone):
                raise forms.ValidationError("Please enter a valid phone number.")
        return phone


class CustomerFeedbackForm(forms.ModelForm):
    """Form for customers to leave feedback after service completion"""
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'rating-radio'
        }),
        help_text="Rate your overall experience"
    )
    
    class Meta:
        model = Testimonial
        fields = ['customer_name', 'email', 'phone', 'service', 'location', 'rating', 'comment', 'title']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter your phone number (optional)'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Brief title for your review (optional)'
            }),
            'service': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'location': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Tell us about your experience with our service...',
                'rows': 5
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.all()
        self.fields['location'].queryset = ServiceArea.objects.filter(is_active=True)
        self.fields['service'].required = False
        self.fields['location'].required = False
        self.fields['phone'].required = False
        self.fields['title'].required = False
        
        # Set default approval status to False for moderation
        if hasattr(self.instance, 'is_approved'):
            self.instance.is_approved = False

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if phone:
            import re
            phone_pattern = re.compile(r'^[\+]?[1-9][\d]{0,15}$')
            cleaned_phone = re.sub(r'[^\d+]', '', phone)
            if not phone_pattern.match(cleaned_phone):
                raise forms.ValidationError("Please enter a valid phone number.")
        return phone
