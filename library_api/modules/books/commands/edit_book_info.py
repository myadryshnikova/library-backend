from library_api.domain.data_access_layer.session import session
from library_api.modules.books.queries.get_book_query import GetBookQuery
from library_api.domain.book import Book

class EditBookInfoCommand:
    def __init__(self):
        pass

    def by_main_field(
            self,
            book_id: int, 
            field_name: str,
            field_value: str
        ) -> int:
        with session() as current_session: 
            book = current_session \
                .query(Book) \
                .filter(Book.id == book_id) \
                .one_or_none()

            setattr(book, field_name, field_value)
            current_session.commit()

