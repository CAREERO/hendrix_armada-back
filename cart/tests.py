from django.test import TestCase
from django.contrib.auth.models import User
from .models import CartItem, Product

class CartItemTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create a test product
        self.product = Product.objects.create(name='Test Product', price=10.0)

    def test_create_cart_item(self):
        # Create a test cart item
        cart_item = CartItem.objects.create(product=self.product, quantity=2)

        # Assert that the cart item was created successfully
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_add_to_cart(self):
        # Add a cart item to the user's cart
        self.client.login(username='testuser', password='password')  # Log in the test user
        response = self.client.post('/add-to-cart/', {'product_id': self.product.id, 'quantity': 2})

        # Assert that the cart item was added successfully
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 1)
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
