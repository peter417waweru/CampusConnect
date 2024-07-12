from django.urls import path
from . import views

app_name = 'uber'

urlpatterns = [
    # Students URLs
    path('students/request/', views.request_uber, name='request_uber'),
    path('students/live_chat/<int:pk>/', views.live_chat, name='live_chat'),
    path('students/view_fare/', views.view_fare, name='view_fare'),
    path('students/track/<int:pk>/', views.track_uber, name='track_uber'),
    path('students/rate/<int:pk>/', views.rate_uber, name='rate_uber'),
    path('', views.uber_home, name='home'),

    # Drivers URLs
    path('driver/profile/', views.driver_profile, name='driver_profile'),
    path('drivers/driver_dashboard', views.driver_dashboard, name='driver_dashboard'),
    path('', views.uber_driver_login, name='driver_login'),
    path('drivers/add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('drivers/view_requests/', views.view_requests, name='view_requests'),
    path('drivers/current_ride/', views.current_ride, name='current_ride'),
    path('drivers/ride_history/', views.ride_history, name='ride_history'),
    path('drivers/earning_dashboard/', views.earning_dashboard, name='earning_dashboard'),
    path('drivers/live_chat/', views.live_chat_driver, name='live_chat_driver'),


    #Admin URLS
    path('admin/create_driver/', views.create_driver, name='create_driver'),
    path('admin/driver_list/', views.driver_list, name='driver_list'),
    path('', views.staff_login, name='staff_login'),
]
