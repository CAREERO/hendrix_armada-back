from django.views import View
from django.http import HttpResponse, JsonResponse
import json

class GelatoView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello from GelatoView!")

class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("User Profile View")

class UserRegistrationView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("User Registration View")

class ShoppingCartView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Shopping Cart View")

class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Add to Cart View")

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Welcome to the Home View!")
    
def gelato_view(request):
    # Your view logic here
    return HttpResponse("Hello, this is the Gelato view!")

class ShopView(View):
    def get(self, request, *args, **kwargs):
        # Your logic to retrieve shop data
        shop_data = {"title": "Shop Title", "description": "Shop Description", "items": []}
        
        # Convert the Python dictionary to a JSON string
        shop_data_json = json.dumps(shop_data)
        
        # Return the JSON response with the appropriate content type
        return JsonResponse(shop_data, safe=False)
