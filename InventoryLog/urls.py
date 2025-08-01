from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_home, name='inventory_home'),
    path('update_inventory/<int:id>', views.update_inventory, name='update_inventory'),
]