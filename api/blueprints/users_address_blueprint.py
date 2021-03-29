from flask import Blueprint, request
from api.models.users_address_model import UsersAddressModel, UsersAddressSchema
from api.models import db

users_address_bp = Blueprint('users_address_bp', __name__)


@users_address_bp.route('/users/address', methods=['POST'])
def users_address_create():
    if request.method == 'POST' and request.is_json:
        data = request.get_json()

        required_fields = ["user_id", "street", "number", "district", "zipcode", "city", "state"]
        for field in required_fields:
            if field not in data:
                response = {
                    "status": "Error",
                    "status_code": 400,
                    "message": "Fields missing in JSON"
                }

                return response, 400

        new_address = UsersAddressModel(
            user_id=data["user_id"],
            street=data["street"],
            number=data["number"],
            district=data["district"],
            zipcode=data["zipcode"],
            city=data["city"],
            state=data["state"]
        )

        db.session.add(new_address)
        db.session.commit()

        users_address_schema = UsersAddressSchema()

        response = {
            "status": "Success",
            "status_code": 201,
            "message": "Address registered successfully",
            "data": users_address_schema.dump(new_address)
        }

        return response, 201

    else:
        response = {
            "status": "Error",
            "status_code": 406,
            "message": "Payload is not a JSON"
        }

        return response, 406
