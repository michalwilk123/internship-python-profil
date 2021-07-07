import unittest
from datetime import datetime, date
from my_logger import LogEntry, ProfilLoggerReader, CSVHandler, ProfilLoggerReaderException
import unittest.mock as mock

base_form_0 = [
    LogEntry(
        date=datetime(2021, 3, 6, 12, 20, 15, 56783),
        level="INFO",
        msg="I’d just like to interject for a moment. important msage no.2",
    ),
    LogEntry(
        date=datetime(2021, 4, 6, 12, 20, 15, 57006),
        level="INFO",
        msg=(
            "What you’re refering to as Linux, is in fact, GNU/Linux, "
            "or as I’ve recently taken to calling it, GNU plus Linux."
        ),
    ),
    LogEntry(
        date=datetime(2021, 5, 6, 12, 20, 15, 57006),
        level="DEBUG",
        msg=(
            "Linux is not an operating system unto itself, "
            "but rather another free component of a fully functioning GNU "
        ),
    ),
    LogEntry(
        date=datetime(2021, 6, 6, 12, 20, 15, 57006),
        level="CRITICAL",
        msg=("Important message no.1 XYZ. operating system moment"),
    ),
    LogEntry(
        date=datetime(2021, 6, 20, 12, 20, 15, 57006),
        level="CRITICAL",
        msg=("sample log message"),
    ),
]

HANDLER_FILENAME = "test.csv"


class TestProfilLoggerReader(unittest.TestCase):
    def test_empty_filter_by_datetime(self):
        entries = ProfilLoggerReader.filter_by_datetime(base_form_0)
        self.assertEqual(entries, base_form_0)

    def test_simple_filter_by_datetime(self):
        start_date = datetime.combine(date(2021, 4, 1), datetime.min.time())
        end_date = datetime.combine(date(2021, 5, 20), datetime.min.time())
        entries = list(
            ProfilLoggerReader.filter_by_datetime(
                base_form_0, start_date, end_date
            )
        )
        self.assertEqual(entries, base_form_0[1:3])

    def test_invalid_date_input(self):
        start_date = datetime.combine(date(2021, 4, 1), datetime.min.time())
        end_date = datetime.combine(date(2021, 5, 20), datetime.min.time())
        self.assertRaises(
            ProfilLoggerReaderException,
            ProfilLoggerReader.filter_by_datetime,
            base_form_0, end_date, end_date
        )

        self.assertRaises(
            ProfilLoggerReaderException,
            ProfilLoggerReader.filter_by_datetime,
            base_form_0, end_date, start_date
        )
        

    def test_find_by_text(self):
        handler = CSVHandler(HANDLER_FILENAME)
        profil_logger_reader = ProfilLoggerReader(handler)
        text = "moment"

        with mock.patch.object(
            CSVHandler, "get_base_form", return_value=base_form_0
        ):
            entries = profil_logger_reader.find_by_text(text)

        self.assertEqual(entries, [base_form_0[0], base_form_0[3]])

    def test_find_by_text_datetime(self):
        start_date = datetime.combine(date(2021, 4, 1), datetime.min.time())
        end_date = datetime.combine(date(2021, 5, 20), datetime.min.time())
        handler = CSVHandler(HANDLER_FILENAME)
        profil_logger_reader = ProfilLoggerReader(handler)
        text = "operating system"

        with mock.patch.object(
            CSVHandler, "get_base_form", return_value=base_form_0
        ):
            entries = profil_logger_reader.find_by_text(
                text, start_date, end_date
            )

        self.assertEqual(entries, [base_form_0[2]])

    def test_find_by_text_empty(self):
        handler = CSVHandler(HANDLER_FILENAME)
        profil_logger_reader = ProfilLoggerReader(handler)
        text = "Microsoft Windows"

        with mock.patch.object(
            CSVHandler, "get_base_form", return_value=base_form_0
        ):
            entries = profil_logger_reader.find_by_text(text)

        self.assertEqual(entries, [])

    def test_find_by_regex(self):
        handler = CSVHandler(HANDLER_FILENAME)
        profil_logger_reader = ProfilLoggerReader(handler)
        expr = ".*[iI]mportant m.{3,5}e no.[0-9]"

        with mock.patch.object(
            CSVHandler, "get_base_form", return_value=base_form_0
        ):
            entries = profil_logger_reader.find_by_regex(expr)

        self.assertEqual(entries, [base_form_0[0], base_form_0[3]])

    def test_find_by_regex_datetime(self):
        start_date = datetime.combine(date(2020, 4, 1), datetime.min.time())
        end_date = datetime.combine(date(2021, 5, 20), datetime.min.time())
        handler = CSVHandler(HANDLER_FILENAME)
        profil_logger_reader = ProfilLoggerReader(handler)
        expr = ".*[iI]mportant m.{3,5}e no.[0-9]"

        with mock.patch.object(
            CSVHandler, "get_base_form", return_value=base_form_0
        ):
            entries = profil_logger_reader.find_by_regex(
                expr, start_date, end_date
            )

        self.assertEqual(entries, [base_form_0[0]])

    def test_groupby_level(self):
        handler = CSVHandler(HANDLER_FILENAME)
        profil_logger_reader = ProfilLoggerReader(handler)

        ref_dict = {
            "INFO": [
                LogEntry(
                    date=datetime(2021, 3, 6, 12, 20, 15, 56783),
                    level="INFO",
                    msg=(
                        "I’d just like to interject for a moment. "
                        "important msage no.2"
                    ),
                ),
                LogEntry(
                    date=datetime(2021, 4, 6, 12, 20, 15, 57006),
                    level="INFO",
                    msg=(
                        "What you’re refering to as Linux, is in fact, "
                        "GNU/Linux, or as I’ve recently taken to calling "
                        "it, GNU plus Linux."
                    ),
                ),
            ],
            "DEBUG": [
                LogEntry(
                    date=datetime(2021, 5, 6, 12, 20, 15, 57006),
                    level="DEBUG",
                    msg=(
                        "Linux is not an operating system unto itself,"
                        " but rather another free component of a fully "
                        "functioning GNU "
                    ),
                )
            ],
            "CRITICAL": [
                LogEntry(
                    date=datetime(2021, 6, 6, 12, 20, 15, 57006),
                    level="CRITICAL",
                    msg="Important message no.1 XYZ. operating system moment",
                ),
                LogEntry(
                    date=datetime(2021, 6, 20, 12, 20, 15, 57006),
                    level="CRITICAL",
                    msg="sample log message",
                ),
            ],
        }

        with mock.patch.object(
            CSVHandler, "get_base_form", return_value=base_form_0
        ):
            log_dict = profil_logger_reader.groupby_level()

        self.assertEqual(log_dict, ref_dict)

    def test_groupby_month(self):
        handler = CSVHandler(HANDLER_FILENAME)
        profil_logger_reader = ProfilLoggerReader(handler)
        ref_dict = {
            "March": [
                LogEntry(
                    date=datetime(2021, 3, 6, 12, 20, 15, 56783),
                    level="INFO",
                    msg=(
                        "I’d just like to interject for a moment."
                        " important msage no.2"
                    ),
                )
            ],
            "April": [
                LogEntry(
                    date=datetime(2021, 4, 6, 12, 20, 15, 57006),
                    level="INFO",
                    msg=(
                        "What you’re refering to as Linux, is in "
                        "fact, GNU/Linux, or as I’ve recently taken"
                        " to calling it, GNU plus Linux."
                    ),
                )
            ],
            "May": [
                LogEntry(
                    date=datetime(2021, 5, 6, 12, 20, 15, 57006),
                    level="DEBUG",
                    msg=(
                        "Linux is not an operating system unto itself, "
                        "but rather another free component of a "
                        "fully functioning GNU "
                    ),
                )
            ],
            "June": [
                LogEntry(
                    date=datetime(2021, 6, 6, 12, 20, 15, 57006),
                    level="CRITICAL",
                    msg="Important message no.1 XYZ. operating system moment",
                ),
                LogEntry(
                    date=datetime(2021, 6, 20, 12, 20, 15, 57006),
                    level="CRITICAL",
                    msg="sample log message",
                ),
            ],
        }

        with mock.patch.object(
            CSVHandler, "get_base_form", return_value=base_form_0
        ):
            log_dict = profil_logger_reader.groupby_month()

        self.assertEqual(log_dict, ref_dict)
