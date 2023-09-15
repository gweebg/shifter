from pydantic import BaseModel, Field


class ScheduleResponse(BaseModel):
    """
    This is a model class that represents the response body of a response to '/schedules/'.

    :param course_name: The name of the requested course.
    :type course_name: str
    :param course_date: The date from which the schedule was fetched.
    :type course_date: str
    :param schedules: A dictionary that represents every event on the schedule. Uses weekdays as keys.
    :type schedules: dict[int, dict]
    :param shifts: A dictionary that represents what shifts each subject has.
    :type shifts: dict[int, dict[str, list[str]]]
    """

    course_name: str = Field(min_length=10)
    course_date: str

    schedules: dict[int, dict]
    shifts: dict[int, dict[str, list[str]]]
