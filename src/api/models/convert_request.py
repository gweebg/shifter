from enum import Enum
from functools import cached_property

from pydantic import BaseModel, Field

from src.api.models.schedule_request import ScheduleRequest


class Format(str, Enum):
    XSLX = 'xlsx'
    ICS = 'ics'
    JSON = 'json'


class ConvertRequest(BaseModel):
    """
    This is a model class that represents the body of a POST request to '/schedules/'.

    :param body: The name of the requested course.
    :type body: str
    :param shifts: The semester of the requested course.
    :type shifts: int
    :param fmt: The year/years to fetch.
    :type fmt: int
    """

    body: ScheduleRequest
    shifts: dict[int, dict[str, list[str]]]
    fmt: Format = Format.JSON
