from flask import Blueprint, request
from api.models.users_model import UsersModel, UsersSchema
from api.utils.decorators import token_required
from api.utils.responses import error_response
from api.models import db
from datetime import datetime
from passlib.hash import sha256_crypt

users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/users', methods=['POST'])
def users_create():
    if not request.is_json:
        return error_response(msg="Payload is not a JSON", code=406)

    if request.method == 'POST':
        data = request.get_json()

        required_fields = ["name", "email", "phone", "password"]
        for field in required_fields:
            if field not in data:
                return error_response(msg="Fields missing in JSON", code=400)

        if "@" not in data["email"] or "." not in data["email"]:
            return error_response(msg="The values of the JSON have invalid types", code=400)

        try:
            email_exists = UsersModel.query.filter_by(email=data["email"]).first()

            if email_exists is not None:
                return error_response(msg="E-mail is already in use", code=422)

            new_user = UsersModel(
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                password=sha256_crypt.hash(data["password"])
            )

            db.session.add(new_user)
            db.session.commit()

            users_schema = UsersSchema()

            response = {
                "status": "Success",
                "status_code": 201,
                "message": "User registered successfully",
                "data": users_schema.dump(new_user)
            }

            return response, 201
        except Exception:
            db.session.rollback()
            return error_response(msg="Unable to execute", code=500)
        finally:
            db.session.close()


@users_bp.route('/users/<user_id>', methods=['GET'])
@token_required
def users_get(current_user, user_id):
    if str(current_user.id) != user_id:
        return error_response(msg="Could not verify", code=401)

    if request.method == "GET":
        try:
            address = UsersModel.query.filter_by(id=user_id).first()
            users_schema = UsersSchema()
            response = {
                "status": "Success",
                "status_code": 200,
                "message": "User received successfully",
                "data": users_schema.dump(address)
            }
            return response, 200
        except Exception:
            return error_response(msg="Unable to execute", code=500)


@users_bp.route('/users/<user_id>', methods=['PUT'])
@token_required
def users_edit(current_user, user_id):
    if not request.is_json:
        return error_response(msg="Payload is not a JSON", code=406)

    if str(current_user.id) != user_id:
        return error_response(msg="Could not verify", code=401)

    if request.method == "PUT":
        try:
            user = UsersModel.query.filter_by(id=user_id).first()

            required_fields = ["name", "email", "phone"]

            data = request.get_json()
            for field in required_fields:
                if field not in data:
                    return error_response(msg="Fields missing in JSON", code=400)

            user.name = data["name"]
            user.email = data["email"]
            user.phone = data["phone"]
            user.updated_at = datetime.now()

            db.session.commit()

            users_schema = UsersSchema()

            response = {
                "status": "Success",
                "status_code": 200,
                "message": "User edited successfully",
                "data": users_schema.dump(user)
            }

            return response, 200
        except Exception:
            db.session.rollback()
            return error_response(msg="Unable to execute", code=500)
        finally:
            db.session.close()
