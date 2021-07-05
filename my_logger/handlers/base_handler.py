from abc import abstractmethod, ABC
from ..log_entry import LogEntry


class Handler(ABC):
    @abstractmethod
    def __init__(self, filename: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_log(self, log: LogEntry):
        raise NotImplementedError

    @abstractmethod
    def get_dict(self):
        raise NotImplementedError
