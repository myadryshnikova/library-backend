from library_api.domain.data_access_layer.session import session
from library_api.domain.book import Book

class GetBookQuery:
    def __init__(self):
        pass

    @staticmethod
    def by_id(book_id: int):
        current_session = session()
        try:
            return current_session \
                .query(Book) \
                .filter(Book.id == book_id) \
                .one_or_none()

        finally:
            current_session.close()

    @staticmethod
    def by_user_id(user_id: int):
        current_session = session()
        try:
            return current_session \
                .query(Book) \
                .filter(Book.user_id == user_id) \
                .all()

        finally:
            current_session.close()

    @staticmethod
    def count_by_bookshef_id(bookshef_id:int):
        current_session = session()
        try:
            return current_session \
                .query(Book) \
                .filter(Book.bookshelf_id == bookshef_id) \
                .count()

        finally:
            current_session.close()


