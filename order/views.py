from store.models import Product
from order.models import Order

import time
import json
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

# Configuration
PIXEL_ID = '1141360628152843'
META_CAPI_TOKEN = getattr(settings, 'META_CAPI_TOKEN', None)

def send_meta_purchase_event(request, order_instance, cart_items, total_price):
    """
    Send purchase event to Meta Conversion API using direct HTTP requests
    This bypasses the buggy Facebook SDK and works reliably
    """
    if not PIXEL_ID or not META_CAPI_TOKEN:
        print("META CAPI: Skipping - PIXEL_ID or TOKEN missing")
        return

    try:
        print(f"META CAPI: Sending purchase event for Order {order_instance.pk}")

        # Build the payload for Facebook CAPI
        payload = {
            'data': [
                {
                    'event_name': 'Purchase',
                    'event_time': int(time.time()),
                    'action_source': 'website',
                    'event_id': str(order_instance.pk),
                    'user_data': {
                        'client_ip_address': request.META.get('REMOTE_ADDR', '127.0.0.1'),
                        'client_user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    },
                    'custom_data': {
                        'value': float(total_price),
                        'currency': 'BDT',
                        'content_type': 'product',
                        'contents': [
                            {
                                'id': str(item['product'].id),
                                'quantity': item['quantity']
                            }
                            for item in cart_items
                        ]
                    }
                }
            ],

            'access_token': META_CAPI_TOKEN

        }



        # Send direct HTTP request to Facebook CAPI
        url = f"https://graph.facebook.com/v19.0/{PIXEL_ID}/events"
        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()
            print(f"META CAPI SUCCESS for Order {order_instance.pk}")
            print(f"Events Received: {result.get('events_received', 0)}")
        else:
            print(f"META CAPI FAILED for Order {order_instance.pk}: Status {response.status_code}")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"META CAPI ERROR for Order {order_instance.pk}: {e}")


# ----------------------------------------------------------------------
# VIEW 1: CART CHECKOUT (create_confirm_order)
# ----------------------------------------------------------------------
def create_confirm_order(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    # Prepare product list and totals
    product_list = []
    total_cart_amount = 0
    delivery_charge = 60

    for item_id_str, quantity in cart.items():
        try:
            item_id = int(item_id_str)
            product = Product.objects.get(id=item_id)
            item_total = product.price * quantity
            product_list.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })
            total_cart_amount += item_total
        except (Product.DoesNotExist, ValueError):
            continue

    final_grand_total = total_cart_amount + delivery_charge

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        contact_number = request.POST.get('contact_number')
        location = request.POST.get('location')
        address = request.POST.get('address')

        # Validate required fields
        if not all([full_name, contact_number, location, address]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'store/confirm_order.html', {
                'product_list': product_list,
                'total_price': total_cart_amount,
                'all_price': final_grand_total,
            })

        with transaction.atomic():
            # 1. Save order
            new_order = Order.objects.create(
                full_name=full_name,
                contact_number=contact_number,
                location=location,
                cart=cart,
                address=address,
                total_price=final_grand_total
            )

            # 2. Send Meta CAPI Purchase Event
            send_meta_purchase_event(request, new_order, product_list, final_grand_total)

        # 3. Clear cart and redirect
        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")
        return redirect('home')

    # GET request - show confirmation page
    return render(request, 'store/confirm_order.html', {
        'product_list': product_list,
        'total_price': total_cart_amount,
        'all_price': final_grand_total,
    })


# ----------------------------------------------------------------------
# VIEW 2: SINGLE PRODUCT CHECKOUT (create_single_order)
# ----------------------------------------------------------------------
def create_single_order(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('home')

    quantity = 1
    delivery_charge = 60
    total_amount = product.price * quantity
    final_grand_total = total_amount + delivery_charge

    product_list = [{
        "product": product,
        "quantity": quantity,
        "item_total": total_amount,
    }]
    cart = {str(product.id): quantity}

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        contact_number = request.POST.get('contact_number')
        location = request.POST.get('location')
        address = request.POST.get('address')

        # Validate required fields
        if not all([full_name, contact_number, location, address]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'store/confirm_order.html', {
                'product_list': product_list,
                'total_price': total_amount,
                'all_price': final_grand_total,
            })

        with transaction.atomic():
            # 1. Save order
            new_order = Order.objects.create(
                full_name=full_name,
                contact_number=contact_number,
                location=location,
                cart=cart,
                address=address,
                total_price=final_grand_total
            )

            # 2. Send Meta CAPI Purchase Event
            send_meta_purchase_event(request, new_order, product_list, final_grand_total)

        messages.success(request, "Order placed successfully!")
        return redirect('home')

    return render(request, 'store/confirm_order.html', {
        'product_list': product_list,
        'total_price': total_amount,
        'all_price': final_grand_total,
    })


#For Admin_____________________________________________________

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

