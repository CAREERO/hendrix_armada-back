from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny, IsAuthenticated
from account.serializers import UserSerializer
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class CustomUserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user registration using DRF.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(CreateView):
    template_name = 'registration/user_registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        """
        Add user profile data to the context.
        """
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.userprofile
        return context

# @login_required
# def csrf_token_view(request):
#     # Get and return the CSRF token
#     csrf_token = get_token(request)
#     print('CSRF Token on the backend:', csrf_token)
#     return JsonResponse({'csrfToken': csrf_token})

class HomeView(View):
    def get(self, request, *args, **kwargs):
        data = {
            'message': 'Welcome to the Home Page!',
            'content': 'Add any additional content you\'d like for your home page.',
        }
        return JsonResponse(data)
# class CSRFTokenView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         # Get and return the CSRF token
#         csrf_token = get_token(request)
#         print('CSRF Token on the backend:', csrf_token)
#         return Response({'csrfToken': csrf_token})