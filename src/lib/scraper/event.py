import re
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Location:
    building: str
    campus: str
    room: str

    @classmethod
    def from_string(cls, string: str) -> "Location":
        campus, building, room = tuple(string.replace(" ", "").split("-"))
        return cls(building=building, campus=campus, room=room)

    def __str__(self):
        return f"{self.building} | {self.campus} | {self.room}"


@dataclass(frozen=True)
class ScheduleBody:
    name: str
    location: Location
    shift: str

    @classmethod
    def from_string(cls, body: str) -> "ScheduleBody":
        matches = re.match(r"(.*)\[(.*)](.*)", body.replace("\n", ""))
        course_name, location, shift = matches.groups()

        location_obj: Location = Location.from_string(location)

        return cls(name=course_name.strip().lower(), location=location_obj, shift=shift.strip())

    def __str__(self):
        return f"{self.name} | {self.location} | {self.shift}"


@dataclass(frozen=True)
class ScheduleEvent:
    body: ScheduleBody
    starts_at: datetime
    duration: datetime
    weekday: str

    @classmethod
    def build(cls, body: str, starts_at: datetime, duration: datetime, weekday: str) -> "ScheduleEvent":
        return cls(
            body=ScheduleBody.from_string(body),
            starts_at=starts_at,
            duration=duration,
            weekday=weekday
        )

    def __str__(self):
        return f"{self.body}\n{self.starts_at}\n{self.duration}\n"
