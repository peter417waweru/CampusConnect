from django import forms
from .models import Feedback, SupportTicket

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message']
