from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from library_api.domain.book import Book


from library_api.modules.auth.queries.user_query import GetUser
from library_api.modules.books.commands.delete_book_command import DeleteBookCommand
from library_api.modules.books.commands.edit_book_info import EditBookInfoCommand
from library_api.modules.books.commands.new_book_command import NewBookCommand
from library_api.modules.books.queries.get_book_query import GetBookQuery


books_blueprint = Blueprint('books', __name__, url_prefix='/books')


@books_blueprint.route('/', methods=['POST'])
@jwt_required()
def add_book():
    current_user_id = get_jwt_identity()
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    request_data = request.json

    book = {
                'name': request_data.get('name'),
                'author': request_data.get('author'),
                'user_id': current_user_id,
                'bookshelf_id': request_data.get('bookshelf_id'),
                'description': request_data.get('description'),
            }


    try:
        book_entity = Book(**book)
        book_id = NewBookCommand().create(book_entity)

        return jsonify(book_id), HTTPStatus.CREATED

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@books_blueprint.route('/edit', methods=['POST'])
@jwt_required()
def edit_book_information():
    current_user_id = get_jwt_identity()
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    request_data = request.json

    try:
        for (field_name, field_value) in request_data.items():
            if field_name in Book.__dict__.keys():
                EditBookInfoCommand().by_main_field(
                    book_id=request_data.get('book_id'),
                    field_name=field_name,
                    field_value=field_value)

        return jsonify(request_data.get('book_id')), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@books_blueprint.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    current_user_id = get_jwt_identity()
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    try:
        DeleteBookCommand().by_id(book_id)
        return jsonify(book_id), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST