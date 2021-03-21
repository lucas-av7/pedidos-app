from api.models import user_model
from api import app, db, ma


def test_if_has_user_model():
    assert hasattr(user_model, "User")


def test_if_User_extends_db_model():
    assert issubclass(user_model.User, db.Model)


def test_if_User_has_expectd_columns():
    assert hasattr(user_model.User, "id")
    assert hasattr(user_model.User, "name")
    assert hasattr(user_model.User, "email")
    assert hasattr(user_model.User, "cpf")
    assert hasattr(user_model.User, "phone")
    assert hasattr(user_model.User, "password")
    assert hasattr(user_model.User, "created_at")
    assert hasattr(user_model.User, "updated_at")


def test_if_User_is_correctly_instantiated():
    global new_user  # for using in another test
    new_user = user_model.User(
        name="Lucas",
        email="lucas@email.com",
        cpf="000.000.000-00",
        phone="(00) 00000-0000",
        password="12345",
    )

    assert new_user.name == "Lucas"
    assert new_user.email == "lucas@email.com"
    assert new_user.cpf == "000.000.000-00"
    assert new_user.phone == "(00) 00000-0000"
    assert new_user.password == "12345"
    assert str(new_user) == "<User: Lucas>"


def test_if_user_has_ma_schema():
    assert hasattr(user_model, "UserSchema")


def test_if_UserSchema_extends_ma_sqlalchemy_schema():
    assert issubclass(user_model.UserSchema, ma.SQLAlchemySchema)


def test_if_UserSchema_has_Meta_and_points_to_User():
    assert hasattr(user_model.UserSchema, "Meta")
    assert user_model.UserSchema.Meta.model == user_model.User


def test_if_UserSchema_returns_only_id_name_email():
    user_schema = user_model.UserSchema()

    serialized = user_schema.dump(new_user)

    assert "id" in serialized
    assert "name" in serialized
    assert "email" in serialized
    assert "cpf" not in serialized
    assert "phone" not in serialized
    assert "password" not in serialized
    assert "created_at" not in serialized
    assert "updated_at" not in serialized
