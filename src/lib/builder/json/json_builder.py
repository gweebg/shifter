from datetime import datetime
from typing import Any

from src.lib.builder.builder import Builder
from src.lib.scraper.schedule import Schedule

import json


class JsonBuilder(Builder):
    """
    This is the class that implements the build method that allows the conception of json files based on a provided
    schedule.

    :param schedule: This value can either be a schedule object or a list of it, if the value is a list then every
        schedule constituting is merged.
    :type schedule: Schedule | list[Schedule]
    """

    def __init__(self, schedule: Schedule | list[Schedule]):
        """
        Class constructor.
        """
        super().__init__(schedule)

    @staticmethod
    def _serialize_unknown_obj(obj: Any) -> str:
        """
        This method is used as the default function once json.dumps encounters an unknown object.
        Datetimes are converted into string formatted times, any other object is converted to its str form.
        :param obj: Object to be serialized.
        :type obj: Any
        :return: Resulting string.
        :rtype: str
        """
        if isinstance(obj, datetime):
            return obj.time().strftime("%H:%M")

        return str(obj)

    def build(self) -> bytes:
        """
        This is the main method inherited from the Builder ABC, and it builds the schedule in a json format.
        The resulting value from this method needs to be encoded in utf-8.

        :return: The calendar in json format as bytes.
        :rtype: bytes
        """
        schedule_as_dict: dict = self.schedule.get_as_dict()
        return json.dumps(
            schedule_as_dict,
            indent=4,
            default=self._serialize_unknown_obj,
            ensure_ascii=False
        ).encode("utf8")
