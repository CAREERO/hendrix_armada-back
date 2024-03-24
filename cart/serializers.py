from rest_framework import serializers
from .models import Cart, CartItem
from product.serializers import ProductSerializer  # Import ProductSerializer from your product app

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print("Serialized CartItem data:", representation)
        return representation
    
    product = ProductSerializer()  # Serialize product using ProductSerializer

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'created_at', 'total_price']  # Include total_price from the property method in the model
