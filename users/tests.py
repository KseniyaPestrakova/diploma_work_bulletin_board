import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_user(api_client):
    url = reverse("users:register")  # Укажите правильный путь
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword",
        "first_name": "John",
        "last_name": "Doe",
    }
    response = api_client.post(url, data)

    # Проверка создания пользователя
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email="newuser@example.com").exists()


@pytest.mark.django_db
def test_delete_user(api_client):
    # Создаем пользователя для удаления
    user = User.objects.create_user(username="deletableuser", email="deleteuser@example.com", password="password123")
    url = reverse("users:user-delete", kwargs={"pk": user.id})  # Укажите правильный путь

    # Отправляем запрос на удаление
    response = api_client.delete(url)

    # Проверка удаления
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(email="deleteuser@example.com").exists()
