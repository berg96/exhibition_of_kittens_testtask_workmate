import pytest
from rest_framework_simplejwt.tokens import RefreshToken

KITTENS_URL = '/api/kittens/'
KITTENS_DETAIL_URL = '/api/kittens/{}/'
KITTEN_SCORE_URL = '/api/kittens/{}/score/'
BREEDS_URL = '/api/breeds/'


@pytest.mark.django_db
def test_jwt_login(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    response = api_client.get(KITTENS_URL)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_breeds(api_client):
    response = api_client.get(BREEDS_URL)
    assert response.status_code == 200
    assert isinstance(response.data['results'], list)


@pytest.mark.django_db
def test_add_kitten(api_client, user, breed):
    api_client.force_authenticate(user=user)
    data = {
        'name': 'Kit',
        'age': 3,
        'color': '#333222',
        'description': 'Test kitten',
        'breed': breed.id
    }
    response = api_client.post(KITTENS_URL, data=data)
    assert response.status_code == 201
    assert response.data['name'] == 'Kit'
    assert response.data['owner']['username'] == user.username


@pytest.mark.django_db
def test_add_kitten_with_partial_data(api_client, user, breed):
    api_client.force_authenticate(user=user)
    data = {
        'name': 'Kit',
        'age': 3,
        'color': '#333222',
        'description': 'Test kitten'
    }
    response = api_client.post(KITTENS_URL, data=data)
    assert response.status_code == 400
    assert 'breed' in response.data


@pytest.mark.django_db
def test_add_kitten_unauthorized(api_client, breed):
    data = {
        'name': 'Kit',
        'age': 3,
        'color': '#333222',
        'description': 'Test kitten',
        'breed': breed.id
    }
    response = api_client.post(KITTENS_URL, data=data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_kittens(api_client, create_kittens):
    response = api_client.get(KITTENS_URL)
    assert response.status_code == 200
    assert isinstance(response.data['results'], list)
    assert len(response.data['results']) > 0


@pytest.mark.django_db
def test_update_kitten(api_client, user, kitten):
    api_client.force_authenticate(user=user)
    data = {
        'name': 'Kot',
        'age': 6
    }
    response = api_client.patch(
        KITTENS_DETAIL_URL.format(kitten.id), data=data
    )
    assert response.status_code == 200
    assert response.data['name'] == 'Kot'


@pytest.mark.django_db
def test_update_kitten_another_user(api_client, another_user, kitten):
    api_client.force_authenticate(user=another_user)
    data = {
        'name': 'Kot',
        'age': 6
    }
    response = api_client.patch(
        KITTENS_DETAIL_URL.format(kitten.id), data=data
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_kitten(api_client, user, kitten):
    api_client.force_authenticate(user=user)
    response = api_client.delete(KITTENS_DETAIL_URL.format(kitten.id))
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_kitten_another_user(api_client, another_user, kitten):
    api_client.force_authenticate(user=another_user)
    response = api_client.delete(KITTENS_DETAIL_URL.format(kitten.id))
    assert response.status_code == 403


@pytest.mark.django_db
def test_rate_kitten(api_client, user, kitten):
    api_client.force_authenticate(user=user)
    data = {"score": 5}
    response = api_client.post(KITTEN_SCORE_URL.format(kitten.id), data=data)
    assert response.status_code == 201
    assert response.data['rating'] == 5.0


@pytest.mark.django_db
def test_double_rate_kitten(api_client, user, kitten, score):
    api_client.force_authenticate(user=user)
    data = {"score": 4}
    response = api_client.post(KITTEN_SCORE_URL.format(kitten.id), data=data)
    assert response.status_code == 400
