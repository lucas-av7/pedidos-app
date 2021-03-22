from api.models import db, ma, users_model
from api import app


def test_if_has_users_model():
    assert hasattr(users_model, "UsersModel")


def test_if_UsersModel_extends_db_model():
    assert issubclass(users_model.UsersModel, db.Model)


def test_if_users_has_expectd_columns():
    assert hasattr(users_model.UsersModel, "id")
    assert hasattr(users_model.UsersModel, "name")
    assert hasattr(users_model.UsersModel, "email")
    assert hasattr(users_model.UsersModel, "phone")
    assert hasattr(users_model.UsersModel, "password")
    assert hasattr(users_model.UsersModel, "created_at")
    assert hasattr(users_model.UsersModel, "updated_at")


def test_if_users_is_correctly_instantiated():
    global new_user  # for using in another test
    new_user = users_model.UsersModel(
        name="Lucas",
        email="lucas@email.com",
        phone="(00) 00000-0000",
        password="12345",
    )

    assert new_user.name == "Lucas"
    assert new_user.email == "lucas@email.com"
    assert new_user.phone == "(00) 00000-0000"
    assert new_user.password == "12345"
    assert str(new_user) == "<User: Lucas>"


def test_if_users_has_ma_schema():
    assert hasattr(users_model, "UsersSchema")


def test_if_UsersSchema_extends_ma_sqlalchemy_schema():
    assert issubclass(users_model.UsersSchema, ma.SQLAlchemySchema)


def test_if_UsersSchema_has_Meta_and_points_to_UsersModel():
    assert hasattr(users_model.UsersSchema, "Meta")
    assert users_model.UsersSchema.Meta.model == users_model.UsersModel


def test_if_UsersSchema_returns_only_id_name_email():
    users_schema = users_model.UsersSchema()

    serialized = users_schema.dump(new_user)

    assert "id" in serialized
    assert "name" in serialized
    assert "email" in serialized
    assert "phone" not in serialized
    assert "password" not in serialized
    assert "created_at" not in serialized
    assert "updated_at" not in serialized
