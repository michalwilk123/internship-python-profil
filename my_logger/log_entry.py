from datetime import datetime
from dataclasses import dataclass
from enum import Enum

Level = Enum("Level", "INFO WARNING DEBUG CRITICAL ERROR")


@dataclass
class LogEntry:
    date: datetime
    level: str
    msg: str
