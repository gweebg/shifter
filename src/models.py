from pydantic import BaseModel


class ScheduleRequest(BaseModel):
    course_name: str
    year: int
    week_date: str
    file_name: str | None
    shifts: dict


class JsonRequest(BaseModel):
    course_name: str
    year: int
    week_date: str
    shifts: dict | None
