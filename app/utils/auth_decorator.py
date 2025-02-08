from functools import wraps
from flask import request, current_app, redirect, url_for
import jwt
from ..models.exceptions import UserNotFoundError


def get_current_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None 

        # if 'Authorization' in request.headers:
        #     token = request.headers.get("Authorization")

        if 'auth_token' in request.cookies:
            token = request.cookies.get("auth_token")

        if not token:
            return redirect(url_for("home.home"))

        try:
            # pure_token = token.replace("Bearer ", "")
            secret_key = current_app.config["SECRET_KEY"]

            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = payload.get("id")

            request.current_user = user_id

        except (jwt.ExpiredSignatureError, UserNotFoundError, jwt.InvalidTokenError):
            return redirect(url_for("home.home"))

        return f(*args, **kwargs)

    return decorated_function
