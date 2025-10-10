from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category,Product
from django.contrib import messages
# Create your views here.


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'store/home.html', context)

def single_product(request,pk):
    product = Product.objects.get(id=pk)
    products = Product.objects.all()
    return render(request, 'store/single_product.html', {'product': product,'products':products})


def add_to_cart(request, pk):
    quantity = int(request.GET.get('quantity'))
    product = Product.objects.get(id=pk)
    cart = request.session.get('cart', {})

    if str(product.id) in cart:
        cart[str(product.id)] += quantity
        request.session['cart'] = cart
    else:
        cart[str(product.id)] = quantity
        request.session['cart'] = cart

    # Calculate total items
    cart_count = sum(cart.values())

    return JsonResponse({
        'success': True,
        'cart_count': cart_count  # Make sure this line is there
    })

