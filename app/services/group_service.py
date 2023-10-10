from .service import Service


class GroupService(Service):

    def _check_if_group_exists(self, name: str) -> bool:
        query = "MATCH (g:Group {name: $name}) RETURN count(g) as count"
        result = self.session.run(query, name=name).single()
        return result['count'] > 0

    def create_group(self, name: str) -> None:
        if not self._check_if_group_exists(name):
            query = "CREATE (g:Group {name: $name})"
            self.session.run(query, name=name)

    def create_subgroup(self, parent_group: str, subgroup_name: str) -> None:
        if (not self._check_if_group_exists(parent_group)
                and not self._check_if_group_exists(subgroup_name)):
            query = '''
            MATCH (g:Group {name: $parent_group})
            CREATE (g)-[:HAS_SUBGROUP]->(sg:Subgroup {name: $subgroup_name})
            '''
            self.session.run(query, parent_group=parent_group, subgroup_name=subgroup_name)