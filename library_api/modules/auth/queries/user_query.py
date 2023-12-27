from library_api.domain import User
from library_api.domain.data_access_layer.session import session


class GetUser:
    def __init__(self):
        pass


    @staticmethod
    def by_id(
        id: int,
        ):

        current_session = session()
        try:
            user: User = current_session \
                .query(User) \
                .filter(User.id == id) \
                .one_or_none()
            return user
        finally:
            current_session.close()
            
    @staticmethod
    def by_username(
        username: str,
        ):
        current_session = session()
        try:
            user: User = current_session \
                .query(User) \
                .filter(User.login == username) \
                .one_or_none()
            return user
        finally:
            current_session.close()
