from django.urls import path, include
from .views import (
    RegisterAPIView,
    ActivationAPIView,
    ResetPasswordAPIView,
    ResetPasswordCompleteAPIView,
    PasswordTokenVerifyAPIView,
    ChangePasswordAPIView
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView
)


urlpatterns = [
    # register
    path('auth/register/', RegisterAPIView.as_view(), name='register-api'),

    # jwt staff
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # reset user's password
    path('auth/reset-password-complete/', ResetPasswordCompleteAPIView.as_view(), name='reset-password-complete'),
    path('auth/reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('auth/reset-token-verify/<uidb64>/<token>/', PasswordTokenVerifyAPIView.as_view(), name='reset-token-verify'),

    # change password
    path('auth/change-password/', ChangePasswordAPIView.as_view(), name='change-passwrd'),
    # email staff
    path('auth/activate/<slug:code>/', ActivationAPIView.as_view(), name='activation-api'),


]
