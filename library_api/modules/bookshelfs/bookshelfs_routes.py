from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from library_api.domain.bookshelf import Bookshelf


from library_api.modules.auth.queries.user_query import GetUser
from library_api.modules.bookshelfs.commands.delete_bookshelf_command import DeleteBookshelfCommand
from library_api.modules.bookshelfs.commands.edit_bookshelf_info import EditBookshelfInfoCommand
from library_api.modules.bookshelfs.commands.new_bookshelf_command import NewBookshelfCommand


bookshelfs_blueprint = Blueprint('bookshelfs', __name__, url_prefix='/bookshelfs')


@bookshelfs_blueprint.route('/', methods=['POST'])
@jwt_required()
def add_bookshelf():
    current_user_id = get_jwt_identity()
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    request_data = request.json

    bookshelf = {
                'name': request_data.get('name'),
                'user_id': current_user_id,
            }


    try:
        bookshelf_entity = Bookshelf(**bookshelf)
        bookshelf_id = NewBookshelfCommand().create(bookshelf_entity)

        return jsonify(bookshelf_id), HTTPStatus.CREATED

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST

@bookshelfs_blueprint.route('/edit', methods=['POST'])
@jwt_required()
def edit_bookshelf_information():
    current_user_id = get_jwt_identity()
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    request_data = request.json

    try:
        for (field_name, field_value) in request_data.items():
            if field_name in Bookshelf.__dict__.keys():
                EditBookshelfInfoCommand().by_main_field(
                    bookshelf_id=request_data.get('bookshelf_id'),
                    field_name=field_name,
                    field_value=field_value)

        return jsonify(request_data.get('bookshelf_id')), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@bookshelfs_blueprint.route('/<int:bookshelf_id>', methods=['DELETE'])
@jwt_required()
def delete_bookshelf(bookshelf_id):
    current_user_id = get_jwt_identity()
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    try:
        DeleteBookshelfCommand().by_id(bookshelf_id)
        return jsonify(bookshelf_id), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST