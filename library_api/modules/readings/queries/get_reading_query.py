from typing import List
from library_api.domain.reading import Reading
from library_api.domain.data_access_layer.session import session

class GetReadingQuery:
    def __init__(self):
        pass

    @staticmethod
    def by_book_id(book_id: int) -> List[Reading]:
        current_session = session()
        try:
            return current_session \
                .query(Reading) \
                .filter(Reading.book_id == book_id) \
                .filter(Reading.deleted_at.is_(None)) \
                .all()

        finally:
            current_session.close()