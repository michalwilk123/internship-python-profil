from .base_handler import Handler
from ..log_entry import LogEntry


class FileHandler(Handler):
    def __init__(self, filename: str) -> None:
        ...

    def add_log(self, log: LogEntry) -> bool:
        raise NotImplementedError

    def get_dict(self) -> dict:
        raise NotImplementedError
