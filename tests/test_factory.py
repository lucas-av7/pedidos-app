import api
from flask import Flask


def test_if_api_has_create_app():
    assert hasattr(api, 'create_app') == True


def test_if_create_app_returns_a_flask_app():
    assert isinstance(api.create_app(), Flask)
