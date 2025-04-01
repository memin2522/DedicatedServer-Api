from flask import Flask
from flask_smorest import Api
import logging

import models

from resources.main import blp as MainBlueprint


def create_app(db_url = None):
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    app.logger.info("🚀 Iniciando la aplicación Flask...")

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "ILCE REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:admin123@192.168.1.124:5432/postgres"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    api = Api(app)

    api.register_blueprint(MainBlueprint)

    app.logger.info("✅ Flask API lista para recibir peticiones.")

    return app
