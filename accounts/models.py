from django.db import models

class Accounts(models.Model):
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    remarks = models.TextField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)