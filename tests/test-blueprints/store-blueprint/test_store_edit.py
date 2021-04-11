from api import app
from flask import url_for
from tests import client
import json

edited_valid_store = {
    "name": "Fake store edited",
    "phone": "(85) 90000-0001",
    "street": "Fake street edited",
    "number": "Fake number edited",
    "district": "Fake district edited",
    "city": "Fake city edited",
    "state": "Fake state edited"
}


def test_if_has_store_edit_route():
    rule = list(app.url_map.iter_rules('store_bp.store_edit'))[0].rule
    assert '/api/store' == rule


def test_if_store_edit_route_accept_put():
    methods = list(app.url_map.iter_rules('store_bp.store_edit'))[0].methods
    assert 'PUT' in methods


def test_if_returns_406_if_the_paylod_is_not_json():
    response = client.put(url_for('store_bp.store_edit'), data="teste")

    expected_return = {
        "status": "Error",
        "status_code": 406,
        "message": "Payload is not a JSON"
    }

    assert response.status_code == 406
    assert json.loads(response.data) == expected_return


def test_if_edit_store_with_success():
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

def test_if_returns_400_if_the_json_is_invalid():
    response = client.put(url_for('store_bp.store_edit'), json={"name": "Fake store edited"})

    expected_return = {
        "status": "Error",
        "status_code": 400,
        "message": "Fields missing in JSON",
    }

    assert response.status_code == 400
    assert json.loads(response.data) == expected_return


# TODO: test_if_store_returns_404_when_no_store_was_found
