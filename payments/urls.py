from django.urls import path
from payments import views

urlpatterns = [
    path('create-card/', views.CreateCardTokenView.as_view()),
    path('update-card/', views.CardUpdateView.as_view()),    
    path('delete-card/', views.DeleteCardView.as_view()),    
    path('card-details/', views.RetrieveCardView.as_view()),
    path('create-checkout-session/', views.CreateCheckoutSession.as_view(), name='create-checkout-session'),
    path('cancel/<int:pk>/', views.CancelPage.as_view(), name='CancelPage'),
    path('success/<int:pk>/', views.SuccessPage.as_view(), name='SuccessPage'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('create-invoice/', views.create_invoice, name='create-invoice'),
    path('retrieve-invoices/', views.retrieve_invoices, name='retrieve-invoices'),
]
