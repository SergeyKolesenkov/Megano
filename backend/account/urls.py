from django.http import HttpResponse
from django.urls import path
from .views import sign_in, sign_up, sign_out, ProfileAPIView, ChangePasswordView, ProfileUpdateAvatar

app_name = "account"

urlpatterns = [
    path('sign-in/', sign_in, name='sign_in'),
    path('sign-up/', sign_up, name='sign_up'),
    path('sign-out/', sign_out, name='sign_out'),
    path('profile/', ProfileAPIView.as_view(), name='api_profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/avatar/', ProfileUpdateAvatar.as_view(), name="update_avatar")
]