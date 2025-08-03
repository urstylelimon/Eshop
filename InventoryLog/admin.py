from django.contrib import admin
from .models import InventoryLog

@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ('Product', 'quantity', 'remarks', 'created_at')