from django.test import Client
import pytest
from rest_framework.test import APIClient
from mixer.backend.django import mixer
from django.contrib.auth.models import User

from store.models import Book
from cart.models import Cart, CartItem
from user_profile.models import UserProfile


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def create_book():
    def _create_book(**kwargs):
        return mixer.blend(Book, **kwargs)

    return _create_book


@pytest.fixture
def create_three_books():
    def _create_books():
        return mixer.cycle(3).blend(Book, photo="/static/img/default-book.png")

    return _create_books


@pytest.fixture
def existing_user():
    # Создаем пользователя для тестов
    user = User.objects.create_user(username="testuser", password="testpassword")
    UserProfile.objects.create(user=user)
    # return User.objects.create_user(username="testuser", password="testpassword")
    return user


@pytest.fixture
def authenticated_API_client(existing_user):
    client = APIClient()
    client.force_authenticate(user=existing_user)
    client.user = existing_user
    return client


@pytest.fixture
def authenticated_client(existing_user):
    client = Client()
    client.force_login(existing_user)
    return client


@pytest.fixture
def create_cart_with_items(existing_user, create_book):
    cart = Cart.objects.create(user=existing_user, is_active=True)

    for i in range(3):
        book = create_book()
        CartItem.objects.create(cart=cart, book=book, quantity=i + 1, price=book.price)

    return cart