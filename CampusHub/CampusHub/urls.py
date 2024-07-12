"""
URL configuration for CampusHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import home_page


urlpatterns = [
    #admin urls
    path('admin/', admin.site.urls),

    #home page urls
    path('', home_page, name='home'),

    #accounts urls
    path('accounts/', include('accounts.urls')),

    #uber urls
    path('uber/', include('uber.urls')),
    path('uber/', include('uber.urls', namespace='uber_students')),
    path('uber/', include('uber.urls', namespace='uber_drivers')),

    #hostel urls
    path('hostel/', include('hostel.urls')),

    #shoptreat urls
    path('shoptreat/', include('shoptreat.urls')),
    path('shoptreat/', include('shoptreat.urls', namespace='cafeteria_staff_login')),
    path('shoptreat/', include('shoptreat.urls', namespace='shop_owner_login')), 

    #trade urls
    path('trade/', include('trade.urls')),

    #workflow urls
    path('workflow/', include('workflow.urls')),

    #support urls
    path('support/', include('support.urls')),
]
