from .service import Service
from app.models.work_model import WorkModel
from datetime import timedelta


class WorkService(Service):

    def _check_if_work_exists(self, w: WorkModel) -> bool:
        query = "MATCH (w:Work {work_id: $work_id}) RETURN count(w) as count"
        result = self.session.run(query, work_id=w.work_id).single()
        return result['count'] > 0

    @staticmethod
    def _calculate_end_date(start_date, working_days, calendar_service):
        current_date = start_date
        remaining_working_days = working_days
        duration_calendar_days = 0

        while remaining_working_days > 0:
            if calendar_service.is_working_day(current_date):
                remaining_working_days -= 1

            current_date += timedelta(days=1)
            duration_calendar_days += 1

        return current_date, duration_calendar_days

    def _update_subgroup_query(self, w: WorkModel) -> None:
        query = f"MATCH (s:Subgroup {{id: {w.subgroup}}}) SET s.startDate = '{w.start_date}', s.endDate = '{w.end_date}'"
        self.session.run(query)

    def _update_group_query(self, w: WorkModel) -> None:
        query = f"MATCH (g:Group {{id: {w.group}}}) SET g.startDate = '{w.start_date}', g.endDate = '{w.end_date}'"
        self.session.run(query)

    def _update_work_query(self, w: WorkModel) -> None:
        query = f"MATCH (w:Work {{work_id: {w.work_id}}}) SET w.startDate = '{w.start_date}', w.endDate = '{w.end_date}'"
        self.session.run(query)

    def create_work(self, work: WorkModel, calendar_service):
        query = """
        CREATE (w:Work {work_id: $work_id, calculation_type: $calculation_type, 
        duration_hours: $duration_hours, duration_working_days: $duration_working_days,
        duration_calendar_days: $duration_calendar_days, start_date: $start_date, end_date: $end_date,
        group: $group, subgroup: $subgroup
        })
        """
        if not self._check_if_work_exists(work):
            end_date, duration_calendar_days = self._calculate_end_date(
                work.start_date, work.duration_working_days, calendar_service)
            work.end_date = end_date
            work.duration_calendar_days=duration_calendar_days
            work.duration_hours = work.duration_working_days * 8 # TODO Нужно добавить функционал указывать скольки часовой рабочий день

            self.session.run(
                query,
                work_id=work.work_id, calculation_type=work.calculation_type,
                duration_hours=work.duration_hours, duration_working_days=work.duration_working_days,
                duration_calendar_days=work.duration_calendar_days, start_date=work.start_date, end_date=work.end_date,
                group=work.group, subgroup=work.subgroup
            )

            self._update_subgroup_query(work)
            self._update_group_query(work)
            self._update_work_query(work)