from my_logger.handlers.file_handler import BadHandlerFileFormatException
from my_logger.handlers.base_handler import Handler
from my_logger import FileHandler, ProfilLogger, LogEntry
import unittest
import os
from datetime import datetime


CORRECT_TEXT = (
    "LogEntry(date=datetime.datetime(2021, 7, 7, 15, 41, 4, 64954), "
    "level='INFO', msg='this is text info')\n"
    "LogEntry(date=datetime.datetime(2021, 7, 7, 15, 41, 4, 65011), "
    "level='WARNING', msg='this is text warning')\n"
    "LogEntry(date=datetime.datetime(2021, 7, 7, 15, 41, 4, 65045), "
    "level='ERROR', msg='this is text error')\n"
)

INVALID_TEXT = """
jndsnd sn dnsa jkdwjkq dme mnd mnsa d
"""

TEXT_FILENAME = "test.txt"


class TestFileHandler(unittest.TestCase):
    def setUp(self) -> None:
        if os.path.exists(TEXT_FILENAME):
            os.remove(TEXT_FILENAME)
        return super().setUp()

    def tearDown(self) -> None:
        if os.path.exists(TEXT_FILENAME):
            os.remove(TEXT_FILENAME)
        return super().tearDown()

    def test_handler_basic_usage(self):
        plogger = ProfilLogger([FileHandler(TEXT_FILENAME)])

        plogger.info("this is text info")
        plogger.warning("this is text warning")
        plogger.error("this is text error")

    def test_handler_bad_file(self):
        file_handler = FileHandler(TEXT_FILENAME)

        with open(TEXT_FILENAME, "w") as txt_file:
            txt_file.write(INVALID_TEXT)
        self.assertRaises(
            BadHandlerFileFormatException, file_handler.get_base_form
        )

    def test_handler_add(self):
        file_handler = FileHandler(TEXT_FILENAME)

        ref_list = [
            LogEntry(
                date=datetime(2021, 7, 6, 21, 53, 16, 837733),
                level="INFO",
                msg="this is text test file number 1",
            ),
            LogEntry(
                date=datetime(2021, 7, 6, 21, 53, 16, 837885),
                level="WARNING",
                msg="this is text test file number 2",
            ),
            LogEntry(
                date=datetime(2021, 1, 6, 22, 53, 16, 837885),
                level="ERROR",
                msg="this is text test error log",
            ),
        ]

        for log in ref_list:
            file_handler.add_log(log)

        base_form = file_handler.get_base_form()
        self.assertEqual(ref_list, base_form)
