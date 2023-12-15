from sqlalchemy.orm import sessionmaker
from library_api.domain.data_access_layer.engine import app_db_engine


def session():
    session_factory = sessionmaker(bind=app_db_engine, autoflush=False, autocommit=False)
    return session_factory()
