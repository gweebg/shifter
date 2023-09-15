from datetime import time, timedelta

from src.lib.scraper.event import ScheduleEvent
from src.lib.scraper.schedule import Schedule


def merge_schedules(schedules: list[Schedule]) -> Schedule:
    weekdays: list[str] = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado"]

    final_schedule: Schedule = Schedule(weekdays=weekdays)

    schedule: Schedule
    for schedule in schedules:

        event: ScheduleEvent
        for event in schedule.get_events():
            final_schedule.add_event(event)

    return final_schedule


def sum_to_time(time_obj: time, duration: time) -> time:
    time_obj_delta: timedelta = timedelta(
        hours=time_obj.hour,
        minutes=time_obj.minute
    )

    duration_delta: timedelta = timedelta(
        hours=duration.hour,
        minutes=duration.minute
    )

    result_delta: timedelta = time_obj_delta + duration_delta

    return time(
        hour=result_delta.seconds // 3600,
        minute=(result_delta.seconds // 60) % 60
    )


def get_abbr(string: str) -> str:
    return "".join([word[0].upper() if len(word) > 3 else "" for word in string.split(" ")])
