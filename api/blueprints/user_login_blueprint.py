from flask import Blueprint, request
from api.utils import response
from datetime import datetime, timedelta
from api.models.users_model import UsersModel
from passlib.hash import sha256_crypt
import os
import jwt

user_login_bp = Blueprint('user_login_bp', __name__)


@user_login_bp.route('/login', methods=['POST'])
def login():
    secret_key = os.getenv('SECRET_KEY')

    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return response(msg="Could not verify", code=401)

    user = UsersModel.query.filter_by(email=auth.username).first()

    if not user:
        return response(msg="User not found", code=401)

    if sha256_crypt.verify(auth.password, user.password):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=30),
            "iat": datetime.utcnow(),
            "sub": user.id
        }

        token = jwt.encode(payload, secret_key, algorithm="HS256")

        data = {
            "token": token,
            "exp": datetime.utcnow() + timedelta(days=30)
        }

        return response(msg="Validated successfuly", code=200, data=data)

    return response(msg="Could not verify", code=401)
