from datetime import datetime
from .log_entry import Level, LogEntry
from typing import List
from .handlers.base_handler import Handler


class ProfilLogger:
    """Logger object. From this class you can perform
    all nessesary logging operations.
    """
    def __init__(self, handlers: List[Handler]) -> None:
        """Initialize object with a list of handlers.
        Logs will be stored in each handler object

        :param handlers: list of handlers
        :type handlers: List[Handler]
        """
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
        """Create log with given message at level
        INFO

        :param msg: log text message
        :type msg: str
        :return: True if log was stored successfully, otherwise False
        :rtype: bool
        """
        return self.__add_log(msg, Level.INFO)

    def warning(self, msg: str) -> bool:
        """Create log with given message at level
        WARNING

        :param msg: log text message
        :type msg: str
        :return: True if log was stored successfully, otherwise False
        :rtype: bool
        """
        return self.__add_log(msg, Level.WARNING)

    def debug(self, msg: str) -> bool:
        """Create log with given message at level
        DEBUG

        :param msg: log text message
        :type msg: str
        :return: True if log was stored successfully, otherwise False
        :rtype: bool
        """
        return self.__add_log(msg, Level.DEBUG)

    def critical(self, msg: str) -> bool:
        """Create log with given message at level
        CRITICAL

        :param msg: log text message
        :type msg: str
        :return: True if log was stored successfully, otherwise False
        :rtype: bool
        """
        return self.__add_log(msg, Level.CRITICAL)

    def error(self, msg: str) -> bool:
        """Create log with given message at level
        ERROR

        :param msg: log text message
        :type msg: str
        :return: True if log was stored successfully, otherwise False
        :rtype: bool
        """
        return self.__add_log(msg, Level.ERROR)

    def set_log_level(self, level: str) -> None:
        """Set minimal log level to save.

        :param level: new minimal log level
        :type level: str
        :raises KeyError: raises exception if wrong log level
        name is given
        """
        try:
            self.__level = Level[level]
        except KeyError:
            raise KeyError(
                f"Log level {level} does not exist. "
                "Available levels: {[a.name for a in Level]}"
            )
