import api
from flask import Flask
import json


def test_if_api_has_flask_app():
    assert isinstance(api.app, Flask)


def test_if_api_has_405_error_handler():
    assert hasattr(api, "not_allowed")
    expected_error = {
        "status": "Error",
        "status_code": 405,
        "message": "Method not allowed"
    }
    assert expected_error == json.loads(api.not_allowed("")[0].response[0])


def test_if_api_has_404_error_handler():
    assert hasattr(api, "not_found")
    expected_error = {
        "status": "Error",
        "status_code": 404,
        "message": "API endpoint not found"
    }
    assert expected_error == json.loads(api.not_found("")[0].response[0])
