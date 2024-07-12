from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'hostel'

urlpatterns = [
    path('', views.hostel_home, name='hostel_home'),
    path('view/', views.view_hostels, name='view_hostels'),
    path('detail/<int:hostel_id>/', views.hostel_detail, name='hostel_detail'),
    path('calendar/<int:hostel_id>/', views.booking_calendar, name='booking_calendar'),
    path('submit/<int:hostel_id>/', views.submit_application, name='submit_application'),
    path('success/', views.booking_success, name='booking_success'),
    path('add/', views.add_hostel, name='add_hostel'),
    path('manager_login/', views.manager_login, name='manager_login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)