from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from library_api.modules.auth.queries.user_query import GetUser

from library_api.modules.auth.services.auth_service import AuthService

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
