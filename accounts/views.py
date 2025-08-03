from django.shortcuts import render
from order.models import Order
# Create your views here.

def home(request):

    all_order = Order.objects.values('total_price')
    print(all_order)

    total_price = 0
    count = 0
    for i in all_order:
        count += 1
        total_price += i['total_price']

    return render(request, 'accounts/accounts_home.html',{'total_price': total_price,'count':count})