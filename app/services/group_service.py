from .service import Service


class GroupService(Service):

    def _check_if_subgroup_exists(self, subgroup_name: str) -> bool:
        query = "MATCH (sg:Subgroup {name: $subgroup_name}) RETURN count(sg) as count"
        result = self.session.run(query, subgroup_name=subgroup_name).single()
        return result['count'] > 0

    def _check_if_group_exists(self, name: str) -> bool:
        query = "MATCH (g:Group {name: $name}) RETURN count(g) as count"
        result = self.session.run(query, name=name).single()
        return result['count'] > 0

    def create_group(self, name: str) -> None:
        if not self._check_if_group_exists(name):
            query = "CREATE (g:Group {name: $name})"
            self.session.run(query, name=name)
            print(f'Группа {name} успешно создана')
        else:
            print(f'Группа {name} уже существует')

    def create_subgroup(self, parent_group: str, subgroup_name: str) -> None:
        if not self._check_if_subgroup_exists(subgroup_name):
            query = '''
            MATCH (g:Group {name: $parent_group})
            CREATE (g)-[:HAS_SUBGROUP]->(sg:Subgroup {name: $subgroup_name})
            '''
            self.session.run(query, parent_group=parent_group, subgroup_name=subgroup_name)
            print(f'Под-группа {subgroup_name} успешно создана')
        else:
            print(f'Под-группа {subgroup_name} уже существует')



