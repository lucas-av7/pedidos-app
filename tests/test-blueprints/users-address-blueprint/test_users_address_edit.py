from api import app
from flask import url_for
from tests import client
import json

edited_valid_address = {
    "street": "Edited",
    "number": "S/N",
    "district": "Fake district",
    "zipcode": "60000-000",
    "city": "Fake city",
    "state": "Fake state"
}


def test_if_has_users_address_edit_route():
    rule = list(app.url_map.iter_rules('users_address_bp.users_address_edit'))[0].rule
    assert '/api/users/<user_id>/address/<address_id>' == rule


def test_if_users_address_edit_route_accept_put():
    methods = list(app.url_map.iter_rules('users_address_bp.users_address_edit'))[0].methods
    assert 'PUT' in methods


def test_if_returns_406_if_the_paylod_is_not_json():
    response = client.put(url_for('users_address_bp.users_address_edit', user_id=1, address_id=1), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_edit_users_address_with_success():
    response = client.put(url_for('users_address_bp.users_address_edit', user_id=1, address_id=1),
                          json=edited_valid_address)

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "Address edited successfully",
        "data": {
            "id": 1,
            "user_id": 1,
            **edited_valid_address
        }
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return


# TODO: test_if_users_addres_was_edited_on_db

def test_if_returns_400_if_the_json_is_invalid():
    response = client.put(url_for('users_address_bp.users_address_edit', user_id=1, address_id=1),
                          json={"street": "Fake street"})

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "Fields missing in JSON",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


def test_if_returns_404_if_the_address_doesnt_exis():
    response = client.put(url_for('users_address_bp.users_address_edit', user_id=1, address_id=10),
                          json={"street": "Fake street"})

    expected_return = {
        "status": "Error",
        "status_code": 404,
        "message": "Address not found",
    }

    assert response.status_code == 404
    assert json.loads(response.data) == expected_return


def test_if_returns_401_if_address_doesnt_belong_to_user():
    response = client.put(url_for('users_address_bp.users_address_edit', user_id=2, address_id=1),
                          json=edited_valid_address)

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return
