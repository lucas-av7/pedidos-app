from api import app
from flask import url_for
from tests import client
from test_users_address_edit import edited_valid_address
import json


def test_if_has_users_address_get_all_route():
    rule = list(app.url_map.iter_rules('users_address_bp.users_address_get_all'))[0].rule
    assert '/api/users/<user_id>/address' == rule


def test_if_users_address_get_all_route_accept_get():
    methods = list(app.url_map.iter_rules('users_address_bp.users_address_get_all'))[0].methods
    assert 'GET' in methods


def test_if_get_all_users_addresses_with_success():
    response = client.get(url_for('users_address_bp.users_address_get_all', user_id=1))

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "Addresses received successfully",
        "data": {
            "user_id": 1,
            "addresses": [{
                "id": 1,
                **edited_valid_address
            }]
        }
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return


def test_if_returns_401_if_user_id_doesnt_match():
    response = client.get(url_for('users_address_bp.users_address_get_all', user_id=2))

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return
