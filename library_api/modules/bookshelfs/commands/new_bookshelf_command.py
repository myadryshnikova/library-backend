from library_api.domain.data_access_layer.session import session
from library_api.domain.bookshelf import Bookshelf

class NewBookshelfCommand:
    def __init__(self):
        pass

    def create(
        self,
        bookshelf_entity: Bookshelf,
        ):
        current_session = session()
        try:
            current_session.add(bookshelf_entity)
            current_session.commit()
            return bookshelf_entity.id
        finally:
            current_session.close()