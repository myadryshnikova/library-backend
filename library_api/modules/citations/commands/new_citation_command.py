from library_api.domain.data_access_layer.session import session
from library_api.domain.citation import Citation

class NewCitationCommand:
    def __init__(self):
        pass

    def create(
        self,
        citation_entity: Citation,
        ):
        current_session = session()
        try:
            current_session.add(citation_entity)
            current_session.commit()
            return citation_entity.id
        finally:
            current_session.close()