from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    actions = ['mark_as_cancelled']

    def mark_as_cancelled(self, request, queryset):
        # Обновляем статус на "Отменен"
        queryset.update(status='cancelled')

        # Для каждого заказа в queryset вызываем return_stock()
        for order in queryset:
            order.return_stock()

    mark_as_cancelled.short_description = "Отменить выбранные заказы"

admin.site.register(OrderItem)
