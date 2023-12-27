from library_api.domain.data_access_layer.session import session
from library_api.domain.citation import Citation
from datetime import datetime

class DeleteCitationCommand:
    def __init__(self):
        pass

    def by_id(
            self,
            citation_id: int, 
        ) -> int:
        with session() as current_session: 
            citation = current_session \
                .query(Citation) \
                .filter(Citation.id == citation_id) \
                .one_or_none()

            citation.deleted_at = datetime.utcnow()
            current_session.commit()