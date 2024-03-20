from django.urls import path
from account import views
from rest_framework_simplejwt.views import TokenObtainPairView
from account.serializers import UserSerializer


urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name="register-page"),
    path('login/', views.MyTokenObtainPairView.as_view(), name="login-page"),
    path('user/<int:pk>/', views.UserAccountDetailsView.as_view(), name="user-details"),
  
]
