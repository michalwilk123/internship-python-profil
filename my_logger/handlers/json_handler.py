from .base_handler import Handler
from ..log_entry import LogEntry


class JsonHandler(Handler):
    def __init__(self, filename: str) -> None:
        ...

    def add_log(self, log: LogEntry) -> bool:
        raise NotImplementedError

    def get_base_form(self) -> dict:
        raise NotImplementedError
