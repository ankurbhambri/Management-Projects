from django.contrib import admin
from product.models import Ingredient, Product, RawMaterial


@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'avaliable_qty')
    search_fields = ('item_name', )


class RecipeAdmin(admin.TabularInline):
    model = Ingredient
    extra = 0
    fk_name = 'product'


@admin.register(Product)
class BusServiceAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'author', 'cost_price', 'marked_price', )
    readonly_fields = ["selling_price"]
    search_fields = ('product_name', 'author', )
    inlines = [RecipeAdmin, ]
