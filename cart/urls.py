from django.urls import path
from .views import AddToCartAPIView, CartItemsAPIView

urlpatterns = [
    path('add/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart-items/', CartItemsAPIView.as_view(), name='cart_items'),

]
