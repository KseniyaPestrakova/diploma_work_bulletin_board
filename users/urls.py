from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserDestroyAPIView, RequestPasswordResetView, PasswordResetConfirmView

app_name = UsersConfig.name

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user-delete"),
    path('reset_password/', RequestPasswordResetView.as_view(), name='password_reset'),
    path('reset_password_confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]