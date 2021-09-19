from django.contrib import admin
from accounts.models import OrderHistory


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'created_at', 'modified_at')