from api import app
from flask import url_for
from tests import client
import json

edited_user = {
    "name": "Lucas Vasconcelos",
    "email": "lucas@email.com",
    "phone": "(85) 90000-0000",
}


def test_if_has_users_edit_route():
    rule = list(app.url_map.iter_rules('users_bp.users_edit'))[0].rule
    assert '/api/users/<user_id>' == rule


def test_if_users_edit_route_accept_put():
    methods = list(app.url_map.iter_rules('users_bp.users_edit'))[0].methods
    assert 'PUT' in methods


def test_if_returns_406_if_the_paylod_is_not_json():
    response = client.put(url_for('users_bp.users_edit', user_id=1), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_edit_users_with_success():
    response = client.put(url_for('users_bp.users_edit', user_id=1), json=edited_user)

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "User edited successfully",
        "data": {
            "id": 1,
            **edited_user
        }
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return


def test_if_returns_400_if_the_json_is_invalid():
    response = client.put(url_for('users_bp.users_edit', user_id=1), json={"name": "New name"})

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "Fields missing in JSON",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


def test_if_returns_401_if_user_doesnt_match():
    response = client.put(url_for('users_bp.users_edit', user_id=2), json={"name": "New name"})

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return
