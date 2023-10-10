from .service import Service
from app.models.relation_model import RelationModel


class RelationService(Service):

    def create_relation(self, relation: RelationModel):
        query = """
        CREATE (r:Relation {start_work_id: $start_work_id, end_work_id: $end_work_id,
        link_type: $link_type, relation_type: $relation_type, offset: $offset})
        """
        self.session.run(
            query,
            start_work_id=relation.start_work_id,
            end_work_id=relation.end_work_id,
            link_type=relation.link_type,
            relation_type=relation.relation_type,
            offset=relation.offset
        )