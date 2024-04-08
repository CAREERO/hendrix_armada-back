import stripe
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from account.models import StripeModel, OrderModel
from datetime import datetime
from django.shortcuts import redirect
from django.views.generic import TemplateView
import math

# Set the Stripe secret test key directly
stripe.api_key = "sk_test_51P1kKeEg0n8FwKM8Ov6SPMRS10qELSGgbkCKkwTIizWCfJyfBJt1sryK3OckKPFGCCubZ1aAyfvU2p2ZIdoiJiKY00R4P0xcsK"

# Function to save card details in the database
def save_card_in_db(card_data, email, card_id, customer_id, user):
    StripeModel.objects.create(
        email=email,
        customer_id=customer_id,
        card_number=card_data["last4"],
        exp_month=card_data["exp_month"],
        exp_year=card_data["exp_year"],
        card_id=card_id,
        user=user,
    )

# API view to create a card token for card validation and save the card details
class CreateCardTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        email = data.get("email")
        card_status = data.get("saveCard", False)

        # Check if the required fields are present in the request data
        if 'card_token' not in data:
            return Response({"detail": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer_data = stripe.Customer.list(email=email).data

            if not customer_data:
                # Create customer in Stripe
                customer = stripe.Customer.create(
                    email=email,
                    description="New customer"
                )
            else:
                customer = customer_data[0]

            create_user_card = stripe.Customer.create_source(
                customer["id"],
                source=data["card_token"],
            )

            # If saveCard flag is True, save the card details in the database
            if card_status:
                try:
                    save_card_in_db(create_user_card, email, create_user_card.id, customer["id"], request.user)
                except Exception as e:
                    return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            message = {"customer_id": customer["id"], "email": email, "card_data": create_user_card}
            return Response(message, status=status.HTTP_200_OK)

        except stripe.error.APIConnectionError:
            return Response({"detail": "Network error, Failed to establish a new connection."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# Charge the customer's card
class ChargeCustomerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            email = data.get("email")
            customer_data = stripe.Customer.list(email=email).data
            customer = customer_data[0]

            stripe.Charge.create(
                customer=customer.id,
                amount=int(float(data["amount"]) * 100),
                currency="inr",
                description='Software development services',
            )

            new_order = OrderModel.objects.create(
                name=data["name"],
                card_number=data["card_number"],
                address=data["address"],
                ordered_item=data["ordered_item"],
                paid_status=data["paid_status"],
                paid_at=datetime.now(),
                total_price=data["total_price"],
                is_delivered=data["is_delivered"],
                delivered_at=data["delivered_at"],
                user=request.user
            )

            return Response(
                data={
                    "data": {
                        "customer_id": customer.id,
                        "message": "Payment Successful",
                    }
                }, status=status.HTTP_200_OK)

        except stripe.error.APIConnectionError:
            return Response({"detail": "Network error, Failed to establish a new connection."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Retrieve card details
class RetrieveCardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            customer_id = request.headers.get("Customer-Id")
            card_id = request.headers.get("Card-Id")
            card_details = stripe.Customer.retrieve_source(customer_id, card_id)
            return Response(card_details, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Update a card
class CardUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            customer_id = data.get("customer_id")
            card_id = data.get("card_id")
            update_card = stripe.Customer.modify_source(
                customer_id,
                card_id,
                exp_month=data.get("exp_month"),
                exp_year=data.get("exp_year"),
                name=data.get("name_on_card"),
                address_city=data.get("address_city"),
                address_country=data.get("address_country"),
                address_state=data.get("address_state"),
                address_zip=data.get("address_zip"),
            )

            obj = StripeModel.objects.get(card_number=data["card_number"])

            if obj:
                obj.name_on_card = data.get("name_on_card", obj.name_on_card)
                obj.exp_month = data.get("exp_month", obj.exp_month)
                obj.exp_year = data.get("exp_year", obj.exp_year)
                obj.address_city = data.get("address_city", obj.address_city)
                obj.address_country = data.get("address_country", obj.address_country)
                obj.address_state = data.get("address_state", obj.address_state)
                obj.address_zip = data.get("address_zip", obj.address_zip)
                obj.save()

            return Response(
                {
                    "detail": "Card updated successfully",
                    "data": {"Updated Card": update_card},
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Delete a card
class DeleteCardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            card_number = data.get("card_number")
            obj_card = StripeModel.objects.get(card_number=card_number)
            customer_id = obj_card.customer_id
            card_id = obj_card.card_id
            stripe.Customer.delete_source(customer_id, card_id)
            obj_card.delete()
            stripe.Customer.delete(customer_id)
            return Response("Card deleted successfully.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateCheckoutSession(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_name = request.data.get('product_name')
        price = float(request.data.get('price'))
        quantity = int(request.data.get('quantity'))
        subtotal = float(request.data.get('subtotal'))
        shipping_price = float(request.data.get('shippingPrice'))
        total_price = float(request.data.get('total'))
        user_id = 1  # Assuming default user ID

        # Convert price and shipping price to cents
        price = math.ceil(price * 100)
        shipping_price = math.ceil(shipping_price * 100)

        try:
            YOUR_DOMAIN = 'https://localhost:8000/'
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': price,
                            'product_data': {
                                'name': product_name,
                            },
                        },
                        'quantity': quantity,
                    },
                    # Adding shipping line item
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': shipping_price,
                            'product_data': {
                                'name': 'Shipping',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "user_id": user_id,
                    "subtotal": subtotal,
                    "shipping_price": shipping_price,
                },
                mode='payment',
                success_url=YOUR_DOMAIN + f'payments/success/{user_id}',
                cancel_url=YOUR_DOMAIN + f'payments/cancel/{user_id}',
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        main_url = checkout_session.url
        data = {
            'message': "success",
            "url": main_url
        }

        return JsonResponse(main_url)

class CancelPage(TemplateView):
    def get(self, request, *args, **kwargs):
        user_id = int(self.kwargs['pk'])
        print("user_id:", user_id)
        print('cancel_page')
        YOUR_DOMAIN1 = 'https://www.hendrix.world/cancel'
        return JsonResponse(YOUR_DOMAIN1)


class SuccessPage(TemplateView):
    def get(self, request):
        session_id = request.GET.get('session_id')
        stripe.api_key = 'sk_test_51P1kKeEg0n8FwKM8Ov6SPMRS10qELSGgbkCKkwTIizWCfJyfBJt1sryK3OckKPFGCCubZ1aAyfvU2p2ZIdoiJiKY00R4P0xcsK'
        
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            status = session['status']
            customer_email = session['customer_details']['email']
            
            return JsonResponse({'status': status, 'customer_email': customer_email})
        except stripe.error.InvalidRequestError as e:
            return JsonResponse({'error': str(e)}, status=400)