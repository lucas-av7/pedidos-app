from flask import Blueprint, request
from api.models.users_model import UsersModel, UsersSchema
from api.utils.responses import error_response
from api.models import db

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

        email_exists = UsersModel.query.filter_by(email=data["email"]).first()

        if email_exists is not None:
            return error_response(msg="E-mail is already in use", code=422)

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
