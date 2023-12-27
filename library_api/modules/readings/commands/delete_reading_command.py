from library_api.domain.data_access_layer.session import session
from library_api.domain.reading import Reading
from datetime import datetime

class DeleteReadingCommand:
    def __init__(self):
        pass

    def by_id(
            self,
            reading_id: int, 
        ) -> int:
        with session() as current_session: 
            reading = current_session \
                .query(Reading) \
                .filter(Reading.id == reading_id) \
                .one_or_none()

            reading.deleted_at = datetime.utcnow()
            current_session.commit()