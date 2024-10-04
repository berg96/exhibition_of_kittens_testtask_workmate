import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from kittens.models import Breed, Kitten, Score


@pytest.fixture
def user(db):
    return User.objects.create_user(username='user', password='Password123')


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username='another_user', password='Password123'
    )


@pytest.fixture
def breed(db):
    return Breed.objects.create(name='Test breed', slug='test')


@pytest.fixture
def kitten(db, breed, user):
    return Kitten.objects.create(
        name='Kit', age=3, color='#333222', description='Test kitten',
        owner=user, breed=breed
    )


@pytest.fixture
def score(db, kitten, user):
    return Score.objects.create(user=user, kitten=kitten, score=5)


@pytest.fixture
def create_kittens(db, breed, user):
    Kitten.objects.bulk_create([
        Kitten(
            name='Kit', age=3, color='#333222', description='Test kitten 1',
            owner=user, breed=breed
        ),
        Kitten(
            name='Snow', age=3, color='#ffffff', description='Test kitten 2',
            owner=user, breed=breed
        )
    ])


@pytest.fixture
def api_client():
    return APIClient()
