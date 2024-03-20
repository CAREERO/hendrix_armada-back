from django.contrib import admin
from .models import CartItem, Cart

# Register your models here.

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity']  # Customize the fields displayed in the admin list view
    list_filter = ['quantity']  # Add filters for the admin list view
    list_editable = ['quantity']  # Make the quantity field editable directly in the list view

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']  # Customize the fields displayed in the admin list view
    filter_horizontal = ['items']  # Add a horizontal filter for the items in the cart
