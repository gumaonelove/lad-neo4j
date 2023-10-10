from .service import Service

from datetime import datetime, timedelta


class CalendarService(Service):
    '''Класс CalendarGraph служит для работы с графом календаря в базе данных Neo4j.
    Он содержит логику для добавления  связей (ребер) между узлами (днями) в графе,
    представляя таким образом рабочие дни и их отношения. '''

    def _check_if_date_exists(self, date: str) -> bool:
        '''Проверка, существует ли уже узел с такой датой в графе'''
        query = "MATCH (c:Calendar {date: $date}) RETURN count(c) as count"
        result = self.session.run(query, date=date).single()
        return result['count'] > 0

    def _create_relationships(self, date1: str, date2: str, relationship_type: str) -> None:
        query = """
        MATCH (c1:Calendar {date: $date1}), (c2:Calendar {date: $date2})
        CREATE (c1)-[:%s]->(c2)
        """ % relationship_type
        self.session.run(query, date1=date1, date2=date2)

    def _create_calendar_node(self, date: str, is_working_day: bool) -> None:
        '''Метод create_calendar создает календарь в базе данных Neo4j.'''
        # Создание календаря на основе производственного календаря текущего года
        # Здесь можно реализовать логику создания календаря, например, добавление узлов для каждого рабочего и
        # нерабочего дня в текущем году
        # Пример:
        query = "CREATE (c:Calendar {date: $date, is_working_day: $is_working_day})"
        self.session.run(query, date=date, is_working_day=is_working_day)

    def create_calendar(self, start_date: datetime.date, end_date: datetime.date) -> None:
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')

            if self._check_if_date_exists(date_str):
                current_date += timedelta(days=1)
                continue

            is_working_day = current_date.weekday() not in [5, 6]  # Понедельник (0) до пятницы (4) - рабочие дни

            self._create_calendar_node(date_str, is_working_day)

            # Создаем связи между подряд идущими календарными днями
            if current_date > start_date:
                self._create_relationships(
                    date1=(current_date - timedelta(days=1)).strftime('%Y-%m-%d'),
                    date2=date_str,
                    relationship_type='NEXT_DAY'
                )

            # Создаем связи между подряд идущими рабочими днями
            if is_working_day and current_date > start_date:
                self._create_relationships(
                    date1=(current_date - timedelta(days=1)).strftime('%Y-%m-%d'),
                    date2=date_str,
                    relationship_type='NEXT_WORKING_DAY'
                )

            current_date += timedelta(days=1)

        print('Календарь успешно заполнен днями')