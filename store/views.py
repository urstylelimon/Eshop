from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
# Create your views here.


def products_list(request):
    products = Product.objects.all()
    return render(request,'store/product_list.html',{'products':products})

def product_detail(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    cart = request.session.get('cart', {})

    if str(pk) in cart:
        cart[str(pk)] += 1  # Increment quantity if already in cart
    else:
        cart[str(pk)] = 1  # Add new product to cart

    request.session['cart'] = cart  # Save back to session

    return redirect('product_detail', pk=pk)