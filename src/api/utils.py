from enum import Enum


class SemesterDates(Enum):
    FIRST_SEMESTER_DATE: str = "01-11-2023"
    SECOND_SEMESTER_DATE: str = "01-03-2024"

    @classmethod
    def from_key(cls, key: int) -> "SemesterDates":
        return [date for date in SemesterDates][key - 1]


