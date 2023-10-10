from .service import Service
from app.models.work_model import WorkModel

class WorkService(Service):

    def create_work(self, work: WorkModel):
        query = """
        CREATE (w:Work {work_id: $work_id, calculation_type: $calculation_type, 
        duration_hours: $duration_hours, duration_working_days: $duration_working_days,
        duration_calendar_days: $duration_calendar_days, start_date: $start_date, end_date: $end_date})
        """
        self.session.run(
            query,
            work_id=work.work_id, calculation_type=work.calculation_type,
            duration_hours=work.duration_hours, duration_working_days=work.duration_working_days,
            duration_calendar_days=work.duration_calendar_days, start_date=work.start_date, end_date=work.end_date
        )

    def update_subgroup_query(self, subgroup: str, current_date: str, end_date: str) -> None:
        # Обновление дат начала и окончания подгруппы 1.1 и группы 1
        # Предполагаем, что подгруппа 1.1 и группа 1 уже существуют в базе данных и имеют свои id
        # Обновляем даты начала и окончания подгруппы 1.1
        query = f"MATCH (s:Subgroup {{id: {subgroup}}}) SET s.startDate = '{current_date}', s.endDate = '{end_date}'"
        self.session.run(query)

    def update_group_query(self, group: str, current_date: str, end_date: str) -> None:
        # Обновляем даты начала и окончания группы 1
        query = f"MATCH (g:Group {{id: {group}}}) SET g.startDate = '{current_date}', g.endDate = '{end_date}'"
        self.session.run(query)

    def update_work_query(self, work: id, current_date: str, end_date: str) -> None:
        query = f"MATCH (w:Work {{work_id: {work}}}) SET w.startDate = '{current_date}', w.endDate = '{end_date}'"
        self.session.run(query)