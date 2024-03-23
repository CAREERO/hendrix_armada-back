from django.urls import path
from .views import AddToCartAPIView, CartItemsAPIView

app_name = 'hendrix_armada' 
urlpatterns = [
    path('add/', AddToCartAPIView.as_view(), name='add_to_cart'),  # Renamed URL name
    path('items/', CartItemsAPIView.as_view(), name='cart_items'),
    path('add/<int:product_id>/', AddToCartAPIView.as_view(), name='add_to_cart'),
]
