from rest_framework import generics, status
from rest_framework.response import Response
from .models import CartItem, Cart, Product
from .serializers import CartItemSerializer
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class AddToCartAPIView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        # Add debug print statements
        print("AddToCartAPIView create method called")
        
        # Log information using Django's logger
        logger.info("AddToCartAPIView create method called")

        # Extract product_id and quantity from the request data
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        # Validate that product_id is provided
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the product using the provided product_id
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # If user is authenticated, add to the cart in the database
        if self.request.user.is_authenticated:
            user_cart, _ = Cart.objects.get_or_create(user=self.request.user)
            cart_item, created = CartItem.objects.get_or_create(
                product=product,
                cart=user_cart,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If user is not authenticated, store the cart item in session
        cart_data = request.session.get('cart', {})
        cart_data[product_id] = cart_data.get(product_id, 0) + quantity
        request.session['cart'] = cart_data
        return Response({"message": "Item added to cart"}, status=status.HTTP_201_CREATED)
