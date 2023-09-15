from functools import cached_property

from pydantic import BaseModel, Field

from src.api.utils import SemesterDates


class ScheduleRequest(BaseModel):
    """
    This is a model class that represents the body of a POST request to '/schedules/'.

    :param course_name: The name of the requested course.
    :type course_name: str
    :param course_semester: The semester of the requested course.
    :type course_semester: int
    :param course_years: The year/years to fetch.
    :type course_years: int
    """
    course_name: str = Field(min_length=10)
    course_semester: int = Field(ge=1, le=2)
    course_years: int = Field(ge=0, le=4)

    @property
    def course_date(self) -> str:
        """
        Class property representing the date to fetch based on the semester.
        :return: The date represented as a string (dd-mm-YYYY).
        :rtype: str
        """
        return SemesterDates.from_key(self.course_semester).value  # Date corresponding to the semester.

    @cached_property
    def cache_key(self) -> str:
        """
        Cached property representing the corresponding cache key.
        :return: The cache key.
        :rtype: str
        """
        return f"{self.course_name.lower().replace(' ', '')}_{self.course_years}_{self.course_semester}"
