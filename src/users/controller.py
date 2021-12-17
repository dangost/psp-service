from flask import Blueprint, request, jsonify, current_app as app

from src.users.schema import user_login_schema, user_registration_schema, user_schema

users_api = Blueprint("users_controller_api", __name__)


@users_api.route("/")
def index():
    return "PSP Service"


@users_api.route("/api/auth", methods=['POST'])
def login():
    user_login = user_login_schema.load(request.json)
    jwt_token = app.config.users_service.login(user_login)
    return jsonify({"Authorization": jwt_token}), 200


@users_api.route("/api/registration", methods=['POST'])
def registration():
    user_registration = user_registration_schema.load(request.json)
    user = app.config.users_service.create(user_registration)

    return jsonify(user_schema.dump(user)), 200


@users_api.route("/api/me", methods=["GET"])
def me():
    user = app.config.users_service.auth(request.headers)
    return jsonify({"login": user.login, "status": "Authorized"})
