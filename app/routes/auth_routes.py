from flask import Blueprint, request, render_template
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
auth_controller = AuthController()


@auth_bp.route("/login", methods=["POST"])
def login_route():
    data = request.get_json()
    return auth_controller.login(data)

@auth_bp.route("/register", methods=["GET"])
def register_route():
    return render_template("register.html")


@auth_bp.route("/register/create_account", methods=["POST"])
def create_account_route():
    data = request.get_json()
    return auth_controller.create_user(data)
     
