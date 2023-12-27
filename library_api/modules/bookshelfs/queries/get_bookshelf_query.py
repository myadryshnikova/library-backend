from library_api.domain.data_access_layer.session import session
from library_api.domain.bookshelf import Bookshelf

class GetBookshelfQuery:
    def __init__(self):
        pass

    @staticmethod
    def by_id(bookshelf_id: int) -> Bookshelf:
        current_session = session()
        try:
            return current_session \
                .query(Bookshelf) \
                .filter(Bookshelf.id == bookshelf_id) \
                .one_or_none()

        finally:
            current_session.close()

    @staticmethod
    def by_user_id(user_id: int):
        current_session = session()
        try:
            return current_session \
                .query(Bookshelf) \
                .filter(Bookshelf.user_id == user_id) \
                .all()

        finally:
            current_session.close()



