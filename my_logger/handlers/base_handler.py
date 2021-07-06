from abc import abstractmethod, ABC
from typing import List
from ..log_entry import LogEntry


class Handler(ABC):
    @abstractmethod
    def __init__(self, filename: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_log(self, log: LogEntry) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_base_form(self) -> List[LogEntry]:
        raise NotImplementedError
