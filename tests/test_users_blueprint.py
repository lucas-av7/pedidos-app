from api import create_app


def test_if_api_has_users_bluprint():
    app = create_app()
    assert "users_bp" in app.blueprints
