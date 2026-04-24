from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum

from order.models import Order
from .models import Accounts


DELIVERY_CHARGE = Decimal("60.00")


def home(request):
    confirmed_orders = Order.objects.filter(is_confirmed=True)

    total_order = confirmed_orders.count()

    total_amount = confirmed_orders.aggregate(
        total=Sum('total_price')
    )['total'] or Decimal("0.00")

    # Count outside orders
    outside_order = confirmed_orders.filter(location='outside').count()

    delivery_cost = DELIVERY_CHARGE * outside_order

    if request.method == 'POST':
        amount = request.POST.get('amount')
        remarks = request.POST.get('remarks')

        if not amount or not remarks:
            messages.error(request, "Please fill in amount and remarks.")
            return redirect('accounts_home')

        Accounts.objects.create(
            amount=amount,
            remarks=remarks
        )

        messages.success(request, "Extra cost added successfully.")
        return redirect('accounts_home')

    accounts_list = Accounts.objects.all().order_by('-created_at')

    miscellaneous_cost = accounts_list.aggregate(
        total=Sum('amount')
    )['total'] or Decimal("0.00")

    net_amount = total_amount - (miscellaneous_cost + delivery_cost)

    context = {
        'total_amount': total_amount,
        'total_order': total_order,
        'outside_order': outside_order,
        'delevery_cost': delivery_cost,  # keeping your template spelling
        'delivery_cost': delivery_cost,  # better spelling also included
        'miscellaneous_cost': miscellaneous_cost,
        'net_amount': net_amount,
        'accounts_list': accounts_list,
    }

    return render(request, 'accounts/accounts_home.html', context)