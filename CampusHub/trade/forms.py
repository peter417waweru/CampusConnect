from django import forms
from .models import TradeItem, TradeRequest

class TradeItemForm(forms.ModelForm):
    class Meta:
        model = TradeItem
        fields = ['name', 'description', 'image', 'price']

class TradeRequestForm(forms.ModelForm):
    class Meta:
        model = TradeRequest
        fields = ['message']
