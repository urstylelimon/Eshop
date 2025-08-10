from django.shortcuts import render, redirect
from order.models import Order
from . models import Accounts
# Create your views here.

def home(request):

    all_order = Order.objects.filter(is_confirmed=True)

    total_order = 0
    total_amount = 0
    for order in all_order:
        total_order += 1
        total_amount += order.total_price


    #Calculate cost for outside order
    outside_order = all_order.filter(location='outside').count()
    delevery_cost = 60 * outside_order

    print("outside order:",delevery_cost)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        remarks = request.POST.get('remarks')

        Accounts.objects.create(
            amount = amount,
            remarks = remarks
        )
        return redirect('accounts_home')

    all_amount = Accounts.objects.values('amount')
    all_accounts = Accounts.objects.all().order_by('-created_at')

    print(all_accounts.values('created_at'))

    miscellaneous_cost  = 0

    for amount in all_amount:
        miscellaneous_cost += amount['amount']

    # Net profit
    net_amount = total_amount - (miscellaneous_cost+delevery_cost)

    context = {
        'total_amount': total_amount,
        'total_order': total_order,

        'outside_order': outside_order,
        'delevery_cost': delevery_cost,
        'net_amount' : net_amount,
        'accounts_list': all_accounts,
    }



    return render(request, 'accounts/accounts_home.html', context)