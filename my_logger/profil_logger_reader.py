from datetime import datetime
from typing import Optional, List, Dict
from .handlers.base_handler import Handler
from .log_entry import LogEntry
import re


class ProfilLoggerReader:
    def __init__(self, handler: Handler) -> None:
        ...

    def find_by_text(self, text: str):
        ...

    def find_by_regex(self, text: str):
        ...

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
