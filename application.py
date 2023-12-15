from flask import Flask, Blueprint
from flask_cors import CORS
from flask_migrate import upgrade as _upgrade

from library_api.domain.data_access_layer.build_connection_string import build_connection_string
from library_api.domain.data_access_layer.db import db, migrate


def create_app():
    """Application factory, used to create application"""
    app = Flask(__name__)

    # allow to call the api from any origin for now
    CORS(
        app,
    )

    app.config.from_object('library_api.config.flask_config')

    app.url_map.strict_slashes = False

    app.config['SQLALCHEMY_DATABASE_URI'] = build_connection_string()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    register_blueprints(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # runs pending migrations
    with app.app_context():
        _upgrade()


    return app


def register_blueprints(app):
    """Register all blueprints for application"""
    api_blueprint = Blueprint('api', __name__, url_prefix='/api')
    # api_blueprint.register_blueprint(orders_blueprint)

    app.register_blueprint(api_blueprint)
