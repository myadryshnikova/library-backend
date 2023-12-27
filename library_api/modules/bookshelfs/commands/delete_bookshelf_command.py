from library_api.domain.data_access_layer.session import session
from library_api.domain.bookshelf import Bookshelf
from datetime import datetime

class DeleteBookshelfCommand:
    def __init__(self):
        pass

    def by_id(
            self,
            bookshelf_id: int, 
        ) -> int:
        with session() as current_session: 
            bookshelf = current_session \
                .query(Bookshelf) \
                .filter(Bookshelf.id == bookshelf_id) \
                .one_or_none()

            bookshelf.deleted_at = datetime.utcnow()
            current_session.commit()