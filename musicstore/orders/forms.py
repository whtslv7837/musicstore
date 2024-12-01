from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['user', 'total_amount', 'status', 'created_at', 'updated_at']
