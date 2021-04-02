# from api import app
from flask import Blueprint, request
from api.utils.responses import error_response
from datetime import datetime, timedelta
from api.models.users_model import UsersModel
import os
import jwt

user_login_bp = Blueprint('user_login_bp', __name__)


@user_login_bp.route('/login', methods=['POST'])
def login():
    secret_key = os.getenv('SECRET_KEY')

    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return error_response(msg="Could not verify", code=401)

    user = UsersModel.query.filter_by(email=auth.username).first()

    if not user:
        return error_response(msg="User not found", code=401)

    if user.password == auth.password:
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=5),
            "iat": datetime.utcnow(),
            "sub": user.email
        }

        token = jwt.encode(payload, secret_key, algorithm="HS256")

        response = {
            "status": "Success",
            "status_code": 200,
            "message": "Validated successfuly",
            "data": {
                "token": token,
                "exp": datetime.now() + timedelta(hours=12)
            }
        }

        return response, 200

    return error_response(msg="Could not verify", code=401)
