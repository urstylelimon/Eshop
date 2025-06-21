# your_app/context_processors.py

def cart_data(request):
    cart = request.session.get('cart', {})
    cart_item_count = 0
    for item, value in cart.items():
        cart_item_count += value

    return {
        'cart_item_count': cart_item_count
    }
