from .base_handler import Handler
from ..log_entry import LogEntry
from typing import List
import sqlite3
import os
import dataclasses
import pathlib
from datetime import datetime


class SQLLiteHandler(Handler):
    def __init__(self, filename: str) -> None:
        self.__filename = filename
        self.__connection = sqlite3.connect(self.__filename)

    def __del__(self) -> None:
        self.__connection.close()

    def __tables_correct(self) -> bool:
        cur = self.__connection.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        cur.close()

        if tables is None:
            return False

        # fetching table names
        tables = set(map(lambda x: x[0], tables))
        res = {"LOG_ENTRIES"} == tables

        return res

    def __create_tables(self) -> None:
        os.remove(self.__filename)
        self.__connection.close()
        self.__connection = sqlite3.connect(self.__filename)

        cur = self.__connection.cursor()

        with open(
            pathlib.Path(f"{os.path.dirname(__file__)}/schema.sql"),
            "r",
        ) as table_file:
            cur.executescript(table_file.read())

        self.__connection.commit()
        cur.close()

    def add_log(self, log: LogEntry) -> None:
        if not self.__tables_correct():
            self.__create_tables()

        cur = self.__connection.cursor()

        cur.execute(
            "INSERT INTO LOG_ENTRIES (date, level, msg) " "VALUES (?, ?, ?)",
            dataclasses.astuple(log),
        )

        self.__connection.commit()
        cur.close()

    def get_base_form(self) -> List[LogEntry]:
        cur = self.__connection.cursor()

        cur.execute("SELECT date, level, msg FROM LOG_ENTRIES ORDER BY ROWID")

        results = cur.fetchall()
        cur.close()

        if results is None:
            return []

        log_list = []
        for row in results:
            log_list.append(
                LogEntry(
                    date=datetime.fromisoformat(row[0]),
                    level=row[1],
                    msg=row[2],
                )
            )

        return log_list
