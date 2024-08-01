from django.urls import path
from .views import (
    SignupView, LoginView,
    # PasswordResetView,
    # CreateUserProfileView,
    # UpdateUserProfileView, 
    LogoutView, RefreshAccessTokenAPIView, UserDetailsView,
    PasswordResetRequestView, PasswordResetConfirmView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('refresh-token/', RefreshAccessTokenAPIView.as_view(), name='refresh-token'),
    # path('create-profile/', CreateUserProfileView.as_view(), name='create-profile'),
    # path('update-profile/', UpdateUserProfileView.as_view(), name='update-profile'),
    path('user/', UserDetailsView.as_view(), name='user-details'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<int:user_id>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]


