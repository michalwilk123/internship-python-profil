from my_logger import SQLLiteHandler, ProfilLogger, LogEntry, log_entry
import unittest
import os
import sqlite3
from datetime import datetime

SQL_FILENAME = "test.db"


class TestSQLLiteHandler(unittest.TestCase):
    def setUp(self) -> None:
        if os.path.exists(SQL_FILENAME):
            os.remove(SQL_FILENAME)
        return super().setUp()

    def tearDown(self) -> None:
        if os.path.exists(SQL_FILENAME):
            os.remove(SQL_FILENAME)
        return super().tearDown()

    def test_handler_basic_usage(self):

        plogger = ProfilLogger([SQLLiteHandler(SQL_FILENAME)])

        plogger.info("this is json test file")
        plogger.warning("this is json test file")
        plogger.error("this is json test file")

    def test_handler_bad_file(self):
        with open(SQL_FILENAME, "w") as sql_file:
            sql_file.write("this is a not valid sqllite file contents")

        plogger = ProfilLogger([SQLLiteHandler(SQL_FILENAME)])
        self.assertRaises(sqlite3.DatabaseError, plogger.info, "lorem ipsum")

    def test_handler_add(self):
        handler = SQLLiteHandler(SQL_FILENAME)
        ref_list = [
            LogEntry(
                date=datetime(2021, 7, 6, 21, 53, 16, 837733),
                level="INFO",
                msg="this is json test file number 1",
            ),
            LogEntry(
                date=datetime(2021, 7, 6, 21, 53, 16, 837885),
                level="WARNING",
                msg="this is json test file number 2",
            ),
            LogEntry(
                date=datetime(2021, 1, 6, 22, 53, 16, 837885),
                level="ERROR",
                msg="this is test error log",
            ),
        ]

        for log in ref_list:
            handler.add_log(log)

        base_form = handler.get_base_form()

        self.assertEqual(base_form, ref_list)

    def test_handler_add_to_existing(self):
        handler = SQLLiteHandler(SQL_FILENAME)
        ref_list = [
            LogEntry(
                date=datetime(2021, 7, 6, 21, 53, 16, 837733),
                level="INFO",
                msg="this is json test file number 1",
            ),
            LogEntry(
                date=datetime(2021, 7, 6, 21, 53, 16, 837885),
                level="WARNING",
                msg="this is json test file number 2",
            ),
            LogEntry(
                date=datetime(2021, 1, 6, 22, 53, 16, 837885),
                level="ERROR",
                msg="this is test error log",
            ),
        ]

        for log in ref_list:
            handler.add_log(log)

        del handler
        log_entry = LogEntry(
            date=datetime(2020, 3, 6, 22, 53, 16, 837885),
            level="WARNING",
            msg="this is newly added log",
        )
        handler = SQLLiteHandler(SQL_FILENAME)
        handler.add_log(log_entry)

        base_form = handler.get_base_form()
        ref_list.append(log_entry)

        self.assertEqual(base_form, ref_list)
