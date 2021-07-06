from my_logger import ProfilLogger
from my_logger import CSVHandler
import unittest
import os


class TestCSVHandler(unittest.TestCase):
    def test_handler_basic_usage(self):
        """Integrity test
        """
        plogger = ProfilLogger([CSVHandler("test.csv")])
        plogger.info("this is a info")
        
        with open("test.csv", "r") as csv_file:
            last_entry = csv_file.read().splitlines()[-1]
            last_entry = last_entry.split(",")
            self.assertEqual(last_entry[1],"INFO")
            self.assertEqual(last_entry[2],"this is a info")
        
        os.remove("test.csv")

    def test_logger_header(self):
        plogger = ProfilLogger([CSVHandler("test.csv")])
        plogger.info("this is a info")

        with open("test.csv", "r") as csv_file:
            header = csv_file.read().splitlines()[0]
            self.assertEqual(header,"date,level,msg")
        
        os.remove("test.csv")
