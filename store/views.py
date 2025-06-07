from django.shortcuts import render
from .models import Product
# Create your views here.


def products_list(request):
    products = Product.objects.all()
    return render(request,'store/product_list.html',{'products':products})

def product_detail(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/product_detail.html', {'product': product})