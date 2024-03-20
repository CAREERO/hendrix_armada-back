from django.urls import path
from .views import AddToCartAPIView

urlpatterns = [
    path('add/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart/add/', AddToCartAPIView.as_view(), name='add-to-cart'),

]
