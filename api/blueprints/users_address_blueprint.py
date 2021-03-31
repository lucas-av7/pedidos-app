from flask import Blueprint, request
from api.models.users_address_model import UsersAddressModel, UsersAddressSchema
from api.utils.responses import error_response
from api.models import db
from datetime import datetime

users_address_bp = Blueprint('users_address_bp', __name__)


@users_address_bp.route('/users/<user_id>/address', methods=['POST'])
def users_address_create(user_id):
    if not request.is_json:
        return error_response(msg="Payload is not a JSON", code=406)

    if request.method == 'POST':
        data = request.get_json()

        required_fields = ["street", "number", "district", "zipcode", "city", "state"]
        for field in required_fields:
            if field not in data:
                return error_response(msg="Fields missing in JSON", code=400)

        new_address = UsersAddressModel(
            user_id=user_id,
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


@users_address_bp.route('/users/<user_id>/address/<address_id>', methods=["PUT"])
def users_address_edit(user_id, address_id):
    if not request.is_json:
        return error_response(msg="Payload is not a JSON", code=406)

    if request.method == "PUT":
        data = request.get_json()

        required_fields = ["street", "number", "district", "zipcode", "city", "state"]
        for field in required_fields:
            if field not in data:
                return error_response(msg="Fields missing in JSON", code=400)

        address = UsersAddressModel.query.filter_by(id=address_id, user_id=user_id).first()

        address.street = data["street"]
        address.number = data["number"]
        address.district = data["district"]
        address.zipcode = data["zipcode"]
        address.city = data["city"]
        address.state = data["state"]
        address.updated_at = datetime.now()

        db.session.commit()

        users_address_schema = UsersAddressSchema()

        response = {
            "status": "Success",
            "status_code": 200,
            "message": "Address edited successfully",
            "data": users_address_schema.dump(address)
        }

        return response, 200
