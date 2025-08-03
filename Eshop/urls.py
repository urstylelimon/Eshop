from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('store.urls')),
    path('order/',include('order.urls')),
    path('inventory/',include('InventoryLog.urls')),
    path('accounts/',include('accounts.urls'))
]