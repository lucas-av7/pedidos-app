from api import app
from flask import url_for
from tests import client
import json


def test_if_has_users_password_edit_route():
    rule = list(app.url_map.iter_rules('users_bp.users_password_edit'))[0].rule
    assert '/api/users/<user_id>/password' == rule


def test_if_users_password_edit_route_accept_put():
    methods = list(app.url_map.iter_rules('users_bp.users_password_edit'))[0].methods
    assert 'PUT' in methods


def test_if_returns_406_if_the_paylod_is_not_json():
    response = client.put(url_for('users_bp.users_password_edit', user_id=1), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_returns_401_if_user_doesnt_match():
    response = client.put(url_for('users_bp.users_password_edit', user_id=2), json={"password": "test"})

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return


def test_if_returns_400_if_the_json_is_invalid():
    response = client.put(url_for('users_bp.users_password_edit', user_id=1), json={"password": "123"})

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "Fields missing in JSON",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


def test_if_returns_401_if_the_password_is_incorrect():
    response = client.put(url_for('users_bp.users_password_edit', user_id=1), json={
                          "password": "password", "new_password": "0102030405"})

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Incorrect password",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return


def test_if_edit_users_password_with_success():
    response = client.put(url_for('users_bp.users_password_edit', user_id=1), json={
                          "password": "password123", "new_password": "0102030405"})

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "Password edited successfully",
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return
