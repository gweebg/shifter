import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from bs4.element import ResultSet

from src.lib.scraper.event import ScheduleEvent
from src.lib.scraper.schedule import Schedule


class ScheduleParser:
    """
    This class provides the methods necessary to parse the html raw scraped content into a Schedule/ScheduleEvent.
    """

    @staticmethod
    def _parse_weekdays(context: BeautifulSoup) -> list[str]:
        """
        Method that parses the present weekdays on the schedule.
        :param context: The current 'container' that is being worked on.
        :type context: BeautifulSoup
        :return: List containing the weekdays used.
        :rtype: list[str]
        """
        weekday_table = (context.find_all("table", class_="rsHorizontalHeaderTable"))[0]
        return [weekday.text.title() for weekday in weekday_table.find_all("a")]

    @staticmethod
    def _parse_time(context: BeautifulSoup) -> datetime:
        """
        Method that parses the hours present in a row.
        :param context: The current 'container' that is being worked on.
        :type context: BeautifulSoup
        :return: The time in the form of a datetime object.
        :rtype: datetime
        """
        time_table = (context.find_all("table", class_="rsVerticalHeaderTable"))[0]
        time_str: str = time_table.find_next("div").text.title().strip()
        return datetime.strptime(time_str, "%H:%M")

    @staticmethod
    def _add_to_time(current_time: datetime, minutes: int) -> datetime:
        """
        Method that adds minutes to a defined time.
        :param current_time: Time to be added to.
        :type current_time: datetime
        :param minutes: Minutes to add on current_time.
        :type minutes: int
        :return: A datetime object of the addition.
        :rtype: datetime
        """
        return current_time + timedelta(minutes=minutes)

    @staticmethod
    def _get_duration(style_string: str) -> datetime:
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

    def _parse_blocks(self, context: ResultSet, current_time: datetime, weekday: str) -> list[ScheduleEvent]:
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
            duration: datetime = self._get_duration(block["style"])
            events.append(
                ScheduleEvent.build(body=block["title"], duration=duration, starts_at=current_time, weekday=weekday)
            )

        return events

    def parse(self, content: str) -> Schedule:
        """
        Given the raw source code of the scraped page, this method is responsible for parsing every and each event
        aggregating them onto a Schedule object.
        :param content: The raw source code of the schedule page.
        :type content: str
        :return: The newly parsed schedule.
        :rtype: Schedule
        """

        soup: BeautifulSoup = BeautifulSoup(content, "lxml")

        weekdays: list[str] = self._parse_weekdays(soup)
        starting_time: datetime = self._parse_time(soup)

        schedule: Schedule = Schedule(weekdays=weekdays)  # Method result
        schedule_rows: ResultSet = soup.find_all("table", class_="rsContentTable")[0].find_all("tr")

        current_time: datetime = starting_time

        for row in schedule_rows:

            for index, column in enumerate(row.find_all("td")):
                current_weekday = weekdays[index]
                schedule_blocks: ResultSet = column.find_all("div", class_="rsApt rsAptSimple")

                events: list[ScheduleEvent] = self._parse_blocks(schedule_blocks, current_time, current_weekday)
                for event in events:
                    schedule.add_event(event)

            current_time = self._add_to_time(current_time, minutes=30)

        return schedule
