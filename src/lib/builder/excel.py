from datetime import time, timedelta
from io import BytesIO

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

    def layout_setup(self) -> None:

        self.worksheet.set_column(0, 10, 23)
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

    def build(self):  # -> bytes:

        self.layout_setup()
        self.paint_rows()

        step: int = 0
        mapped_weekdays: dict[str, str] = self.get_weekday_mapper(self.schedule.weekdays, step)
        mapped_hours: dict[str, int] = self.get_hours_mapper(self.time_data)

        weekday: str
        events: list[ScheduleEvent]
        for weekday, events in self.schedule.schedule.items():

            overlapping_times: list[time] = self.schedule.get_collisions(weekday)
            starting_column: str = mapped_weekdays[weekday]

            if overlapping_times:  # If there are overlapping events, we expand the column by the number of events.

                ending_column: str = self.next_column(starting_column, step=len(overlapping_times))
                self.worksheet.merge_range(
                    f"{starting_column}1:{ending_column}1",
                    weekday,
                    self.cell_styles["header_merge_style"]
                )

            else:  # Else we simply write on the corresponding column.
                self.worksheet.write(f"{starting_column}1", weekday, self.cell_styles["header_style"])

            event: ScheduleEvent
            for event in events:
                ...

            step += len(overlapping_times)
            mapped_weekdays = self.get_weekday_mapper(self.schedule.weekdays, step)

        self.workbook.close()

        # return self.result.getvalue()
