from api import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def test_if_api_has_flask_app():
    assert isinstance(app, Flask)
