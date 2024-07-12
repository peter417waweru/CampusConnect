from django.urls import path
from .views import trade_home, list_items, item_detail, create_item, boardroom

app_name = 'trade'

urlpatterns = [
    path('', trade_home, name='trade_home'),
    path('items/', list_items, name='list_items'),
    path('items/<int:pk>/', item_detail, name='item_detail'),
    path('items/new/', create_item, name='create_item'),
    path('boardroom/', boardroom, name='boardroom'),
]
