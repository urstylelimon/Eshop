from django.urls import path
from . import views

urlpatterns = [
    path('',views.products_list,name='products_list'),
    path('product/<int:pk>',views.product_detail,name='product_detail'),
    path('addtocart/<int:pk>',views.add_to_cart,name='addtocart'),
]





from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
