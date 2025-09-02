from store.models import Product
from order.models import Order


from django.shortcuts import render, redirect
from django.contrib import messages

from store.views import single_product


# For User
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

        total_price = 60
        for key,value in cart.items():
            single_product = Product.objects.get(id=key)
            total_price += single_product.price * value

        # Save order
        Order.objects.create(
            full_name =full_name,
            contact_number=contact_number,
            location=location,
            cart=cart,
            address=address,
            total_price= total_price
        )

        # Clear cart after successful order
        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")

        return redirect('home')

    product_list = {}
    delevery = 60
    total_price = 0
    for key, value in cart.items():
        s_product = Product.objects.get(id=key)
        product_list[key] = {'name': s_product.name, 'price': s_product.price, 'quantity': value}
        total_price += s_product.price * value
    all_price = total_price + delevery

    return render(request, 'store/confirm_order.html', {
        'product_list': product_list,
        'total_price': total_price,
        'all_price': all_price,

    })


def create_single_order(request, pk):

    product_list = {}


    one_product = Product.objects.get(id=pk)

    total_price = one_product.price
    quantity = 1

    product_list[1] = {'name': one_product.name, 'price': one_product.price, 'quantity': 1}

    total_price += 60

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        contact_number = request.POST.get('contact_number')
        location = request.POST.get('location')
        address = request.POST.get('address')
        cart = {one_product.id: quantity}

        # Save order
        Order.objects.create(
            full_name =full_name,
            contact_number=contact_number,
            location=location,
            cart=cart,
            address=address,
            total_price= total_price
        )

        messages.success(request, "Order placed successfully!")

        return redirect('home')




    return render(request,'store/confirm_order.html',{
        'product_list': product_list,
        'total_price': total_price,
    })



#For Admin

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order

# Show all orders for the employee/admin panel


def order_home(request):
    return render(request,'orders/order_home.html')

def order_list(request):
    orders = Order.objects.all().order_by('-created_at')  # Most recent first
    details = []
    for order in orders:
        products = []
        for key,value in order.cart.items():

            product = Product.objects.get(id = key)

            products.append({'name': product.name, 'price': product.price, 'quantity': value})
        details.append({
            'full_name': order.full_name,
            'contact_number': order.contact_number,
            'location': order.location,
            'address': order.address,
            'total_price': order.total_price,
            'is_cancelled': order.is_cancelled,
            'is_confirmed': order.is_confirmed,
            'created_at': order.created_at,
            'id': order.id,
            'products': products

        })



    return render(request, 'orders/order_list.html', {'orders': details})

# Confirm an order

from  InventoryLog.models import InventoryLog
def confirm_order(request, order_id):
    single_order = Order.objects.get(id = order_id)
    single_order.is_confirmed = True
    single_order.save()

    # Automatic Update Inventory by Confirm Order
    for pk,value in single_order.cart.items():
        single_inventory = InventoryLog.objects.get(id=pk)
        single_inventory.quantity -= value
        single_inventory.save()


    return redirect('order_list')

# Cancel an order
def cancel_order(request, order_id):
    single_order = Order.objects.get(id = order_id)
    single_order.is_cancelled = True
    single_order.save()

    return redirect('order_list')

