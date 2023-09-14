from datetime import datetime, time

from src.lib.builder.builder import Builder
from src.lib.builder.utils import sum_to_time, get_abbr
from src.lib.scraper.event import ScheduleEvent
from src.lib.scraper.schedule import Schedule

from icalendar import Calendar, Event
from pytz import timezone


class IcalBuilder(Builder):
    """
    This is the class that implements the build method that allows the conception of ICal files based on a provided
    schedule.

    :param schedule: This value can either be a schedule object or a list of it, if the value is a list then every
        schedule constituting is merged.
    :type schedule: Schedule | list[Schedule]
    """

    def __init__(self, schedule: Schedule | list[Schedule]):
        """
        Constructor method for the xlsx builder.
        """

        super().__init__(schedule)

        self._weekday_abbr_map: dict[str, str] = {
            "Segunda-Feira": "MO",
            "Terça-Feira": "TU",
            "Quarta-Feira": "WE",
            "Quinta-Feira": "TH",
            "Sexta-Feira": "FR",
            "Sábado": "SA",
            "Domingo": "SU"
        }

    def _to_ical_event(self, event: ScheduleEvent) -> Event:
        """
        This private method is responsible to convert a ScheduleEvent into an icalendar recognizable Event.

        :param event: Provided event to convert.
        :type event: ScheduleEvent
        :return: The converted icalendar event object.
        :rtype: Event
        """
        result_event: Event = Event()

        starts_at: datetime = datetime(
            2021, 7, 30,
            hour=event.starts_at.hour, minute=event.starts_at.minute,
            tzinfo=timezone("Europe/Lisbon")
        )

        ends_at_time: time = sum_to_time(event.starts_at.time(), event.duration.time())
        ends_at: datetime = datetime(
            2021, 7, 30,
            hour=ends_at_time.hour, minute=ends_at_time.minute,
            tzinfo=timezone("Europe/Lisbon")
        )

        result_event.add("summary", f"{event.body.shift} - {str(event.body.location)} - {get_abbr(event.body.name)}")
        result_event.add("description", str(event))
        result_event.add('location', str(event.body.location))
        result_event.add('dtstart', starts_at)
        result_event.add('dtend', ends_at)

        result_event.add('rrule', {'freq': 'weekly', 'byday': self._weekday_abbr_map[event.weekday]})

        return result_event

    def build(self) -> bytes:
        """
        This is the main method inherited from the Builder ABC, and it builds the schedule in an icalendar format.

        :return: The calendar in icalendar format as bytes.
        :rtype: bytes
        """
        calendar: Calendar = Calendar()
        calendar.add('name', "Shifter Schedule")

        events: list[ScheduleEvent] = self.schedule.get_events()

        event: ScheduleEvent
        for event in events:
            calendar.add_component(self._to_ical_event(event))

        # file = open("debug.ics", "wb")
        # file.write(calendar.to_ical())

        return calendar.to_ical()
