from api import app
from flask import url_for
import os


def test_if_api_has_user_bluprint():
    assert "user_bp" in app.blueprints


def test_if_has_register_route():
    url = list(app.url_map.iter_rules('user_bp.register'))[0].rule
    assert '/api/user/register' == url


def test_if_register_user_with_success():
    client = app.test_client()
    
    response = client.post(url_for('user_bp.register'), json={
        "name": "Lucas Vasconcelos",
        "email": "lucas@email.com",
        "cpf": "000.000.000-00",
        "phone": "(85) 90000-0000",
        "password": "password123"
    })

    assert response.status_code == 201
