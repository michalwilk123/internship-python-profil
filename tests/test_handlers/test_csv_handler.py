from my_logger.handlers.csv_handler import (
    InvalidCSVFileException,
    InvalidCSVHeaderException,
)
from my_logger import ProfilLogger, CSVHandler, LogEntry
from datetime import datetime
import unittest
import unittest.mock as mock
import os

CORRECT_CSV = """
date,level,msg
2021-07-06 12:20:15.056783,INFO,this is a info no. 0
2021-07-06 12:20:15.057006,DEBUG,this is a info no. 1
"""

# bad csv file
INVALID_CSV_0 = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Donec condimentum vulputate blandit. Pellentesque consequat
orci quis neque malesuada, at tristique ex bibendum.
Quisque non eros luctus, ultricies nisi vel, venenatis ipsum.
"""

# correct csv, invalid fieldnames
INVALID_CSV_1 = """
date,level,msg,author
2021-07-06 12:20:15.056783,INFO,this is a info,michal
2021-07-06 12:20:15.057006,DEBUG,this is debug,tomek
"""

# correct csv, correct field, bad time format (POSIX)
INVALID_CSV_2 = """
date,level,msg
1625567110,INFO,this is a info
1625567110,INFO,this is a info
"""

CSV_FILENAME = "test.csv"


class TestCSVHandler(unittest.TestCase):
    def test_handler_basic_usage(self):
        """Integration test: test basic class usage"""
        plogger = ProfilLogger([CSVHandler(CSV_FILENAME)])
        plogger.info("this is a info")

        with open(CSV_FILENAME, "r") as csv_file:
            last_entry = csv_file.read().splitlines()[-1]
            last_entry = last_entry.split(",")
            self.assertEqual(last_entry[1], "INFO")
            self.assertEqual(last_entry[2], "this is a info")

        os.remove(CSV_FILENAME)

    def test_logger_header(self):
        """Integration test: test header creation"""
        plogger = ProfilLogger([CSVHandler(CSV_FILENAME)])
        plogger.info("this is a info")

        with open(CSV_FILENAME, "r") as csv_file:
            header = csv_file.read().splitlines()[0]
            self.assertEqual(header, "date,level,msg")

        os.remove(CSV_FILENAME)

    def test_handler_base_form(self):
        """Unit test: test dictionary creation"""
        m = mock.mock_open(read_data=CORRECT_CSV)
        handler = CSVHandler(CSV_FILENAME)

        with mock.patch("builtins.open", m):
            base_form = handler.get_base_form()
            m.assert_called_once_with(CSV_FILENAME, "r")
            correct_form = [
                LogEntry(
                    date=datetime(2021, 7, 6, 12, 20, 15, 56783),
                    level="INFO",
                    msg="this is a info no. 0",
                ),
                LogEntry(
                    date=datetime(2021, 7, 6, 12, 20, 15, 57006),
                    level="DEBUG",
                    msg="this is a info no. 1",
                ),
            ]
            self.assertEqual(base_form, correct_form)

    def test_handler_bad_csv(self):
        """Unit test: test if exception raised for invalid csv file format"""
        m = mock.mock_open(read_data=INVALID_CSV_0)
        handler = CSVHandler(CSV_FILENAME)

        with mock.patch("builtins.open", m):
            self.assertRaises(InvalidCSVFileException, handler.get_base_form)

            m.assert_called_once_with(CSV_FILENAME, "r")

    def test_handler_bad_header(self):
        """Unit test: test if exception raised for invalid csv file header"""
        m = mock.mock_open(read_data=INVALID_CSV_1)
        handler = CSVHandler(CSV_FILENAME)

        with mock.patch("builtins.open", m):
            self.assertRaises(InvalidCSVHeaderException, handler.get_base_form)

            m.assert_called_once_with(CSV_FILENAME, "r")

    def test_handler_bad_time_format(self):
        """Unit test: test if ValueError raised for invalid time
        format (not ISO)"""
        m = mock.mock_open(read_data=INVALID_CSV_2)
        handler = CSVHandler(CSV_FILENAME)

        with mock.patch("builtins.open", m):
            self.assertRaises(ValueError, handler.get_base_form)

            m.assert_called_once_with(CSV_FILENAME, "r")
