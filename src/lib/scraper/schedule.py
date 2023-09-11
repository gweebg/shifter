from dataclasses import asdict
from datetime import datetime, time, timedelta
from typing import Optional

from src.lib.scraper.event import ScheduleEvent

"""
1. (Client) User inputs the course and date on the form.
2. (Server) Check cache for the course and date.
    2.1. If the cache hits, use the Schedule objects stored.
    2.2. If the cache misses, use the scraper to retrieve the Schedule objects.
3. (Server) Upon loading the schedule, send the user, shifts, course names and ScheduleEvent objects.
4. (Client) Chooses the shifts for each weekday and hits the download button.
5. (Server) Upon receiving the request, check cache for the Schedule objects and generate the excel/image (depending
   on user preferences).
6. (Client) File is downloaded.  
"""


class Schedule:

    def __init__(self, weekdays: list[str]) -> None:

        self.weekdays: list[str] = weekdays
        self.schedule: dict = {weekday: [] for weekday in weekdays}

    def add_event(self, event: ScheduleEvent) -> None:
        self.schedule[event.weekday].append(event)

    def get_events_from_weekday(self, weekday: str) -> list[ScheduleEvent]:
        return self.schedule[weekday]

    @staticmethod
    def _calculate_final_time(when: time, duration: time) -> time:

        when_delta: timedelta = timedelta(hours=when.hour, minutes=when.minute)
        duration_delta: timedelta = timedelta(hours=duration.hour, minutes=duration.minute)

        result_delta: timedelta = when_delta + duration_delta
        return time(
            hour=result_delta.seconds // 3600,
            minute=(result_delta.seconds // 60) % 60
        )

    def get_starting_and_ending_time(self) -> tuple[time, time]:

        # TODO | Refactor this trash code :)

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

        all_events: list[ScheduleEvent] = []

        events: list[ScheduleEvent]
        for _, events in self.schedule.items():

            event: ScheduleEvent
            for event in events:
                all_events.append(event)

        return all_events

    def get_course_names(self) -> list[str]:

        course_names: list[str] = []

        events: list[ScheduleEvent]
        for _, events in self.schedule.items():

            event: ScheduleEvent
            for event in events:

                if event.body.name not in course_names:
                    course_names.append(event.body.name.title())

        return course_names

    def get_shifts_from_courses(self) -> dict[str, list[str]]:
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

        as_dict: dict = dict.fromkeys(self.weekdays, list())

        weekday: str
        for weekday in self.schedule:

            event: ScheduleEvent
            for event in self.schedule[weekday]:
                as_dict[weekday].append(asdict(event))

        return as_dict
