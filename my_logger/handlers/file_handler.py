from datetime import datetime
from .base_handler import Handler
from ..log_entry import LogEntry
from typing import List
import os
import shlex
import re


class BadHandlerFileFormatException(Exception):
    ...


class FileHandler(Handler):
    def __init__(self, filename: str) -> None:
        self.__filename = filename
        self.__re_expr = re.compile(
            "LogEntry\\(date=datetime.datetime\\([0-9]{4},"
            "[ 0-9,]*\\), level=.*msg=.*\\)"
        )

    def add_log(self, log: LogEntry) -> None:

        with open(self.__filename, "a") as text_file:
            if os.stat(self.__filename).st_size:
                text_file.write("\n")

            text_file.write(log.__repr__())

    @staticmethod
    def __parse_datetime(ll: List[str]) -> datetime:
        y = int(ll[0][-5:-1])
        mth = int(ll[1][:-1])
        d = int(ll[2][:-1])
        h = int(ll[3][:-1])
        m = int(ll[4][:-1])
        s = int(ll[5][:-1])
        ms = int(ll[6][:-2])
        return datetime(y, mth, d, h, m, s, ms)

    @staticmethod
    def __parse_level(ll: str) -> str:
        return ll[6:-1]

    @staticmethod
    def __parse_msg(ll: str) -> str:
        return ll[4:-1]

    def get_base_form(self) -> List[LogEntry]:
        log_entries = []

        with open(self.__filename, "r") as text_file:
            """
            I know that this all this work could be ignored
            by using eval command, but I am not comfortable
            using it on arbitrary textfile. Kinda bad practice.
            """
            for line in text_file.readlines():
                if not self.__re_expr.match(line):
                    raise BadHandlerFileFormatException(
                        f"There has been some issues with line: {line}"
                    )

                tokenized_line = shlex.split(line)
                date = FileHandler.__parse_datetime(tokenized_line[:7])
                level = FileHandler.__parse_level(tokenized_line[7])
                msg = FileHandler.__parse_msg(tokenized_line[8])
                log_entries.append(LogEntry(date=date, level=level, msg=msg))

        return log_entries
