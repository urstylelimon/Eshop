from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib import messages
# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products':products})

def single_product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/single_product.html', {'product': product})

def add_to_cart(request,pk):
    product = Product.objects.get(id=pk)
    cart = request.session.get('cart',{})
    print("My name is Limon")
    print(cart)

    if str(product.id) in cart:
        cart[str(product.id)] += 1
        request.session['cart'] = cart
    else:
        cart[str(product.id)] = 1
        request.session['cart'] = cart
    print(cart)

    return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart',{})
    print("I am form cart view")
    print(cart)

    cart_items = []
    total_amount = 0

    for item, value in cart.items():
        print(item)
        print(value)
        product = Product.objects.get(id=item)

        item_total = product.price * value
        cart_items.append({
            'product': product,
            'quantity': value,
            'item_total': item_total,
        })
        total_amount += item_total

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }

    return render(request, 'store/cart_view.html', context)






from django.shortcuts import render, redirect
from django.contrib import messages

def confirm_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        contact_number = request.POST.get('contact_number')
        location = request.POST.get('location')
        address = request.POST.get('address')

        # ✅ Do something with the data (e.g., save to DB, send email, print)
        print("Order Info:")
        print("Name:", full_name)
        print("Phone:", contact_number)
        print("Location:", location)
        print("Address:", address)
        print("Cart:", cart)

        # Clear cart after successful order
        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")

        return redirect('home')

    total_price = 20000
    return render(request, 'store/confirm_order.html', {
        'cart': cart,
        'total_price': total_price
    })

