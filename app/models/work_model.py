from typing import Optional
from datetime import datetime


class WorkModel:
    def __init__(
            self,
            work_id: int,
            work_name: str,
            calculation_type: str,
            start_date: datetime.date,
            group: str,
            duration_hours: Optional[int] = None,
            duration_working_days: Optional[int] = None,
            duration_calendar_days: Optional[int] = None,
            subgroup: Optional[str] = None,
    ):
        self.work_id = work_id
        self.work_name = work_name
        self.calculation_type = calculation_type
        self.duration_hours = duration_hours
        self.duration_working_days = duration_working_days
        self.duration_calendar_days = duration_calendar_days
        self.start_date = start_date
        self.end_date: Optional[datetime.date] = None
        self.subgroup = subgroup
        self.group = group

    def __repr__(self):
        return f"""
            Work(Id: {self.work_id}, 
            Name: {self.work_name})
        """