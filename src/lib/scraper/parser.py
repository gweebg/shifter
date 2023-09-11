import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from bs4.element import ResultSet

from src.lib.scraper.event import ScheduleEvent
from src.lib.scraper.schedule import Schedule


class ScheduleParser:

    @staticmethod
    def _parse_weekdays(context: BeautifulSoup) -> list[str]:

        weekday_table = (context.find_all("table", class_="rsHorizontalHeaderTable"))[0]
        return [weekday.text.title() for weekday in weekday_table.find_all("a")]

    @staticmethod
    def _parse_time(context: BeautifulSoup) -> datetime:

        time_table = (context.find_all("table", class_="rsVerticalHeaderTable"))[0]
        time_str: str = time_table.find_next("div").text.title().strip()
        return datetime.strptime(time_str, "%H:%M")

    @staticmethod
    def _add_to_time(current_time: datetime, minutes: int) -> datetime:
        return current_time + timedelta(minutes=minutes)

    @staticmethod
    def _get_duration(style_string: str) -> datetime:

        block_height_match: re.Match = re.search(r"height:(\d+)px", style_string)

        if int(block_height_match.group(1)) > 200:
            duration: str = "2:00"

        else:
            duration: str = "1:00"

        return datetime.strptime(duration, "%H:%M")

    def _parse_blocks(self, context: ResultSet, current_time: datetime, weekday: str) -> list[ScheduleEvent]:

        events: list[ScheduleEvent] = []

        for block in context:
            duration: datetime = self._get_duration(block["style"])
            events.append(
                ScheduleEvent.build(body=block["title"], duration=duration, starts_at=current_time, weekday=weekday)
            )

        return events

    def parse(self, content: str):

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
