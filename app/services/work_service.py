from .service import Service
from .calendar_service import CalendarService
from app.models.work_model import WorkModel
from datetime import timedelta


class WorkService(Service):

    def _check_if_work_exists(self, w: WorkModel) -> bool:
        query = "MATCH (w:Work {work_id: $work_id}) RETURN count(w) as count"
        result = self.session.run(query, work_id=w.work_id).single()
        return result['count'] > 0

    @staticmethod
    def _calculate_end_date(w: WorkModel, calendar_service: CalendarService):
        current_date = w.start_date
        remaining_days = w.duration_working_days if w.calculation_type == 'WorkingDays' else w.duration_calendar_days
        duration_days = 0
        working_days = 0

        while remaining_days > 0:
            if calendar_service.is_working_day(current_date):
                working_days += 1
                if w.calculation_type == 'WorkingDays':
                    remaining_days -= 1

            if w.calculation_type == 'CalendarDays':
                remaining_days -= 1

            current_date += timedelta(days=1)
            duration_days += 1

        current_date -= timedelta(days=1)
        return current_date, duration_days, working_days

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
            end_date, duration_days, working_days = self._calculate_end_date(work, calendar_service)
            work.end_date = end_date
            work.duration_calendar_days = duration_days
            work.duration_working_days = working_days
            work.duration_hours = work.duration_working_days * 8  # TODO Нужно добавить функционал указывать скольки часовой рабочий день
            print(f'Дата окончания {work.work_name}: {end_date}, {duration_days} календарных дней, {working_days} рабочих')

            self.session.run(
                query,
                work_id=work.work_id, calculation_type=work.calculation_type,
                duration_hours=work.duration_hours, duration_working_days=work.duration_working_days,
                duration_calendar_days=work.duration_calendar_days, start_date=work.start_date, end_date=work.end_date,
                group=work.group, subgroup=work.subgroup
            )
            print(f'Информация о работе {work.work_name} записана в базу')

            self._update_subgroup_query(work)
            self._update_group_query(work)
            self._update_work_query(work)
            print(f'Работа {work.work_name} успешно создана')
        else:
            print(f'Работа {work.work_name} уже существует')