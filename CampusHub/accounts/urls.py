"""This module defines URL patterns for a Django application."""
from django.urls import path
from .views import register, login_page, profile_page, logout_page

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    path('profile/', profile_page, name='profile'),
    path('logout/', logout_page, name='logout'),
]
