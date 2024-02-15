from abc import ABC, abstractmethod

from src.lib.scraper.schedule import Schedule
from src.lib.builder.utils import merge_schedules


class Builder(ABC):
    """
    This is the abstract base class for any class that builds over the Schedule class.

    :param schedule: This value can either be a schedule object or a list of it, if the value is a list then every
        schedule constituting is merged.
    :type schedule: Schedule | list[Schedule]
    """

    __slots__ = ("schedule", "content_type")

    @abstractmethod
    def __init__(self, schedule: Schedule | list[Schedule], *args, **kwargs):
        self.content_type: str = ""

        if isinstance(schedule, list):
            self.schedule: Schedule = merge_schedules(schedule)

        else:
            self.schedule: Schedule = schedule

    @abstractmethod
    def build(self):
        ...
