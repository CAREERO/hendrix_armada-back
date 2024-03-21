from rest_framework import generics, status
from rest_framework.response import Response
from .models import CartItem, Cart, Product
from .serializers import CartItemSerializer

class AddToCartAPIView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        try:
            product_data = request.data.get('product')
            if not product_data or 'id' not in product_data:
                return Response({"error": "Product data is invalid"}, status=status.HTTP_400_BAD_REQUEST)

            product_id = product_data['id']
            quantity = request.data.get('quantity', 1)

            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_authenticated:
            # If user is authenticated, associate the cart item with the user's cart
            user_cart, _ = Cart.objects.get_or_create(user=request.user)
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
        else:
            # If user is not authenticated, handle adding to session/cart accordingly
            cart_data = request.session.get('cart', {})
            cart_data[product_id] = cart_data.get(product_id, 0) + quantity
            request.session['cart'] = cart_data
            return Response({"message": "Item added to cart"}, status=status.HTTP_201_CREATED)


class CartItemsAPIView(generics.ListAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        user_cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=user_cart)
