from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from store.models import Product
from order.models import Order
from InventoryLog.models import InventoryLog


DELIVERY_CHARGE = 60


def build_product_list_from_cart(cart):
    product_list = []
    subtotal = 0

    for product_id_str, quantity in cart.items():
        try:
            product_id = int(product_id_str)
            quantity = int(quantity)

            if quantity < 1:
                continue

            product = Product.objects.get(id=product_id)
            item_total = product.price * quantity

            product_list.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })

            subtotal += item_total

        except (Product.DoesNotExist, ValueError, TypeError):
            continue

    return product_list, subtotal


def create_confirm_order(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    product_list, total_cart_amount = build_product_list_from_cart(cart)

    if not product_list:
        request.session['cart'] = {}
        request.session.modified = True
        messages.warning(request, "Your cart products are not available.")
        return redirect('cart')

    final_grand_total = total_cart_amount + DELIVERY_CHARGE

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        location = request.POST.get('location', '').strip()
        address = request.POST.get('address', '').strip()

        if not all([full_name, contact_number, location, address]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'store/confirm_order.html', {
                'product_list': product_list,
                'total_price': total_cart_amount,
                'all_price': final_grand_total,
            })

        with transaction.atomic():
            Order.objects.create(
                full_name=full_name,
                contact_number=contact_number,
                location=location,
                cart=cart,
                address=address,
                total_price=final_grand_total,
            )

        request.session['cart'] = {}
        request.session.modified = True

        messages.success(request, "Order placed successfully!")
        return redirect('home')

    return render(request, 'store/confirm_order.html', {
        'product_list': product_list,
        'total_price': total_cart_amount,
        'all_price': final_grand_total,
    })


def create_single_order(request, pk):
    product = get_object_or_404(Product, id=pk)

    try:
        if request.method == 'POST':
            quantity = int(request.POST.get('quantity', 1))
        else:
            quantity = int(request.GET.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    total_amount = product.price * quantity
    final_grand_total = total_amount + DELIVERY_CHARGE

    product_list = [{
        'product': product,
        'quantity': quantity,
        'item_total': total_amount,
    }]

    cart = {
        str(product.id): quantity
    }

    context = {
        'product_list': product_list,
        'total_price': total_amount,
        'all_price': final_grand_total,
        'quantity': quantity,
    }

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        location = request.POST.get('location', '').strip()
        address = request.POST.get('address', '').strip()

        if not all([full_name, contact_number, location, address]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'store/confirm_order.html', context)

        with transaction.atomic():
            Order.objects.create(
                full_name=full_name,
                contact_number=contact_number,
                location=location,
                cart=cart,
                address=address,
                total_price=final_grand_total,
            )

        messages.success(request, "Order placed successfully!")
        return redirect('home')

    return render(request, 'store/confirm_order.html', context)



def order_home(request):
    return render(request, 'orders/order_home.html')


def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    details = []

    for order in orders:
        products = []

        for product_id_str, quantity in order.cart.items():
            try:
                product_id = int(product_id_str)
                quantity = int(quantity)

                product = Product.objects.get(id=product_id)

                products.append({
                    'name': product.name,
                    'price': product.price,
                    'quantity': quantity,
                    'total': product.price * quantity,
                })

            except (Product.DoesNotExist, ValueError, TypeError):
                products.append({
                    'name': 'Product not found',
                    'price': 0,
                    'quantity': quantity,
                    'total': 0,
                })

        details.append({
            'id': order.id,
            'full_name': order.full_name,
            'contact_number': order.contact_number,
            'location': order.location,
            'address': order.address,
            'total_price': order.total_price,
            'is_cancelled': order.is_cancelled,
            'is_confirmed': order.is_confirmed,
            'created_at': order.created_at,
            'products': products,
        })

    return render(request, 'orders/order_list.html', {
        'orders': details,
    })


def confirm_order(request, order_id):
    single_order = get_object_or_404(Order, id=order_id)

    if single_order.is_cancelled:
        messages.error(request, "Cancelled order cannot be confirmed.")
        return redirect('order_list')

    if single_order.is_confirmed:
        messages.warning(request, "This order is already confirmed.")
        return redirect('order_list')

    with transaction.atomic():
        single_order.is_confirmed = True
        single_order.save(update_fields=['is_confirmed'])

        for product_id_str, quantity in single_order.cart.items():
            try:
                product_id = int(product_id_str)
                quantity = int(quantity)

                product = Product.objects.get(id=product_id)

                inventory = InventoryLog.objects.filter(
                    Product_id=product_id
                ).order_by('-id').first()

                if inventory:
                    inventory.quantity -= quantity

                    if inventory.quantity < 0:
                        inventory.quantity = 0

                    inventory.save(update_fields=['quantity'])
                else:
                    messages.warning(
                        request,
                        f"Order confirmed, but inventory not found for {product.name}."
                    )

            except Product.DoesNotExist:
                messages.warning(
                    request,
                    f"Order confirmed, but product id {product_id_str} was not found."
                )

            except (ValueError, TypeError):
                messages.warning(
                    request,
                    "Order confirmed, but some cart data was invalid."
                )

    messages.success(request, f"Order #{single_order.id} confirmed successfully.")
    return redirect('order_list')


def cancel_order(request, order_id):
    single_order = get_object_or_404(Order, id=order_id)

    if single_order.is_confirmed:
        messages.error(request, "Confirmed order cannot be cancelled.")
        return redirect('order_list')

    if single_order.is_cancelled:
        messages.warning(request, "This order is already cancelled.")
        return redirect('order_list')

    single_order.is_cancelled = True
    single_order.save(update_fields=['is_cancelled'])

    messages.success(request, f"Order #{single_order.id} cancelled successfully.")
    return redirect('order_list')