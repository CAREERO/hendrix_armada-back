from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartItemSerializer
from product.models import Product
from django.contrib.auth.models import AnonymousUser

class AddToCartAPIView(APIView):
    def post(self, request, product_id):
        user = request.user
        if isinstance(user, AnonymousUser):
            # For anonymous users, create a cart without associating it with a specific user
            cart, created = Cart.objects.get_or_create(user=None)
        else:
            cart, created = Cart.objects.get_or_create(user=user)

        # Retrieve the product from the database
        product = get_object_or_404(Product, pk=product_id)

        # Create or get the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CartItemsAPIView(APIView):
    def get(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            # For anonymous users, retrieve the cart associated with None user
            cart = Cart.objects.filter(user=None).first()
        else:
            cart = Cart.objects.filter(user=user).first()

        if cart:
            cart_items = cart.cartitem_set.all()
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_200_OK)


class UpdateCartItemQuantityAPIView(APIView):
    def put(self, request, cart_item_id):
        data = request.data
        new_quantity = data.get('quantity')
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)
        cart_item.quantity = new_quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RemoveCartItemAPIView(APIView):
    def delete(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)