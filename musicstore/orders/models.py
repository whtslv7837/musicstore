from itertools import product
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
import datetime


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидается'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.pk:  # Если объект уже существует
            original = Order.objects.get(pk=self.pk)
            if original.status != 'cancelled' and self.status == 'cancelled':
                # Если статус изменился на "отменен"
                self.return_stock()

        super().save(*args, **kwargs)

    def return_stock(self):
        for item in self.orderitem_set.all():  # Получаем все товары в заказе
            item.product.stock_quantity += item.quantity
            item.product.save()

    def __str__(self):
        return f"Заказ #{self.id} от {self.created_at}"

    def get_items(self):
        return self.order_items.all()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

    def total_items(self):
        return sum(item.quantity for item in self.cart_items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity