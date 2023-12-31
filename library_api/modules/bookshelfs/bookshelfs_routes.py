from http import HTTPStatus

from flask import Blueprint, jsonify, request
from library_api.domain.bookshelf import Bookshelf


from library_api.modules.auth.queries.user_query import GetUser
from library_api.modules.bookshelfs.commands.delete_bookshelf_command import DeleteBookshelfCommand
from library_api.modules.bookshelfs.commands.edit_bookshelf_info import EditBookshelfInfoCommand
from library_api.modules.bookshelfs.commands.new_bookshelf_command import NewBookshelfCommand
from library_api.modules.bookshelfs.queries.get_bookshelf_query import GetBookshelfQuery
from library_api.modules.books.queries.get_book_query import GetBookQuery


bookshelfs_blueprint = Blueprint('bookshelfs', __name__, url_prefix='/bookshelfs')


@bookshelfs_blueprint.route('/', methods=['POST'])
def add_bookshelf():
    current_user_id = 1
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
def edit_bookshelf_information():
    current_user_id = 1
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
def delete_bookshelf(bookshelf_id):
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    try:
        DeleteBookshelfCommand().by_id(bookshelf_id)
        return jsonify(bookshelf_id), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@bookshelfs_blueprint.route('/', methods=['GET'])
def get_all_bookshelfs():
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    try:
        bookshelfs = GetBookshelfQuery().by_user_id(current_user_id)

        bookshelfs_response = []
        for bookshelf in bookshelfs:
            bookshelfs_response.append(
                {
                    "bookshelfId": bookshelf.id,
                    "bookshelfName": bookshelf.name,
                    "bookCount": GetBookQuery().count_by_bookshef_id(bookshelf.id),
                }
            )

        return jsonify(bookshelfs_response), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@bookshelfs_blueprint.route('/<int:bookshelf_id>', methods=['GET'])
def get_books_on_bookshelf(bookshelf_id):
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    try:
        books = GetBookQuery().by_bookshelf_id(bookshelf_id)

        books_response = {
            "bookshelfName": GetBookshelfQuery().by_id(bookshelf_id).name,
            "books": [],
        }
        for book in books:
            books_response['books'].append(
                {
                    "bookId": book.id,
                    "bookName": book.name,
                    "bookAuthor": book.author,
                }
            )

        return jsonify(books_response), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST