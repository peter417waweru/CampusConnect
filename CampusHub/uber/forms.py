from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Driver, Vehicle, UberRequest, Trip

class DriverCreationForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['license_number', 'car_model', 'car_license_plate', 'phone_number', 'address']

    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['license_number', 'car_model', 'car_license_plate', 'phone_number', 'address',]


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['car_model', 'car_license_plate', 'is_available']

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['distance', 'fare']

        
class UberRequestForm(forms.ModelForm):
    class Meta:
        model = UberRequest
        fields = ['destination', 'fare_estimate', 'pickup_location']
