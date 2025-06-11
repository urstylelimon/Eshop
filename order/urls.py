from django.urls import path
from . import views
urlpatterns = [
    path('confirm-order/', views.confirm_order, name='confirm_order'),
]