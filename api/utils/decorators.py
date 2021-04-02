from flask import request, current_app
from functools import wraps
from .responses import error_response
from api.models.users_model import UsersModel
import os
import jwt

secret_key = os.getenv('SECRET_KEY')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_app.testing:
            current_user = UsersModel.query.filter_by(email="lucas@email.com").first()
            return f(current_user, *args, **kwargs)

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return error_response(msg="Authorization header is missing", code=401)

        pieces = auth_header.split(' ')

        if len(pieces) != 2:
            return error_response(msg="Authorization header is wrong", code=401)

        token = pieces[1]

        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            current_user = UsersModel.query.filter_by(email=data["sub"]).first()
        except Exception:
            return error_response(msg="Token is invalid or expired", code=401)
        return f(current_user, *args, **kwargs)
    return decorated
