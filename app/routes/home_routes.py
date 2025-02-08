from flask import Blueprint, request, jsonify, render_template

home_bp = Blueprint("home", __name__, url_prefix="/")


@home_bp.route("/", methods=["GET"])
def home():
    return render_template("home.html")
