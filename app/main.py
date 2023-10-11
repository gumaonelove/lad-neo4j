from datetime import datetime

from config import uri, user, password
from models.relation_model import RelationModel
from models.work_model import WorkModel
from neo4j_connector import Neo4jConnection
from services.calendar_service import CalendarService
from services.group_service import GroupService
from services.relation_service import RelationService
from services.work_service import WorkService

if __name__ == '__main__':
    # Пример использования
    connection = Neo4jConnection(uri, user, password)

    with connection.connect().session() as session:
        calendar_service = CalendarService(session)
        group_service = GroupService(session)
        work_service = WorkService(session)
        relation_service = RelationService(session)

        # Задание 1
        # В системе необходимо создать календарь, с узлами, которые содержат информацию о дате и о том,
        # является ли этот день рабочим. Используем производственный календарь текущего года.
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        calendar_service.create_calendar(start_date, end_date)

        # Задание 2
        # Необходимо создать группу “Группа 1” и сохранить ее в БД в виде узла графа (используем python и cypher).
        group_service.create_group(name="Группа 1")

        # Задание 3
        # Необходимо создать подгруппу “Подгруппа 1.1” и
        # сохранить ее в БД в виде узла графа с указанием связи с группой 1.
        group_service.create_subgroup(parent_group="Группа 1", subgroup_name="Подгруппа 1.1")

        # Задание 4
        # Необходимо создать работу “Работа 1.1.1”, которая начинается 1.08.23, заканчивается 10.08.23
        # и имеет длительность 8 рабочих дней. в виде узла графа с указанием связи с подгруппой 1.1.
        # После создания работы сроки начала и завершения группы и подгруппы должны пересчитаться и
        # соответствовать работе.
        work_1_1_1 = WorkModel(
            work_id=1,
            work_name='Работа 1.1.1',
            calculation_type="WorkingDays",
            duration_working_days=8,
            start_date="2023-08-01",
            group='1',
            subgroup='1.1'
        )
        work_service.create_work(work_1_1_1, calendar_service)

        # Задание 5
        # Необходимо создать работу “Работа 1.1.2”, которая начинается 5.08.23, заканчивается 14.08.23 и
        # имеет длительность 10 календарных дней. в виде узла графа с указанием связи с подгруппой 1.1.
        # После создания работы сроки начала и завершения группы и подгруппы должны пересчитаться и
        # стать с 01.08.23 по 14.08.23. Расчитать для группы длительность в календарных и рабочих днях
        work_1_1_2 = WorkModel(
            work_id=2,
            work_name='Работа 1.1.2',
            calculation_type="CalendarDays",
            duration_calendar_days=10,
            start_date="2023-08-05",
            group='1',
            subgroup='1.1'
        )

        # Задание 6
        # Необходимо создать работу 1.2, входящую в группу 1, но не в подгруппу 1.1
        # Указать ей длительность 3 рабочих дня.
        # Создать связи от работ 1.1.1 и 1.1.2 типа Окончание-Начало, у связи от работы 1.1.2 будет смещение старта
        # на 5 календарных дней. После создания работы ее даты начала и завершения должны пересчитаться,
        # на 20.08.23 и 24.08.23 соответственно. сроки начала и завершения группы 1 должны пересчитаться и
        # стать с 01.08.23 по 24.08.23. У группы 1.1. не измениться. Рассчитать для группы 1 длительность в календарных
        # и рабочих днях
        work_1_2 = WorkModel(
            work_id=3,
            work_name='Работа 1.2',
            calculation_type="WorkingDays",
            duration_working_days=3,
            start_date='20.08.23',
            group='1',
        )
        work_service.create_work(work_1_2, calendar_service)  # Создание работы 1.2 в базе данных
        # Создание связи "Окончание-Начало" от работы 1.1.1 к работе 1.2
        relation_1_1_1_to_1_2 = RelationModel(
            start_work_id=1,
            end_work_id=3,
            link_type="outgoing",
            relation_type="EndToStart",
            offset=0
        )  # Нет смещения

        # Создание связи "Окончание-Начало" от работы 1.1.2 к работе 1.2 со смещением в 5 календарных дней
        relation_1_1_2_to_1_2 = RelationModel(
            start_work_id=2,
            end_work_id=3,
            link_type="outgoing",
            relation_type="EndToStart",
            offset=5
        )
        # Создание связей в базе данных
        relation_service.create_relation(relation_1_1_1_to_1_2)
        relation_service.create_relation(relation_1_1_2_to_1_2)

        print("Выполнение программы завершено")