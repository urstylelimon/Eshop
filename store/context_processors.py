# your_app/context_processors.py
from store.models import Product


def cart_data(request):
    cart = request.session.get('cart', {})
    cart_item_count = 0
    cart_items = []
    total_amount = 0

    for item, value in cart.items():
        cart_item_count += value
        product = Product.objects.get(id=item)

        item_total = product.price * value
        cart_items.append({
            'product': product,
            'quantity': value,
            'item_total': item_total,
        })
        total_amount += item_total

    return {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'cart_item_count': cart_item_count,
    }