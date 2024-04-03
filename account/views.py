from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password, check_password
from .models import StripeModel, BillingAddress, OrderModel
from .serializers import (
    UserSerializer, 
    UserRegisterTokenSerializer, 
    CardsListSerializer, 
    BillingAddressSerializer,
    AllOrdersListSerializer
)

# Home View
class HomeView(APIView):
    """Home View for your application."""
    def get(self, request, *args, **kwargs):
        return Response({"message": "Welcome to the HomeView!"}, status=status.HTTP_200_OK)

# Register user
class UserRegisterView(APIView):
    """To Register the User"""
    def post(self, request, format=None):
        data = request.data  # holds username, email, password, and termsChecked
        username = data["username"]
        email = data["email"]
        plain_password = data.get("password")  # Change to 'password' instead of 'hashedPassword'
        terms_checked = data.get("termsChecked", False)

        if not all([username, email, plain_password, terms_checked]):
            return Response({"detail": "Incomplete or missing registration information"}, status=status.HTTP_400_BAD_REQUEST)

        check_username = User.objects.filter(username=username).exists()
        check_email = User.objects.filter(email=email).exists()

        if check_username:
            message = "A user with that username already exists!"
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)
        if check_email:
            message = "A user with that email address already exists!"
            return Response({"detail": message}, status=status.HTTP_403_FORBIDDEN)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(plain_password),
            is_active=True,
        )

        # Additional steps for termsChecked field
        if terms_checked:
            # Perform actions based on termsChecked, e.g., store it in the user model
            user.terms_checked = True
            user.save()

        serializer = UserRegisterTokenSerializer(user)
        return Response(serializer.data)

# Login user
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserRegisterTokenSerializer(self.user)
        for k, v in serializer.data.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# List all the cards of currently logged in user only
class CardsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stripeCards = StripeModel.objects.filter(user=request.user)
        serializer = CardsListSerializer(stripeCards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Get user details
class UserAccountDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Update user account
class UserAccountUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        user = get_object_or_404(User, id=pk)
        data = request.data

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            if data.get("password"):
                user.set_password(data["password"])
            user.username = data.get("username", user.username)
            user.email = data.get("email", user.email)
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete user account
class UserAccountDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)
        data = request.data

        if request.user.id == user.id:
            if check_password(data["password"], user.password):
                user.delete()
                return Response({"details": "User successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"details": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"details": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)

# Get billing address details
class UserAddressesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_address = BillingAddress.objects.filter(user=request.user)
            serializer = BillingAddressSerializer(user_address, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create or update billing address
class CreateUserAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data["user"] = request.user.id  # Add user information to the data

        billing_address = BillingAddress.objects.filter(user=request.user).first()

        serializer = BillingAddressSerializer(instance=billing_address, data=data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():  # Use transaction to ensure atomicity
                serializer.save()

                # Update user's first name and last name based on shipping details
                user = request.user
                user.first_name = data.get("firstname", user.first_name)
                user.last_name = data.get("lastname", user.last_name)
                user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update billing address and user details
class UpdateUserAddressView(APIView):
    permission_classes = [IsAuthenticated]

class UpdateUserAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        data = request.data

        try:
            user_address = BillingAddress.objects.get(id=pk)

            if request.user.id == user_address.user.id:
                # Update user details
                user = user_address.user
                user.first_name = data.get("firstname", user.first_name)
                user.last_name = data.get("lastname", user.last_name)
                user.save()

                # Update billing address details
                updated_address_data = {
                    "firstname": data.get("firstname", user_address.firstname),
                    "lastname": data.get("lastname", user_address.lastname),
                    "phone_number": data.get("phone", user_address.phone_number),
                    "zip_code": data.get("zipCode", user_address.zip_code),
                    "house_no": data.get("houseNo", user_address.house_no),
                    "apartment": data.get("apartment", user_address.apartment),
                    "street_address": data.get("streetAddress", user_address.street_address),
                    "landmark": data.get("landmark", user_address.landmark),
                    "city": data.get("city", user_address.city),
                    "state": data.get("state", user_address.state),
                    "country": data.get("country", user_address.country),
                    "company": data.get("company", user_address.company),
                }

                serializer = BillingAddressSerializer(user_address, data=updated_address_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"details": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except BillingAddress.DoesNotExist:
            return Response({"details": "Billing address not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete billing address
class DeleteUserAddressView(APIView):

    def delete(self, request, pk):
        
        try:
            user_address = BillingAddress.objects.get(id=pk)

            if request.user.id == user_address.user.id:
                user_address.delete()
                return Response({"details": "Address successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"details": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"details": "Not found."}, status=status.HTTP_404_NOT_FOUND)

# List all orders
class OrdersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user_staff_status = request.user.is_staff
        
        if user_staff_status:
            all_users_orders = OrderModel.objects.all()
            serializer = AllOrdersListSerializer(all_users_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            all_orders = OrderModel.objects.filter(user=request.user)
            serializer = AllOrdersListSerializer(all_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

# Change order delivered status
class ChangeOrderStatus(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        data = request.data       
        order = get_object_or_404(OrderModel, id=pk)

        order.is_delivered = data.get("is_delivered")
        order.delivered_at = data.get("delivered_at")
        order.save()
        
        serializer = AllOrdersListSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
