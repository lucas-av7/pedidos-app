from api import app
from flask import url_for
from tests import client
from api.models import db
from api.models.users_model import UsersModel
import pytest
import json


@pytest.fixture
def valid_user():
    return {
        "name": "Lucas Vasconcelos",
        "email": "lucas@email.com",
        "phone": "(85) 90000-0000",
        "password": "password123"
    }


@pytest.fixture
def create_user(valid_user):
    response = client.post(url_for('users_bp.users_create'), json=valid_user)

    yield response

    user = UsersModel.query.filter_by(email="lucas@email.com").first()
    db.session.delete(user)
    db.session.commit()


def test_if_api_has_users_bluprint():
    assert "users_bp" in app.blueprints


# users_create

def test_if_has_users_route():
    rule = list(app.url_map.iter_rules('users_bp.users_create'))[0].rule
    assert '/api/users' == rule


def test_if_users_route_accept_post():
    methods = list(app.url_map.iter_rules('users_bp.users_create'))[0].methods
    assert 'POST' in methods


def test_if_users_create_returns_406_if_the_paylod_is_not_json():
    response = client.post(url_for('users_bp.users_create'), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_register_users_with_success(create_user):
    expected_return = {
        "status": "Success",
        "status_code": 201,
        "message": "User registered successfully",
        "data": {
            "id": 1,
            "name": "Lucas Vasconcelos",
            "email": "lucas@email.com",
            "phone": "(85) 90000-0000"
        }
    }

    assert create_user.status_code == 201
    assert json.loads(create_user.data) == expected_return


# TODO: test_if_users_is_on_db

def test_if_returns_422_if_users_already_exists(create_user, valid_user):
    response = client.post(url_for('users_bp.users_create'), json=valid_user)

    expected_return = {
        "status": "Error",
        "status_code": 422,
        "message": "E-mail is already in use",
    }

    assert response.status_code == 422
    assert json.loads(response.data) == expected_return


def test_if_users_create_returns_400_if_the_json_is_invalid():
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


def test_if_returns_400_if_the_email_is_invalid(valid_user):
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


# users_edit

@pytest.fixture
def edited_user():
    return {
        "name": "Lucas Vasconcelos",
        "email": "lucas@email.com",
        "phone": "(85) 90000-0000"
    }


def test_if_has_users_edit_route():
    rule = list(app.url_map.iter_rules('users_bp.users_edit'))[0].rule
    assert '/api/users/<user_id>' == rule


def test_if_users_edit_route_accept_put():
    methods = list(app.url_map.iter_rules('users_bp.users_edit'))[0].methods
    assert 'PUT' in methods


def test_if_users_edit_returns_406_if_the_paylod_is_not_json():
    response = client.put(url_for('users_bp.users_edit', user_id=1), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_edit_users_with_success(create_user, edited_user):
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


def test_if_users_edit_returns_400_if_the_json_is_invalid(create_user):
    response = client.put(url_for('users_bp.users_edit', user_id=1), json={"name": "New name"})

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "Fields missing in JSON",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


def test_if_returns_401_if_user_doesnt_match(create_user):
    response = client.put(url_for('users_bp.users_edit', user_id=2), json={"name": "New name"})

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return


# users_get

def test_if_has_users_get_route():
    rule = list(app.url_map.iter_rules('users_bp.users_get'))[0].rule
    assert '/api/users/<user_id>' == rule


def test_if_users_route_accept_get():
    methods = list(app.url_map.iter_rules('users_bp.users_get'))[0].methods
    assert 'GET' in methods


def test_if_get_user_with_success(create_user):
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


def test_if_users_get_returns_401_if_user_doesnt_match(create_user):
    response = client.get(url_for('users_bp.users_get', user_id=2))

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return


# users_password_edit

def test_if_has_users_password_edit_route():
    rule = list(app.url_map.iter_rules('users_bp.users_password_edit'))[0].rule
    assert '/api/users/<user_id>/password' == rule


def test_if_users_password_edit_route_accept_put():
    methods = list(app.url_map.iter_rules('users_bp.users_password_edit'))[0].methods
    assert 'PUT' in methods


def test_if_returns_406_if_the_paylod_is_not_json(create_user):
    response = client.put(url_for('users_bp.users_password_edit', user_id=1), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_users_password_edit_returns_401_if_user_doesnt_match(create_user):
    response = client.put(url_for('users_bp.users_password_edit', user_id=2), json={"password": "test"})

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return


def test_if_returns_400_if_the_json_is_invalid(create_user):
    response = client.put(url_for('users_bp.users_password_edit', user_id=1), json={"password": "123"})

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "Fields missing in JSON",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


def test_if_returns_401_if_the_password_is_incorrect(create_user):
    response = client.put(url_for('users_bp.users_password_edit', user_id=1), json={
                          "password": "password", "new_password": "0102030405"})

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Incorrect password",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return


def test_if_edit_users_password_with_success(create_user):
    response = client.put(url_for('users_bp.users_password_edit', user_id=1), json={
                          "password": "password123", "new_password": "0102030405"})

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "Password edited successfully",
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return
