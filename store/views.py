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

    return redirect('home')

# def cart_view(request):
#     cart = request.session.get('cart',{})
#     print("I am form cart view")
#     print(cart)
#
#     cart_items = []
#     total_amount = 0
#
#     for item, value in cart.items():
#         print(item)
#         print(value)
#         product = Product.objects.get(id=item)
#
#         item_total = product.price * value
#         cart_items.append({
#             'product': product,
#             'quantity': value,
#             'item_total': item_total,
#         })
#         total_amount += item_total
#
#     context = {
#         'cart_items': cart_items,
#         'total_amount': total_amount,
#     }
#
#     return render(request, 'store/cart_view.html', context)


