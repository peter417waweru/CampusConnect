from django.shortcuts import render, get_object_or_404, redirect
from .models import Hostel, Booking
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
from .forms import BookingForm, HostelForm, HostelManagerLoginForm

def hostel_home(request):
    return render(request, 'hostel/hostel_home.html')

def view_hostels(request):
    hostels = Hostel.objects.all()
    return render(request, 'hostel/hostel_list.html', {'hostels': hostels})

def hostel_detail(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    return render(request, 'hostel/hostel_detail.html', {'hostel': hostel})

def manager_login(request):
    if request.method == 'POST':
        form = HostelManagerLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('hostel:manager_dashboard')
    else:
        form = HostelManagerLoginForm()
    return render(request, 'hostel/manager_login.html', {'form': form})

@login_required
def add_hostel(request):
    if request.method == 'POST':
        form = HostelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hostel:view_hostels')
        
    else:
        form = HostelForm()
    
    return render(request, 'hostel/add_hostel.html', {'form':form})

@login_required
def booking_calendar(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    bookings = Booking.objects.filter(hostel=hostel).order_by('start_date')
    return render(request, 'hostel/booking_calendar.html', {'hostel': hostel, 'bookings': bookings})

@login_required
def submit_application(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.hostel = hostel
            booking.user = request.user
            booking.save()
            return redirect('hostel:booking_success')
    else:
        form = BookingForm()
    return render(request, 'hostel/submit_application.html', {'form': form, 'hostel': hostel})

def booking_success(request):
    return render(request, 'hostel/booking_success.html')
