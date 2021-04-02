from api import app
from flask import url_for
from tests import client
import json
import base64


def test_if_api_has_user_login_bluprint():
    assert "user_login_bp" in app.blueprints


def test_if_has_login_route():
    rule = list(app.url_map.iter_rules('user_login_bp.login'))[0].rule
    assert '/api/login' == rule


def test_if_users_address_route_accept_post():
    methods = list(app.url_map.iter_rules('user_login_bp.login'))[0].methods
    assert 'POST' in methods


def test_if_login_with_success():
    response = client.post(url_for('user_login_bp.login'), headers={
                           "Authorization": "Basic {}"
                           .format(base64.b64encode(b"lucas@email.com:password123").decode("utf8"))})

    assert response.json["status"] == "Success"


def test_if_get_401_when_has_not_auth():
    response = client.post(url_for('user_login_bp.login'))

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return


def test_if_get_401_when_user_not_exist():
    response = client.post(url_for('user_login_bp.login'), headers={
        "Authorization": "Basic {}"
        .format(base64.b64encode(b"lucas90@email.com:password").decode("utf8"))})

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "User not found",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return


def test_if_get_401_when_password_not_match():
    response = client.post(url_for('user_login_bp.login'), headers={
        "Authorization": "Basic {}"
        .format(base64.b64encode(b"lucas@email.com:password").decode("utf8"))})

    expected_return = {
        "status": "Error",
        "status_code": 401,
        "message": "Could not verify",
    }

    assert response.status_code == 401
    assert json.loads(response.data) == expected_return
