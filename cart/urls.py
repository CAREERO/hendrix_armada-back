from django.urls import path
from .views import (
    AddToCartAPIView,
    CartItemsAPIView,
    UpdateCartItemQuantityAPIView,
    RemoveCartItemAPIView,
    CartItemAPIView
)

app_name = 'hendrix_armada' 
urlpatterns = [
    path('add/', AddToCartAPIView.as_view(), name='add_to_cart'),  # Renamed URL name
    path('items/', CartItemsAPIView.as_view(), name='cart_items'),
    path('add/<int:product_id>/', AddToCartAPIView.as_view(), name='add_to_cart'),
    path('items/<int:cart_item_id>/', CartItemAPIView.as_view(), name='cart_item_detail'),
    path('items/update/<int:cart_item_id>/', UpdateCartItemQuantityAPIView.as_view(), name='update_cart_item'),
    path('item/remove/<int:cart_item_id>/', RemoveCartItemAPIView.as_view(), name='remove_cart_item'), 
]
