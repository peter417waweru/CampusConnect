from django.urls import path
from .views import support_home, submit_feedback, list_feedback, support_ticket, list_tickets

app_name = 'support'

urlpatterns = [
    path('', support_home, name='support_home'),
    path('feedback/', submit_feedback, name='submit_feedback'),
    path('feedback/list/', list_feedback, name='list_feedback'),
    path('ticket/', support_ticket, name='support_ticket'),
    path('ticket/list/', list_tickets, name='list_tickets'),
]
