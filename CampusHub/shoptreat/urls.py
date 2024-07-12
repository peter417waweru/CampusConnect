from django.urls import path
from . import views

app_name = 'shoptreat'

urlpatterns = [
    path('', views.marketplace_home, name='marketplace_home'),
    path('cafeteria/', views.cafeteria_menu, name='cafeteria_menu'),
    path('cafeteria/pre_order/', views.pre_order_meal, name='pre_order_meal'),
    path('shop/', views.shop_browse, name='shop_browse'),
    path('shop/cart/', views.shopping_cart, name='shopping_cart'),
    path('payment/', views.payment, name='payment'),

    path('cafeteria_staff/login/', views.cafeteria_staff_login, name='cafeteria_staff_login'),
    path('shop_owner/login/', views.shop_owner_login, name='shop_owner_login'),
    path('cafeteria/dashboard/', views.cafeteria_dashboard, name='cafeteria_dashboard'),
    path('shop_owner/dashboard/', views.shop_owner_dashboard, name='shop_owner_dashboard'),
]
