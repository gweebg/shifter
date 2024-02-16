import re
from datetime import datetime

from bs4 import BeautifulSoup
from bs4.element import ResultSet

from src.lib.scraper.event import ScheduleEvent
from src.lib.scraper.schedule import Schedule
from src.lib.scraper.utils import add_to_time

# todo: remove hard coded values, put them in variables or onto a config class


class ScheduleParser:
    """
    This class provides the methods necessary to parse the html raw scraped content into a Schedule/ScheduleEvent.
    """

    @staticmethod
    def __parse_weekdays(sched: BeautifulSoup) -> list[str]:
        """Get a list of the weekdays that are occupied in the schedule.

        Args:
            sched (BeautifulSoup): Queriable schedule object.

        Returns:
            list[str]: List of the weekdays as strings
        """
        weekday_table = (sched.find_all("table", class_="rsHorizontalHeaderTable"))[0]
        return [weekday.text.title() for weekday in weekday_table.find_all("a")]

    @staticmethod
    def __parse_start_time(sched: BeautifulSoup) -> datetime:
        """Get the starting time of the schedule, present on the first time table row.

        Args:
            sched (BeautifulSoup): Queriable schedule object.

        Returns:
            datetime: Starting time as a datatime object.
        """
        time_table = (sched.find_all("table", class_="rsVerticalHeaderTable"))[0]
        time_str: str = time_table.find_next("div").text.title().strip()
        return datetime.strptime(time_str, "%H:%M")

    @staticmethod
    def __parse_duration(style_string: str) -> datetime:
        """
        Given a style css string, this method extracts the height of the container and based on that calculates the
        duration of it. Height above 200 means a duration of 2 hours, height bellow 200 means a duration of 1 hour.
        :param style_string: String containing the css string of the container.
        :type style_string: str
        :return: The duration as a datetime.
        :rtype: datetime
        """
        block_height_match: re.Match = re.search(r"height:(\d+)px", style_string)
        duration: str = "2:00" if int(block_height_match.group(1)) > 200 else "1:00"

        return datetime.strptime(duration, "%H:%M")

    def __parse_blocks(
        self, context: ResultSet, current_time: datetime, weekday: str
    ) -> list[ScheduleEvent]:
        """
        Each row of the schedule can and will have multiple events, this method parses those events into
        ScheduleEvent objects.
        :param context: Current 'block' we are in.
        :type context: ResultSet
        :param current_time: Current time of events.
        :type current_time: datetime
        :param weekday: Current weekday.
        :type weekday: str
        :return: List of every parsed block inside the container.
        :rtype: list[ScheduleEvent]
        """

        events: list[ScheduleEvent] = []
        for block in context:
            duration: datetime = self.__parse_duration(block["style"])
            event = ScheduleEvent.build(
                body=block["title"],
                duration=duration,
                starts_at=current_time,
                weekday=weekday,
            )
            events.append(event)

        return events

    def parse(self, raw_content: str) -> Schedule:
        """
        Given the raw source code of the scraped page, this method is responsible for parsing every and each event
        aggregating them onto a Schedule object.
        :param content: The raw source code of the schedule page.
        :type content: str
        :return: The newly parsed schedule.
        :rtype: Schedule
        """

        soup: BeautifulSoup = BeautifulSoup(raw_content, "lxml")  # parse into soup

        weekdays: list[str] = self.__parse_weekdays(soup)
        starting_time: datetime = self.__parse_start_time(soup)

        schedule: Schedule = Schedule(weekdays)
        schedule_rows = soup.find_all("table", class_="rsContentTable")[0].find_all(
            "tr"
        )

        current_time: datetime = starting_time
        for row in schedule_rows:
            for index, column in enumerate(row.find_all("td")):
                current_weekday = weekdays[index]
                schedule_blocks = column.find_all("div", class_="rsApt rsAptSimple")

                events: list[ScheduleEvent] = self.__parse_blocks(
                    schedule_blocks, current_time, current_weekday
                )

                # there may be more than one event at a given time
                for event in events:
                    schedule.add_event(event)

            current_time = add_to_time(current_time, minutes=30)

        return schedule
