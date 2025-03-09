import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Advertisement, Comment

User = get_user_model()


@pytest.fixture
def user():
    '''Создание обычного пользователя для дальнейшего тестирования'''
    return User.objects.create_user(email="testuser@example.com", username="testuser", password="testpassword")


@pytest.fixture
def admin_user():
    '''Создание администратора для дальнейшего тестирования'''
    return User.objects.create_superuser(email="admin@example.com", username="admin", password="adminpassword")


@pytest.fixture
def advertisement(user):
    '''Создание объявления для дальнейшего тестирования'''
    return Advertisement.objects.create(title="Test Ad", price=1000, description="Test Description", author=user)


@pytest.fixture
def comment(user, advertisement):
    '''Создание комментария для дальнейшего тестирования'''
    return Comment.objects.create(text="Test Comment", ad=advertisement, author=user)


@pytest.fixture
def api_client():
    '''Cоздание экземпляра API клиента'''
    return APIClient()


@pytest.mark.django_db
def test_create_advertisement(api_client, user):
    '''Проверка создания объявления'''
    api_client.force_authenticate(user=user)
    url = reverse("callboard:ad-create")  # Используем имя маршрута
    data = {"title": "New Ad", "price": 2000, "description": "New Ad Description"}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "New Ad"
    assert response.data["price"] == 2000


@pytest.mark.django_db
def test_get_advertisement_list(api_client, advertisement):
    '''Проверка получения списка объявлений'''
    url = reverse("callboard:ad-list")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == advertisement.title


@pytest.mark.django_db
def test_get_advertisement_detail(api_client, advertisement):
    '''Проверка просмотра конкретного объявления'''
    url = reverse(
        "callboard:ad-get",
        args=[
            advertisement.id,
        ],
    )
    api_client.force_authenticate(user=advertisement.author)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == advertisement.title
    assert response.data["price"] == advertisement.price


@pytest.mark.django_db
def test_update_advertisement(api_client, advertisement, user):
    '''Проверка изменения объявления'''
    api_client.force_authenticate(user=user)
    url = reverse("callboard:ad-update", args=[advertisement.id])
    data = {"title": "Updated Ad", "price": 3000, "description": "Updated Description"}

    response = api_client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Updated Ad"
    assert response.data["price"] == 3000


@pytest.mark.django_db
def test_delete_advertisement(api_client, advertisement, user):
    '''Проверка удаления объявления'''
    api_client.force_authenticate(user=user)
    url = reverse("callboard:ad-delete", args=[advertisement.id])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Advertisement.objects.count() == 0


@pytest.mark.django_db
def test_create_comment(api_client, user, advertisement):
    '''Проверка создания комментария'''
    api_client.force_authenticate(user=user)
    url = reverse("callboard:comment-create")
    data = {"text": "New Comment", "ad": advertisement.id}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["text"] == "New Comment"
    assert response.data["ad"] == advertisement.id


@pytest.mark.django_db
def test_get_comment_list(api_client, comment, user):
    '''Проверка получения списка комментариев'''
    api_client.force_authenticate(user=user)
    url = reverse("callboard:comment-list")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["text"] == comment.text


@pytest.mark.django_db
def test_get_comment_detail(api_client, comment, user):
    '''Проверка просмотра конкретного комментария'''
    api_client.force_authenticate(user=user)
    url = reverse("callboard:comment-get", args=[comment.id])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["text"] == comment.text


@pytest.mark.django_db
def test_update_comment(api_client, comment, user):
    '''Проверка изменения комментария'''
    api_client.force_authenticate(user=user)
    url = reverse("callboard:comment-update", args=[comment.id])
    data = {"text": "Updated Comment"}

    response = api_client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["text"] == "Updated Comment"


@pytest.mark.django_db
def test_delete_comment(api_client, comment, user):
    '''Проверка удаления комментария'''
    api_client.force_authenticate(user=user)
    url = reverse("callboard:comment-delete", args=[comment.id])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.count() == 0
