from datetime import datetime
from typing import Iterable, Optional, List, Dict
from .handlers.base_handler import Handler
from .log_entry import LogEntry
import re


class ProfilLoggerReader:
    def __init__(self, handler: Handler) -> None:
        self.__handler = handler

    @staticmethod
    def filter_by_datetime(
        log_entries: Iterable[LogEntry],
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> Iterable[LogEntry]:

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
        ...

    def groupby_month(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, List[LogEntry]]:
        ...
