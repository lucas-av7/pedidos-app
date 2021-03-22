from flask import Blueprint, request
from api.models.user_model import UserModel, UserSchema
from api.models import db

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()

            required_fields = ["name", "email", "phone", "password"]
            for field in required_fields:
                if field not in data:
                    response = {
                        "status_code": 400,
                        "message": "Fields missing in json"
                    }

                    return response, 400
                
            if "@" not in data["email"] or "." not in data["email"]:
                response = {
                    "status_code": 400,
                    "message": "The values of the JSON have invalid types"
                }

                return response, 400

            email_exists = UserModel.query.filter_by(email=data["email"]).first()

            if email_exists is not None:
                response = {
                    "status_code": 422,
                    "message": "E-mail is already in use"
                }

                return response, 422

            new_user = UserModel(
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                password=data["password"]
            )

            db.session.add(new_user)
            db.session.commit()

            user_schema = UserSchema()

            response = {
                "status_code": 201,
                "message": "User registered successfully",
                "data": user_schema.dump(new_user)
            }

            return response, 201
