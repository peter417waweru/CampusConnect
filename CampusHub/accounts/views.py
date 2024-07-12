# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import UserRegistrationForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='students')
            user.groups.add(group)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirect based on user group
            if user.groups.filter(name='students').exists():
                return redirect('home')
            elif user.groups.filter(name='uber_drivers').exists():
                return redirect('uber:driver_dashboard')
            elif user.groups.filter(name='hostel_managers').exists():
                return redirect('hostel:manager_dashboard')
            elif user.groups.filter(name='cafeteria_staff').exists():
                return redirect('order:cafeteria_staff_dashboard')
            elif user.groups.filter(name='shop_owners').exists():
                return redirect('order:shop_owner_dashboard')
            elif user.groups.filter(name='administrators').exists():
                return redirect('admin:index')  # or any admin-specific page
            else:
                return redirect('home')  # Default redirect

    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_page(request):
    logout(request)
    return redirect('login')

@login_required
def profile_page(request):
    return render(request, 'accounts/profile.html')

@login_required
def home_page(request):
    is_student = request.user.groups.filter(name='students').exists()
    return render(request, 'home.html', {'is_student': is_student})
