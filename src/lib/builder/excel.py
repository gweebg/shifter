from datetime import time, timedelta
from io import BytesIO
from typing import Optional

import xlsxwriter as writer
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet
from xlsxwriter.workbook import Workbook

from src.lib.builder import styles
from src.lib.builder.builder import merge_schedules
from src.lib.scraper.event import ScheduleEvent
from src.lib.scraper.schedule import Schedule


class XlsxBuilder:

    def __init__(self, schedule: Schedule | list[Schedule]) -> None:

        if isinstance(schedule, list):
            self.schedule: Schedule = merge_schedules(schedule)

        else:
            self.schedule: Schedule = schedule

        starting_time, ending_time = schedule.get_starting_and_ending_time()
        self.time_data: list[str] = self.generate_time_intervals(starting_time, ending_time)

        self.result: BytesIO = BytesIO()
        # self.workbook: Workbook = Workbook(self.result)
        self.workbook: Workbook = Workbook("text.xlsx")
        self.worksheet: Worksheet = self.workbook.add_worksheet("Your Schedule")

        self.cell_styles: dict[str, Format] = {}

    @staticmethod
    def generate_time_intervals(starting_time: time, ending_time: time) -> list[str]:
        time_list: list[str] = []

        interval: timedelta = timedelta(minutes=30)
        starting_time_delta: timedelta = timedelta(hours=starting_time.hour, minutes=starting_time.minute)
        ending_time_delta: timedelta = timedelta(hours=ending_time.hour, minutes=ending_time.minute)

        current_time_delta: timedelta = starting_time_delta

        while current_time_delta <= ending_time_delta:
            current_time: time = time(hour=current_time_delta.seconds // 3600,
                                      minute=(current_time_delta.seconds // 60) % 60)
            time_list.append(current_time.strftime("%H:%M"))

            current_time_delta = current_time_delta + interval

        return time_list

    @staticmethod
    def get_weekday_mapper(weekdays: list[str], step: int = 0) -> dict[str, str]:

        alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        weekdays_map: dict[str, str] = {}

        starting_index: int = 1

        weekdays: str
        for weekday in weekdays:
            weekdays_map[weekday] = alphabet[starting_index + step]
            starting_index = (starting_index + 1) % len(alphabet)

        return weekdays_map

    @staticmethod
    def get_hours_mapper(time_data: list[str]) -> dict[str, int]:
        time_map: dict[str, int] = {}
        starting_index: int = 2

        time_str: str
        for time_str in time_data:
            time_map[time_str] = starting_index
            starting_index += 1

        return time_map

    @staticmethod
    def next_column(column_letter: str, step: int = 1) -> str:
        alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return alphabet[alphabet.index(column_letter) + step % len(alphabet)]

    @staticmethod
    def get_in_between_columns(starting_columns: str, ending_column: str) -> list[str]:
        alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        result: list[str] = []
        starting_index: int = alphabet.index(starting_columns)
        ending_index: int = alphabet.index(ending_column)

        i: int
        for i in range(starting_index, ending_index + 1):
            result.append(alphabet[i])

        return result

    def layout_setup(self) -> None:

        self.worksheet.set_column(0, 30, 23)
        self.worksheet.set_default_row(23)
        self.worksheet.set_row(0, 30)

        header_style = self.workbook.add_format(styles.HEADER_CELL)
        header_style.set_font_name(styles.FONT)
        header_style.set_font_color("white")
        self.cell_styles["header_style"] = header_style

        dark_color = self.workbook.add_format(styles.DARK_COLOR_CELL)
        dark_color.set_font_name(styles.FONT)
        dark_color.set_font_color(styles.FONT_COLOR)
        self.cell_styles["dark_color"] = dark_color

        light_color = self.workbook.add_format(styles.LIGHT_COLOR_CELL)
        light_color.set_font_name(styles.FONT)
        light_color.set_font_color(styles.FONT_COLOR)
        self.cell_styles["light_color"] = light_color

        header_merge_style = self.workbook.add_format(styles.MERGE_CELL)
        header_merge_style.set_font_size(styles.MERGE_FONT_SIZE)
        header_merge_style.set_font_name(styles.FONT)
        header_merge_style.set_font_color("white")
        header_merge_style.set_bg_color(styles.DARK_COLOR)
        self.cell_styles["header_merge_style"] = header_merge_style

    def paint_rows(self) -> None:

        column_counter: int = 0
        for weekday in self.schedule.schedule:

            overlap_count: int = len(self.schedule.get_collisions(weekday))

            if overlap_count == 0:
                column_counter += 1

            else:
                column_counter += overlap_count + 1

        for i in range(2, len(self.time_data) + 2):
            self.worksheet.write_row(
                f"A{i}:F{i}",
                data=[self.time_data[i - 2]] + [""] * column_counter,
                cell_format=self.cell_styles["dark_color"] if i % 2 == 0 else self.cell_styles["light_color"]
            )

    @staticmethod
    def is_event_overlapping(event_time: time, overlapping_hours: list[time | tuple[time, ...]]) -> bool:

        hour: time | tuple[time, ...]
        for hour in overlapping_hours:

            if (hour == event_time) or (isinstance(hour, tuple) and event_time in hour):
                return True

        return False

    def build(self):  # -> bytes:
        """
        Builds the xlsx schedule based on the Schedule object provided.

        :return: The schedule stored in memory as BytesIO.
        """

        self.layout_setup()  # Setup row and column heights and widths.
        self.paint_rows()  # Setup base color layout for the schedule.

        # Control variables for the placement of events on the worksheet.
        step: int = 0
        mapped_weekdays: dict[str, str] = self.get_weekday_mapper(self.schedule.weekdays, step)
        mapped_weekdays_for_events: dict[str, list[str]] = dict.fromkeys(self.schedule.weekdays, list())
        mapped_hours: dict[str, int] = self.get_hours_mapper(self.time_data)

        # Control variables for the colors of the events.
        event_color_index: dict[str, str] = {}
        color_index: int = 0

        weekday: str
        events: list[ScheduleEvent]
        for weekday, events in self.schedule.schedule.items():  # Looping over every weekday and their events.

            # Retrieving the event collisions for the current weekday.
            overlapping_times: list[time] = self.schedule.get_collisions(weekday)
            starting_column: str = mapped_weekdays[weekday]

            if overlapping_times:  # If there are overlapping events, we expand the column by the number of events.

                ending_column: str = self.next_column(starting_column, step=len(overlapping_times))
                self.worksheet.merge_range(
                    f"{starting_column}1:{ending_column}1",
                    weekday,
                    self.cell_styles["header_merge_style"]
                )

                # Storing the used columns by the current weekday in a dictionary.
                mapped_weekdays_for_events[weekday] = self.get_in_between_columns(starting_column, ending_column)

            else:  # Else we simply write on the corresponding column.
                self.worksheet.write(f"{starting_column}1", weekday, self.cell_styles["header_style"])
                mapped_weekdays_for_events[weekday] = [starting_column]

            # Indicates in which column from the mapped_weekdays_for_events dictionary to place the event.
            overlap_index: int = 0

            event: ScheduleEvent
            for event in events:  # Looping over every weekday event.

                # Getting the row based on the event starting time.
                mapped_row: int = mapped_hours[event.starts_at.time().strftime("%H:%M")]

                ############################## TODO | Refactor

                # Coloring stuff.
                if event.body.name not in event_color_index:
                    event_color_index[event.body.name] = styles.COLORS[color_index]
                    color_index += 1

                merge_style = self.workbook.add_format(styles.MERGE_CELL)
                merge_style.set_font_size(styles.MERGE_FONT_SIZE)
                merge_style.set_font_name(styles.FONT)
                merge_style.set_font_color(styles.FONT_COLOR)
                merge_style.set_fg_color(event_color_index[event.body.name])

                ##############################

                to_draw_column: str = mapped_weekdays_for_events[weekday][0]
                if self.is_event_overlapping(event.starts_at.time(), overlapping_times):  # If the event overlaps.
                    print(mapped_weekdays_for_events, weekday, overlap_index)
                    to_draw_column = mapped_weekdays_for_events[weekday][overlap_index]
                    overlap_index += 1

                else:  # If it is a regular event.
                    overlap_index = 0

                if event.duration.hour == 2:
                    self.worksheet.merge_range(
                        f"{to_draw_column}{mapped_row}:{to_draw_column}{mapped_row + 3}",
                        str(event.body),
                        merge_style
                    )

                elif event.duration.hour == 1:
                    self.worksheet.merge_range(
                        f"{to_draw_column}{mapped_row}:{to_draw_column}{mapped_row + 1}",
                        str(event.body),
                        merge_style
                    )

            # Control for the column counting on weekdays with overlapping events.
            step += len(overlapping_times)
            mapped_weekdays = self.get_weekday_mapper(self.schedule.weekdays, step)

        self.workbook.close()

        # return self.result.getvalue()
