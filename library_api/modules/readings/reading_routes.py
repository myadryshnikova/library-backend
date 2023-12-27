from http import HTTPStatus

from flask import Blueprint, jsonify, request
from library_api.domain.reading import Reading

from datetime import datetime

from library_api.modules.auth.queries.user_query import GetUser
from library_api.modules.citations.commands.new_citation_command import NewCitationCommand
from library_api.modules.readings.commands.delete_reading_command import DeleteReadingCommand
from library_api.modules.readings.commands.edit_reading_info import EditReadingInfoCommand
from library_api.modules.readings.commands.new_reading_command import NewReadingCommand


readings_blueprint = Blueprint('readings', __name__, url_prefix='/readings')


@readings_blueprint.route('/', methods=['POST'])
def add_reading():
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    request_data = request.json

    reading = {
                'grade': request_data.get('grade'),
                'impression': request_data.get('impression'),
                'start_date': datetime.strptime(str(request_data.get('start_date')), '%Y-%m-%d'),
                'end_date': datetime.strptime(str(request_data.get('end_date')), '%Y-%m-%d'),
                'book_id': request_data.get('book_id'),
            }

    try:
        reading_entity = Reading(**reading)
        reading_id = NewReadingCommand().create(reading_entity)

        return jsonify(reading_id), HTTPStatus.CREATED

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@readings_blueprint.route('/edit', methods=['POST'])
def edit_reading_information():
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    request_data = request.json

    try:
        for (field_name, field_value) in request_data.items():
            if field_name in Reading.__dict__.keys():
                EditReadingInfoCommand().by_main_field(
                    reading_id=request_data.get('reading_id'),
                    field_name=field_name,
                    field_value=field_value)

        return jsonify(request_data.get('reading_id')), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@readings_blueprint.route('/<int:reading_id>', methods=['DELETE'])
def delete_reading(reading_id):
    current_user_id = 1
    user = GetUser().by_id(current_user_id)
    if not user:
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    try:
        DeleteReadingCommand().by_id(reading_id)
        return jsonify(reading_id), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST