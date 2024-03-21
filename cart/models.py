from django.db import models
from product.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    accepted = models.BooleanField(default=False)  # Indicates if the item is accepted
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of item creation

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) - {'Accepted' if self.accepted else 'Not Accepted'}"

    @property
    def total_price(self):
        """Calculate total price for the cart item."""
        return self.product.price * self.quantity
