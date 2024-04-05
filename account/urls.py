from django.urls import path
from account import views
from rest_framework_simplejwt.views import TokenObtainPairView
from account.serializers import UserSerializer


urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name="register-page"),
    path('login/', views.MyTokenObtainPairView.as_view(), name="login-page"),
    path('user/<int:pk>/', views.UserAccountDetailsView.as_view(), name="user-details"),
    
 # Address URLs
    path('addresses/', views.UserAddressesListView.as_view(), name="user-addresses-list"),
    path('addresses/<int:pk>/', views.UserAddressesListView.as_view(), name="user-address-details"),
    path('addresses/create/', views.CreateUserAddressView.as_view(), name="create-user-address"),
    path('addresses/update/<int:pk>/', views.UpdateUserAddressView.as_view(), name="update-user-address"),
    path('addresses/delete/<int:pk>/', views.DeleteUserAddressView.as_view(), name="delete-user-address"),
    
    # Order URLs
    path('orders/', views.OrdersListView.as_view(), name="orders-list"),
    path('orders/change-status/<int:pk>/', views.ChangeOrderStatus.as_view(), name="change-order-status"),
    
    # Stripe URL
    path('stripe/cards/', views.CardsListView.as_view(), name="stripe-cards-list"),
]
