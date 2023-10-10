from neo4j import Driver


class Service:
    def __init__(self, session: Driver.session) -> None:
        '''Конструктор класса CalendarGraph принимает параметр session,
        представляющий собой активную сессию (соединение) с базой данных Neo4j.'''
        self.session = session