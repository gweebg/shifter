from datetime import datetime, time, timedelta
from io import BytesIO
from typing import Optional

import xlsxwriter as writer

from src.lib.scraper.event import ScheduleEvent
from src.lib.scraper.schedule import Schedule
import src.lib.builder.styles as styles


def merge_schedules(schedules: list[Schedule]) -> Schedule:
    weekdays: list[str] = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]

    final_schedule: Schedule = Schedule(weekdays=weekdays)

    schedule: Schedule
    for schedule in schedules:

        event: ScheduleEvent
        for event in schedule.get_events():
            final_schedule.add_event(event)

    return final_schedule


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


def get_hours_map(time_data: list[str]) -> dict[str, int]:
    time_map: dict[str, int] = {}
    starting_index: int = 2

    time_str: str
    for time_str in time_data:
        time_map[time_str] = starting_index
        starting_index += 1

    return time_map


def get_weekday_map(weekdays: list[str], step: int) -> dict[str, str]:
    alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    weekdays_map: dict[str, str] = {}

    letter_index: int = 1

    weekdays: str
    for weekday in weekdays:
        weekdays_map[weekday] = alphabet[letter_index + step]
        letter_index = (letter_index + 1) % len(alphabet)

    return weekdays_map


def next_column(letter: str) -> str:
    alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return alphabet[alphabet.index(letter) + 1 % len(alphabet)]


def build_schedule_xlsx(schedule: Schedule):  # -> bytes:

    # output: BytesIO = BytesIO()
    current_date: str = datetime.now().strftime("%d-%m-%Y")

    # Workbook creation.
    workbook = writer.Workbook("text.xlsx")
    # workbook = writer.Workbook(output)  # Saving the workbook in memory.
    worksheet = workbook.add_worksheet(f"Your Schedule ({current_date})")

    # Base schedule setup (rows, columns, header, styles).

    worksheet.set_column(0, 5, 23)  # Column length.
    worksheet.set_default_row(23)  # Default number of rows.
    worksheet.set_row(0, 30)  # Row length.

    header_style = workbook.add_format(styles.HEADER_CELL)
    header_style.set_font_name(styles.FONT)
    header_style.set_font_color("white")

    dark_color = workbook.add_format(styles.DARK_COLOR_CELL)
    dark_color.set_font_name(styles.FONT)
    dark_color.set_font_color(styles.FONT_COLOR)

    light_color = workbook.add_format(styles.LIGHT_COLOR_CELL)
    light_color.set_font_name(styles.FONT)
    light_color.set_font_color(styles.FONT_COLOR)

    # Setting up "chess" pattern as the background of the schedule and headers.

    worksheet.write_row("A1:F1", data=[""] + schedule.weekdays, cell_format=header_style)

    starting_time, ending_time = schedule.get_starting_and_ending_time()
    time_data: list[str] = generate_time_intervals(starting_time, ending_time)

    for i in range(2, len(time_data) + 2):
        worksheet.write_row(f"A{i}:F{i}",
                            data=[time_data[i - 2]] + [""] * len(schedule.weekdays),
                            cell_format=dark_color if i % 2 == 0 else light_color)

    # Drawing the schedule events.

    weekday_step: int = 0
    weekday_map: dict[str, str] = get_weekday_map(schedule.weekdays, weekday_step)

    time_map: dict[str, int] = get_hours_map(time_data)

    event_color_index: dict[str, str] = {}
    color_index: int = 0

    weekday: str
    events: list[ScheduleEvent]
    for weekday, events in schedule.schedule.items():

        collisions: list[time] = schedule.get_collisions(weekday)
        print(collisions)
        prev_event: Optional[ScheduleEvent] = None

        event: ScheduleEvent
        for event in events:

            if prev_event is None:
                prev_event = event

            if event.body.name not in event_color_index:
                event_color_index[event.body.name] = styles.COLORS[color_index]
                color_index += 1

            merge_style = workbook.add_format(styles.MERGE_CELL)
            merge_style.set_font_size(styles.MERGE_FONT_SIZE)
            merge_style.set_font_name(styles.FONT)
            merge_style.set_font_color(styles.FONT_COLOR)
            merge_style.set_fg_color(event_color_index[event.body.name])

            mapped_row: int = time_map[event.starts_at.time().strftime("%H:%M")]
            mapped_column: str = weekday_map[event.weekday]

            if event.starts_at.time() in collisions and prev_event.starts_at.time() != event.starts_at.time():

                mapped_column: str = next_column(weekday_map[event.weekday])
                weekday_step += 1
                weekday_map = get_weekday_map(schedule.weekdays, weekday_step)

            if event.duration.hour == 2:
                worksheet.merge_range(
                    f"{mapped_column}{mapped_row}:{mapped_column}{mapped_row + 3}",
                    str(event.body),
                    merge_style
                )

            elif event.duration.hour == 1:
                worksheet.merge_range(
                    f"{mapped_column}{mapped_row}:{mapped_column}{mapped_row + 1}",
                    str(event.body),
                    merge_style
                )

            prev_event = event

    workbook.close()

    # return output.getvalue()


"""
For each weekday, check whether there are event collisions.
If there is, then skip a row for each event in collision.
"""
