from django import forms
from .models import Booking, Hostel
from django.contrib.auth.forms import AuthenticationForm

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'description', 'amenities', 'rental_rate', 'image']

class HostelManagerLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))