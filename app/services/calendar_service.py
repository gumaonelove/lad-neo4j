from .service import Service

from datetime import datetime, timedelta


class CalendarService(Service):
    '''
    Класс CalendarGraph служит для работы с графом календаря в базе данных Neo4j.
    Он содержит логику для добавления  связей (ребер) между узлами (днями) в графе,
    представляя таким образом рабочие дни и их отношения
    '''

    def _check_if_date_exists(self, date: datetime.date) -> bool:
        '''Проверка, существует ли уже узел с такой датой в графе'''
        query = "MATCH (c:Calendar {date: $date}) RETURN count(c) as count"
        result = self.session.run(query, date=date.strftime("%Y-%m-%d")).single()
        return result['count'] > 0

    def _create_relationships(self, date1: datetime.date, date2: datetime.date, relationship_type: str) -> None:
        '''Создание связи между днями'''
        query = """
        MATCH (c1:Calendar {date: $date1}), (c2:Calendar {date: $date2})
        CREATE (c1)-[:%s]->(c2)
        """ % relationship_type
        self.session.run(query, date1=date1, date2=date2)

    def _create_calendar_node(self, date: datetime.date, is_working_day: bool) -> None:
        '''Метод create_calendar создает календарь в базе данных Neo4j.'''
        query = "CREATE (c:Calendar {date: $date, is_working_day: $is_working_day})"
        self.session.run(query, date=date.strftime("%Y-%m-%d"), is_working_day=is_working_day)

    def is_working_day(self, date: datetime.date):
        '''Проверка: является ли день рабочим'''
        query = "MATCH (c:Calendar {date: $date}) RETURN c.is_working_day as is_working_day"
        result = self.session.run(query,
                                  date=date.strftime("%Y-%m-%d"))  # TODO решить в каком формате хранить даты в базе
        record = result.single()
        if record is not None:
            return record['is_working_day']
        else:
            return False

    def create_calendar(self, start_date: datetime.date, end_date: datetime.date) -> None:
        '''Создание календаря с пометками'''
        current_date = start_date
        while current_date <= end_date:

            if self._check_if_date_exists(current_date):
                current_date += timedelta(days=1)
                print('Календарь уже существует')
                return  # TODO На этапе дебага, что бы скратить время запуска программы

            is_working_day = current_date.weekday() not in [5, 6]  # Понедельник (0) до пятницы (4) - рабочие дни

            self._create_calendar_node(current_date, is_working_day)

            # Создаем связи между подряд идущими календарными днями
            if current_date > start_date:
                self._create_relationships(
                    date1=(current_date - timedelta(days=1)),
                    date2=current_date,
                    relationship_type='NEXT_DAY'
                )

            # Создаем связи между подряд идущими рабочими днями
            if is_working_day and current_date > start_date:
                self._create_relationships(
                    date1=(current_date - timedelta(days=1)),
                    date2=current_date,
                    relationship_type='NEXT_WORKING_DAY'
                )

            current_date += timedelta(days=1)

        print('Календарь успешно заполнен')
