from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('single_product/<int:pk>',views.single_product,name='single_product'),
    # path('cart_view/',views.cart_view,name='cart_view'),
    path('add_to_cart/<int:pk>',views.add_to_cart,name='add_to_cart'),

]




from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
