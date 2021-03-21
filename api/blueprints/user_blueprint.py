from flask import Blueprint, request
from api.models.user_model import UserModel, UserSchema
from api import db

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        if request.is_json:
            user_schema = UserSchema()

            data = request.get_json()
            new_user = UserModel(
                name=data["name"],
                email=data["email"],
                cpf=data["cpf"],
                phone=data["phone"],
                password=data["password"]
            )
            # db.session.add(new_user)
            # db.session.commit()

            return user_schema.dump(user_schema), 201
