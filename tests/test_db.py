import api
from api import app
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


def test_if_api_has_db():
    assert hasattr(api, 'db')


def test_if_db_has_api_as_application():
    assert api.db.get_app().name == "api"


def test_if_db_sqlite_is_configured():
    db_path = app.config.get('SQLALCHEMY_DATABASE_URI')
    assert db_path != "sqlite:///:memory:"


def test_if_db_is_postgresql():
    db_path = app.config.get('SQLALCHEMY_DATABASE_URI')
    assert "postgresql" in db_path


def test_if_api_has_postgres_connection_data():
    assert hasattr(api, 'pg_user')
    assert hasattr(api, 'pg_password')
    assert hasattr(api, 'pg_database')


def test_if_api_has_a_valid_db_uri():
    from api import pg_user, pg_password, pg_database
    db_path = app.config.get('SQLALCHEMY_DATABASE_URI')
    expected_path = f"postgresql://{pg_user}:{pg_password}@localhost:5432/test"
    assert db_path == expected_path


def test_if_api_has_db_migrate_config():
    assert hasattr(api, "migrate")


def test_if_migrate_is_instance_of_Migrate():
    assert isinstance(api.migrate, Migrate)


def test_if_migrate_has_api_as_application():
    assert api.migrate.db.app.name == 'api'


def test_if_api_has_marshmallow():
    assert hasattr(api, "ma")


def test_if_ma_is_instance_of_Marshmallow():
    assert isinstance(api.ma, Marshmallow)
