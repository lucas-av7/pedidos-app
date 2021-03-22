from api.models import db, ma, users_model
from api import app


def test_if_has_users_model():
    assert hasattr(users_model, "UserModel")


def test_if_UserModel_extends_db_model():
    assert issubclass(users_model.UserModel, db.Model)


def test_if_User_has_expectd_columns():
    assert hasattr(users_model.UserModel, "id")
    assert hasattr(users_model.UserModel, "name")
    assert hasattr(users_model.UserModel, "email")
    assert hasattr(users_model.UserModel, "phone")
    assert hasattr(users_model.UserModel, "password")
    assert hasattr(users_model.UserModel, "created_at")
    assert hasattr(users_model.UserModel, "updated_at")


def test_if_User_is_correctly_instantiated():
    global new_user  # for using in another test
    new_user = users_model.UserModel(
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


def test_if_user_has_ma_schema():
    assert hasattr(users_model, "UserSchema")


def test_if_UserSchema_extends_ma_sqlalchemy_schema():
    assert issubclass(users_model.UserSchema, ma.SQLAlchemySchema)


def test_if_UserSchema_has_Meta_and_points_to_UserModel():
    assert hasattr(users_model.UserSchema, "Meta")
    assert users_model.UserSchema.Meta.model == users_model.UserModel


def test_if_UserSchema_returns_only_id_name_email():
    user_schema = users_model.UserSchema()

    serialized = user_schema.dump(new_user)

    assert "id" in serialized
    assert "name" in serialized
    assert "email" in serialized
    assert "phone" not in serialized
    assert "password" not in serialized
    assert "created_at" not in serialized
    assert "updated_at" not in serialized
