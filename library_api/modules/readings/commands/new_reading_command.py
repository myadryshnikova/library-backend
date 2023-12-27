from library_api.domain.data_access_layer.session import session
from library_api.domain.reading import Reading

class NewReadingCommand:
    def __init__(self):
        pass

    def create(
        self,
        reading_entity: Reading,
        ):
        current_session = session()
        try:
            current_session.add(reading_entity)
            current_session.commit()
            return reading_entity.id
        finally:
            current_session.close()