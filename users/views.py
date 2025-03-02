from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import EMAIL_HOST_USER
from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


# Генератор токенов для сброса пароля
token_generator = PasswordResetTokenGenerator()


class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if email:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            reset_url = request.build_absolute_uri(
                reverse("users:password_reset_confirm", kwargs={"uidb64": uid, "token": token})
            )
            send_mail(
                subject="Сброс пароля",
                message=f"Для сброса пароля перейдите по следующей ссылке: {reset_url}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[email],
            )
            return Response({"message": "Письмо для сброса пароля отправлено"}, status=status.HTTP_200_OK)
        return Response({"error": "Email не указан"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"message": "Пароль успешно изменен"})
        else:
            return Response({"error": "Недействительный токен или пользователь"}, status=status.HTTP_400_BAD_REQUEST)
