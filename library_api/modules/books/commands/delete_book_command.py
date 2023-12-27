from library_api.domain.data_access_layer.session import session
from library_api.domain.book import Book
from datetime import datetime

class DeleteBookCommand:
    def __init__(self):
        pass

    def by_id(
            self,
            book_id: int, 
        ) -> int:
        with session() as current_session: 
            book = current_session \
                .query(Book) \
                .filter(Book.id == book_id) \
                .one_or_none()

            book.deleted_at = datetime.utcnow()
            current_session.commit()