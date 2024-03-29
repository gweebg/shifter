from datetime import time, timedelta
from io import BytesIO
from typing import Optional

from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from src.lib.builder.xlsx import styles
from src.lib.builder.builder import Builder
from src.lib.scraper.event import ScheduleEvent
from src.lib.scraper.schedule import Schedule


class XlsxBuilder(Builder):
    """
    This is the class that implements the build method that allows the conception of XSLX files based on a provided
    schedule.

    :param schedule: This value can either be a schedule object or a list of it, if the value is a list then every
        schedule constituting is merged.
    :type schedule: Schedule | list[Schedule]

    :param debug: This value is used to determine whether the build function should store the data to a file or
        in memory using BytesIO.
    :type debug: bool, optional

    """

    def __init__(
        self, schedule: Schedule | list[Schedule], debug: bool = False
    ) -> None:
        """
        Constructor method for the xlsx builder.
        """

        super().__init__(schedule)

        self.content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        self.debug: bool = debug

        self.__time_data: list[str] = self._generate_time_intervals(
            *(self.schedule.get_starting_and_ending_time())
        )
        self.__result: BytesIO = BytesIO()
        self.__workbook: Workbook = (
            Workbook(self.__result) if not debug else Workbook("debug.xlsx")
        )
        self.__worksheet: Worksheet = self.__workbook.add_worksheet("Your Schedule")

        self.__cell_styles: dict[str, Format] = {}

    @staticmethod
    def _generate_time_intervals(starting_time: time, ending_time: time) -> list[str]:
        """
        This static private method generates a timetable once given a starting and ending times.
        :param starting_time: Starting time for the timetable.
        :type starting_time: time
        :param ending_time: Ending time for the timetable.
        :type ending_time: time
        :return: Timetable represented as a list of times (as str).
        :rtype: list[str]
        """
        time_list: list[str] = []

        interval: timedelta = timedelta(minutes=30)
        starting_time_delta: timedelta = timedelta(
            hours=starting_time.hour, minutes=starting_time.minute
        )
        ending_time_delta: timedelta = timedelta(
            hours=ending_time.hour, minutes=ending_time.minute
        )

        current_time_delta: timedelta = starting_time_delta

        while current_time_delta <= ending_time_delta:
            current_time: time = time(
                hour=current_time_delta.seconds // 3600,
                minute=(current_time_delta.seconds // 60) % 60,
            )
            time_list.append(current_time.strftime("%H:%M"))

            current_time_delta = current_time_delta + interval

        return time_list

    @staticmethod
    def _get_weekday_mapper(weekdays: list[str], step: int = 0) -> dict[str, str]:
        """
        This static private method generates a map from weekday to the column where to place the event.
        :param weekdays: The weekdays to map.
        :type weekdays: list[str]
        :param step: Optional parameter used to skip columns.
        :type step: int, optional
        :return: Dictionary with the mappings.
        :rtype: dict[str, str]
        """
        alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        weekdays_map: dict[str, str] = {}
        starting_index: int = 1

        weekdays: str
        for weekday in weekdays:
            weekdays_map[weekday] = alphabet[starting_index + step]
            starting_index = (starting_index + 1) % len(alphabet)

        return weekdays_map

    @staticmethod
    def _get_hours_mapper(time_data: list[str]) -> dict[str, int]:
        """
        This static private method generates a map that maps each hour on the timetable to its corresponding row.
        :param time_data: Timetable generated by _generate_time_intervals.
        :type time_data: list[str]
        :return: Dictionary with the mappings.
        :rtype: dict[str, int]
        """
        time_map: dict[str, int] = {}
        starting_index: int = 2

        time_str: str
        for time_str in time_data:
            time_map[time_str] = starting_index
            starting_index += 1

        return time_map

    @staticmethod
    def _next_column(column_letter: str, step: int = 1) -> str:
        """
        Given a column letter this function skips *n* columns based on a parameter step and returns the new column.
        :param column_letter: The provided initial column letter.
        :type column_letter: str
        :param step: Number of columns to skip.
        :type step: int, optional
        :return: The new column letter.
        :rtype: str
        """
        alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return alphabet[alphabet.index(column_letter) + step % len(alphabet)]

    @staticmethod
    def _get_in_between_columns(starting_columns: str, ending_column: str) -> list[str]:
        """
        This static private method returns every column letter in between a starting and ending letter (bound included).
        :param starting_columns: Starting letter.
        :type starting_columns: str
        :param ending_column: Ending letter.
        :type ending_column: srt
        :return: List of the column letters.
        :rtype: list[str]
        """
        result: list[str] = []

        alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        starting_index: int = alphabet.index(starting_columns)
        ending_index: int = alphabet.index(ending_column)

        i: int
        for i in range(starting_index, ending_index + 1):
            result.append(alphabet[i])

        return result

    @staticmethod
    def _is_event_overlapping(
        event_time: time, overlapping_hours: list[time | tuple[time, time]]
    ) -> bool:
        """
        Checks whether an event is overlapping with others.
        :param event_time: The event at which the event starts.
        :type event_time: time
        :param overlapping_hours: List containing the times at overlapping occurs.
        :type overlapping_hours: list[time | tuple[time, time]]
        :return: True if the event overlaps, False otherwise.
        :rtype: bool
        """

        hour: time | tuple[time, ...]
        for hour in overlapping_hours:
            if (hour == event_time) or (isinstance(hour, tuple) and event_time in hour):
                return True

        return False

    def setup_layout(self) -> None:
        """
        This method sets up the worksheet column and rows heights and widths as well as defining the different cell
        styles used throughout the page.
        """

        # Column/Row count, width and heights.
        self.__worksheet.set_column(0, 30, 23)
        self.__worksheet.set_default_row(23)
        self.__worksheet.set_row(0, 30)

        # Cells used on the header of the schedule.
        header_style = self.__workbook.add_format(styles.HEADER_CELL)
        header_style.set_font_name(styles.FONT)
        header_style.set_font_color("white")
        self.__cell_styles["header_style"] = header_style

        # Dark cell style for better visibility.
        dark_color = self.__workbook.add_format(styles.DARK_COLOR_CELL)
        dark_color.set_font_name(styles.FONT)
        dark_color.set_font_color(styles.FONT_COLOR)
        self.__cell_styles["dark_color"] = dark_color

        # Light cell style for better visibility.
        light_color = self.__workbook.add_format(styles.LIGHT_COLOR_CELL)
        light_color.set_font_name(styles.FONT)
        light_color.set_font_color(styles.FONT_COLOR)
        self.__cell_styles["light_color"] = light_color

        # Cells used on the header when merging is needed.
        header_merge_style = self.__workbook.add_format(styles.MERGE_CELL)
        header_merge_style.set_font_size(styles.MERGE_FONT_SIZE)
        header_merge_style.set_font_name(styles.FONT)
        header_merge_style.set_font_color("white")
        header_merge_style.set_bg_color(styles.DARK_COLOR)
        self.__cell_styles["header_merge_style"] = header_merge_style

    def setup_rows(self) -> None:
        """
        This method is responsible for drawing the rows and the times with their respective time values and colors.
        :return:
        """

        column_counter: int = 0
        for weekday in self.schedule.schedule:
            overlap_count: int = len(self.schedule.get_collisions(weekday))
            if overlap_count == 0:
                column_counter += 1
            else:
                column_counter += overlap_count + 1

        for i in range(2, len(self.__time_data) + 2):
            self.__worksheet.write_row(
                f"A{i}:F{i}",
                data=[self.__time_data[i - 2]] + [""] * column_counter,
                cell_format=self.__cell_styles["dark_color"]
                if i % 2 == 0
                else self.__cell_styles["light_color"],
            )

    def build(self) -> Optional[bytes]:
        """
        This is the main method inherited from the Builder ABC, and it builds the schedule as a xslx.

        :return: If the debug flag is set to True returns None, otherwise returns bytes.
        :rtype: bytes, optional
        """

        self.setup_layout()  # Setup row and column heights and widths.
        self.setup_rows()  # Setup base color layout for the schedule.

        # Control variables for the placement of events on the worksheet.
        step: int = 0
        mapped_weekdays: dict[str, str] = self._get_weekday_mapper(
            self.schedule.weekdays, step
        )
        mapped_weekdays_for_events: dict[str, list[str]] = dict.fromkeys(
            self.schedule.weekdays, list()
        )
        mapped_hours: dict[str, int] = self._get_hours_mapper(self.__time_data)

        # Control variables for the colors of the events.
        event_color_index: dict[str, str] = {}
        color_index: int = 0

        weekday: str
        events: list[ScheduleEvent]
        for (
            weekday,
            events,
        ) in (
            self.schedule.schedule.items()
        ):  # Looping over every weekday and their events.
            # Retrieving the event collisions for the current weekday.
            overlapping_times: list[time] = self.schedule.get_collisions(weekday)
            starting_column: str = mapped_weekdays[weekday]

            if overlapping_times:  # If there are overlapping events, we expand the column by the number of events.
                ending_column: str = self._next_column(
                    starting_column, step=len(overlapping_times)
                )
                self.__worksheet.merge_range(
                    f"{starting_column}1:{ending_column}1",
                    weekday,
                    self.__cell_styles["header_merge_style"],
                )

                # Storing the used columns by the current weekday in a dictionary.
                mapped_weekdays_for_events[weekday] = self._get_in_between_columns(
                    starting_column, ending_column
                )

            else:  # Else we simply write on the corresponding column.
                self.__worksheet.write(
                    f"{starting_column}1", weekday, self.__cell_styles["header_style"]
                )
                mapped_weekdays_for_events[weekday] = [starting_column]

            # Indicates in which column from the mapped_weekdays_for_events dictionary to place the event.
            overlap_index: int = 0

            event: ScheduleEvent
            for event in events:  # Looping over every weekday event.
                # Getting the row based on the event starting time.
                mapped_row: int = mapped_hours[event.starts_at.time().strftime("%H:%M")]

                # TODO | Refactor

                # Coloring stuff.
                if event.body.name not in event_color_index:
                    event_color_index[event.body.name] = styles.COLORS[color_index]
                    color_index += 1

                merge_style = self.__workbook.add_format(styles.MERGE_CELL)
                merge_style.set_font_size(styles.MERGE_FONT_SIZE)
                merge_style.set_font_name(styles.FONT)
                merge_style.set_font_color(styles.FONT_COLOR)
                merge_style.set_fg_color(event_color_index[event.body.name])

                to_draw_column: str = mapped_weekdays_for_events[weekday][0]
                if self._is_event_overlapping(
                    event.starts_at.time(), overlapping_times
                ):  # If the event overlaps.
                    to_draw_column = mapped_weekdays_for_events[weekday][overlap_index]
                    overlap_index += 1

                else:  # If it is a regular event.
                    overlap_index = 0

                if event.duration.hour == 2:
                    self.__worksheet.merge_range(
                        f"{to_draw_column}{mapped_row}:{to_draw_column}{mapped_row + 3}",
                        str(event.body),
                        merge_style,
                    )

                elif event.duration.hour == 1:
                    self.__worksheet.merge_range(
                        f"{to_draw_column}{mapped_row}:{to_draw_column}{mapped_row + 1}",
                        str(event.body),
                        merge_style,
                    )

            # Control for the column counting on weekdays with overlapping events.
            step += len(overlapping_times)
            mapped_weekdays = self._get_weekday_mapper(self.schedule.weekdays, step)

        self.__workbook.close()

        return self.__result.getvalue() if not self.debug else None
