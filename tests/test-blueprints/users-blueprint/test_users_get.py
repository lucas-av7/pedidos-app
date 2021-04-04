from api import app
from flask import url_for
from tests import client
import json


def test_if_has_users_get_route():
    rule = list(app.url_map.iter_rules('users_bp.users_get'))[0].rule
    assert '/api/users/<user_id>' == rule


def test_if_users_route_accept_get():
    methods = list(app.url_map.iter_rules('users_bp.users_get'))[0].methods
    assert 'GET' in methods


def test_if_get_user_with_success():
    response = client.get(url_for('users_bp.users_get', user_id=1))

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "User received successfully",
        "data": {
            "id": 1,
            "name": "Lucas Vasconcelos",
            "email": "lucas@email.com",
            "phone": "(85) 90000-0000",
        }
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return


def test_if_returns_401_if_user_doesnt_match():
    response = client.get(url_for('users_bp.users_get', user_id=2))

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return
