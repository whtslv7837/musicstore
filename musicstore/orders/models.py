from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from .utils import generate_qr_code
from django.core.files.base import ContentFile

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
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Новый объект
            super().save(*args, **kwargs)
            self.generate_qr_code()  # Генерация QR-кода
        elif self.pk:  # Существующий объект
            original = Order.objects.get(pk=self.pk)
            if original.status != 'cancelled' and self.status == 'cancelled':
                self.return_stock()  # Возврат товара
            elif original.status == 'cancelled' and self.status != 'cancelled':
                self.deduct_stock()  # Вычитание товара

        super().save(*args, **kwargs)

    def generate_qr_code(self):
        """Генерирует QR-код для заказа и сохраняет его в поле qr_code"""
        qr_data = f"Заказ №{self.id}\nСумма: {self.total_amount} руб."
        qr_image = generate_qr_code(qr_data)
        qr_filename = f"order_{self.id}.png"
        self.qr_code.save(qr_filename, ContentFile(qr_image), save=False)

    def deduct_stock(self):
        """Вычитание товара со склада"""
        for item in self.order_items.all():
            if item.product.quantity < item.quantity:
                raise ValueError(f"Недостаточно товара {item.product.name} на складе!")
            item.product.quantity -= item.quantity
            item.product.save()

    def return_stock(self):
        """Возврат товара на склад"""
        for item in self.order_items.all():
            item.product.quantity += item.quantity
            item.product.save()

    def __str__(self):
        return f"Заказ #{self.id} от {self.created_at}"

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
