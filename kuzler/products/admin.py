from django.contrib import admin
from products.models import Product, NFCTag


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nfc_id', 'name', 'price', 'created_at')
    search_fields = ('nfc_id', 'name')
    list_filter = ('created_at',)


@admin.register(NFCTag)
class NFCTagAdmin(admin.ModelAdmin):
    list_display = ('uid', 'product_link', 'assigned_at')
    raw_id_fields = ('product',)
    date_hierarchy = 'assigned_at'
    search_fields = ('uid', 'product__name')

    def product_link(self, obj):
        return f'{obj.product.name} (код: {obj.product.nfc_id})' if obj.product else "-"

    product_link.short_description = 'Товар'
    product_link.admin_order_field = 'product__name'
