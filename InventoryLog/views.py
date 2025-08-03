
from django.shortcuts import render, redirect
from InventoryLog.models import InventoryLog

def inventory_home (request):
    all_inventory = InventoryLog.objects.all()
    context = {'inventoryLogs': all_inventory}
    return render(request,'inventory/inventory_home.html',context)

def update_inventory (request,id):
    single_inventory = InventoryLog.objects.get(id=id)

    if request.method == 'POST':
        quantity = int(request.POST["quantity"])
        print(quantity)
        single_inventory.quantity += quantity
        single_inventory.save()

        return redirect('inventory_home')
    else:
        return redirect('inventory_home')

