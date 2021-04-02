from api import app
from flask import url_for
from tests import client
from test_users_address_create import valid_address
import json


def test_if_has_users_address_delete_route():
    rule = list(app.url_map.iter_rules('users_address_bp.users_address_delete'))[0].rule
    assert '/api/users/<user_id>/address/<address_id>' == rule


def test_if_users_address_edit_route_accept_delete():
    methods = list(app.url_map.iter_rules('users_address_bp.users_address_delete'))[0].methods
    assert 'DELETE' in methods


def test_if_delete_users_address_with_success():
    # Creating address for testing
    client.post(url_for('users_address_bp.users_address_create', user_id=1), json=valid_address)

    response = client.delete(url_for('users_address_bp.users_address_delete', user_id=1, address_id=2))

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "Address deleted successfully",
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return


# TODO: test_if_users_addres_was_deleted_on_db

def test_if_returns_404_if_the_address_doesnt_exist():
    response = client.delete(url_for('users_address_bp.users_address_delete', user_id=1, address_id=10))

    expected_return = {
        "status": "Error",
        "status_code": 404,
        "message": "Address not found",
    }

    assert response.status_code == 404
    assert json.loads(response.data) == expected_return


def test_if_returns_401_if_address_doesnt_belong_to_user():
    response = client.delete(url_for('users_address_bp.users_address_delete', user_id=2, address_id=1))

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return
