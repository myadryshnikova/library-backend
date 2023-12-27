from http import HTTPStatus

from flask import Blueprint, jsonify, request
from library_api.domain.book import Book


from library_api.modules.auth.queries.user_query import GetUser
from library_api.modules.books.commands.delete_book_command import DeleteBookCommand
from library_api.modules.books.commands.edit_book_info import EditBookInfoCommand
from library_api.modules.books.commands.new_book_command import NewBookCommand
from library_api.modules.books.queries.get_book_query import GetBookQuery
from library_api.modules.bookshelfs.queries.get_bookshelf_query import GetBookshelfQuery
from library_api.modules.citations.queries.get_citation_query import GetCitationQuery
from library_api.modules.readings.queries.get_reading_query import GetReadingQuery


books_blueprint = Blueprint('books', __name__, url_prefix='/books')


@books_blueprint.route('/', methods=['POST'])
def add_book():
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    request_data = request.json

    book = {
        'user_id': current_user_id,
        'additional_fields': {}
    }

    for (field_name, field_value) in request_data.items():
        if field_name in Book.__dict__.keys():
                book[field_name] = field_value
        else:
            book['additional_fields'].update({field_name: field_value})


    try:
        book_entity = Book(**book)
        book_id = NewBookCommand().create(book_entity)

        return jsonify(book_id), HTTPStatus.CREATED

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@books_blueprint.route('/edit', methods=['POST'])
def edit_book_information():
    current_user_id = 1
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
def delete_book(book_id):
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    try:
        DeleteBookCommand().by_id(book_id)
        return jsonify(book_id), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@books_blueprint.route('/all', methods=['GET'])
def get_all_book():
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    try:
        books = GetBookQuery().by_user_id(current_user_id)

        books_response = []
        for book in books:
            books_response.append(
                {
                    "bookId": book.id,
                    "bookName": book.name,
                    "bookAuthor": book.author,
                }
            )

        return jsonify(books_response), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@books_blueprint.route('/<int:book_id>', methods=['GET'])
def get_book_info(book_id):
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    try:
        book = GetBookQuery().by_id(book_id)
        bookshelf = GetBookshelfQuery().by_id(book.bookshelf_id)

        books_response = {
            'bookId': book.id,
            'bookName': book.name,
            'bookAuthor': book.author,
            'bookshelfName': bookshelf.name if bookshelf else None,
            'description': book.description,
            'citations': [],
            'readings': [],

        }
        if book.additional_fields:
            books_response.update(book.additional_fields)

        citations = GetCitationQuery().by_book_id(book.id)
        for citation in citations:
            books_response['citations'].append(
                {
                    'citationId': citation.id,
                    'citationAuthor': citation.author,
                    'citationDescription': citation.citation_description,
                }
            )

        readings = GetReadingQuery().by_book_id(book.id)
        for reading in readings:
            books_response['readings'].append(
                {
                    'readingId': reading.id,
                    'readingGrade': reading.grade,
                    'readingImpression': reading.impression,
                    'readingStartDate': reading.start_date,
                    'readingEndDate': reading.end_date,
                }
            )

        return jsonify(books_response), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST
