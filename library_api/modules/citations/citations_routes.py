from http import HTTPStatus

from flask import Blueprint, jsonify, request
from library_api.domain.citation import Citation


from library_api.modules.auth.queries.user_query import GetUser
from library_api.modules.citations.commands.delete_citation_command import DeleteCitationCommand
from library_api.modules.citations.commands.edit_citation_info import EditCitationInfoCommand
from library_api.modules.citations.commands.new_citation_command import NewCitationCommand


citations_blueprint = Blueprint('citations', __name__, url_prefix='/citations')


@citations_blueprint.route('/', methods=['POST'])
def add_citation():
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    request_data = request.json

    citation = {
                'citation_description': request_data.get('citation_description'),
                'author': request_data.get('author'),
                'book_id': request_data.get('book_id'),
            }


    try:
        citation_entity = Citation(**citation)
        citation_id = NewCitationCommand().create(citation_entity)

        return jsonify(citation_id), HTTPStatus.CREATED

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@citations_blueprint.route('/edit', methods=['POST'])
def edit_citation_information():
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    request_data = request.json

    try:
        for (field_name, field_value) in request_data.items():
            if field_name in Citation.__dict__.keys():
                EditCitationInfoCommand().by_main_field(
                    citation_id=request_data.get('citation_id'),
                    field_name=field_name,
                    field_value=field_value)

        return jsonify(request_data.get('citation_id')), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@citations_blueprint.route('/<int:citation_id>', methods=['DELETE'])
def delete_bookshelf(citation_id):
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    try:
        DeleteCitationCommand().by_id(citation_id)
        return jsonify(citation_id), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST