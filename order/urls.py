from django.urls import path
from . import views
urlpatterns = [
    path('create_confirm_order/', views.create_confirm_order, name='create_confirm_order'),
    path('create_single_order/<int:pk>', views.create_single_order, name='create_single_order'),
    path('order_list/',views.order_list, name="order_list"),
    path('confirm_order/<int:order_id>',views.confirm_order, name="confirm_order"),
    path('cancel_order/<int:order_id>',views.cancel_order, name="cancel_order"),
]