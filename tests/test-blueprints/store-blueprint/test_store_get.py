from api import app
from flask import url_for
from tests import client
from api.models import db
from test_store_edit import edited_valid_store
from api.models.store_model import StoreModel
import json


def test_if_has_store_get_route():
    rule = list(app.url_map.iter_rules('store_bp.store_get'))[0].rule
    assert '/api/store' == rule


def test_if_store_get_route_accept_get():
    methods = list(app.url_map.iter_rules('store_bp.store_get'))[0].methods
    assert 'GET' in methods


def test_if_get_store_with_success():
    response = client.get(url_for('store_bp.store_get'))

    expected_return = {
        "status": "Success",
        "status_code": 200,
        "message": "Store received successfully",
        "data": {
            **edited_valid_store
        }
    }

    assert response.status_code == 200
    assert json.loads(response.data) == expected_return


def test_if_returns_404_if_store_doesnt_exist():
    store = StoreModel.query.first()

    db.session.delete(store)
    db.session.commit()

    response = client.get(url_for('store_bp.store_get'))

    expected_return = {
        "status": "Error",
        "status_code": 404,
        "message": "No store created"
    }

    assert response.status_code == 404
    assert json.loads(response.data) == expected_return
