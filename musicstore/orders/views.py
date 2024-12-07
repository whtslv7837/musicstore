from django.shortcuts import render, redirect
from .models import Order, OrderItem, Cart, CartItem
from .forms import OrderForm
from products.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def create_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if cart.cart_items.count() == 0:
        return redirect('cart')

    # Вычисляем общую сумму заказа
    total_amount = cart.total_price()

    # Обработка формы заказа
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total_amount
            order.save()

            # Переносим товары из корзины в заказ и обновляем количество на складе
            for cart_item in cart.cart_items.all():
                if cart_item.product.quantity < cart_item.quantity:
                    # Если товара не хватает на складе
                    return redirect('insufficient_stock', product_id=cart_item.product.id)

                # Создаем запись о товаре в заказе
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

                # Уменьшаем количество товара на складе
                cart_item.product.quantity -= cart_item.quantity
                cart_item.product.save()

            # Очищаем корзину после оформления заказа
            cart.cart_items.all().delete()

            return redirect('order_success')
        else:
            return render(request, 'orders/create_order.html', {'form': form, 'cart': cart, 'total_amount': total_amount, 'errors': form.errors})
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form, 'cart': cart, 'total_amount': total_amount})

def insufficient_stock(request, product_id):
    product = Product.objects.get(id=product_id)  # Получаем товар по его ID
    return render(request, 'orders/insufficient_stock.html', {'product': product})

def order_success(request):
    return render(request, 'orders/order_success.html')

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    # Получаем или создаем корзину для пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Проверяем, есть ли уже товар в корзине
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:  # Если товар уже в корзине, увеличиваем его количество
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})


from django.shortcuts import render, get_object_or_404
from .models import Order

def order_details(request, order_id):
    """
    Вьюха для отображения деталей заказа.
    """
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'orders/order_details.html', {
        'order': order,
    })

@login_required
def order_list(request):
    """
    Вьюха для отображения списка заказов текущего пользователя.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {
        'orders': orders,
    })