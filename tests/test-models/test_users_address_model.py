from api.models import db, ma, users_address_model


def test_if_has_users_address_model():
    assert hasattr(users_address_model, "UsersAddressModel")


def test_if_UserAddressModel_extends_db_model():
    assert issubclass(users_address_model.UsersAddressModel, db.Model)


def test_if_UserAddress_has_expectd_columns():
    assert hasattr(users_address_model.UsersAddressModel, "id")
    assert hasattr(users_address_model.UsersAddressModel, "user_id")
    assert hasattr(users_address_model.UsersAddressModel, "street")
    assert hasattr(users_address_model.UsersAddressModel, "number")
    assert hasattr(users_address_model.UsersAddressModel, "district")
    assert hasattr(users_address_model.UsersAddressModel, "zipcode")
    assert hasattr(users_address_model.UsersAddressModel, "city")
    assert hasattr(users_address_model.UsersAddressModel, "state")
    assert hasattr(users_address_model.UsersAddressModel, "created_at")
    assert hasattr(users_address_model.UsersAddressModel, "updated_at")


def test_if_users_is_correctly_instantiated():
    global new_address  # for using in another test
    new_address = users_address_model.UsersAddressModel(
        street="Fake street",
        number="S/N",
        district="Fake district",
        zipcode="60000-000",
        city="Fake city",
        state="Fake state"
    )

    assert new_address.street == "Fake street"
    assert new_address.number == "S/N"
    assert new_address.district == "Fake district"
    assert new_address.zipcode == "60000-000"
    assert new_address.city == "Fake city"
    assert new_address.state == "Fake state"
    assert str(new_address) == "<Address: Fake street, S/N - Fake district>"


def test_if_users_address_has_ma_schema():
    assert hasattr(users_address_model, "UsersAddressSchema")


def test_if_UsersAddressSchema_extends_ma_sqlalchemy_schema():
    assert issubclass(users_address_model.UsersAddressSchema, ma.SQLAlchemySchema)


def test_if_UsersAddressSchema_has_Meta_and_points_to_UsersAddressModel():
    assert hasattr(users_address_model.UsersAddressSchema, "Meta")
    assert users_address_model.UsersAddressSchema.Meta.model == users_address_model.UsersAddressModel


def test_if_UsersAddressSchema_returns_all_fields_except_create_and_update():
    users_address_schema = users_address_model.UsersAddressSchema()

    serialized = users_address_schema.dump(new_address)

    assert "id" in serialized
    assert "user_id" in serialized
    assert "street" in serialized
    assert "number" in serialized
    assert "district" in serialized
    assert "zipcode" in serialized
    assert "city" in serialized
    assert "state" in serialized
    assert "created_at" not in serialized
    assert "updated_at" not in serialized
