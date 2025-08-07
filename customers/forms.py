from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import CustomerProfile
from core.validators import clean_phone_number, validate_phone_number


class CustomerRegistrationForm(UserCreationForm):
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(
        max_length=128, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. (506) 234-5678'
        }),
        help_text="Enter a valid Canadian phone number"
    )
    service_area = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=True,
        empty_label="Select your location",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Choose your service area location"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'service_area', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set service area queryset
        from areas.models import ServiceArea
        self.fields['service_area'].queryset = ServiceArea.objects.filter(is_active=True).order_by('name')
        
        self.fields['username'].help_text = 'Choose a unique username'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters'
        self.fields['password2'].help_text = 'Enter the same password as before'

        # Add CSS classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            return clean_phone_number(phone)
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Create customer profile with cleaned phone number and service area
            CustomerProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', ''),
                service_area=self.cleaned_data.get('service_area')
            )
        return user


class CustomerProfileForm(forms.ModelForm):
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(
        max_length=128, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. (506) 234-5678'
        }),
        help_text="Enter a valid Canadian phone number"
    )
    emergency_phone = forms.CharField(
        max_length=128, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. (506) 234-5678'
        }),
        help_text="Enter a valid Canadian emergency contact phone number"
    )
    service_area = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        empty_label="Select your location",
        widget=forms.Select(),
        help_text="Choose your service area location"
    )

    class Meta:
        model = CustomerProfile
        fields = [
            'service_area', 'address', 'city', 'postal_code',
            'emergency_contact',
            'preferred_contact_method', 'email_notifications', 'sms_notifications'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'preferred_contact_method': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set service area queryset
        from areas.models import ServiceArea
        self.fields['service_area'].queryset = ServiceArea.objects.filter(is_active=True).order_by('name')
        
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            # Set phone field initials from instance
            self.fields['phone'].initial = self.instance.phone
            self.fields['emergency_phone'].initial = self.instance.emergency_phone

        # Add CSS classes for Tailwind styling
        base_input_class = 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-blue focus:border-transparent transition duration-200 bg-gray-50 focus:bg-white'
        checkbox_class = 'w-4 h-4 text-primary-blue bg-gray-100 border-gray-300 rounded focus:ring-primary-blue focus:ring-2'
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = checkbox_class
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = base_input_class
                field.widget.attrs['rows'] = 3
            else:
                field.widget.attrs['class'] = base_input_class

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            validate_phone_number(phone)
            return phone
        return phone

    def clean_emergency_phone(self):
        emergency_phone = self.cleaned_data.get('emergency_phone')
        if emergency_phone:
            validate_phone_number(emergency_phone)
            return emergency_phone
        return emergency_phone

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Update user fields
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
            
            # Save the profile (phone fields are already handled by ModelForm)
            profile.save()
        return profile


class QuickBookingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate service choices from database
        from services.models import Service
        service_choices = [(service.id, service.name) for service in Service.objects.filter(is_active=True)]
        if not service_choices:
            # Fallback if no services in database
            service_choices = [('', 'No services available')]
        self.fields['service'].choices = service_choices

    service = forms.ChoiceField(
        choices=[],  # Will be populated in __init__
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select the type of service you need'
    )
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
    preferred_time = forms.ChoiceField(
        choices=[
            ('morning', 'Morning (8AM - 12PM)'),
            ('afternoon', 'Afternoon (12PM - 5PM)'),
            ('evening', 'Evening (5PM - 8PM)'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        help_text='Please describe the issue or service needed'
    )
    is_emergency = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Check if this is an emergency'
    )
