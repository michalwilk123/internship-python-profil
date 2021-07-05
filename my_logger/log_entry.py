from datetime import datetime
from dataclasses import dataclass
from enum import Enum

Level = Enum("Level", "DEBUG INFO WARNING ERROR CRITICAL")


@dataclass
class LogEntry:
    date: datetime
    level: str
    msg: str
