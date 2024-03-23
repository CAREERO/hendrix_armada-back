from django.contrib import admin
from .models import CartItem  # Updated import statement
from product.models import Product  # Imported Product model from product app

admin.site.register(CartItem)