from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib import messages
# Create your views here.


def products_list(request):
    products = Product.objects.all()
    return render(request,'store/product_list.html',{'products':products})

def product_detail(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Get or create the cart session
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        cart[str(pk)] += 1
    else:
        cart[str(pk)] = 1

    request.session['cart'] = cart

    messages.success(request, f"✅ {product.name} added to your cart!")
    return redirect('product_detail', pk=pk)

def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []

    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],
        })

    return render(request, 'store/cart.html', {'cart_items': cart_items})