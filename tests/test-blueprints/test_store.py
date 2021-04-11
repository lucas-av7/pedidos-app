from api import app
from flask import url_for
from tests import client
from api.models import db
from api.models.store_model import StoreModel
import pytest
import json


@pytest.fixture
def valid_store():
    return {
        "name": "Fake store",
        "phone": "(85) 90000-0000",
        "street": "Fake street",
        "number": "Fake number",
        "district": "Fake district",
        "city": "Fake city",
        "state": "Fake state"
    }


@pytest.fixture
def create_store(valid_store):
    response = client.post(url_for('store_bp.store_create'), json=valid_store)
    yield response
    store = StoreModel.query.first()
    db.session.delete(store)
    db.session.commit()


@pytest.fixture
def edited_valid_store():
    return {
        "name": "Fake store edited",
        "phone": "(85) 90000-0001",
        "street": "Fake street edited",
        "number": "Fake number edited",
        "district": "Fake district edited",
        "city": "Fake city edited",
        "state": "Fake state edited"
    }


def test_if_api_has_store_bluprint():
    assert "store_bp" in app.blueprints


# store_create

def test_if_has_store_route():
    rule = list(app.url_map.iter_rules('store_bp.store_create'))[0].rule
    assert '/api/store' == rule


def test_if_store_route_accept_post():
    methods = list(app.url_map.iter_rules('store_bp.store_create'))[0].methods
    assert 'POST' in methods


def test_if_store_create_returns_406_if_the_paylod_is_not_json():
    response = client.post(url_for('store_bp.store_create'), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_store_create_returns_400_if_the_json_is_invalid():
    response = client.post(url_for('store_bp.store_create'), json={"name": "Fake store"})

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "Fields missing in JSON",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


def test_if_create_store_with_success(create_store):

    expected_return = {
        "status": "Success",
        "status_code": 201,
        "message": "Store created successfully",
        "data": {
            "name": "Fake store",
            "phone": "(85) 90000-0000",
            "street": "Fake street",
            "number": "Fake number",
            "district": "Fake district",
            "city": "Fake city",
            "state": "Fake state"
        }
    }

    assert create_store.status_code == 201
    assert json.loads(create_store.data) == expected_return


def test_if_returns_400_if_db_already_has_one_store(create_store, valid_store):
    response = client.post(url_for('store_bp.store_create'), json=valid_store)

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "The database already has a store created"
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


# store_edit

def test_if_has_store_edit_route():
    rule = list(app.url_map.iter_rules('store_bp.store_edit'))[0].rule
    assert '/api/store' == rule


def test_if_store_edit_route_accept_put():
    methods = list(app.url_map.iter_rules('store_bp.store_edit'))[0].methods
    assert 'PUT' in methods


def test_if_store_edit_returns_406_if_the_paylod_is_not_json():
    response = client.put(url_for('store_bp.store_edit'), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_edit_store_with_success(create_store, edited_valid_store):
    response = client.put(url_for('store_bp.store_edit'), json=edited_valid_store)

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "Store edited successfully",
        "data": {
            **edited_valid_store
        }
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return


# TODO: test_if_store_was_edited_on_db

def test_if_store_edit_returns_400_if_the_json_is_invalid(create_store):
    response = client.put(url_for('store_bp.store_edit'), json={"name": "Fake store edited"})

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "Fields missing in JSON",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


# TODO: test_if_store_returns_404_when_no_store_was_found

# store_get

def test_if_has_store_get_route():
    rule = list(app.url_map.iter_rules('store_bp.store_get'))[0].rule
    assert '/api/store' == rule


def test_if_store_get_route_accept_get():
    methods = list(app.url_map.iter_rules('store_bp.store_get'))[0].methods
    assert 'GET' in methods


def test_if_get_store_with_success(create_store, valid_store):
    response = client.get(url_for('store_bp.store_get'))

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "Store received successfully",
        "data": {
            **valid_store
        }
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return


def test_if_returns_404_if_store_doesnt_exist():
    response = client.get(url_for('store_bp.store_get'))

    expected_return = {
        "status": "Error",
        "status_code": 404,
        "message": "No store created"
    }

    assert response.status_code == 404
    assert json.loads(response.data) == expected_return
