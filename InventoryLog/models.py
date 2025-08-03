from django.db import models
from store.models import Product


class InventoryLog(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null = False)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_at']