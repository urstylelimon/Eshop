from store.models import Product
from order.models import Order


from django.shortcuts import render, redirect
from django.contrib import messages

from store.views import single_product



def order_home(request):
    return render(request,'orders/order_home.html')

def create_confirm_order(request):
    cart = request.session.get('cart', {})
    print(cart)
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


        total_price = 0
        for key,value in cart.items():
            single_product = Product.objects.get(id=key)
            total_price += single_product.price * value

        print(total_price)
        # Save order
        Order.objects.create(
            full_name =full_name,
            contact_number=contact_number,
            location=location,
            cart=cart,  # ✅ Save dict directly
            address=address,
            total_price= total_price
        )

        # Clear cart after successful order
        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")

        return redirect('home')

    product_list = {}
    total_price = 0
    for key, value in cart.items():
        single_product = Product.objects.get(id=key)
        product_list[key] = {'name': single_product.name, 'price': single_product.price, 'quantity': value}
        total_price += single_product.price * value

    return render(request, 'store/confirm_order.html', {
        'product_list': product_list,
        'total_price': total_price,
    })


def create_single_order(request, pk):

    product_list = {}


    single_product = Product.objects.get(id=pk)

    total_price = single_product.price

    product_list[1] = {'name': single_product.name, 'price': single_product.price, 'quantity': 1}

    return render(request,'store/confirm_order.html',{
        'product_list': product_list,
        'total_price': total_price,
    })






from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order

# Show all orders for the employee/admin panel
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')  # Most recent first
    return render(request, 'orders/order_list.html', {'orders': orders})

# Confirm an order
def confirm_order(request, order_id):
    single_order = Order.objects.get(id = order_id)
    single_order.is_confirmed = True
    single_order.save()

    return redirect('order_list')

# Cancel an order
def cancel_order(request, order_id):
    single_order = Order.objects.get(id = order_id)
    single_order.is_cancelled = True
    single_order.save()

    return redirect('order_list')

