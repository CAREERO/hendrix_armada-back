from rest_framework import serializers
from .models import CartItem, Product, Cart

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    product_description = serializers.ReadOnlyField(source='product.description')
    product_stock = serializers.ReadOnlyField(source='product.stock')
    product_image = serializers.ReadOnlyField(source='product.image')
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['id', 'product_name', 'product_price', 'product_description', 'product_stock', 'product_image', 'quantity', 'product']

    def create(self, validated_data):
        product = validated_data.pop('product', None)
        if product is None:
            raise serializers.ValidationError('Product is required.')

        cart_item = CartItem.objects.create(product=product, **validated_data)
        return cart_item

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField(source='cart.total_price')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']