from flask import Blueprint, request
from api.models.users_address_model import UsersAddressModel, UsersAddressSchema
from api.utils.responses import error_response, success_response
from api.utils.decorators import token_required
from api.models import db
from datetime import datetime

users_address_bp = Blueprint('users_address_bp', __name__)


@users_address_bp.route('/users/<user_id>/address', methods=['POST'])
@token_required
def users_address_create(current_user, user_id):
    if not request.is_json:
        return error_response(msg="Payload is not a JSON", code=406)

    if str(current_user.id) != user_id:
        return error_response(msg="Could not verify", code=401)

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

        try:
            db.session.add(new_address)
            db.session.commit()

            users_address_schema = UsersAddressSchema()

            data = users_address_schema.dump(new_address)

            return success_response(msg="Address registered successfully", code=201, data=data)
        except Exception:
            db.session.rollback()
            return error_response(msg="Unable to execute", code=500)
        finally:
            db.session.close()


@users_address_bp.route('/users/<user_id>/address', methods=['GET'])
@token_required
def users_address_get_all(current_user, user_id):
    if str(current_user.id) != user_id:
        return error_response(msg="Could not verify", code=401)

    if request.method == "GET":
        try:
            addresses = UsersAddressModel.query.filter_by(user_id=user_id).all()
            users_addresses_schema = UsersAddressSchema(many=True)

            data = {
                "user_id": current_user.id,
                "addresses": users_addresses_schema.dump(addresses)
            }

            return success_response(msg="Addresses received successfully", code=200, data=data)
        except Exception:
            return error_response(msg="Unable to execute", code=500)


@users_address_bp.route('/users/<user_id>/address/<address_id>', methods=['GET'])
@token_required
def users_address_get(current_user, user_id, address_id):
    if str(current_user.id) != user_id:
        return error_response(msg="Could not verify", code=401)

    if request.method == "GET":
        try:
            address = UsersAddressModel.query.filter_by(id=address_id, user_id=user_id).first()

            if not address:
                return error_response(msg="Address not found", code=404)

            users_address_schema = UsersAddressSchema()

            data = {
                "user_id": current_user.id,
                "address": users_address_schema.dump(address)
            }

            return success_response(msg="Address received successfully", code=200, data=data)
        except Exception:
            return error_response(msg="Unable to execute", code=500)


@users_address_bp.route('/users/<user_id>/address/<address_id>', methods=["PUT"])
@token_required
def users_address_edit(current_user, user_id, address_id):
    if not request.is_json:
        return error_response(msg="Payload is not a JSON", code=406)

    if str(current_user.id) != user_id:
        return error_response(msg="Could not verify", code=401)

    if request.method == "PUT":
        try:
            address = UsersAddressModel.query.filter_by(id=address_id, user_id=user_id).first()
            if not address:
                return error_response(msg="Address not found", code=404)

            required_fields = ["street", "number", "district", "zipcode", "city", "state"]

            data = request.get_json()
            for field in required_fields:
                if field not in data:
                    return error_response(msg="Fields missing in JSON", code=400)

            address.street = data["street"]
            address.number = data["number"]
            address.district = data["district"]
            address.zipcode = data["zipcode"]
            address.city = data["city"]
            address.state = data["state"]
            address.updated_at = datetime.now()

            db.session.commit()

            users_address_schema = UsersAddressSchema()

            data = users_address_schema.dump(address)

            return success_response(msg="Address edited successfully", code=200, data=data)
        except Exception:
            db.session.rollback()
            return error_response(msg="Unable to execute", code=500)
        finally:
            db.session.close()


@users_address_bp.route('/users/<user_id>/address/<address_id>', methods=["DELETE"])
@token_required
def users_address_delete(current_user, user_id, address_id):
    if str(current_user.id) != user_id:
        return error_response(msg="Could not verify", code=401)

    if request.method == "DELETE":
        try:
            address = UsersAddressModel.query.filter_by(id=address_id, user_id=user_id).first()

            if not address:
                return error_response(msg="Address not found", code=404)

            db.session.delete(address)
            db.session.commit()

            return success_response(msg="Address deleted successfully", code=200)
        except Exception:
            db.session.rollback()
            return error_response(msg="Unable to execute", code=500)
        finally:
            db.session.close()
