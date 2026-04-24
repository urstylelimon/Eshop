from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def home(request):
    products = Product.objects.all().order_by('-id')
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'products': products,
    }

    return render(request, 'store/home.html', context)


def single_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    products = Product.objects.exclude(id=pk).order_by('-id')[:8]

    context = {
        'product': product,
        'products': products,
    }

    return render(request, 'store/single_product.html', context)


def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)

    try:
        quantity = int(request.GET.get('quantity', 1))
    except ValueError:
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart = request.session.get('cart', {})

    product_id = str(product.id)

    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    request.session['cart'] = cart
    request.session.modified = True

    cart_count = sum(cart.values())

    return JsonResponse({
        'success': True,
        'cart_count': cart_count,
    })