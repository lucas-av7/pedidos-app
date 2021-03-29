from flask import Blueprint, request
from api.models.users_model import UsersModel, UsersSchema
from api.models import db

users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/users', methods=['POST'])
def users_create():
    if request.method == 'POST' and request.is_json:
        data = request.get_json()

        required_fields = ["name", "email", "phone", "password"]
        for field in required_fields:
            if field not in data:
                response = {
                    "status": "Error",
                    "status_code": 400,
                    "message": "Fields missing in JSON"
                }

                return response, 400

        if "@" not in data["email"] or "." not in data["email"]:
            response = {
                "status": "Error",
                "status_code": 400,
                "message": "The values of the JSON have invalid types"
            }

            return response, 400

        email_exists = UsersModel.query.filter_by(email=data["email"]).first()

        if email_exists is not None:
            response = {
                "status": "Error",
                "status_code": 422,
                "message": "E-mail is already in use"
            }

            return response, 422

        new_user = UsersModel(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            password=data["password"]
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

    else:
        response = {
            "status": "Error",
            "status_code": 406,
            "message": "Payload is not a JSON"
        }

        return response, 406
