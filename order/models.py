from django.db import models

from django.db import models

class Order(models.Model):
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    address = models.TextField()
    cart = models.JSONField(default=dict)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
