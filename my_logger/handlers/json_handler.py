from .base_handler import Handler
from ..log_entry import LogEntry
from typing import List


class JsonHandler(Handler):
    def __init__(self, filename: str) -> None:
        ...

    def add_log(self, log: LogEntry) -> None:
        raise NotImplementedError

    def get_base_form(self) -> List[LogEntry]:
        raise NotImplementedError
