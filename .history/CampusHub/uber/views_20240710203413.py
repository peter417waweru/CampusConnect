from datetime import timedelta, timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.messages import error
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, User
from django.http import JsonResponse
from .forms import  DriverCreationForm, VehicleForm, UberRequestForm, DriverProfileForm, TripForm
from .models import UberRequest, Driver, Vehicle, ChatMessage, Trip

# Custom decorator to check group
def group_required(group_name):
    def decorator(view_func):
        decorated_view_func = user_passes_test(
            lambda user: user.is_authenticated and user.groups.filter(name=group_name).exists(),
            login_url='login'
        )(view_func)
        return decorated_view_func
    return decorator

@group_required('students')
def uber_home(request):
    uber_requests = UberRequest.objects.filter(user=request.user)
    vehicles = Vehicle.objects.filter(is_available=True)
    
    context = {
        'vehicles':vehicles,
        'uber_request':uber_requests,
    }
    return render(request, 'uber/students/uber_home.html', context)
    
@login_required
def request_uber(request):
    if request.method == 'POST':
        form = UberRequestForm(request.POST)
        if form.is_valid():
            uber_request = form.save(commit=False)
            uber_request.user = request.user
            uber_request.status = 'requested'
            uber_request.save()

            driver = Vehicle.objects.filter(is_available=True).first().driver
            ChatMessage.objects.create(
                user = driver.user,
                uber_request = uber_request,
                message = f"You have a new request from {request.user.username}."
            )
            return redirect('uber:track_uber', pk=uber_request.pk)
    else:
        form = UberRequestForm()
    return render(request, 'uber/students/request_uber.html', {'form': form})


@login_required
def track_uber(request, pk):
    uber_request = get_object_or_404(UberRequest, pk=pk)
    return render(request, 'uber/students/track_uber.html', {'uber_request': uber_request,})


@login_required
def rate_uber(request, pk):
    uber_request = get_object_or_404(UberRequest, pk=pk)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        uber_request.driver_rating = rating
        uber_request.save()
        return redirect('uber:uber_home')
    return render(request, 'uber/students/rate_uber.html', {'uber_request': uber_request})


@login_required
def live_chat(request, pk):
    uber_request = get_object_or_404(UberRequest, pk=pk)
    if request.method == 'POST':
        message = request.POST.get('message')
        ChatMessage.objects.create(user=request.user, uber_request=uber_request, message=message)
        return redirect('uber:live_chat', pk=pk)
    
    chat_messages = ChatMessage.objects.filter(uber_request=uber_request)
    return render(request, 'uber/students/live_chat.html', {'uber_request': uber_request, 'chat_messages': chat_messages})


@login_required
def view_fare(request):
    if request.method == 'POST':
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        distance = calculate_distance(origin, destination)
        fare = calculate_fare(distance)
        return JsonResponse({'fare': fare})
    return render(request, 'uber/students/view_fare.html')


# Driver Creation & staff login.
def staff_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                return redirect('uber:create_driver')  
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'uber/admin/staff_login.html', context)

@login_required 
def create_driver(request):
    if request.method == 'POST':
        form = DriverCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.is_staff = False  
            user.save()
            return redirect('uber:driver_list')  
    else:
        form = DriverCreationForm()

    context = {'form': form}
    return render(request, 'uber/admin/create_driver.html', context)

@login_required
@staff_member_required 
def driver_list(request):
    drivers = User.objects.filter(is_staff=False)  
    context = {'drivers': drivers}
    return render(request, 'uber/admin/driver_list.html', context)

#Driver details and login
def uber_driver_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                
                try:
                    driver = Driver.objects.get(user=user) 
                    login(request, user)
                    return redirect('uber:driver_dashboard') 
                
                except Driver.DoesNotExist:
                    error(request, 'You are not a registered Uber Driver.')
                    pass
    else:
        form = AuthenticationForm()

    context = {'form': form, 'driver':driver}
    return render(request, 'login.html', context)
@login_required
def driver_profile(request):
    driver = Driver.objects.get(user=request.user)
    vehicle = Vehicle.objects.get(driver=driver)
    
    if request.method == 'POST':
        driver_form = DriverProfileForm(request.POST, instance=driver)
        vehicle_form = VehicleForm(request.POST, instance=vehicle)
        
        if driver_form.is_valid() and vehicle_form.is_valid():
            driver_form.save()
            vehicle_form.save()
            return redirect('uber:driver_profile')
    else:
        driver_form = DriverProfileForm(instance=driver)
        vehicle_form = VehicleForm(instance=vehicle)
    
    context = {
        'driver_form': driver_form,
        'vehicle_form': vehicle_form,
        'driver': driver,
        'vehicle': vehicle
    }
    
    return render(request, 'uber/drivers/driver_profile.html', context)

@login_required
@group_required('uber_drivers')
def driver_home(request):
    return render (request, 'uber/drivers/driver_home.html')


@login_required
@permission_required('uber.is_driver')
def driver_dashboard(request):
    return render(request, 'uber/drivers/driver_dashboard.html')


@login_required
def add_vehicle(request):
    user = request.user
    try:
        driver = Driver.objects.get(user=user)
    except Driver.DoesNotExist:
        driver = Driver.objects.create(user=user, license_number='', car_model='', car_license_plate='', phone_number='', address='')

    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.driver = driver
            vehicle.save()
            return redirect('uber:driver_dashboard')
    else:
        form = VehicleForm()
    
    return render(request, 'uber/drivers/add_vehicle.html', {'form': form})

@login_required
@permission_required('uber.is_driver')
def view_requests(request):
    if request.method ==  'POST':
        uber_request = get_object_or_404(UberRequest, pk=request.POST.get('request_id'))
        uber_request.status = 'accepted'
        uber_request.driver = Driver.objects.get(user=request.user)
        uber_request.estimated_arrival_time = timezone.now() + timedelta(minutes=10)
        uber_request.save()
        return redirect('uber:driver_dashboard')

@login_required
@permission_required('uber.is_driver')
def confirm_uber_request(request, pk):
    uber_request = get_object_or_404(UberRequest, pk=pk)
    if uber_request.status == 'requested':
        uber_request.status = 'accepted'
        uber_request.driver = Driver.objects.get(user=request.user)
        uber_request.save()

        ChatMessage.objects.create(
            user=uber_request.user,
            uber_request=uber_request,
            message=f"Your request has been accepted by {request.user.username}. Estimated arrival time is 10 minutes."
        )
        return redirect('uber:driver_dashboard')
    return render(request, 'uber/drivers/view_request.html', {'uber_request': uber_request})


@login_required
@permission_required('uber.is_driver')
def current_ride(request):
    ride = UberRequest.objects.filter(driver=request.user, status='accepted').first()
    return render(request, 'uber/drivers/current_ride.html', {'ride': ride})

@login_required
@permission_required('uber.is_driver')
def ride_history(request):
    rides = UberRequest.objects.filter(driver=request.user, status='completed').order_by('-updated_at')
    return render(request, 'uber/drivers/ride_history.html', {'rides': rides})


@login_required
@permission_required('uber.is_driver')
def live_chat_driver(request):
    # Logic for live chat with rider will be added here
    return render(request, 'uber/drivers/live_chat_driver.html')

@login_required
def record_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)  
            trip.driver = request.user  
            trip.save()
            return redirect('earning_dashboard')  
    else:
        form = TripForm()

    context = {'form': form}
    return render(request, 'earning_dashboard.html', context)

@login_required
def earning_dashboard(request):
    trips = Trip.objects.filter(driver=request.user)  # Filter trips for current driver
    total_earnings = sum(trip.fare for trip in trips)  # Calculate total earnings

    context = {'trips': trips, 'total_earnings': total_earnings}
    return render(request, 'earning_dashboard.html', context)


#Fare calculation
def calculate_distance(origin, destination):
    # Use hardcoded distance for development and testing
    distance = 10  # distance in kilometers
    return distance

def calculate_fare(distance):
    base_fare = 5.00  # base fare in currency
    fare_per_km = 2.00  # fare per kilometer in currency
    return base_fare + (fare_per_km * distance)
