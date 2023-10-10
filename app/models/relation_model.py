class RelationModel:
    def __init__(self, start_work_id, end_work_id, link_type, relation_type, offset):
        self.start_work_id = start_work_id
        self.end_work_id = end_work_id
        self.link_type = link_type
        self.relation_type = relation_type
        self.offset = offset

    def __repr__(self):
        return f"Relation(StartWorkId: {self.start_work_id}, EndWorkId: {self.end_work_id}, " \
               f"LinkType: {self.link_type}, RelationType: {self.relation_type}, Offset: {self.offset})"