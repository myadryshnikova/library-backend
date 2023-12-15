from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from library_api.domain.data_access_layer.engine import add_engine_pidguard, app_db_engine


add_engine_pidguard(app_db_engine)

db = SQLAlchemy(metadata=MetaData())
migrate = Migrate()
