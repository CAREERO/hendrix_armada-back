from django.contrib import admin
from .models import CartItem, Cart

# Register your models here.

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'accepted', 'created_at']  # Customize the fields displayed in the admin list view
    list_filter = ['quantity', 'accepted', 'created_at']  # Add filters for the admin list view
    list_editable = ['quantity', 'accepted']  # Make the quantity and accepted fields editable directly in the list view
    search_fields = ['product__name']  # Add search functionality based on the product name

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']  # Customize the fields displayed in the admin list view

    def cart_items(self, obj):
        return obj.items.all()  # Access CartItem instances related to this Cart
    cart_items.short_description = 'Cart Items'

    readonly_fields = ['cart_items']  # Make cart_items field read-only in the admin interface

