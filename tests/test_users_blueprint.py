from api import app
from flask import url_for
import os

client = app.test_client()
valid_user = {
    "name": "Lucas Vasconcelos",
    "email": "lucas@email.com",
    "phone": "(85) 90000-0000",
    "password": "password123"
}


def test_if_api_has_user_bluprint():
    assert "user_bp" in app.blueprints


def test_if_has_register_route():
    url = list(app.url_map.iter_rules('user_bp.register'))[0].rule
    assert '/api/user/register' == url


def test_if_register_user_with_success():

    response = client.post(url_for('user_bp.register'), json=valid_user)

    expected_return = {
        "status_code": 201,
        "message": "User registered successfully",
        "data": {
            "id": 1,
            "name": "Lucas Vasconcelos",
            "email": "lucas@email.com"
        }
    }

    assert response.status_code == 201
    assert response.json == expected_return


def test_if_returns_422_if_user_already_exists():
    response = client.post(url_for('user_bp.register'), json=valid_user)

    expected_return = {
        "status_code": 422,
        "message": "E-mail is already in use",
    }

    assert response.status_code == 422
    assert response.json == expected_return


def test_if_returns_400_if_the_json_is_invalid():
    response = client.post(url_for('user_bp.register'), json={
        "name": "Lucas Vasconcelos",
    })

    expected_return = {
        "status_code": 400,
        "message": "Fields missing in json",
    }

    assert response.status_code == 400
    assert response.json == expected_return


def test_if_returns_400_if_the_email_is_invalid():
    invalid_email = {**valid_user}
    invalid_email['email'] = "lucas"

    response = client.post(url_for('user_bp.register'), json=invalid_email)

    expected_return = {
        "status_code": 400,
        "message": "The values of the JSON have invalid types",
    }

    assert response.status_code == 400
    assert response.json == expected_return
