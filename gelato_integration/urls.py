# gelato_integration/urls.py
from django.urls import path
from .views import GelatoView, UserProfileView, UserRegistrationView, ShoppingCartView, AddToCartView, ShopView

urlpatterns = [
    path('gelato/', GelatoView.as_view(), name='gelato-view'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('shopping-cart/', ShoppingCartView.as_view(), name='shopping-cart'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    # Add more URL patterns as needed
]
