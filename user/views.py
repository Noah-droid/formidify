
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserProfileSerializer, LoginSerializer
from .models import UserProfile
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import logging
from django.http import JsonResponse
from datetime import timedelta, datetime
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
import smtplib
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from django.utils.html import strip_tags
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction
# logger = logging.getLogger(__name__)


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data)

        try:
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            user.set_password(user.password)
            user.save()

            

            # Check if the user has created a profile
            has_profile = UserProfile.objects.filter(user=user).exists()

            if user is not None:
                user_refresh_token = RefreshToken.for_user(user)

            response = Response({
                'message': 'Signup successful. Welcome to Skuwave!',
                'has_profile': has_profile,
                'refresh_token': str(user_refresh_token),
                'access_token': str(user_refresh_token.access_token),
            }, status=status.HTTP_201_CREATED)
            return response

        except ValidationError as e:
            errors = {field: error[0] for field, error in e.detail.items()}
            joined_errors = " ".join(errors.values())
            return Response({'error': joined_errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        errors = {}

        # Validate username
        if not username:
            errors['username'] = 'Username is required.'
        elif not User.objects.filter(username=username).exists():
            errors['username'] = 'User with this username does not exist.'

        # Validate password
        if not password:
            errors['password'] = 'Password is required.'

        # If there are validation errors, return them
        if errors:
            joined_errors = " ".join(errors.values())
            return Response({'error': joined_errors}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            user_refresh_token = RefreshToken.for_user(user)

            # Check if the user has created a profile
            has_profile = UserProfile.objects.filter(user=user).exists()

            response_data = {
                'message': 'Login successful.',
                'has_profile': has_profile,
                'refresh_token': str(user_refresh_token),
                'access_token': str(user_refresh_token.access_token),
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials: Wrong username or password inputted'}, status=status.HTTP_401_UNAUTHORIZED)



class RefreshAccessTokenAPIView(TokenRefreshView):
    """Inheriting class for refreshing access token"""

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            response_data = {
                'refresh_token': data.get('refresh'),
                'access_token': data.get('access'),
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return response



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response({
            'message': 'Logout successful.'
        }, status=status.HTTP_200_OK)






class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if user:
            # Generate a password reset token
            token = default_token_generator.make_token(user)
            # Construct password reset link
            reset_link = f"{settings.FRONTEND_URL}/app/reset-password/{user.pk}/{token}/"
            
            # Prepare email content
            subject = 'Password Reset Request'
            context = {
                'user': user,
                'reset_link': reset_link,
              
            }
            html_message = render_to_string('password_reset_email.html', context)
            plain_message = strip_tags(html_message)

            # Send email
            try:
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    html_message=html_message,
                    fail_silently=False,
                )
                return Response({'detail': 'Password reset email sent'}, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"Email sending error: {e}")
                return Response({'detail': 'Failed to send password reset email. Please try again later.'}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'detail': 'User with this email not found.'}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        token = kwargs.get('token')
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({'detail': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'detail': 'Password has been reset.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid user ID.'}, status=status.HTTP_404_NOT_FOUND)



class UserDetailsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        # Ensure to get the UserProfile instance associated with the authenticated user
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if not user_profile:
            return Response({'detail': 'UserProfile not found.'}, status=404)

        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)