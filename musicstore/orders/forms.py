from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']  # Вы можете добавить дополнительные поля, например, адрес или телефон.
