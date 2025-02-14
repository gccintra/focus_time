from flask import Blueprint, request, render_template, redirect, url_for
from app.controllers.auth_controller import AuthController
from ..utils.auth_decorator import redirect_if_logged_in


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
auth_controller = AuthController()


@auth_bp.route("/login", methods=["POST"])
@redirect_if_logged_in
def login_route():
    data = request.get_json()
    return auth_controller.login(data)

@auth_bp.route("/register", methods=["GET"])
@redirect_if_logged_in
def register_route():
    return render_template("register.html")


@auth_bp.route("/register/create_account", methods=["POST"])
@redirect_if_logged_in
def create_account_route():
    data = request.get_json()
    return auth_controller.create_user(data)
     
