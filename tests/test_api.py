import pytest
from starlette.testclient import TestClient

from src.main import app
from tests.conftest import get_test_user_data


@pytest.fixture
def client():
    return TestClient(app)


def test_get_user_info_by_id(client):
    response = client.get('/users/info/1')
    assert response.status_code == 200
    assert response.json()['user_id'] == get_test_user_data()[0].user_id
    assert response.json()['first_name'] == get_test_user_data()[0].first_name
    response = client.get('/users/user_id/5')
    assert response.status_code == 404


def test_get_all_users_info(client):
    response = client.get('/users/all')
    assert response.status_code == 200
    assert len(response.json()) == len(get_test_user_data())


def test_get_users_info_by_firstname(client):
    response = client.get('/users/search/roger')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]['first_name'] == get_test_user_data()[0].first_name
    response = client.get('/users/search/jo')
    assert response.status_code == 404


def test_update_user_info_by_id(client):
    response = client.put('/users/update/2', json={'username': 'jane'})
    assert response.status_code == 200
    updated_user = client.get('/users/info/2').json()
    assert updated_user['username'] == 'jane'


def test_delete_user_by_id(client):
    response = client.delete('/users/delete/1')
    assert response.status_code == 200
    deleted_user_response = client.get('/users/info/1')
    assert deleted_user_response.status_code == 404
