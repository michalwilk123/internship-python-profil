from datetime import datetime
from .log_entry import Level, LogEntry
from typing import List
from .handlers.base_handler import Handler


class ProfilLogger:
    def __init__(self, handlers: List[Handler]) -> None:
        self.__handlers = handlers
        self.__level = Level.DEBUG

    @property
    def handlers(self) -> List[Handler]:
        return self.__handlers

    def __add_log(self, msg: str, level: Level) -> bool:
        if self.__level.value > level.value:
            return False

        entry = LogEntry(datetime.now(), level.name, msg)

        for hnd in self.__handlers:
            hnd.add_log(entry)

        return True

    def info(self, msg: str) -> bool:
        return self.__add_log(msg, Level.INFO)

    def warning(self, msg: str) -> bool:
        return self.__add_log(msg, Level.WARNING)

    def debug(self, msg: str) -> bool:
        return self.__add_log(msg, Level.DEBUG)

    def critical(self, msg: str) -> bool:
        return self.__add_log(msg, Level.CRITICAL)

    def error(self, msg: str) -> bool:
        return self.__add_log(msg, Level.ERROR)

    def set_log_level(self, level: str) -> None:
        try:
            self.__level = Level[level]
        except KeyError:
            raise KeyError(
                f"Log level {level} does not exist. "
                "Available levels: {[a.name for a in Level]}"
            )
