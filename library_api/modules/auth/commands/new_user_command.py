from library_api.domain.data_access_layer.session import session
from library_api.domain.user import User


class NewUserCommand:
    def __init__(self):
        pass

    def add_user(
        self,
        user_entity: User,
        ):
        current_session = session()
        try:
            current_session.add(user_entity)
            current_session.commit()
            return user_entity.id
        finally:
            current_session.close()