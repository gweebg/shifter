from dataclasses import asdict, dataclass
from datetime import time, timedelta
from typing import Optional

from src.lib.scraper.event import ScheduleEvent


class Schedule:
    """
    This class represents a schedule composed of an amount of weekdays and their respective events.
    """

    __slots__ = (
        'weekdays',
        'schedule'
    )

    def __init__(self, weekdays: list[str]) -> None:
        """
        Schedule class constructor.
        :param weekdays: List of weekdays from on to build the schedule.
        :type weekdays list[str]:
        """

        self.weekdays: list[str] = weekdays
        self.schedule: dict = {weekday: [] for weekday in weekdays}
        """
        This variable represents the schedule itself, its keys represent the weekday and the values a list
        of ScheduleEvent. 
        """

    def add_event(self, event: ScheduleEvent) -> None:
        """
        Add an event to the schedule.
        :param event: Event to add on the schedule.
        :type event: ScheduleEvent
        """
        self.schedule[event.weekday].append(event)

    def get_events_from_weekday(self, weekday: str) -> list[ScheduleEvent]:
        """
        Obtain every event for a given weekday.
        :param weekday: Weekday to filter the events from.
        :type weekday: str
        :return: List of ScheduleEvent containing the requested events.
        :rtype: list[ScheduleEvent]
        """
        return self.schedule[weekday]

    @staticmethod
    def _calculate_final_time(when: time, duration: time) -> time:
        """
        Static private method that calculates the time the event ends at.
        :param when: Time value that represents when the event starts.
        :type when: time
        :param duration: Value that represents the duration of the event.
        :type duration: time
        :return: Returns the time at which the event ends.
        :rtype: time
        """

        when_delta: timedelta = timedelta(hours=when.hour, minutes=when.minute)
        duration_delta: timedelta = timedelta(hours=duration.hour, minutes=duration.minute)

        result_delta: timedelta = when_delta + duration_delta
        return time(
            hour=result_delta.seconds // 3600,
            minute=(result_delta.seconds // 60) % 60
        )

    def get_starting_and_ending_time(self) -> tuple[time, time]:
        """
        Method that calculates the earliest event and the latest event times.
        :return: A tuple containing the starting and ending times.
        :rtype: tuple[time, time]

        TODO: Refactor for better and clear code.
        """

        starting_time: Optional[time] = None
        ending_time: Optional[time] = None

        events: list[ScheduleEvent]
        for _, events in self.schedule.items():

            event: ScheduleEvent
            for event in events:

                event_delta: timedelta = timedelta(hours=event.starts_at.hour, minutes=event.starts_at.minute)

                if starting_time and ending_time:
                    starting_delta: timedelta = timedelta(hours=starting_time.hour, minutes=starting_time.minute)
                    ending_delta: timedelta = timedelta(hours=ending_time.hour, minutes=ending_time.minute)

                if starting_time is None:
                    starting_time = event.starts_at.time()

                elif event_delta < starting_delta:
                    starting_time = event.starts_at.time()

                if ending_time is None:
                    ending_time = self._calculate_final_time(event.starts_at.time(), event.duration.time())

                else:

                    event_ending: time = self._calculate_final_time(event.starts_at.time(), event.duration.time())
                    event_ending_delta: timedelta = timedelta(hours=event_ending.hour, minutes=event_ending.minute)

                    if event_ending_delta > ending_delta:
                        ending_time = event_ending

        return starting_time, ending_time

    def get_events(self) -> list[ScheduleEvent]:
        """
        Retrieves the every event from de schedule.
        :return: List of ScheduleEvent with every event on the schedule.
        :rtype: list[ScheduleEvent]
        """

        all_events: list[ScheduleEvent] = []

        events: list[ScheduleEvent]
        for _, events in self.schedule.items():

            event: ScheduleEvent
            for event in events:
                all_events.append(event)

        return all_events

    def get_course_names(self) -> list[str]:
        """
        Gets the name of every event on the schedule.
        :return: List of the names.
        :rtype: list[str]
        """

        course_names: list[str] = []

        events: list[ScheduleEvent]
        for _, events in self.schedule.items():

            event: ScheduleEvent
            for event in events:

                if event.body.name not in course_names:
                    course_names.append(event.body.name.title())

        return course_names

    def get_shifts_from_courses(self) -> dict[str, list[str]]:
        """
        This method returns the corresponding shifts to each event in the form of a dictionary.
        :return: Dictionary containing as a key the event name and the value a list with the shifts as string.
        :rtype: dict[str, list[str]]
        """
        shifts: dict[str, list[str]] = {}

        weekday: str
        for weekday in self.schedule:

            event: ScheduleEvent
            for event in self.schedule[weekday]:

                if event.body.name not in shifts:
                    shifts[event.body.name] = []

                shifts[event.body.name].append(event.body.shift)

        return shifts

    def filter(self, shifts: dict[str, list[str]]) -> "Schedule":
        """
        Method that filters the schedule by the given shifts 'map'.

        :param shifts: Dictionary containing the event name as the keys and list of shifts as value.
        :return: A new Schedule object with the new schedule.
        :rtype: Schedule
        """

        shifts = {course.lower(): shifts[course] for course in shifts}  # Normalize course names to lower case
        result: Schedule = Schedule(self.weekdays)

        weekday: str
        for weekday in self.schedule:  # Iterate over weekdays

            event: ScheduleEvent
            for event in self.schedule[weekday]:  # Iterate over events in the weekday

                if event.body.name in shifts and event.body.shift in shifts[event.body.name]:  # Match course/shift
                    result.add_event(event)

        return result

    def get_as_dict(self) -> dict:
        """
        :return: A dictionary representation of the schedule.
        :rtype: dict
        """

        as_dict: dict = dict.fromkeys(self.weekdays, list())

        weekday: str
        for weekday in self.schedule:

            event: ScheduleEvent
            for event in self.schedule[weekday]:
                as_dict[weekday].append(asdict(event))

        return as_dict

    @staticmethod
    def _check_if_collides(main_event: ScheduleEvent, test_event: ScheduleEvent) -> bool:
        """
        Static private method that checks whether two events overlap. Two events overlap if:
            1. The events start at the same time.
            2. One of the events starts in the middle of the other.
        :param main_event: The main event to compare with.
        :type main_event: ScheduleEvent
        :param test_event: The test event to compare against the main event.
        :type test_event: ScheduleEvent
        :return: True if they overlap, False otherwise.
        :rtype: bool
        """

        if main_event.starts_at.time() == test_event.starts_at.time():
            return True

        main_event_delta: timedelta = timedelta(hours=main_event.starts_at.hour, minutes=main_event.starts_at.minute)
        duration_delta: timedelta = timedelta(hours=main_event.duration.hour, minutes=main_event.duration.minute)

        ending_timedelta: timedelta = main_event_delta + duration_delta
        main_event_ends: time = time(
            hour=ending_timedelta.seconds // 3600,
            minute=(ending_timedelta.seconds // 60) % 60
        )

        return main_event.starts_at.time() < test_event.starts_at.time() < main_event_ends

    def get_collisions(self, weekday: str) -> list[time | tuple[time, time]]:
        """
        For a given weekday, this method computes at which times event overlapping occurs.

        :param weekday: Weekday to search on.
        :type weekday: str
        :return: List containing either the time or a tuple of times (that represent midway overlaps).
        :rtype: list[time | tuple[time, ...]]
        """

        previous_event: Optional[ScheduleEvent] = None
        collisions: list[time | tuple[time, ...]] = []

        event: ScheduleEvent
        for event in self.schedule[weekday]:

            if previous_event and self._check_if_collides(previous_event, event):

                # In the case of the overlapping events starting time doesn't match, we aggregate them in a tuple.
                if previous_event.starts_at.time() != event.starts_at.time():
                    collisions.append((previous_event.starts_at.time(), event.starts_at.time()))

                else:  # Else we just append the hour.
                    collisions.append(event.starts_at.time())

            previous_event = event

        return collisions


class ScheduleGroup:

    def __init__(self, course_name: str) -> None:

        self.course_name = course_name
        self.years: dict[int, Schedule] = {}

    @property
    def shifts(self) -> dict[int, dict[str, list[str]]]:
        return {year: self.years[year].get_shifts_from_courses() for year in self.years}

    def add_event_to_year(self, year: int, event: Schedule) -> None:
        self.years[year] = event

    def as_dict(self) -> dict:
        return {year: self.years[year].get_as_dict() for year in self.years}





