from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from library_api.modules.auth.commands.new_user_command import NewUserCommand
from library_api.modules.auth.queries.user_query import GetUser

from library_api.modules.auth.services.auth_service import AuthService
from library_api.domain.data_access_layer import session
from library_api.domain.user import User

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = GetUser().by_username(
        username
        )

    if not user:
        return jsonify({'msg': 'Bad username or password'}), 401

    if not AuthService.check_password(password, user.hashed_password, user.password_salt):
        return jsonify({'msg': 'Bad username or password'}), 401
    access_token = create_access_token(identity=user.id)

    return jsonify({
        'accessToken': {
            'value': access_token,
        },
    }), HTTPStatus.OK


@auth_blueprint.route('/registration', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({'msg': 'Bad username or password'}), 401

    password_props = AuthService.get_hashed_password(password)

    user_entity = User(
        login=username,
        hashed_password=password_props.hashed_password,
        password_salt=password_props.salt
    )

    user_id = NewUserCommand().add_user(user_entity)

    return jsonify(
        user_id
        ), HTTPStatus.OK
