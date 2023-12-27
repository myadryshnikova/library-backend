from library_api.domain.data_access_layer.session import session
from library_api.domain.book import Book

class NewBookCommand:
    def __init__(self):
        pass

    def create(
        self,
        book_entity: Book,
        ):
        current_session = session()
        try:
            current_session.add(book_entity)
            current_session.commit()
            return book_entity.id
        finally:
            current_session.close()