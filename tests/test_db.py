import api
from api import app
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from api import models


def test_if_models_has_db():
    assert hasattr(models, 'db')


def test_if_db_has_api_as_application():
    assert models.db.get_app().name == "api"


def test_if_db_sqlite_is_configured():
    db_path = app.config.get('SQLALCHEMY_DATABASE_URI')
    assert db_path != "sqlite:///:memory:"


def test_if_tes_db_is_sqlite():
    db_path = app.config.get('SQLALCHEMY_DATABASE_URI')
    assert "sqlite" in db_path


def test_if_api_has_postgres_connection_data():
    assert hasattr(api, 'pg_user')
    assert hasattr(api, 'pg_password')
    assert hasattr(api, 'pg_database')


def test_if_models_has_db_migrate_config():
    assert hasattr(models, "migrate")


def test_if_migrate_is_instance_of_Migrate():
    assert isinstance(models.migrate, Migrate)


def test_if_models_has_marshmallow():
    assert hasattr(models, "ma")


def test_if_ma_is_instance_of_Marshmallow():
    assert isinstance(models.ma, Marshmallow)
