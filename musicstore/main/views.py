from django.shortcuts import render
from .models import Product, Review


def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:4]
    reviews = Review.objects.all()[:12]

    context = {
        'featured_products': featured_products,
        'reviews': reviews,
    }
    return render(request, 'main/home.html', context)

def contact(request):
    return render(request, 'main/contact.html')