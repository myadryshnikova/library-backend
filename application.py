from flask import Flask, Blueprint
from flask_cors import CORS
from flask_migrate import upgrade as _upgrade
from flask_jwt_extended import JWTManager

from datetime import timedelta

from library_api.domain.data_access_layer.build_connection_string import build_connection_string
from library_api.domain.data_access_layer.db import db, migrate
from library_api.domain.user import User

from library_api.modules.auth.auth_routes import auth_blueprint
from library_api.modules.auth.commands.new_user_command import NewUserCommand
from library_api.modules.books.books_routes import books_blueprint
from library_api.modules.bookshelfs.bookshelfs_routes import bookshelfs_blueprint
from library_api.modules.citations.citations_routes import citations_blueprint
from library_api.modules.readings.reading_routes import readings_blueprint
from library_api.modules.auth.services.auth_service import AuthService
from library_api.modules.auth.queries.user_query import GetUser


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

    app.config['JWT_SECRET_KEY'] = 'super-secret' 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=31)
    jwt = JWTManager(app)



    register_blueprints(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # runs pending migrations
    with app.app_context():
        _upgrade()

    username = "user"
    password = "password"
    user = GetUser().by_username(username)

    if not user:
        password_props = AuthService().get_hashed_password(password)
        user_entity = User(
            login=username,
            hashed_password=password_props.hashed_password,
            password_salt=password_props.salt
        )

        NewUserCommand().add_user(user_entity)

    return app


def register_blueprints(app):
    """Register all blueprints for application"""
    api_blueprint = Blueprint('api', __name__, url_prefix='/api')
    api_blueprint.register_blueprint(auth_blueprint)
    api_blueprint.register_blueprint(books_blueprint)
    api_blueprint.register_blueprint(bookshelfs_blueprint)
    api_blueprint.register_blueprint(citations_blueprint)
    api_blueprint.register_blueprint(readings_blueprint)

    app.register_blueprint(api_blueprint)
