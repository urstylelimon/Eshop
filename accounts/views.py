from itertools import count

from django.shortcuts import render
from order.models import Order
# Create your views here.

def home(request):

    all_order = Order.objects.filter(is_confirmed=True)

    count = 0
    total_price = 0
    for order in all_order:
        count += 1
        total_price += order.total_price


    #Calculate cost for outside order
    outside_order = all_order.filter(location='outside').count()
    delevery_cost = 60 * outside_order

    print("outside order:",delevery_cost)


    context = {
        'total_price': total_price,
        'count': count,
        'outside_order': outside_order,
        'delevery_cost': delevery_cost,
    }



    return render(request, 'accounts/accounts_home.html', context)