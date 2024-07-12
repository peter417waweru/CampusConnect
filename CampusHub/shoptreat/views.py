from django.shortcuts import render, redirect, get_object_or_404
from .models import Meal, ShopItem, Order, OrderItem
from django.contrib.auth import login
from .forms import CafeteriaStaffLoginForm, ShopOwnerLoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

def marketplace_home(request):
    return render(request, 'shoptreat/marketplace_home.html')

def cafeteria_staff_login(request):
    if request.method == 'POST':
        form = CafeteriaStaffLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.groups.filter(name='cafeteria_staff').exists():
                login(request, user)
                return redirect('shoptreat:cafeteria_dashboard')
            else:
                form.add_error(None, 'You do not have cafeteria staff permissions.')
    else:
        form = CafeteriaStaffLoginForm()
    return render(request, 'shoptreat/cafeteria_staff_login.html', {'form': form})

@login_required
def cafeteria_dashboard(request):
    return render(request, 'shoptreat/cafeteria_dashboard.html')


def cafeteria_menu(request):
    meals = Meal.objects.all()
    return render(request, 'shoptreat/cafeteria_menu.html', {'meals': meals})

@login_required
def pre_order_meal(request):
    if request.method == 'POST':
        # Handle meal pre-order logic
        pass
    return render(request, 'shoptreat/pre_order.html')

@login_required
def shop_owner_dashboard(request):
    return render(request, 'shoptreat/shop_owner_dashboard.html')

def shop_owner_login(request):
    if request.method == 'POST':
        form = ShopOwnerLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.groups.filter(name='shop_owners').exists():
                login(request, user)
                return redirect('shoptreat:shop_owner_dashboard')
            else:
                form.add_error(None, 'You do not have shop owner permissions.')
    else:
        form = ShopOwnerLoginForm()
    return render(request, 'shoptreat/shop_owner_login.html', {'form': form})


def shop_browse(request):
    items = ShopItem.objects.all()
    return render(request, 'shoptreat/shop.html', {'items': items})

@login_required
def shopping_cart(request):
    # Handle shopping cart logic
    return render(request, 'shoptreat/shopping_cart.html')

@login_required
@csrf_exempt
def payment(request):
    if request.method == 'POST':
        # Process payment here
        # Mark the order as paid
        order = get_object_or_404(Order, user=request.user, paid=False)
        order.paid = True
        order.save()
        return redirect('shoptreat:marketplace_home')
    return render(request, 'shoptreat/payment.html')

