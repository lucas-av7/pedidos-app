from api import app
from flask import url_for
from tests import client
import json

valid_store = {
    "name": "Fake store",
    "phone": "(85) 90000-0000",
    "street": "Fake street",
    "number": "Fake number",
    "district": "Fake district",
    "city": "Fake city",
    "state": "Fake state"
}


def test_if_api_has_store_bluprint():
    assert "store_bp" in app.blueprints


def test_if_has_store_route():
    rule = list(app.url_map.iter_rules('store_bp.store_create'))[0].rule
    assert '/api/store' == rule


def test_if_store_route_accept_post():
    methods = list(app.url_map.iter_rules('store_bp.store_create'))[0].methods
    assert 'POST' in methods


def test_if_returns_406_if_the_paylod_is_not_json():
    response = client.post(url_for('store_bp.store_create'), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_returns_400_if_the_json_is_invalid():
    response = client.post(url_for('store_bp.store_create'), json={"name": "Fake store"})

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "Fields missing in JSON",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


def test_if_create_store_with_success():
    response = client.post(url_for('store_bp.store_create'), json=valid_store)

    expected_return = {
        "status": "Success",
        "status_code": 201,
        "message": "Store created successfully",
        "data": {
            "id": 1,
            "name": "Fake store",
            "phone": "(85) 90000-0000",
            "street": "Fake street",
            "number": "Fake number",
            "district": "Fake district",
            "city": "Fake city",
            "state": "Fake state"
        }
    }

    assert response.status_code == 201
    assert json.loads(response.data) == expected_return


def test_if_returns_400_if_db_already_has_one_store():
    response = client.post(url_for('store_bp.store_create'), json=valid_store)

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "The database already has a store created"
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return
