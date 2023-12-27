from library_api.domain.data_access_layer.session import session
from library_api.domain.reading import Reading

class EditReadingInfoCommand:
    def __init__(self):
        pass

    def by_main_field(
            self,
            reading_id: int, 
            field_name: str,
            field_value: str
        ) -> int:
        with session() as current_session: 
            reading = current_session \
                .query(Reading) \
                .filter(Reading.id == reading_id) \
                .one_or_none()

            setattr(reading, field_name, field_value)
            current_session.commit()

