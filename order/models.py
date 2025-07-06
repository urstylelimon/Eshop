from django.db import models

from django.db import models

class Order(models.Model):
    LOCATION_CHOICES = [
        ('inside_dhaka', 'Inside Dhaka'),
        ('outside_dhaka', 'Outside Dhaka'),
    ]

    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    address = models.TextField()
    cart = models.JSONField(default=dict)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order from {self.full_name} - {self.contact_number}"
