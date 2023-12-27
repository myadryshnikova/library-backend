from library_api.domain.data_access_layer.session import session
from library_api.domain.citation import Citation

class EditCitationInfoCommand:
    def __init__(self):
        pass

    def by_main_field(
            self,
            citation_id: int, 
            field_name: str,
            field_value: str
        ) -> int:
        with session() as current_session: 
            citation = current_session \
                .query(Citation) \
                .filter(Citation.id == citation_id) \
                .one_or_none()

            setattr(citation, field_name, field_value)
            current_session.commit()

