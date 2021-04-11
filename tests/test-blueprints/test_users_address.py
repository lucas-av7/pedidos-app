from api import app
from flask import url_for
from tests import client
from api.models import db
from api.models.users_model import UsersModel
from api.models.users_address_model import UsersAddressModel
import pytest
import json


@pytest.fixture
def create_user():
    response = client.post(url_for('users_bp.users_create'), json={
        "name": "Lucas Vasconcelos",
        "email": "lucas@email.com",
        "phone": "(85) 90000-0000",
        "password": "password123"
    })

    yield response

    user = UsersModel.query.filter_by(email="lucas@email.com").first()
    db.session.delete(user)
    db.session.commit()


@pytest.fixture
def valid_address():
    return {
        "user_id": 1,
        "street": "Fake street",
        "number": "S/N",
        "district": "Fake district",
        "zipcode": "60000-000",
        "city": "Fake city",
        "state": "Fake state"
    }


@pytest.fixture
def create_address(create_user, valid_address):
    response = client.post(url_for('users_address_bp.users_address_create', user_id=1), json=valid_address)

    yield response

    address = UsersAddressModel.query.filter_by(id=1).first()
    db.session.delete(address)
    db.session.commit()


def test_if_api_has_users_adress_bluprint():
    assert "users_address_bp" in app.blueprints


# users_address_create

def test_if_has_users_address_route():
    rule = list(app.url_map.iter_rules('users_address_bp.users_address_create'))[0].rule
    assert '/api/users/<user_id>/address' == rule


def test_if_users_address_route_accept_post():
    methods = list(app.url_map.iter_rules('users_address_bp.users_address_create'))[0].methods
    assert 'POST' in methods


def test_if_users_address_create_returns_406_if_the_paylod_is_not_json():
    response = client.post(url_for('users_address_bp.users_address_create', user_id=1), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_register_users_address_with_success(create_address, valid_address):
    address = {**valid_address}
    address.pop("user_id")

    expected_return = {
        "status": "Success",
        "status_code": 201,
        "message": "Address registered successfully",
        "data": {
            "id": 1,
            **address
        }
    }

    assert create_address.status_code == 201
    assert json.loads(create_address.data) == expected_return


# TODO: test_if_users_is_on_db

def test_if_users_address_create_returns_400_if_the_json_is_invalid(create_user):
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


def test_if_users_address_create_returns_401_if_user_id_doesnt_match(create_user, valid_address):
    response = client.post(url_for('users_address_bp.users_address_create', user_id=2), json=valid_address)

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return


# users_address_get_all

def test_if_has_users_address_get_all_route():
    rule = list(app.url_map.iter_rules('users_address_bp.users_address_get_all'))[0].rule
    assert '/api/users/<user_id>/address' == rule


def test_if_users_address_get_all_route_accept_get():
    methods = list(app.url_map.iter_rules('users_address_bp.users_address_get_all'))[0].methods
    assert 'GET' in methods


def test_if_get_all_users_addresses_with_success(create_user, create_address, valid_address):
    response = client.get(url_for('users_address_bp.users_address_get_all', user_id=1))

    address = {**valid_address}
    address.pop("user_id")

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "Addresses received successfully",
        "data": {
            "user_id": 1,
            "addresses": [{
                "id": 1,
                **address
            }]
        }
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return


def test_if_users_address_get_all_returns_401_if_user_id_doesnt_match(create_user):
    response = client.get(url_for('users_address_bp.users_address_get_all', user_id=2))

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return


# users_address_get

def test_if_has_users_address_get_route():
    rule = list(app.url_map.iter_rules('users_address_bp.users_address_get'))[0].rule
    assert '/api/users/<user_id>/address/<address_id>' == rule


def test_if_users_address_get_route_accept_get():
    methods = list(app.url_map.iter_rules('users_address_bp.users_address_get'))[0].methods
    assert 'GET' in methods


def test_if_get_users_address_with_success(create_user, create_address, valid_address):
    response = client.get(url_for('users_address_bp.users_address_get', user_id=1, address_id=1))

    address = {**valid_address}
    address.pop("user_id")

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "Address received successfully",
        "data": {
            "user_id": 1,
            "address": {
                "id": 1,
                **address
            }
        }
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return


def test_if_users_address_get_returns_404_if_the_address_doesnt_exist(create_user):
    response = client.get(url_for('users_address_bp.users_address_get', user_id=1, address_id=1))

    expected_return = {
        "status": "Error",
        "status_code": 404,
        "message": "Address not found",
    }

    assert response.status_code == 404
    assert json.loads(response.data) == expected_return


def test_if_users_address_get_returns_401_if_address_doesnt_belong_to_user(create_user, create_address):
    response = client.get(url_for('users_address_bp.users_address_get', user_id=2, address_id=1))

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return


# users_address_edit

@pytest.fixture
def edited_valid_address():
    return {
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


def test_if_users_addres_edit_returns_406_if_the_paylod_is_not_json():
    response = client.put(url_for('users_address_bp.users_address_edit', user_id=1, address_id=1), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_edit_users_address_with_success(create_user, create_address, edited_valid_address):
    response = client.put(url_for('users_address_bp.users_address_edit', user_id=1, address_id=1),
                          json=edited_valid_address)

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "Address edited successfully",
        "data": {
            "id": 1,
            **edited_valid_address
        }
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return


# TODO: test_if_users_addres_was_edited_on_db

def test_if_users_address_edit_returns_400_if_the_json_is_invalid(create_user, create_address):
    response = client.put(url_for('users_address_bp.users_address_edit', user_id=1, address_id=1),
                          json={"street": "Fake street"})

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "Fields missing in JSON",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


def test_if_users_address_edit_returns_404_if_the_address_doesnt_exist(create_user):
    response = client.put(url_for('users_address_bp.users_address_edit', user_id=1, address_id=10),
                          json={"street": "Fake street"})

    expected_return = {
        "status": "Error",
        "status_code": 404,
        "message": "Address not found",
    }

    assert response.status_code == 404
    assert json.loads(response.data) == expected_return


def test_if_users_address_edit_returns_401_if_address_doesnt_belong_to_user(create_user,
                                                                            create_address,
                                                                            edited_valid_address):
    response = client.put(url_for('users_address_bp.users_address_edit', user_id=2, address_id=1),
                          json=edited_valid_address)

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return


# users_address_delete

def test_if_has_users_address_delete_route():
    rule = list(app.url_map.iter_rules('users_address_bp.users_address_delete'))[0].rule
    assert '/api/users/<user_id>/address/<address_id>' == rule


def test_if_users_address_edit_route_accept_delete():
    methods = list(app.url_map.iter_rules('users_address_bp.users_address_delete'))[0].methods
    assert 'DELETE' in methods


def test_if_delete_users_address_with_success(create_user, valid_address):
    # Creating address for testing
    client.post(url_for('users_address_bp.users_address_create', user_id=1), json=valid_address)

    response = client.delete(url_for('users_address_bp.users_address_delete', user_id=1, address_id=1))

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "Address deleted successfully",
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return


# TODO: test_if_users_addres_was_deleted_on_db

def test_if_returns_404_if_the_address_doesnt_exist(create_user):
    response = client.delete(url_for('users_address_bp.users_address_delete', user_id=1, address_id=10))

    expected_return = {
        "status": "Error",
        "status_code": 404,
        "message": "Address not found",
    }

    assert response.status_code == 404
    assert json.loads(response.data) == expected_return


def test_if_returns_401_if_address_doesnt_belong_to_user(create_user, create_address):
    response = client.delete(url_for('users_address_bp.users_address_delete', user_id=2, address_id=1))

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return
