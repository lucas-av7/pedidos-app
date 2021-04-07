from flask import Blueprint, request
from api.utils import response
from api.models.store_model import StoreModel, StoreSchema
from api.models import db

store_bp = Blueprint('store_bp', __name__)


@store_bp.route('/store', methods=['POST'])
def store_create():
    if not request.is_json:
        return response(msg="Payload is not a JSON", code=406)

    if request.method == 'POST':
        data = request.get_json()

        required_fields = ["name", "phone", "street", "number", "district", "city", "state"]
        for field in required_fields:
            if field not in data:
                return response(msg="Fields missing in JSON", code=400)

        try:
            store = StoreModel.query.all()

            if len(store) > 0:
                return response(msg="The database already has a store created", code=400)

            new_store = StoreModel(
                name=data["name"],
                phone=data["phone"],
                street=data["street"],
                number=data["number"],
                district=data["district"],
                city=data["city"],
                state=data["state"]
            )

            db.session.add(new_store)
            db.session.commit()

            store_schema = StoreSchema()

            data = store_schema.dump(new_store)

            return response(msg="Store created successfully", code=201, data=data)
        except Exception:
            db.session.rollback()
            return response(msg="Unable to execute", code=500)
        finally:
            db.session.close()
