from library_api.domain.data_access_layer.session import session
from library_api.domain.bookshelf import Bookshelf

class EditBookshelfInfoCommand:
    def __init__(self):
        pass

    def by_main_field(
            self,
            bookshelf_id: int, 
            field_name: str,
            field_value: str
        ) -> int:
        with session() as current_session: 
            bookshelf = current_session \
                .query(Bookshelf) \
                .filter(Bookshelf.id == bookshelf_id) \
                .one_or_none()

            setattr(bookshelf, field_name, field_value)
            current_session.commit()

