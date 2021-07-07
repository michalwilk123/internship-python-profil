from datetime import datetime
from typing import Iterable, Optional, List, Dict
from .handlers.base_handler import Handler
from .log_entry import LogEntry
import re
import itertools


class ProfilLoggerReader:
    """Access logs entries from files."""

    def __init__(self, handler: Handler) -> None:
        self.__handler = handler

    @staticmethod
    def filter_by_datetime(
        log_entries: Iterable[LogEntry],
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> Iterable[LogEntry]:
        """Filter list of entries by the time interval.
        If dates are None, this date bound is skipped

        :param log_entries: Iterable of log objects, could be list, map
        or anything you can iterate
        :type log_entries: Iterable[LogEntry]
        :param start_date: [description], logs older than this
        date will be skipped, defaults to None
        :type start_date: datetime, optional
        :param end_date: [description],  logs newer than this
        date will be skipped, defaults to None
        :type end_date: datetime, optional
        :return: list or filter object with given constraints.
        Threfore O(n) = 1
        :rtype: Iterable[LogEntry]
        """
        if start_date is not None:
            log_entries = filter(lambda le: le.date >= start_date, log_entries)

        if end_date is not None:
            log_entries = filter(lambda le: le.date <= end_date, log_entries)

        return log_entries

    def find_by_text(
        self,
        text: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[LogEntry]:
        """find log entries caontaining given
        chunk of text sequence in the message attribute.
        You can also filter logs by their date attribute.

        :param text: sequence of text to look for
        :type text: str
        :param start_date: lower bound date, defaults to None
        :type start_date: Optional[datetime], optional
        :param end_date: upper bound date, defaults to None
        :type end_date: Optional[datetime], optional
        :return: list of filtered logs. If no logs found,
        method returns empty list
        :rtype: List[LogEntry]
        """

        log_entry_list = self.__handler.get_base_form()
        log_entry_list = ProfilLoggerReader.filter_by_datetime(
            log_entry_list, start_date, end_date
        )
        return list(filter(lambda le: text in le.msg, log_entry_list))

    def find_by_regex(
        self,
        regex: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[LogEntry]:
        """Filter logs by regular expression. You can
        filter also by the time interval in which they were made

        :param regex: regular expression string
        :type regex: str
        :param start_date: lower bound date, defaults to None
        :type start_date: Optional[datetime], optional
        :param end_date: upper bound date, defaults to None
        :type end_date: Optional[datetime], optional
        :return: list of filtered logs. If no logs found,
        method returns empty list
        :rtype: List[LogEntry]
        """
        log_entry_list = self.__handler.get_base_form()
        log_entry_list = ProfilLoggerReader.filter_by_datetime(
            log_entry_list, start_date, end_date
        )
        re_expression = re.compile(regex)
        return list(
            filter(lambda le: re_expression.match(le.msg), log_entry_list)
        )

    def groupby_level(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, List[LogEntry]]:
        """Create dictionary of keys (text name of the log level)
        like: INFO, WARNING, DEBUG, etc.
        and values (list of logs from the same level).
        If they are no logs with some level, the level key is not
        created. You can filter those logs also by their
        date attribute.

        :param start_date: lower bound date, defaults to None
        :type start_date: Optional[datetime], optional
        :param end_date: upper bound date, defaults to None
        :type end_date: Optional[datetime], optional
        :return: dictionary of grouped log entries. Returns
        empty set if dictionary is not containing any entries
        :rtype: List[LogEntry]
        """
        log_entry_list = self.__handler.get_base_form()
        log_entry_list = ProfilLoggerReader.filter_by_datetime(
            log_entry_list, start_date, end_date
        )
        log_dict = {}

        for key, group in itertools.groupby(
            log_entry_list, key=lambda le: le.level
        ):
            log_dict[key] = list(group)

        return log_dict

    def groupby_month(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, List[LogEntry]]:
        """Create dictionary of keys (text name of the month!)
        like: July, May, April, etc.
        and values (list of logs from the same month).
        If they are no logs from given month, the month key is not
        created. You can filter those logs also by their
        date attribute.

        :param start_date: lower bound date, defaults to None
        :type start_date: Optional[datetime], optional
        :param end_date: upper bound date, defaults to None
        :type end_date: Optional[datetime], optional
        :return: dictionary of grouped log entries. Returns
        empty set if dictionary is not containing any entries
        :rtype: List[LogEntry]
        """
        log_entry_list = self.__handler.get_base_form()
        log_entry_list = ProfilLoggerReader.filter_by_datetime(
            log_entry_list, start_date, end_date
        )
        log_dict = {}

        for key, group in itertools.groupby(
            log_entry_list, key=lambda le: le.date.strftime("%B")
        ):
            log_dict[key] = list(group)

        return log_dict
