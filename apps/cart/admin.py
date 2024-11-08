from django.contrib import admin
from .models import Cart, Product, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'qr_code', 'is_synced', 'checked_out', 'total_price', 'created_at', 'updated_at')
    list_filter = ('is_synced', 'checked_out')
    search_fields = ('qr_code', 'user__email', 'user__username')
    date_hierarchy = 'created_at'
    

# Register your models here.
admin.site.register(Cart, CartAdmin)
admin.site.register(Product)
admin.site.register(CartItem)