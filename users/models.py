from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("user", "Пользователь"),
        ("admin", "Администратор"),
    ]

    first_name = models.CharField(max_length=50, verbose_name="Имя", help_text="Укажите свое имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", help_text="Укажите свою фамилию")
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Укажите email")
    phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Телефон", help_text="Укажите номер телефона"
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    role = models.CharField(max_length=21, choices=ROLE_CHOICES, default="user")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
