from django.contrib import admin
from orders.models import OrderTable
# Register your models here.


@admin.register(OrderTable)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "query", "created_date", "modified_date")
    search_fields = ("user__id", "query__id", "id")
