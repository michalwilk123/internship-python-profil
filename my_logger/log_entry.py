from datetime import datetime
from dataclasses import dataclass, fields
from typing import List
from enum import Enum
from functools import lru_cache

Level = Enum("Level", "DEBUG INFO WARNING ERROR CRITICAL")


@dataclass
class LogEntry:
    date: datetime
    level: str
    msg: str

    @staticmethod
    @lru_cache
    def get_field_names() -> List[str]:
        return [f.name for f in fields(LogEntry)]
