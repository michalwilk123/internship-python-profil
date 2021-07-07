from .base_handler import Handler
from ..log_entry import LogEntry
from typing import List
import json
import dataclasses
from datetime import datetime


class JsonHandler(Handler):
    def __init__(self, filename: str) -> None:
        self.__filename = filename

    def add_log(self, log: LogEntry) -> None:
        try:
            with open(self.__filename, "r") as json_file:
                json_dict = json.loads(json_file.read())
        except FileNotFoundError:
            # file with given name does not exist
            json_dict = []

        log_dict = dataclasses.asdict(log)
        log_dict["date"] = log_dict["date"].isoformat()
        json_dict.append(log_dict)

        with open(self.__filename, "w") as json_file:
            json_file.write(json.dumps(json_dict))

    def get_base_form(self) -> List[LogEntry]:
        with open(self.__filename, "r") as json_file:
            json_dict = json.loads(json_file.read())

        log_entries = []

        for li in json_dict:
            log_entries.append(
                LogEntry(
                    date=datetime.fromisoformat(li["date"]),
                    level=li["level"],
                    msg=li["msg"],
                )
            )

        return log_entries
