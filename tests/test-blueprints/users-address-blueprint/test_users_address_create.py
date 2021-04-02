from api import app
from flask import url_for
from tests import client
import json

valid_address = {
    "user_id": 1,
    "street": "Fake street",
    "number": "S/N",
    "district": "Fake district",
    "zipcode": "60000-000",
    "city": "Fake city",
    "state": "Fake state"
}


def test_if_api_has_users_adress_bluprint():
    assert "users_address_bp" in app.blueprints


def test_if_has_users_address_route():
    rule = list(app.url_map.iter_rules('users_address_bp.users_address_create'))[0].rule
    assert '/api/users/<user_id>/address' == rule


def test_if_users_address_route_accept_post():
    methods = list(app.url_map.iter_rules('users_address_bp.users_address_create'))[0].methods
    assert 'POST' in methods


def test_if_returns_406_if_the_paylod_is_not_json():
    response = client.post(url_for('users_address_bp.users_address_create', user_id=1), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_register_users_address_with_success():
    response = client.post(url_for('users_address_bp.users_address_create', user_id=1), json=valid_address)

    expected_return = {
        "status": "Success",
        "status_code": 201,
        "message": "Address registered successfully",
        "data": {
            "id": 1,
            **valid_address
        }
    }

    assert response.status_code == 201
    assert json.loads(response.data) == expected_return


# TODO: test_if_users_is_on_db

def test_if_returns_400_if_the_json_is_invalid():
    response = client.post(url_for('users_address_bp.users_address_create', user_id=1), json={
        "street": "Fake street",
    })

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "Fields missing in JSON",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


def test_if_returns_401_if_user_id_doesnt_match():
    response = client.post(url_for('users_address_bp.users_address_create', user_id=2), json=valid_address)

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return
