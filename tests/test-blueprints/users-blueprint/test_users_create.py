from api import app
from flask import url_for
from tests import client
import json

valid_user = {
    "name": "Lucas Vasconcelos",
    "email": "lucas@email.com",
    "phone": "(85) 90000-0000",
    "password": "password123"
}


def test_if_api_has_users_bluprint():
    assert "users_bp" in app.blueprints


def test_if_has_users_route():
    rule = list(app.url_map.iter_rules('users_bp.users_create'))[0].rule
    assert '/api/users' == rule


def test_if_users_route_accept_post():
    methods = list(app.url_map.iter_rules('users_bp.users_create'))[0].methods
    assert 'POST' in methods


def test_if_returns_406_if_the_paylod_is_not_json():
    response = client.post(url_for('users_bp.users_create'), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_register_users_with_success():
    response = client.post(url_for('users_bp.users_create'), json=valid_user)

    expected_return = {
        "status": "Success",
        "status_code": 201,
        "message": "User registered successfully",
        "data": {
            "id": 1,
            "name": "Lucas Vasconcelos",
            "email": "lucas@email.com"
        }
    }

    assert response.status_code == 201
    assert json.loads(response.data) == expected_return


# TODO: test_if_users_is_on_db

def test_if_returns_422_if_users_already_exists():
    response = client.post(url_for('users_bp.users_create'), json=valid_user)

    expected_return = {
        "status": "Error",
        "status_code": 422,
        "message": "E-mail is already in use",
    }

    assert response.status_code == 422
    assert json.loads(response.data) == expected_return


def test_if_returns_400_if_the_json_is_invalid():
    response = client.post(url_for('users_bp.users_create'), json={
        "name": "Lucas Vasconcelos",
    })

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "Fields missing in JSON",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


def test_if_returns_400_if_the_email_is_invalid():
    invalid_email = {**valid_user}
    invalid_email['email'] = "lucas"

    response = client.post(url_for('users_bp.users_create'), json=invalid_email)

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "The values of the JSON have invalid types",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return
