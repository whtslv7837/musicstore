from django.contrib import admin
from .models import Product, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_featured')
    list_filter = ('is_featured',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at')
    search_fields = ('author', 'text')
