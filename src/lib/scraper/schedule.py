from dataclasses import asdict

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
