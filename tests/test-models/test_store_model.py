from api.models import db, ma, store_model


def test_if_has_store_model():
    assert hasattr(store_model, "StoreModel")


def test_if_StoreModel_extends_db_model():
    assert issubclass(store_model.StoreModel, db.Model)


def test_if_store_has_expectd_columns():
    columns = ["id", "name", "phone", "street", "number", "district", "city", "state", "created_at", "updated_at"]
    for column in columns:
        assert hasattr(store_model.StoreModel, column)


def test_if_store_has_ma_schema():
    assert hasattr(store_model, "StoreSchema")


def test_if_StoreSchema_extends_ma_sqlalchemy_schema():
    assert issubclass(store_model.StoreSchema, ma.SQLAlchemySchema)


def test_if_StoreSchema_has_Meta_and_points_to_StoreModel():
    assert hasattr(store_model.StoreSchema, "Meta")
    assert store_model.StoreSchema.Meta.model == store_model.StoreModel


new_store = store_model.StoreModel(
    name="Fake store",
    phone="(00) 00000-0000",
    street="Fake street",
    number="S/N",
    district="Fake district",
    city="Fake city",
    state="Fake state",
)


def test_if_store_is_correctly_instantiated():
    assert new_store.name == "Fake store"
    assert new_store.phone == "(00) 00000-0000"
    assert new_store.street == "Fake street"
    assert new_store.number == "S/N"
    assert new_store.district == "Fake district"
    assert new_store.city == "Fake city"
    assert new_store.state == "Fake state"
    assert str(new_store) == "<Store: Fake store>"


def test_if_StoreSchema_returns_expected_fields():
    store_schema = store_model.StoreSchema()

    serialized = store_schema.dump(new_store)

    assert "id" in serialized
    assert "name" in serialized
    assert "phone" in serialized
    assert "street" in serialized
    assert "number" in serialized
    assert "district" in serialized
    assert "city" in serialized
    assert "state" in serialized
    assert "created_at" not in serialized
    assert "updated_at" not in serialized
