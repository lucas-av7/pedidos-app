from api.models import db, ma, users_model
import pytest


@pytest.fixture
def new_user():
    return users_model.UsersModel(
        name="Lucas",
        email="lucas@email.com",
        phone="(00) 00000-0000",
        password="12345",
    )


def test_if_has_users_model():
    assert hasattr(users_model, "UsersModel")


def test_if_UsersModel_extends_db_model():
    assert issubclass(users_model.UsersModel, db.Model)


def test_if_users_has_expectd_columns():
    columns = ["id", "name", "email", "phone", "password", "created_at", "updated_at"]
    for column in columns:
        assert hasattr(users_model.UsersModel, column)


def test_if_users_has_ma_schema():
    assert hasattr(users_model, "UsersSchema")


def test_if_UsersSchema_extends_ma_sqlalchemy_schema():
    assert issubclass(users_model.UsersSchema, ma.SQLAlchemySchema)


def test_if_UsersSchema_has_Meta_and_points_to_UsersModel():
    assert hasattr(users_model.UsersSchema, "Meta")
    assert users_model.UsersSchema.Meta.model == users_model.UsersModel


def test_if_users_is_correctly_instantiated(new_user):
    assert new_user.name == "Lucas"
    assert new_user.email == "lucas@email.com"
    assert new_user.phone == "(00) 00000-0000"
    assert new_user.password == "12345"
    assert str(new_user) == "<User: Lucas>"


def test_if_UsersSchema_returns_only_id_name_email(new_user):
    users_schema = users_model.UsersSchema()

    serialized = users_schema.dump(new_user)

    assert "id" in serialized
    assert "name" in serialized
    assert "email" in serialized
    assert "phone" in serialized
    assert "password" not in serialized
    assert "created_at" not in serialized
    assert "updated_at" not in serialized
