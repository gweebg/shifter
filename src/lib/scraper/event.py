import re
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Location:
    """
    This class represents the location of an event.
    :param building: Building where the event is taking place.
    :type building: str
    :param campus: Campus where the event is taking place.
    :type campus: str
    :param room: Room where the event is taking place.
    :type room: str
    """
    building: str
    campus: str
    room: str

    @classmethod
    def from_string(cls, string: str) -> "Location":
        """
        Class method that builds a Location from a given string.
        :param string: Given string to be parsed into a Location object.
        :type string: str
        :return: Location object from the string.
        :rtype: Location
        """
        campus, building, room = tuple(string.replace(" ", "").split("-"))
        return cls(building=building.replace("Edificio", "CP"), campus=campus, room=room)

    def __str__(self) -> str:
        """
        String representation of the class.
        """
        return f"{self.campus} - {self.building} {self.room}"


@dataclass(frozen=True)
class ScheduleBody:
    """
    This class represents the body of an event.
    :param name: Event name.
    :type name: str
    :param location: Location object that represents where the event is taking place.
    :type location: Location
    :param shift: Shift for the event.
    :type shift: str
    """
    name: str
    location: Location
    shift: str

    @classmethod
    def from_string(cls, body: str) -> "ScheduleBody":
        """
        Class method that builds a ScheduleBody from a given string.
        :param body: Given string to be parsed into a ScheduleBody object.
        :type body: str
        :return: ScheduleBody object from the string.
        :rtype: ScheduleBody
        """
        matches = re.match(r"(.*)\[(.*)](.*)", body.replace("\n", ""))
        course_name, location, shift = matches.groups()

        location_obj: Location = Location.from_string(location)

        return cls(name=course_name.strip().lower(), location=location_obj, shift=shift.strip())

    def __str__(self):
        """
        String representation of the class.
        """
        return f"{self.name.title()}\n{self.location} - {self.shift}"


@dataclass(frozen=True)
class ScheduleEvent:
    """
    This class represents an event.
    :param body: Event details.
    :type body: ScheduleBody
    :param starts_at: Starting that of the event.
    :type starts_at: datetime
    :param duration: Duration of the event.
    :type duration: datetime
    :param weekday: Weekday of the event.
    :type weekday: str
    """
    body: ScheduleBody
    starts_at: datetime
    duration: datetime
    weekday: str

    @classmethod
    def build(cls, body: str, starts_at: datetime, duration: datetime, weekday: str) -> "ScheduleEvent":
        """
        Given a string and some details (duration, starting time, weekday), this method builds an event.
        :param body: Event details as string.
        :type body: str
        :param starts_at: Starting that of the event.
        :type starts_at: datetime
        :param duration: Duration of the event.
        :type duration: datetime
        :param weekday: Weekday of the event.
        :type weekday: str
        :return: ScheduleEvent object representing the event.
        :rtype: ScheduleEvent
        """
        return cls(
            body=ScheduleBody.from_string(body),
            starts_at=starts_at,
            duration=duration,
            weekday=weekday
        )

    def __str__(self):
        """
        String representation of the class.
        """
        return f"{self.body}\n{self.starts_at}\n{self.duration}\n"
