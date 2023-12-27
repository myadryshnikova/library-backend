from library_api.domain.citation import Citation
from library_api.domain.data_access_layer.session import session

class GetCitationQuery:
    def __init__(self):
        pass

    @staticmethod
    def by_book_id(book_id: int):
        current_session = session()
        try:
            return current_session \
                .query(Citation) \
                .filter(Citation.book_id == book_id) \
                .filter(Citation.deleted_at.is_(None)) \
                .all()

        finally:
            current_session.close()