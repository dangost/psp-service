from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, Unauthorized

from src.app_config import AppConfig
from src.users.controller import users_api
from src.users.exceptions import UserNotFoundException
from src.users.service import UsersService


def create_app(config: AppConfig) -> Flask:
    app = Flask("psp-service")

    # users blueprints
    app.register_blueprint(users_api)

    app.register_error_handler(HTTPException, error_handler)
    app.register_error_handler(Unauthorized, error_handler)

    app = init_services(app, config)

    config.sql_config.metadata.create_all(checkfirst=True)

    return app


def init_services(app: Flask, config: AppConfig):
    app.config.users_service = UsersService(
        config.sql_config, config.jwt_secret
    )
    return app


def error_handler(exc: HTTPException):
    return jsonify(
        {"statusCode": exc.code, "message": exc.description}
    ), exc.code

